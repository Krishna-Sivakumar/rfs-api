import requests, json
'''
board = {
    'board_name': 'Science Board',
    'description': 'A board for science'
}

user = {
    'username': 'John Doe',
    'user_email': 'johndoe@example.com',
    'password': 'password1'
}

post = {
    'name': 'Whatevs',
    'content': 'Lorem ipsum dolor',
    'board_name': 'Science Board',
    'user_email': user['user_email']
}
response_1 = requests.post('http://127.0.0.1:5000/users', json.dumps(user))
print(response_1.json())

response_2 = requests.post('http://127.0.0.1:5000/boards', json.dumps(board))
print(response_2.json())

response_3 = requests.post('http://127.0.0.1:5000/posts', json.dumps(post))
print(response_3.json())


for _ in range(3):
    response = requests.post('http://127.0.0.1:5000/comments', json.dumps({
        'user_email': user['user_email'],
        'post_id': 1,
        'content': 'Lorem ipsum dolor'
    }))
    print(response.json())

response = requests.get('http://127.0.0.1:5000/posts', {'post_id': 1})
response = response.json()['data']
for comment_string in json.loads(response).get('comments'):
    print(json.loads(comment_string))
'''
for i in range(1,6):
    response = requests.get('http://127.0.0.1:5000/comments', {'comment_id': i})
    print(response.json())