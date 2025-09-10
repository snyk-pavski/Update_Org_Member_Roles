import sys
import requests
import argparse
import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

def get_org_members(org_id, pat_token):
    api_url = f"https://api.snyk.io/rest/orgs/{org_id}/memberships?version=2024-10-15"
    headers = {
        "accept": "application/vnd.api+json",
        "authorization": f"Token {pat_token}"
    }

    try:
        response = requests.get(api_url, headers=headers)
    
        response.raise_for_status()
        api_response = response.json()

        members_data = []
        if 'data' in api_response:
            for item in api_response['data']:
                try:
                    user_info = item['relationships']['user']['data']
                    role_info = item['relationships']['role']['data']

                    member_details = {
                        "username": user_info['attributes'].get('username', 'N/A'),
                        "user_id": user_info.get('id', 'N/A'),
                        "role_name": role_info['attributes'].get('name', 'N/A'),
                        "role_id": role_info.get('id', 'N/A')
                    }
                    members_data.append(member_details)
                except KeyError as e:
                    print(f"Warning: Skipping a record due to missing key: {e}", file=sys.stderr)
        return members_data

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}", file=sys.stderr)
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}", file=sys.stderr)
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}", file=sys.stderr)
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}", file=sys.stderr)
    
    return []

def main():
    parser = argparse.ArgumentParser(
        description="Fetch members from a Snyk organization and output their details in CSV format."
    )
    parser.add_argument("--org", dest="org_id", required=True, help="Your Snyk Organization ID.")
    parser.add_argument("--token", dest="pat_token", required=True, help="Your Snyk Personal Access Token (PAT).")
    args = parser.parse_args()

    members = get_org_members(args.org_id, args.pat_token)

    if members:
    
        print("username,user_id,role_name,role_id")
    
        for member in members:
            print(f"{member['username']},{member['user_id']},{member['role_name']},{member['role_id']}")
    else:
        print("No member data retrieved or an error occurred.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

