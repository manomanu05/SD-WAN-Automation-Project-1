# This script creates and attaches a policy to vSmart in Cisco SD-WAN Always-On Sandbox

import requests
import json

requests.packages.urllib3.disable_warnings()

USERNAME = "devnetuser"
PASSWORD = "RG!_Yw919_83"

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
token_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/client/token'
headers = {'Cookie': token1, 'content-type': 'application/json'}
response = requests.get(url=token_url, headers=headers, verify=False)
if response.status_code != 200:
    print(f"Failed to get token: {response.text}")
    exit()
token2 = response.text
print('token2=', token2)

# Create and attach policy to vSmart
url = "https://sandbox-sdwan-2.cisco.com/dataservice/template/policy/vsmart/"
payload = {
    "policyName": "Policy_For_Vsmart",
    "policyDescription": "Policy_For_Vsmart",
    "policyType": "feature",
    "policyDefinition": {
        "assembly": [
            {
                "definitionId": "24c100b0-7c73-438d-bc2f-6345dcf7087c",  # AAR Policy ID
                "type": "appRoute",
                "entries": [
                    {
                        "siteLists": [
                            "49665e93-5498-4db1-8906-d99dd5f75989"  # Site List ID
                        ],
                        "vpnLists": [
                            "d100cc41-2e4f-4841-b85c-443e20a141b0"  # VPN List ID
                        ]
                    }
                ]
            },
            {
                "definitionId": "0bd97d73-b2e6-41d7-8682-9c99eee49ed4",  # Mesh Topology ID
                "type": "mesh"
            }
        ]
    },
    "isPolicyActivated": False
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-XSRF-TOKEN': token2,
    'Cookie': token1
}

response = requests.post(url, headers=headers, json=payload, verify=False)
if response.status_code != 200:
    print(f"Failed to create and attach policy: {response.text}")
    exit()

print(response.text)
