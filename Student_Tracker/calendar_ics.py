"""
Google Calendar .ics File Parser
No authentication required - just export your calendar!
"""
import os
import json
from datetime import datetime
from dateutil import parser as dateparser

TRACKER_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_ics_file(ics_path):
    """Parse .ics file and return events"""
    events = []
    
    if not os.path.exists(ics_path):
        return events
    
    with open(ics_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    event = {}
    in_event = False
    
    for line in lines:
        line = line.strip()
        
        if line == 'BEGIN:VEVENT':
            in_event = True
            event = {}
        elif line == 'END:VEVENT':
            in_event = False
            if event:
                events.append(event)
        elif in_event:
            if line.startswith('DTSTART'):
                event['start'] = line.split(':')[1]
            elif line.startswith('DTEND'):
                event['end'] = line.split(':')[1]
            elif line.startswith('SUMMARY'):
                event['summary'] = line.split(':')[1]
            elif line.startswith('DESCRIPTION'):
                event['description'] = line.split(':', 1)[1] if ':' in line else ''
            elif line.startswith('LOCATION'):
                event['location'] = line.split(':')[1]
    
    return events

def get_calendar_events(ics_path=None):
    """Get events from .ics file"""
    if ics_path is None:
        ics_path = os.path.join(TRACKER_DIR, "calendar_export.ics")
    
    events = parse_ics_file(ics_path)
    
    if not events:
        print("No events found or file not found.")
        print(f"Looking for: {ics_path}")
        return []
    
    print(f"\n=== CALENDAR EVENTS ===")
    for e in events[:15]:
        start = e.get('start', 'Unknown')
        try:
            dt = dateparser.parse(start)
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        except:
            date_str = start[:8]
        
        print(f"{date_str} - {e.get('summary', 'No title')}")
    
    return events

def show_today_events(ics_path=None):
    """Show only today's events"""
    events = get_calendar_events(ics_path)
    today = datetime.now().strftime("%Y-%m-%d")
    
    today_events = []
    for e in events:
        start = e.get('start', '')
        if today in start:
            today_events.append(e)
    
    if today_events:
        print(f"\n=== TODAY'S EVENTS ({today}) ===")
        for e in today_events:
            print(f"  - {e.get('summary', 'No title')}")
    
    return today_events

if __name__ == '__main__':
    get_calendar_events()
    show_today_events()
