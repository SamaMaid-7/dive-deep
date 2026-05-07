import requests

# Login first
login = requests.post('http://127.0.0.1:5000/login', json={
    "email": "test@test.com",
    "password": "123456"
})

token = login.json()['token']
headers = {"Authorization": f"Bearer {token}"}

# Set a manual reminder
set_r = requests.post('http://127.0.0.1:5000/reminder/set',
    json={"reminder_time": "08:00"},
    headers=headers
)
print("Set reminder:", set_r.json())

# Get reminder
get_r = requests.get('http://127.0.0.1:5000/reminder', headers=headers)
print("Get reminder:", get_r.json())

# Check auto suggestion
suggest = requests.get('http://127.0.0.1:5000/reminder/suggest', headers=headers)
print("Suggest reminder:", suggest.json())