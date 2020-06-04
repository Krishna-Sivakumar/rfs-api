from __init__ import app
from flask import request
from models import *
import json


def process_request_data():

    result = dict(request.form)

    if request.authorization:
        result['user'] = dict(request.authorization)
        result['user']['user_email'] = result['user']['username']

    return result


@app.route('/users/get', methods = ['GET', 'POST'])
def get_user():

    result = {
        'message': None,
        'data': None,
    }

    data = request.args

    if request.method == 'GET':

        if User.query.get(data['user_email']):
            result['data'] = User.query.get(data['user_email'])

    return result


@app.route('/users/post', methods = ['POST'])
def post_user():

    result = {
        'message': None,
        'data': None,
    }

    if request.method == 'POST':

        data = process_request_data()

        user = User(username = data['username'], user_email = data['user_email'], deleted = False)
        user.set_password(data['password'])

        if User.query.get(data['user_email']):
            result['message'] = 'User already exists'

        else:

            db.session.add(user)
            db.session.commit()
            result['message'] = 'User created'

    return result


@app.route('/users/put', methods = ['GET', 'POST'])
def update_user():

    result = {
        'message': None,
        'data': None,
    }

    data = process_request_data()
    user = User.query.get(data['user']['user_email'])

    if user and user.check_password(data['user']['password']) and data['target_user_email'] == user.user_email:
        user.deleted = data['deleted']
        user.description = data['description']
        user.username = data['username']
        result['message'] = 'User modified'
    else:
        result['message'] = 'Invalid User-email/Password combination'


@app.route('/boards/get', methods=['GET', 'POST'])
def get_board():

    result = {
        'message': '',
        'data': '',
    }

    if request.method == 'GET':

        data = request.args

        if data['filter'] == 'all':

            request['data'] = [board.to_json() for board in Board.query.all()]

        else:

            request['data'] = Board.query.get(data['board_name'])


@app.route('/boards/post', methods = ['POST'])
def post_board():

    result = {
        'message': '',
        'data': '',
    }

    if request.method == 'POST':

        data = process_request_data()

        user = User.query.get(data['user']['user_email'])

        if (not user == None) and (user.check_password(data['user']['password'])):

            if Board.query.get(data['board_name']) == None:
                board = Board(board_name = data['board_name'], description = data['description'])
                db.session.add(board)
                db.session.commit()
                result['message'] = 'Board was created'

            else:
                result['message'] = 'Board already exists'
        else:

            result['message'] = 'User-email/Password combination is invalid'

    return result


@app.route('/threads/get', methods=['GET'])
def get_thread():

    result = {}

    if request.method == 'GET':

        data = request.args

        if not data['filter'] == 'all':

            thread_id = data['thread_id']
            thread = Thread.query.filter_by(thread_id = thread_id).first()
            if thread:
                result['data'] = thread.to_json()


        else:

            result['data'] = [thread.to_json() for thread in Thread.query.all()]

    return result


@app.route('/threads/post', methods = ['POST'])
def post_thread():

    result = {
        'message': '',
        'data': ''
    }

    if request.method == 'POST':

        data = process_request_data()

        if (not User.query.get(data['user']['email']) == None) and (not Board.query.get(data['board_name']) == None):

            thread = Thread(name = data['name'], content = data['content'], user_email = data['user']['user_email'])
            user = User.query.get(data['user']['user_email'])

            if user.check_password(data['user']['password']):
                db.session.add(thread)
                db.session.commit()
                result['message'] = 'Thread created'
            else:
                result['message'] = 'User-email/Password combination is invalid'
        else:
            result['message'] = 'User/Board does not exist'

    return result


@app.route('/comments/get', methods = ['GET'])
def get_comment():

    result = {
        'message': '',
        'data': '',
    }

    data = request.args

    if data['filter'] == 'all':

        result['message'] = 'Cannot return all comments'

    else:
        if Comment.query.get(data['comment_id']):
            result['data'] = Comment.query.get(data['comment_id'])

    return result


@app.route('/comments/post', methods=['POST'])
def post_comment():

    result = {
        'message': '',
        'data': ''
    }

    data = process_request_data()
    user = User.query.get(data['user']['user_email'])

    if (not user == None) and (user.check_password(data['user']['password'])):

        if not Thread.query.get(data['thread_id']) == None:

            if data['parent_id'] == None:

                comment = Comment(user_email = user.user_email, thread_id = data['thread_id'], content = data['content'])

            else:

                if not Comment.query.get(data['parent_id']) == None:

                    comment = Comment(user_email=user.user_email, thread_id=data['thread_id'], parent_id = data['parent_id'], content=data['content'])

                else:

                    result['message'] = 'Parent comment does not exist'

        else:

            result['message'] = 'Thread does not exist'

    else:
        result['message'] = 'User-email/Password combination is invalid'