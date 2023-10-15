import requests

#********************* Start of register testing *******************************#

# # Define the URL for the registration endpoint
# url = 'http://localhost:5000/api/register'

# # Define the data you want to send as a dictionary
# data = {
#     'username': 'miami3d',
#     'email': 'iam@gmail.com',
#     'password': 'iampassword12',
#     'confirmPassword': 'iampassword12'  # Confirm password can be the same as the password
# }

#*************************** End of register testing ********************************#

#*************************** Start of update profile ********************************#

# Define the URL for the registration endpoint
url = 'http://localhost:5000/api/update_profile'

# Define the data you want to send as a dictionary
data = {
    'user_id': 1,
    'user_level': '2', # User levels 3 - admin, 2 - coach, 1 - wrestler
    'username': 'miami8',
    'email': 'weare@gmail.com',
    'name': 'Me3',
    'address': "80345 Newyork City",
    'password': 'iampassword12',
    'confirm_password': 'iampassword12',  # Confirm password can be the same as the password
    'weight': 50.5, # Weight in Kgs
    'team': 'Wagon'
}

#***************************** End of update profile ****************************#

# Send a POST request with the data
response = requests.post(url, json=data)  # Using json to automatically serialize the data as JSON

if response.status_code == 200:
    data = response.json()
    message = data['message']
    print(message)
else:
    error_data = response.json()
    error_message = error_data['error']
    error_code = response.status_code
    print(f'Error {error_code}: {error_message}')