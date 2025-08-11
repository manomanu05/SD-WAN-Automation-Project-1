# This Script will show the Activation Status of a Policy on the controller (Cisco SD-WAN Always-On Sandbox)

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

# Show Activation Status Policy
# Replace the Policy ID here with the actual ID from your sandbox environment
policy_id = "45a57f12-af13-4926-85d9-3dac14b446cc"
request_url = f'https://sandbox-sdwan-2.cisco.com/dataservice/device/action/status/vsmart_policy_config-{policy_id}'

headers = {
    'Content-Type': "application/json",
    'Cookie': token1,
    'X-XSRF-TOKEN': token2
}

response = requests.get(url=request_url, headers=headers, verify=False)
print("status:", response.status_code)
print(json.dumps(response.json(), indent=5))
