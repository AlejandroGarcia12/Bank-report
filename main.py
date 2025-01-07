import time
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
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

LISTEN = os.getenv('LISTEN')
if LISTEN == "True":
    LISTEN = True
else:
    LISTEN = False

SERVICE_ACCOUNT_FILE = 'service-account.json'

if not MAIL_USERNAME or not MAIL_PASSWORD:
    raise ValueError('Please set your credentials')

def main():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)
    print("Starting...")
    print("Getting data from mails...")
    while True:
        try:
            # values = get_info_from_mails(MAIL_USERNAME, MAIL_PASSWORD, LISTEN)
            values = [['2023-01-01 00:00:00', 'Test', '100.00', 'Pago']]
            if values:
                body = {"values": values}
                sheet = service.spreadsheets()
                result = sheet.values().append(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range=SAMPLE_RANGE_NAME, 
                    valueInputOption="RAW", 
                    body=body
                ).execute()
                print("Data successfully written to Google Sheets.")
                if not LISTEN:
                    break
                time.sleep(60*5)
                print("Getting data from mails...")
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()