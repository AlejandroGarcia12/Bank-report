from dotenv import load_dotenv
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import Request

from services.mail import get_info_from_mails

# Variables
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SAMPLE_RANGE_NAME = os.getenv('SAMPLE_RANGE_NAME')

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

if not MAIL_USERNAME or not MAIL_PASSWORD:
    raise ValueError('Please set your credentials')

def authenticate_google_sheets():
    creds = None
    # The file 'credentials.json' should be in the same directory as your script
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8888)
        # Save the credentials for the next run
        # with open("token.json", "w") as token:
        #     token.write(creds.to_json())
    return creds

def main():
    creds = authenticate_google_sheets()
    service = build("sheets", "v4", credentials=creds)
    try:
        values = get_info_from_mails(MAIL_USERNAME, MAIL_PASSWORD)
        body = {"values": values}
        sheet = service.spreadsheets()
        result = sheet.values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, 
            range=SAMPLE_RANGE_NAME, 
            valueInputOption="RAW", 
            body=body
        ).execute()
        print("Data successfully written to Google Sheets.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()