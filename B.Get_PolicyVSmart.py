# This Script will show us the Policy configured on the controller (Cisco SD-WAN Always-On Sandbox)

import requests
import json
from prettytable import PrettyTable
from colorama import init, Fore, Style

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Sandbox credentials
USERNAME = "devnetuser"
PASSWORD = "RG!_Yw919_83"

# Authentication
login_url = 'https://sandbox-sdwan-2.cisco.com/j_security_check'
login_data = {'j_username': USERNAME, 'j_password': PASSWORD}

response = requests.post(url=login_url, data=login_data, verify=False)
if response.status_code != 200:
    print(f"Authentication failed: {response.text}")
    exit()

token1 = 'JSESSIONID=' + response.cookies.get_dict()['JSESSIONID']
print('token1 =', token1)

# Get Token
token_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/client/token'
headers = {'Cookie': token1, 'content-type': 'application/json'}

response = requests.get(url=token_url, headers=headers, verify=False)
if response.status_code != 200:
    print(f"Failed to get token: {response.text}")
    exit()

token2 = response.text
print('token2 =', token2)

# Show Policy configured on controller
request_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/template/policy/vsmart/'
headers = {'Content-Type': "application/json", 'Cookie': token1, 'X-XSRF-TOKEN': token2}

response = requests.get(url=request_url, headers=headers, verify=False)
print("status:", response.status_code)
print(json.dumps(response.json(), indent=5))

# Parse JSON response
Get_Policy_Configured = response.json()

# Create PrettyTable
table = PrettyTable()
table.field_names = ["PolicyName", "PolicyType", "PolicyId", "CreatedBy"]

# Populate the table
for policy in Get_Policy_Configured.get('data', []):
    table.add_row([
        f"{Fore.GREEN}{policy['policyName']}{Style.RESET_ALL}",
        f"{Fore.YELLOW}{policy['policyType']}{Style.RESET_ALL}",
        f"{Fore.RED}{policy['policyId']}{Style.RESET_ALL}",
        f"{Fore.MAGENTA}{policy.get('createdBy', '')}{Style.RESET_ALL}"
    ])

# Align columns
table.align['PolicyName'] = 'l'
table.align['PolicyType'] = 'l'
table.align['PolicyId'] = 'l'
table.align['CreatedBy'] = 'l'

# Print table
init(autoreset=True)
print(table)
