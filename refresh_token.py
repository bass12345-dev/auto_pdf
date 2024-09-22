from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Define the scope for Google Drive (full access)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Path to your OAuth 2.0 client secret JSON file
CLIENT_SECRET_FILE = 'client_secret_key.json'

# Path to save the generated token file
TOKEN_FILE = 'token.json'

def generate_drive_token():
    creds = None
    
    # Check if token file exists and load credentials from it
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials available, prompt user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials to a token file for future use
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    print(f"Token has been saved to {TOKEN_FILE}")
    return creds.token

if __name__ == '__main__':
    token = generate_drive_token()
    print(f"Generated Access Token: {token}")
