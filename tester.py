import requests, json

board = {
    'name': 'Science Board',
    'description': 'A board for science'
}

user = {
    'name': 'John Doe',
    'email': 'johndoe@example.com',
    'password': 'password1'
}

post = {
    'name': 'Whatevs',
    'content': 'asodnlkadnlkn asdnklasjdoijs djioa joidasjdio jasiojdaiosajiod jsiojiodsj',
    'user_id': 1,
    'board_name': 'Science Board',
}

response = requests.post('http://127.0.0.1:5000/users', json.dumps(user))
print(response.json())