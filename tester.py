import requests, json

board = {
    'name': 'Science Board',
    'description': 'A board for science'
}

user = {
    'name': 'John Doe',
    'password': 'password1'
}

post = {
    'name': 'Whatevs',
    'content': 'asodnlkadnlkn asdnklasjdoijs djioa joidasjdio jasiojdaiosajiod jsiojiodsj',
    'user_id': 1,
    'board_name': 'Science Board',
}
'''
x = requests.post('http://127.0.0.1:5000/boards', json.dumps(board))
print(x.json())

y = requests.post('http://127.0.0.1:5000/users', json.dumps(user))
print(y.json())
post['userID'] = x.json()['data']['user_id']
'''
z = requests.post('http://127.0.0.1:5000/posts', json.dumps(post))
print(z)
print(z.json())
print(z.raw)