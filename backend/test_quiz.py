import requests

# Login first
login = requests.post('http://127.0.0.1:5000/login', json={
    "email": "test@test.com",
    "password": "123456"
})

token = login.json()['token']
headers = {"Authorization": f"Bearer {token}"}

# Get quiz questions for session 1
questions = requests.get('http://127.0.0.1:5000/quiz/1', headers=headers)
print("Questions:", questions.json())

# Submit quiz answers
# We will answer all with option "a" just for testing
quiz_data = questions.json()
answers = {str(q['id']): 'a' for q in quiz_data}

submit = requests.post('http://127.0.0.1:5000/quiz/submit',
    json={
        "session_id": 1,
        "answers": answers
    },
    headers=headers
)
print("Quiz Result:", submit.json())