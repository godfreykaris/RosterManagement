#import requests
# #********************* Start of register testing *******************************#

# # # Define the URL for the registration endpoint
# # url = 'http://localhost:5000/api/register'

# # # Define the data you want to send as a dictionary
# # data = {
# #     'username': 'miami3d',
# #     'email': 'iam@gmail.com',
# #     'password': 'iampassword12',
# #     'confirmPassword': 'iampassword12'  # Confirm password can be the same as the password
# # }

# #*************************** End of register testing ********************************#

# #*************************** Start of update profile ********************************#

# # Define the URL for the registration endpoint
# url = 'http://localhost:5000/api/update_profile'

# # Define the data you want to send as a dictionary
# data = {
#     'user_id': 1,
#     'user_level': '2', # User levels 3 - admin, 2 - coach, 1 - wrestler
#     'username': 'miami8',
#     'email': 'weare@gmail.com',
#     'name': 'Me3',
#     'address': "80345 Newyork City",
#     'password': 'iampassword12',
#     'confirm_password': 'iampassword12',  # Confirm password can be the same as the password
#     'weight': 50.5, # Weight in Kgs
#     'team': 'Wagon'
# }

# #***************************** End of update profile ****************************#

# # Send a POST request with the data
# response = requests.post(url, json=data)  # Using json to automatically serialize the data as JSON

# if response.status_code == 200:
#     data = response.json()
#     message = data['message']
#     print(message)
# else:
#     error_data = response.json()
#     error_message = error_data['error']
#     error_code = response.status_code
#     print(f'Error {error_code}: {error_message}')

# Define the URL for the registration endpoint
# url = 'http://localhost:5000/api/update_profile'

# # Define the data you want to send as a dictionary
# data = {
#     'user_id': 1,
#     'user_level': '2', # User levels 3 - admin, 2 - coach, 1 - wrestler
#     'username': 'miami8',
#     'email': 'weare@gmail.com',
#     'name': 'Me3',
#     'address': "80345 Newyork City",
#     'password': 'iampassword12',
#     'confirm_password': 'iampassword12',  # Confirm password can be the same as the password
#     'weight': 50.5, # Weight in Kgs
#     'team': 'Wagon'
# }

############################### UserRetriever class ####################################
import requests
# Replace with the actual URL of your Flask app
base_url = 'http://localhost:5000'  # Update with your app's URL

user_id = 8  # Replace with the user_id you want to fetch

response = requests.get(f'{base_url}/api/fetch_user/{user_id}')

# Print the response
print(response.status_code)
print(response.json())  # Assuming the response is in JSON format



# Replace with the actual URL of your Flask app
# base_url = 'http://localhost:5000'  # Update with your app's URL

# response = requests.get(f'{base_url}/api/fetch_coaches')

# # Print the response
# print(response.status_code)
# print(response.json())  # Assuming the response is in JSON format

# # Replace with the actual URL of your Flask app
# base_url = 'http://localhost:5000'  # Update with your app's URL

# team_id = 1  # Replace with the team_id you want to fetch wrestlers for

# response = requests.get(f'{base_url}/api/fetch_wrestlers/{team_id}')

# # Print the response
# print(response.status_code)
# print(response.json())  # Assuming the response is in JSON format


# # Replace with the actual URL of your Flask app
# base_url = 'http://localhost:5000'  # Update with your app's URL

# user_id = 1  # Replace with the user_id you want to delete
# user_level = 2  # Replace with the user_level for authorization

# # Define the data to send in the POST request
# data = {
#     'user_id': user_id,
#     'user_level': user_level,
# }

# response = requests.post(f'{base_url}/api/delete_user/{user_id}/{user_level}', json=data)

# # Print the response
# print(response.status_code)
# print(response.json())  # Assuming the response is in JSON format

# ##############################################################################################