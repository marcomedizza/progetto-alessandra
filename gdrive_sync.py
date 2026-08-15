#!/usr/bin/env python3
"""
Google Drive Sync - Sincronizza file dashboard locale ↔ Google Drive
Monitora i file locali e li carica automaticamente su GDrive
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Google Drive
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GDRIVE_AVAILABLE = True
except ImportError:
    print("⚠️  Google Drive API non disponibile. Installa con:")
    print("   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    GDRIVE_AVAILABLE = False

# CONFIG
LOCAL_DASHBOARD = r"D:\progetto-alessandra\DASHBOARD_ALESSANDRA_v2.html"
LOCAL_BACKUP = r"D:\progetto-alessandra\backups"
CREDENTIALS_FILE = r"D:\progetto-alessandra\credentials.json"
TOKEN_FILE = r"D:\progetto-alessandra\token.json"
SCOPES = ['https://www.googleapis.com/auth/drive']

# State file
STATE_FILE = r"D:\progetto-alessandra\sync_state.json"

class DashboardSyncHandler(FileSystemEventHandler):
    """Monitor file changes and sync to Google Drive"""

    def __init__(self, drive_service):
        self.drive = drive_service
        self.last_sync = self.load_state()

    def on_modified(self, event):
        if event.is_directory:
            return

        if "DASHBOARD_ALESSANDRA_v2.html" in event.src_path:
            print(f"\n📝 File modificato: {event.src_path}")
            time.sleep(1)  # Wait for file write to complete
            self.sync_to_gdrive()

    def sync_to_gdrive(self):
        """Upload file to Google Drive"""
        if not GDRIVE_AVAILABLE or not self.drive:
            self.backup_local()
            return

        try:
            print("☁️  Sincronizzando con Google Drive...")

            # Find or create folder
            folder_id = self.get_or_create_folder("progetto-alessandra")

            # Upload file
            file_metadata = {
                'name': 'DASHBOARD_ALESSANDRA_v2.html',
                'parents': [folder_id],
                'mimeType': 'text/html'
            }

            media = MediaFileUpload(LOCAL_DASHBOARD, mimetype='text/html', resumable=True)

            # Check if file exists
            query = f"name = 'DASHBOARD_ALESSANDRA_v2.html' and '{folder_id}' in parents"
            results = self.drive.files().list(q=query, spaces='drive', fields='files(id)').execute()
            files = results.get('files', [])

            if files:
                # Update existing file
                file_id = files[0]['id']
                file = self.drive.files().update(fileId=file_id, media_body=media).execute()
                print(f"✅ File aggiornato su GDrive (ID: {file_id})")
            else:
                # Create new file
                file = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"✅ File caricato su GDrive (ID: {file['id']})")

            self.backup_local()
            self.save_state()

        except Exception as e:
            print(f"❌ Errore sync GDrive: {e}")
            self.backup_local()

    def get_or_create_folder(self, folder_name):
        """Get or create folder on Google Drive"""
        try:
            query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            results = self.drive.files().list(q=query, spaces='drive', fields='files(id)').execute()
            folders = results.get('files', [])

            if folders:
                return folders[0]['id']
            else:
                file_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.drive.files().create(body=file_metadata, fields='id').execute()
                print(f"📁 Cartella creata: {folder_name}")
                return folder['id']
        except Exception as e:
            print(f"⚠️  Errore creazione cartella: {e}")
            return None

    def backup_local(self):
        """Create local backup"""
        os.makedirs(LOCAL_BACKUP, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(LOCAL_BACKUP, f"DASHBOARD_{timestamp}.html")

        try:
            import shutil
            shutil.copy2(LOCAL_DASHBOARD, backup_path)
            print(f"💾 Backup locale: {backup_path}")
        except Exception as e:
            print(f"⚠️  Errore backup: {e}")

    def save_state(self):
        """Save sync state"""
        state = {
            'last_sync': datetime.now().isoformat(),
            'file': LOCAL_DASHBOARD,
            'status': 'synced'
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        """Load sync state"""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return None

def authenticate_gdrive():
    """Authenticate with Google Drive"""
    creds = None

    # Load saved token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print("\n❌ Credentials not found!")
                print(f"   Scarica da https://console.cloud.google.com/")
                print(f"   e salva in: {CREDENTIALS_FILE}")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def main():
    print("\n" + "="*70)
    print("🔄 GOOGLE DRIVE SYNC - Dashboard Alessandra")
    print("="*70)

    if not os.path.exists(LOCAL_DASHBOARD):
        print(f"❌ File non trovato: {LOCAL_DASHBOARD}")
        return

    print(f"📁 Monitorando: {LOCAL_DASHBOARD}")
    print(f"☁️  Cartella GDrive: progetto-alessandra")
    print(f"💾 Backup locale: {LOCAL_BACKUP}\n")

    # Try to authenticate (optional)
    drive_service = None
    if GDRIVE_AVAILABLE:
        try:
            drive_service = authenticate_gdrive()
            if drive_service:
                print("✅ Autenticato con Google Drive\n")
            else:
                print("⚠️  Google Drive non disponibile, usando solo backup locale\n")
        except Exception as e:
            print(f"⚠️  Errore autenticazione GDrive: {e}\n")

    # Start file monitoring
    event_handler = DashboardSyncHandler(drive_service)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(LOCAL_DASHBOARD), recursive=False)
    observer.start()

    print("🚀 Sincronizzazione attiva!")
    print("💡 Modifica il file HTML e sarà sincronizzato automaticamente")
    print("⏸️  Premi CTRL+C per fermare\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Sincronizzazione fermata")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
