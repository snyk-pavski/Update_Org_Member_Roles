import sys
import requests
import argparse
import json

def update_user_role(org_id, pat_token, user_id, role_id):
    api_url = f"https://api.snyk.io/v1/org/{org_id}/members/update/{user_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {pat_token}'
    }
    payload = {
        "rolePublicId": role_id
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

def main():
    parser = argparse.ArgumentParser(
        description="Update the role for a list of users in a Snyk organization."
    )
    parser.add_argument("--org", dest="org_id", required=True, help="Your Snyk Organization ID.")
    parser.add_argument("--token", dest="pat_token", required=True, help="Your Snyk Personal Access Token (PAT).")
    parser.add_argument("--users", dest="user_ids", required=True, help="A comma-separated list of Snyk User IDs to update.")
    parser.add_argument("--role", dest="role_id", required=True, help="The public ID of the new role to assign.")
    
    args = parser.parse_args()

    user_ids = [uid.strip() for uid in args.user_ids.split(',')]
    
    if not user_ids:
        print("No user IDs provided.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting role update for {len(user_ids)} user(s) in organization {args.org_id}...")
    
    successful_updates = 0
    failed_updates = 0

    for user_id in user_ids:
        if update_user_role(args.org_id, args.pat_token, user_id, args.role_id):
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
