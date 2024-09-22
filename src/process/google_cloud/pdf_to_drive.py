from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scope for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    # The token.json file stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'service-key-google-cloud.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_to_drive(file_path, file_name, folder_id):

    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Define the metadata for the file, including the parent folder ID
    file_metadata = {
        'name': file_name,             # Name of the file on Google Drive
        'parents': [folder_id]         # ID of the folder to upload the file into
    }
    # Define the media type and file to upload
    media = MediaFileUpload(file_path, mimetype='application/pdf')

    # Upload the file to the specified folder
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f'File Link: https://drive.google.com/file/d/{file.get("id")}')
    return file.get('id')
