# Snyk Organization Member Management Scripts

A collection of Python scripts to help manage members within a Snyk organization using the Snyk API.

## Features

* **List Members**: Fetch a list of all members in a specific Snyk organization and output their details (username, user ID, role name, role ID) in CSV format.

* **Update Roles**: Bulk update the roles for a list of users within a Snyk organization.

## Prerequisites

* Python 3.6+

* The `requests` library

## Installation

1. Clone this repository or download the scripts.

2. Install the required Python library:



`pip install requests`


## Usage

You will need a Snyk Personal Access Token (PAT) with at least Org Collaborator permissions to use these scripts.

### 1. Get Org Members

This script retrieves all members from a specified organization and prints their details.

**Command:**


`python get_org_members.py --org <YOUR_ORG_ID> --token <YOUR_PAT_TOKEN>`


**Example Output:**

```
username,user_id,role_name,role_id
user.one@example.com,xxx-xx-xx-xx-xxx,Org Admin,xxx-xx-xx-xx-xx
user.two@example.com,xxx-xx-xx-xxx-xxx,Collaborator,xxx-xx-xx-xx-xx
```

### 2. Update member Roles

This script updates the role for one or more users in a specified organization.

**Command:**


`python update_snyk_roles.py --org <YOUR_ORG_ID> --token <YOUR_PAT_TOKEN> --role <NEW_ROLE_ID> --users <USER_ID_1>,<USER_ID_2>`


* `--users`: A comma-separated list of user IDs (with no spaces) to update.

* `--role`: The public ID of the new role you want to assign.


## License

This project is licensed under the MIT License. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
