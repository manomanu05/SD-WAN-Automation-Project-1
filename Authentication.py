# This Script will authenticate user and obtain JSESSIONID from Cisco SD-WAN Always-On Sandbox

import requests

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Sandbox credentials
USERNAME = "devnetuser"
PASSWORD = "RG!_Yw919_83"

# Authentication
login_url = 'https://sandbox-sdwan-2.cisco.com/j_security_check'
login_data = {'j_username': USERNAME, 'j_password': PASSWORD}

# Send POST request to login
response = requests.post(url=login_url, data=login_data, verify=False)

# Check login status
if response.status_code != 200:
    print(f"Authentication failed: {response.text}")
    exit()

# Extract JSESSIONID
token1 = 'JSESSIONID=' + response.cookies.get_dict()['JSESSIONID']
print('token1 =', token1)
