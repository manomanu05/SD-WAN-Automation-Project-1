# This script will create a Voice SLA Class List in Cisco SD-WAN Sandbox

import requests
import json

requests.packages.urllib3.disable_warnings()  # Disable SSL warnings

USERNAME = "devnetuser"  # Sandbox username
PASSWORD = "RG!_Yw919_83"  # Sandbox password

# Authenticate and get session ID
login_url = 'https://sandbox-sdwan-2.cisco.com/j_security_check'
login_data = {'j_username': USERNAME, 'j_password': PASSWORD}
response = requests.post(url=login_url, data=login_data, verify=False)
if response.status_code != 200:
    print(f"Authentication failed: {response.text}")
    exit()
token1 = 'JSESSIONID=' + response.cookies.get_dict()['JSESSIONID']
print('token1=', token1)

# Get XSRF token
token_url = 'https://sandbox-sdwan-2.cisco.com:443/dataservice/client/token'
headers = {'Cookie': token1, 'content-type': 'application/json'}
response = requests.get(url=token_url, headers=headers, verify=False)
if response.status_code != 200:
    print(f"Failed to get token: {response.text}")
    exit()
token2 = response.text
print('token2=', token2)

# Create Voice SLA Class List
url = "https://sandbox-sdwan-2.cisco.com:443/dataservice/template/policy/list/sla"
payload = {
    "name": "Voice_SLA_Class",
    "description": "Create Voice_SLA_Class",
    "type": "sla",
    "entries": [
        {
            "latency": "180",
            "loss": "2",
            "jitter": "35"
        }
    ]
}
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-XSRF-TOKEN': token2,
    'Cookie': token1
}
response = requests.post(url, headers=headers, json=payload, verify=False)
if response.status_code != 200:
    print(f"Failed to create template: {response.text}")
    exit()

print(response.text)
