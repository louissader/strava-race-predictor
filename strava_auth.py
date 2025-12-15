"""
Strava OAuth authentication helper
Run this script to get your refresh token for the first time
"""

import os
from stravalib.client import Client
from dotenv import load_dotenv

load_dotenv()

def get_authorization_url():
    """Get the URL to authorize the application"""
    client = Client()
    client_id = os.getenv('STRAVA_CLIENT_ID')

    if not client_id:
        print("Error: STRAVA_CLIENT_ID not found in .env file")
        return None

    authorize_url = client.authorization_url(
        client_id=client_id,
        redirect_uri='http://localhost',
        scope=['read_all', 'activity:read_all']
    )

    return authorize_url

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    client = Client()
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    if not client_id or not client_secret:
        print("Error: STRAVA_CLIENT_ID or STRAVA_CLIENT_SECRET not found in .env file")
        return None

    token_response = client.exchange_code_for_token(
        client_id=client_id,
        client_secret=client_secret,
        code=code
    )

    return token_response

def get_client():
    """Get authenticated Strava client using refresh token"""
    client = Client()
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("Error: Missing credentials in .env file")
        return None

    # Refresh the access token
    token_response = client.refresh_access_token(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    # Create a new client with the access token
    client = Client(access_token=token_response['access_token'])

    return client

if __name__ == "__main__":
    print("Strava OAuth Setup")
    print("=" * 50)
    print("\nStep 1: Get your authorization URL")

    auth_url = get_authorization_url()
    if auth_url:
        print(f"\nPlease visit this URL and authorize the application:\n{auth_url}")
        print("\nAfter authorization, you'll be redirected to a URL like:")
        print("http://localhost/?state=&code=XXXXX&scope=read,activity:read_all")

        code = input("\nEnter the 'code' parameter from the redirect URL: ").strip()

        if code:
            print("\nStep 2: Exchanging code for token...")
            token_response = exchange_code_for_token(code)

            if token_response:
                print("\nSuccess! Add this to your .env file:")
                print(f"STRAVA_REFRESH_TOKEN={token_response['refresh_token']}")
                print(f"\nAccess Token (expires in {token_response['expires_in']} seconds):")
                print(f"{token_response['access_token']}")
            else:
                print("\nFailed to exchange code for token")
        else:
            print("\nNo code provided")
    else:
        print("\nFailed to generate authorization URL")
