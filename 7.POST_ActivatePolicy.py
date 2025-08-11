# This script activates an existing vSmart policy in Cisco SD-WAN Always-On Sandbox

import requests

requests.packages.urllib3.disable_warnings()

USERNAME = "devnetuser"
PASSWORD = "RG!_Yw919_83"

# Step 1: Authenticate and get JSESSIONID
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

# Step 3: Activate the Policy (Replace policyId with actual value)
policy_id = "2f50318b-c8fc-4729-9719-146d08520df7"  # Example Policy ID
url = f"https://sandbox-sdwan-2.cisco.com/dataservice/template/policy/vsmart/activate/{policy_id}?confirm=true"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-XSRF-TOKEN': token2,
    'Cookie': token1
}

response = requests.post(url, headers=headers, json={}, verify=False)

if response.status_code != 200:
    print(f"Failed to activate policy: {response.text}")
    exit()

print("Policy activated successfully:", response.text)
