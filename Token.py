# This Script will obtain X-XSRF-TOKEN Token (API-Token) from Cisco SD-WAN Always-On Sandbox

import requests

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

# Get X-XSRF-TOKEN
token_url = 'https://sandbox-sdwan-2.cisco.com/dataservice/client/token'
headers = {'Cookie': token1, 'content-type': 'application/json'}

response = requests.get(url=token_url, headers=headers, verify=False)
if response.status_code != 200:
    print(f"Failed to get token: {response.text}")
    exit()

token2 = response.text
print('token2 =', token2)
