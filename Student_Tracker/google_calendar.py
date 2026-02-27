from __future__ import print_function
import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TRACKER_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(TRACKER_DIR, "credentials.json")
TOKEN_FILE = os.path.join(TRACKER_DIR, "token.json")

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token:
            creds = json.load(token)
    
    if not creds or creds.get('invalid', False):
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            json.dump({
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }, token)
    else:
        creds = Credentials(
            token=creds.get('token'),
            refresh_token=creds.get('refresh_token'),
            token_uri=creds.get('token_uri'),
            client_id=creds.get('client_id'),
            client_secret=creds.get('client_secret'),
            scopes=creds.get('scopes')
        )
    return creds

def get_calendar_events(days_ahead=7):
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)
        
        now = datetime.utcnow()
        end_time = now + timedelta(days=days_ahead)
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return []
        
        print(f'\n=== GOOGLE CALENDAR - Next {days_ahead} Days ===')
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'No title')
            
            print(f"{start[:10]} {start[11:16] if len(start) > 10 else ''} - {summary}")
            event_list.append({
                'start': start,
                'end': end,
                'summary': summary,
                'id': event.get('id')
            })
        
        return event_list
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_today_events():
    return get_calendar_events(days_ahead=1)

if __name__ == '__main__':
    get_calendar_events()
