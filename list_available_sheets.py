from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print("Credentials file not found.")
        return

    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    print("--- SEARCHING FOR SHARED SPREADSHEETS ---")
    try:
        # List all spreadsheets
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print("No spreadsheets found. The bot has properly authenticated but cannot see ANY sheets.")
            print("Double check the email in 'credentials.json' matches the one you shared with.")
        else:
            print("Found the following accessible sheets:")
            for item in items:
                print(f"Name: '{item['name']}' | ID: '{item['id']}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
