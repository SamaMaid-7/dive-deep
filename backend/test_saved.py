import requests

# Login first
login = requests.post('http://127.0.0.1:5000/login', json={
    "email": "test@test.com",
    "password": "123456"
})

token = login.json()['token']
headers = {"Authorization": f"Bearer {token}"}

# Save a lesson
save = requests.post('http://127.0.0.1:5000/saved/add',
    json={"lesson_id": 1},
    headers=headers
)
print("Save lesson:", save.json())

# Get all saved lessons
saved = requests.get('http://127.0.0.1:5000/saved', headers=headers)
print("Saved lessons:", saved.json())

# Unsave a lesson
unsave = requests.post('http://127.0.0.1:5000/saved/remove',
    json={"lesson_id": 1},
    headers=headers
)
print("Unsave lesson:", unsave.json())