import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime

def append_to_sheet(name, email, question, session_id=None):
    json_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_name = os.getenv("GOOGLE_SHEETS_SPREADSHEET_NAME")

    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(json_path, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, name, email, question, session_id or "-"])
    print(f"✅ Logged to sheet: {name}, {email}, {question}")
    return True
