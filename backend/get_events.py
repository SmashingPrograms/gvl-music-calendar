import datetime
import os.path
import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

private_folder = "../private"
token_path = f"{private_folder}/token.json"
credentials_path = f"{private_folder}/credentials.json"
config_path = f"{private_folder}/config.yaml"

def get_calendar_events():
    """Fetch events from multiple calendars."""
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

    private_folder = "../private"
    token_path = f"{private_folder}/token.json"
    credentials_path = f"{private_folder}/credentials.json"
    config_path = f"{private_folder}/config.yaml"

    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        print("Access Token:", creds.token)
        print("Refresh Token:", creds.refresh_token)
        print("Token Expiration:", creds.expiry)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0, prompt='consent')
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    try:
        calendar_service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        # Read private/config.yaml and get the list of calendar IDs
        with open(config_path, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                calendar_ids = config
            except yaml.YAMLError as exc:
                print(exc)

        if not calendar_ids:
            print('No calendar IDs found in config.yaml.')
            return

        all_events = []
        for calendar_id in calendar_ids:
            print(f'Getting events for calendar ID: {calendar_id}')
            events_result = calendar_service.events().list(
                calendarId=calendar_id, timeMin=now, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print(f'No upcoming events found for calendar ID: {calendar_id}')
            else:
                all_events += events

        if all_events:
            # You can process the combined list of events here
            print(f'Combined events from all calendars: {all_events}')

        return all_events

    except HttpError as error:
        print(f"An error occurred: {error}")