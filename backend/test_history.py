import requests

# First login to get token
login = requests.post('http://127.0.0.1:5000/login', json={
    "email": "test@test.com",
    "password": "123456"
})

token = login.json()['token']
headers = {"Authorization": f"Bearer {token}"}

# Add a history record
add = requests.post('http://127.0.0.1:5000/history/add',
    json={"session_id": 1, "completed": True},
    headers=headers
)
print("Add history:", add.json())

# Get history
history = requests.get('http://127.0.0.1:5000/history', headers=headers)
print("History:", history.json())

# Get calendar
calendar = requests.get('http://127.0.0.1:5000/history/calendar', headers=headers)
print("Calendar:", calendar.json())