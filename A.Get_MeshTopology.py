# This Script will show the Mesh Topology configured on Cisco SD-WAN Controller (Always-On Sandbox)

import requests
import json
from prettytable import PrettyTable
from colorama import init, Fore, Style

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Sandbox credentials
USERNAME = "devnetuser"
PASSWORD = "RG!_Yw919_83"

# Step 1: Authentication - Get JSESSIONID
login_url = 'https://sandbox-sdwan-2.cisco.com/j_security_check'
login_data = {'j_username': USERNAME, 'j_password': PASSWORD}

response = requests.post(url=login_url, data=login_data, verify=False)
if response.status_code != 200:
    print(f"Authentication failed: {response.text}")
    exit()

token1 = 'JSESSIONID=' + response.cookies.get_dict()['JSESSIONID']
print('token1 =', token1)

# Step 2: Get XSRF Token
token_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/client/token'
headers = {'Cookie': token1, 'content-type': 'application/json'}

response = requests.get(url=token_url, headers=headers, verify=False)
if response.status_code != 200:
    print(f"Failed to get token: {response.text}")
    exit()

token2 = response.text
print('token2 =', token2)

# Step 3: Fetch Mesh Topology details
request_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/template/policy/definition/mesh/'
headers = {
    'Content-Type': 'application/json',
    'Cookie': token1,
    'X-XSRF-TOKEN': token2
}

response = requests.get(url=request_url, headers=headers, verify=False)
print("status:", response.status_code)

# Pretty print raw JSON
print(json.dumps(response.json(), indent=4))

# Step 4: Parse JSON and display in table
mesh_data = response.json()

table = PrettyTable()
table.field_names = ["Name", "DefinitionId", "Type", "References"]

for entry in mesh_data.get('data', []):
    table.add_row([
        f"{Fore.GREEN}{entry['name']}{Style.RESET_ALL}",
        f"{Fore.YELLOW}{entry['definitionId']}{Style.RESET_ALL}",
        f"{Fore.RED}{entry['type']}{Style.RESET_ALL}",
        f"{Fore.MAGENTA}{entry.get('references', '')}{Style.RESET_ALL}"
    ])

# Align columns
table.align['Name'] = 'l'
table.align['DefinitionId'] = 'l'
table.align['Type'] = 'l'
table.align['References'] = 'l'

# Print table with color
init(autoreset=True)
print(table)
