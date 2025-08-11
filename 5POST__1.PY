# This script creates an Application-Aware Routing (AAR) policy in Cisco SD-WAN Sandbox

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
token_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/client/token'
headers = {'Cookie': token1, 'content-type': 'application/json'}
response = requests.get(url=token_url, headers=headers, verify=False)
if response.status_code != 200:
    print(f"Failed to get token: {response.text}")
    exit()
token2 = response.text
print('token2=', token2)

# Create AAR Policy
url = "https://sandbox-sdwan-2.cisco.com/dataservice/template/policy/definition/approute"
payload = {
    "name": "AAR_VoiceTraffic_MPLS",
    "type": "appRoute",
    "description": "Voice DSCP 46 should prefer MPLS circuits",
    "sequences": [
        {
            "sequenceId": 1,
            "sequenceName": "App Route",
            "sequenceType": "appRoute",
            "match": {
                "entries": [
                    {"field": "dscp", "value": "46"}
                ]
            },
            "actions": [
                {
                    "type": "slaClass",
                    "parameter": [
                        {"field": "name", "ref": "69f6ceaf-a34b-45d8-a0f7-ad568a25bf8c"},  # SLA Class ID
                        {"field": "preferredColor", "value": "mpls"}
                    ]
                },
                {"type": "backupSlaPreferredColor", "parameter": "biz-internet"}
            ]
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
