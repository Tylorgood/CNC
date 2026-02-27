"""
Google Calendar - Device Flow (Best for Desktop)
Uses OAuth2 device flow for devices without browsers
"""
import os
import json
import socket
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_device_flow_url():
    """Get device flow URL"""
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), "credentials.json"), 
        SCOPES
    )
    # Use device flow
    return flow.authorization_url(access_type='offline', prompt='consent')

def main():
    print("\n" + "="*60)
    print("GOOGLE CALENDAR - DEVICE FLOW")
    print("="*60)
    
    creds_file = os.path.join(os.path.dirname(__file__), "credentials.json")
    token_file = os.path.join(os.path.dirname(__file__), "token.json")
    
    if os.path.exists(token_file):
        print("Already authenticated! Run tracker.py")
        return
    
    # For device code flow, we need special scope
    # Let's try the standard local server with custom port
    
    # Try automatic with port 0 (random available port)
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    
    try:
        # This opens browser automatically
        creds = flow.run_local_server(
            port=0, 
            prompt='consent',
            open_browser=True
        )
        
        # Save token
        with open(token_file, 'w') as f:
            json.dump({
                'token': creds.token,
                'refresh_token': creds.refresh_token,
            }, f)
        
        print("\nSuccess! Token saved.")
        
        # Test it
        service = build('calendar', 'v3', credentials=creds)
        events = service.events().list(
            calendarId='primary',
            timeMin=datetime.utcnow().isoformat() + 'Z',
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        print("\nYour upcoming events:")
        for e in events.get('items', []):
            start = e['start'].get('dateTime', e['start'].get('date'))
            print(f"  {start[:16]} - {e.get('summary', 'No title')}")
            
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTry this instead:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Create NEW credentials -> OAuth client ID")
        print("3. Select 'Desktop app' (NOT Web application)")
        print("4. Download and replace credentials.json")

if __name__ == '__main__':
    main()
