import requests

BASE = "http://127.0.0.1:5000/"

users = [
    {"username": "alanhu", "password": "12345"}, 
    {"username": "lindahu", "password": "54321"}, 
    {"username": " " , "password": " "}
]

# Creates users
for i in range(len(users)):
    response = requests.post(BASE + "api/auth/signup", json=users[i])
    if response.status_code == 201:
        try:
            print(response.json())
        except ValueError: 
            print("Response content is not valid JSON")
    else:
        print(f'Failed request with status code: {response.status_code}, response: {response.text}')

# Should print a message saying user already exists
response = requests.post(BASE + "api/auth/signup", json=users[0])


input()

# Logs in, given a token for the specific user
response = requests.post(BASE + "api/auth/login", json=users[0])
print(response.json())

input()

# Logs in, given a token for the specific user
response = requests.post(BASE + "api/auth/login", json=users[1])
print(response.json())
