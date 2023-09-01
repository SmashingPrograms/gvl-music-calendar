import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
import yaml
import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

private_folder = "../private"
token_path = f"{private_folder}/token.json"
credentials_path = f"{private_folder}/credentials.json"
config_path = f"{private_folder}/config.yaml"

def get_calendar_events():
    # Read private/config.yaml and get the calendar_id attribute
    with open(config_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            calendar_id = config['calendar_id']
        except yaml.YAMLError as exc:
            print(exc)


    # def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # try:
            creds.refresh(Request())
            # with open(token_path, 'w') as token:
            #     token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0, prompt='consent')  # Add 'prompt' parameter
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    try:
        calendar_service = build('calendar', 'v3', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = calendar_service.events().list(calendarId=calendar_id, timeMin=now,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return None
            # return

        # Prints the start and name of the next 10 events
        # for event in events:
        #     # start = event['start'].get('dateTime', event['start'].get('date'))
        #     print("")
        return {"events": events}

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# get_events()