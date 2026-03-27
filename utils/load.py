import pandas as pd

def load_to_csv(df, filepath="products.csv"):
    """Simpan DataFrame ke CSV."""
    try:
        if df.empty:
            raise ValueError("DataFrame kosong, tidak ada yang disimpan.")
        df.to_csv(filepath, index=False)
        print(f"[OK] Data disimpan ke {filepath} ({len(df)} baris)")
    except Exception as e:
        print(f"[ERROR] load_to_csv gagal: {e}")

def load_to_google_sheets(df, spreadsheet_id, credentials_file="google-sheets-api.json"):
    """Simpan DataFrame ke Google Sheets (opsional, untuk Skilled/Advanced)."""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        if df.empty:
            raise ValueError("DataFrame kosong.")

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        service = build("sheets", "v4", credentials=creds)

        values = [df.columns.tolist()] + df.values.tolist()
        body = {"values": [[str(v) for v in row] for row in values]}

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body
        ).execute()

        print(f"[OK] Data disimpan ke Google Sheets ({len(df)} baris)")
    except Exception as e:
        print(f"[ERROR] load_to_google_sheets gagal: {e}")

def load_to_postgresql(df, connection_string):
    """Simpan DataFrame ke PostgreSQL (opsional, untuk Advanced)."""
    try:
        from sqlalchemy import create_engine

        if df.empty:
            raise ValueError("DataFrame kosong.")

        engine = create_engine(connection_string)
        df.to_sql("products", engine, if_exists="replace", index=False)
        print(f"[OK] Data disimpan ke PostgreSQL ({len(df)} baris)")
    except Exception as e:
        print(f"[ERROR] load_to_postgresql gagal: {e}")