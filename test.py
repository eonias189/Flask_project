import requests

url = 'http://127.0.0.1:5000/api/login'

response = requests.post(url, json={'login': '1', 'password': '2'}, params={'key': 'login_key'})
print(response.json())