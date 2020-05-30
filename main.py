from flask import Flask, request
from models import *
import os, os.path, json


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    db.init_app(app)
    return app


def init_database(app):
    with app.app_context():
        db.create_all()

app = create_app()
if not os.path.isfile('sqlite:///test.db'):
    init_database(app)

@app.route('/users/get', methods = ['GET', 'POST'])
def get_user():

    result = {
        'message': None,
        'data': None,
    }

    data = request.args

    if request.method == 'GET':

        result['data'] = User.query.get(data['user_email']).to_json()

    return result


@app.route('/users/post', methods = ['POST'])
def post_user():

    result = {
        'message': None,
        'data': None,
    }

    if request.method == 'POST':
        data = json.loads(request.data)

        user = User(username = data['username'], user_email = data['user_email'], deleted = False)
        user.set_password(data['password'])

        if User.query.get(data['user_email']):

            result['message'] = 'User already exists'

        else:

            db.session.add(user)
            db.session.commit()
            result['message'] = 'User created'

    return result


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

        data = json.loads(request.data)
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

        data = json.loads(request.data)

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

        result['data'] = Comment.query.get(data['comment_id'])


@app.route('/comments/post', methods=['POST'])
def post_comment():

    result = {
        'message': '',
        'data': ''
    }

    data = json.loads(request.data)
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