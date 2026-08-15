#!/usr/bin/env python3
"""
Google Drive Sync Setup - One-time OAuth2 configuration
Run this first to get the credentials
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def setup_oauth():
    """Setup OAuth2 credentials for Google Drive API"""

    print("\n" + "="*70)
    print("🔐 GOOGLE DRIVE SYNC - SETUP OAUTH2")
    print("="*70)

    print("\n1️⃣  SCARICA CREDENTIALS DA GOOGLE CLOUD:")
    print("   a) Vai a: https://console.cloud.google.com/")
    print("   b) Crea un nuovo progetto 'Progetto Alessandra'")
    print("   c) Abilita: Google Drive API")
    print("   d) Crea: 'Desktop app' OAuth 2.0 credentials")
    print("   e) Scarica il JSON e salvalo come:")
    print("      C:\\Users\\User\\AppData\\Local\\Temp\\...\\credentials.json")

    print("\n2️⃣  OPPURE Usa questo setup semplificato:")

    credentials_path = r"D:\progetto-alessandra\credentials.json"
    token_path = r"D:\progetto-alessandra\token.json"

    print(f"\n   Percorso credentials: {credentials_path}")
    print(f"   Percorso token: {token_path}")

    print("\n3️⃣  ISTRUZIONI RAPIDE (consigliato):")
    print("   - Se non hai credenziali Google Cloud:")
    print("   - Usa Google Drive web per caricare il file manualmente UNA volta")
    print("   - Poi questo script lo sincronizza automaticamente")

    print("\n" + "="*70)
    print("Continua quando hai i credentials pronti (o salta per sync manuale)")
    print("="*70 + "\n")

if __name__ == "__main__":
    setup_oauth()
