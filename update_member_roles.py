import sys
import requests
import argparse
import json
import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

def update_user_role(org_id, pat_token, user_id, new_role_id):
    api_url = f"https://api.snyk.io/v1/org/{org_id}/members/update/{user_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {pat_token}'
    }
    payload = {
        "rolePublicId": new_role_id
    }

    try:
        response = requests.put(api_url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            print(f"Successfully updated role for user: {user_id}")
            return True
        else:
            print(f"Failed to update role for user: {user_id}", file=sys.stderr)
            print(f"Status Code: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request for user {user_id}: {e}", file=sys.stderr)
        return False

def get_org_members(org_id, pat_token, role_id):
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
                    if member_details['role_id'] == role_id:
                        members_data.append(member_details['user_id'])
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
        description="Update the role for a list of users in a Snyk organization."
    )
    parser.add_argument("--org", dest="org_id", required=True, help="Your Snyk Organization ID.")
    parser.add_argument("--token", dest="pat_token", required=True, help="Your Snyk Personal Access Token (PAT).")
    parser.add_argument("--role", dest="role_id", required=True, help="The public ID of the existing role to update.")
    parser.add_argument("--new_role", dest="new_role_id", required=True, help="The public ID of the new role to assign.")
    
    args = parser.parse_args()

    user_ids = get_org_members(args.org_id, args.pat_token, args.role_id)
    
    if not user_ids:
        print("No users for given role.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting role update for {len(user_ids)} user(s) in organization {args.org_id}...")
    
    successful_updates = 0
    failed_updates = 0

    for user_id in user_ids:
        if update_user_role(args.org_id, args.pat_token, user_id, args.new_role_id):
            successful_updates += 1
        else:
            failed_updates += 1
    
    print("\n--- Update Summary ---")
    print(f"Successful updates: {successful_updates}")
    print(f"Failed updates: {failed_updates}")
    
    if failed_updates > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
