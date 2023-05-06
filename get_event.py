import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yaml
import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

# Read private/config.yaml and get the calendar_id attribute
with open("private/config.yaml", 'r') as stream:
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
if os.path.exists('private/token.json'):
    creds = Credentials.from_authorized_user_file('private/token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'private/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('private/token.json', 'w') as token:
        token.write(creds.to_json())

try:
    calendar_service = build('calendar', 'v3', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = calendar_service.events().list(calendarId=calendar_id, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        exit()
        # return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event['start'].get('dateTime', event['start'].get('date'))
      print(start, event['summary'], event['location'], event['description'])
      print(event['attachments'])
      print(event)
      if 'attachments' in event:
        for attachment in event['attachments']:
            # try to download attachment
            file_id = attachment['fileId']
            filename = attachment['title']
            try:
              request = drive_service.files().get_media(fileId=file_id)
              file = io.BytesIO()
              downloader = MediaIoBaseDownload(file, request)
              done = False
              while done is False:
                  status, done = downloader.next_chunk()
                  print(f'Download {int(status.progress() * 100)}.')

            except HttpError as error:
                print(f'An error occurred: {error}')
                file = None
            # Write the attachment to a file

            if file:
              with open(f'{filename}', 'wb') as f:
                  f.write(file.getvalue())
            
      else:
          print("No attachments found for the event.")

except HttpError as error:
    print(f"An error occurred: {error}")