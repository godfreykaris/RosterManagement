import requests

# Define the URL for the registration endpoint
url = 'http://localhost:5000/api/register'

# Define the data you want to send as a dictionary
data = {
    'username': 'miami3d',
    'email': 'iam@gmail.com',
    'password': 'iampassword12',
    'confirmPassword': 'iampassword12'  # Confirm password can be the same as the password
}

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

    