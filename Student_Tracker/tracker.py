import json
import os
from datetime import datetime

TRACKER_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(TRACKER_DIR, "students.json")
TASKS_FILE = os.path.join(TRACKER_DIR, "tasks.json")
BLACKBOX_FILE = os.path.join(TRACKER_DIR, "blackbox.json")

def load_blackbox():
    if os.path.exists(BLACKBOX_FILE):
        with open(BLACKBOX_FILE, "r") as f:
            return json.load(f)
    return {"sessions": []}

def show_blackbox_instructions():
    data = load_blackbox()
    if "instructions" in data:
        print("\n=== BLACKBOX ACTIVE ===")
        print(f"Status: {'ACTIVE' if data['instructions'].get('active') else 'INACTIVE'}")
        print(f"Last Updated: {data['instructions'].get('last_updated', 'Unknown')}")
        print(f"System: {data['instructions'].get('system_prompt', 'No instructions')}")
        print("========================\n")
    return data

def save_blackbox(data):
    with open(BLACKBOX_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_to_blackbox(prompt_summary, action_taken):
    data = load_blackbox()
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    today_session = None
    for session in data["sessions"]:
        if session["date"] == today:
            today_session = session
            break
    
    if not today_session:
        today_session = {"date": today, "entries": []}
        data["sessions"].append(today_session)
    
    today_session["entries"].append({
        "time": current_time,
        "type": "prompt",
        "user": prompt_summary
    })
    if action_taken:
        today_session["entries"].append({
            "time": current_time,
            "type": "action",
            "description": action_taken
        })
    
    save_blackbox(data)
    return True

def load_students():
    with open(STUDENTS_FILE, "r") as f:
        return json.load(f)

def save_students(data):
    with open(STUDENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_current_student():
    data = load_students()
    sid = data.get("current_student_id")
    for student in data["students"]:
        if student["id"] == sid:
            return student
    return None

def add_reflection(student_id, reflection_data):
    data = load_students()
    for student in data["students"]:
        if student["id"] == student_id:
            reflection = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "period_1": reflection_data.get("period_1", ""),
                "period_2": reflection_data.get("period_2", ""),
                "period_3": reflection_data.get("period_3", ""),
                "period_4": reflection_data.get("period_4", ""),
                "highlights": reflection_data.get("highlights", ""),
                "challenges": reflection_data.get("challenges", ""),
                "goals": reflection_data.get("goals", "")
            }
            student["reflections"].append(reflection)
            save_students(data)
            return True
    return False

def update_competency(student_id, competency, status):
    data = load_students()
    for student in data["students"]:
        if student["id"] == student_id:
            student["competencies"][competency] = status
            save_students(data)
            return True
    return False

def load_tasks():
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(data):
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_tasks():
    data = load_tasks()
    print("\n=== TASKS ===")
    for task in data["tasks"]:
        status_icon = "[X]" if task["status"] == "completed" else "[ ]" if task["status"] == "pending" else "[~]"
        print(f"{status_icon} {task['title']}")
        print(f"    Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        if task["description"]:
            print(f"    {task['description']}")
        print()

def complete_task(task_id):
    data = load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = "completed"
            data["completed_history"].append({
                "id": task["id"],
                "title": task["title"],
                "completed_date": datetime.now().strftime("%Y-%m-%d")
            })
            save_tasks(data)
            return True
    return False

def get_schedule_today():
    today = datetime.now().strftime("%Y-%m-%d")
    schedule = {
        "2026-02-23": {"day": 1, "periods": ["CNC Setup + Clean", "Tramming Bridgeport", "Blueprint Reading", "Lathe Part"], "notes": "Kyle joins tomorrow"},
        "2026-02-24": {"day": 2, "periods": ["CNC (Kyle starts)", "Tramming", "Blueprint Assignment", "Test Review (Micrometers)"], "notes": "9am Marvin Mock Interview | 11:30am Weekly Meeting"},
        "2026-02-25": {"day": 3, "periods": ["CNC", "Open Shop", "Programming Practice", "Programming Practice"], "notes": "Mock Interviews - Kyle review"},
        "2026-02-26": {"day": 4, "periods": ["Open", "Open", "Project Work", "Project Work"], "notes": ""},
        "2026-02-27": {"day": 5, "periods": ["Grad Prep", "Graduation Ceremony", "Review", "Review"], "notes": "GRADUATION DAY - MARVIN"}
    }
    return schedule.get(today, {"day": 0, "periods": [], "notes": "No class scheduled"})

def show_status():
    student = get_current_student()
    if not student:
        print("No active student")
        return
    
    print(f"\n=== {student['name'].upper()} - Status ===")
    print(f"Start: {student['start_date']} | Graduation: {student['graduation_date']}")
    print(f"Week {student['week']}, Day {student['day']}")
    print(f"\nCompetencies:")
    for comp, status in student["competencies"].items():
        symbol = "[X]" if status == "completed" else "[~]" if status == "in_progress" else "[ ]"
        print(f"  {symbol} {comp.replace('_', ' ').title()}")
    print(f"\nReflections: {len(student['reflections'])} entries")
    print(f"Mock Interview: {student['mock_interview']['scheduled']} ({student['mock_interview']['status']})")

if __name__ == "__main__":
    show_blackbox_instructions()
    show_status()
    show_tasks()
