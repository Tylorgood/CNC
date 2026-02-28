import os
import time
import subprocess
import threading
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TEAMUP_FOLDER_PATH = r"C:\Users\journi\OneDrive\Drive\Desktop\Team Up Desktop"
REPO_PATH = r"C:\Users\journi\OneDrive\Drive\Desktop\TeamUp-Git"
BRANCH = "main"
DEBOUNCE_SECONDS = 20
LOG_PATH = r"C:\Users\journi\OneDrive\Drive\Desktop\TeamUp-Git\sync.log"
DRY_RUN = False

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_change = time.time()
        self.pending_changes = []
        
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.git' + os.sep):
            return
        self.last_change = time.time()
        self.pending_changes.append(event.src_path)
        
    def should_commit(self):
        return time.time() - self.last_change > DEBOUNCE_SECONDS
    
    def get_changed_files_summary(self):
        if not self.pending_changes:
            return "No changes"
        unique_files = list(set(self.pending_changes))[:10]
        suffix = "..." if len(self.pending_changes) > 10 else ""
        return ", ".join([os.path.basename(f) for f in unique_files]) + suffix

handler = ChangeHandler()
observer = Observer()

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def sync():
    if not handler.should_commit():
        return
        
    handler.pending_changes = []
    
    try:
        os.chdir(REPO_PATH)
        
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not result.stdout.strip():
            log("No changes to commit")
            return
        
        if DRY_RUN:
            log(f"DRY RUN - Would commit and push:\n{result.stdout}")
            return
        
        log("Pulling latest changes...")
        subprocess.run(["git", "pull", "--rebase"], capture_output=True)
        
        log("Staging changes...")
        subprocess.run(["git", "add", "-A"])
        
        commit_msg = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M')} - {handler.get_changed_files_summary()}"
        log(f"Committing: {commit_msg}")
        subprocess.run(["git", "commit", "-m", commit_msg])
        
        log("Pushing to remote...")
        push_result = subprocess.run(["git", "push", "origin", BRANCH], capture_output=True, text=True)
        
        if push_result.returncode == 0:
            log("Sync complete")
        else:
            log(f"Push failed: {push_result.stderr}")
            
    except Exception as e:
        log(f"Error: {e}")

def run_watcher():
    log(f"Watching: {TEAMUP_FOLDER_PATH}")
    log(f"Repo: {REPO_PATH}")
    log(f"DRY RUN: {DRY_RUN}")
    
    observer.schedule(handler, TEAMUP_FOLDER_PATH, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(5)
            if handler.pending_changes and handler.should_commit():
                sync()
                handler.pending_changes = []
    except KeyboardInterrupt:
        observer.stop()
        log("Watcher stopped")
    observer.join()

if __name__ == "__main__":
    run_watcher()
