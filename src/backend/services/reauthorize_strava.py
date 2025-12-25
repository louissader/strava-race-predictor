"""
Re-authorize Strava with correct scopes (activity:read_all)
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def reauthorize():
    """Generate authorization URL with correct scopes"""
    client_id = os.getenv('STRAVA_CLIENT_ID')

    if not client_id:
        print("❌ STRAVA_CLIENT_ID not found in .env file")
        return

    # Create authorization URL with correct scopes
    scopes = 'read,activity:read_all'
    redirect_uri = 'http://localhost'

    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"approval_prompt=force&"
        f"scope={scopes}"
    )

    print("=" * 70)
    print("STRAVA RE-AUTHORIZATION")
    print("=" * 70)
    print("\nYour current refresh token only has 'read' scope.")
    print("We need 'activity:read_all' scope to fetch all your activities.")
    print("\n" + "=" * 70)
    print("STEP 1: Authorize the Application")
    print("=" * 70)
    print("\nPlease visit this URL in your browser:\n")
    print(auth_url)
    print("\n" + "=" * 70)
    print("STEP 2: Get the Authorization Code")
    print("=" * 70)
    print("\nAfter authorizing:")
    print("1. You'll be redirected to a URL like:")
    print("   http://localhost/?state=&code=XXXXXXXXXXXXX&scope=read,activity:read_all")
    print("2. Copy the value after 'code=' (before '&scope')")
    print("3. Paste it below")

    code = input("\nEnter the authorization code: ").strip()

    if not code:
        print("\n❌ No code provided")
        return

    # Exchange code for token
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    print("\n" + "=" * 70)
    print("STEP 3: Exchanging Code for Token")
    print("=" * 70)

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        token_data = response.json()

        print("\n✅ SUCCESS! Tokens received")
        print("\n" + "=" * 70)
        print("STEP 4: Update Your .env File")
        print("=" * 70)
        print("\nReplace the STRAVA_REFRESH_TOKEN in your .env file with:")
        print(f"\nSTRAVA_REFRESH_TOKEN={token_data['refresh_token']}")
        print(f"\nScopes granted: {token_data.get('scope', 'N/A')}")
        print(f"\nAccess token (expires in {token_data.get('expires_in', 'N/A')} seconds):")
        print(f"{token_data['access_token']}")

        # Ask if we should update .env automatically
        update = input("\n\nWould you like me to update the .env file automatically? (y/n): ").strip().lower()

        if update == 'y':
            # Read current .env
            env_path = '.env'
            with open(env_path, 'r') as f:
                lines = f.readlines()

            # Update refresh token
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('STRAVA_REFRESH_TOKEN='):
                    lines[i] = f"STRAVA_REFRESH_TOKEN={token_data['refresh_token']}\n"
                    updated = True
                    break

            if not updated:
                lines.append(f"STRAVA_REFRESH_TOKEN={token_data['refresh_token']}\n")

            # Write back
            with open(env_path, 'w') as f:
                f.writelines(lines)

            print("\n✅ .env file updated successfully!")
            print("\nYou can now run:")
            print("  python fetch_strava_data_rest.py")

        else:
            print("\nPlease update your .env file manually with the refresh token above.")

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {e}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    reauthorize()
