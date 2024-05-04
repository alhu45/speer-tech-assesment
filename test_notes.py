import requests

BASE = "http://127.0.0.1:5000/"

users = [
    {"username": "alanhu", "password": "12345"},
    {"username": "lindahu", "password": "54321"}
]

for i in range(len(users)):
    response = requests.post(BASE + "api/auth/signup", json=users[i])
    if response.status_code == 201:
        try:
            print(response.json())
        except ValueError: 
            print("Response content is not valid JSON")
    else:
        print(f'Failed request with status code: {response.status_code}, response: {response.text}')

# Logins in user
response = requests.post(BASE + "api/auth/login", json=users[0])
print(response.json())


data = [
    {"title": "Note 1", "content": "Hello. This is note 1.", "user_id": "1"},
    {"title": "Note 2", "content": "Hi! This is note 2", "user_id": "2"},
    {"title": "Note 3", "content": "Hi! This is note 3", "user_id": "2"},
    {"title": "Note 4", "content": "", "user_id": "2"},
    {"title": "", "content": "Note 5", "user_id": "1"}
]

for i in range(len(data)):
    response = requests.post(BASE + "notes/" + str(i), json=data[i])
    if response.status_code == 201:
        try:
            print(response.json())
        except ValueError: 
            print("Response content is not valid JSON")
    else:
        print(f'Failed request with status code: {response.status_code}, response: {response.text}')


input()

# Gets a note using the note ID
response = requests.get(BASE + "notes/0")
print(response.json())

input()

# Gets all the notes in database
response = requests.get(BASE + "notes/999")
print(response.json())

input()

# Updates a note
response = requests.patch(BASE + "notes/0", {"content": "The note was changed!"})
print(response.json())

input()

# Search notes based off keyword
response = requests.get(BASE + "noteSearch/search", params={"query": "Hi!"})
print(response.json())

input()

# Delete a note
response = requests.delete(BASE + "notes/0")
response = requests.delete(BASE + "notes/1")
response = requests.delete(BASE + "notes/2")

input()

# Checks if the note(s) is deleted
response = requests.get(BASE + "notes/0")
print(response.json())

response = requests.get(BASE + "notes/1")
print(response.json())

response = requests.get(BASE + "notes/2")
print(response.json())
