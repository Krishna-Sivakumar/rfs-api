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


if __name__ == '__main__':

    app = create_app()
    if not os.path.isfile('sqlite:///test.db'):
        init_database(app)

    @app.route('/users', methods = ['GET', 'POST'])
    def users():
        result = {
            'message': None,
            'data': None,
        }

        if request.method == 'GET':
            user_email = request.args['user_email']
            if not isinstance(user_email, int):
                result['message'] = 'Error: user_email must be of type integer'
            else:
                result['message'] = 'User exists'
                result['data'] = User.query.filter_by(user_email = user_email).first().to_json()

        elif request.method == 'POST':
            data = json.loads(request.data)

            try:
                user = User(username = data['username'], user_email = data['user_email'], deleted = False)
                user.set_password(data['password'])

                if len(User.query.filter_by(user_email = user.user_email).all()) > 0:
                    result['message'] = 'User already exists'
                else:
                    db.session.add(user)
                    db.session.commit()
                    result['message'] = 'User created'
                    result['data'] = user.to_json()

            except KeyError:
                result['message'] = 'Error: request does not match format'

        return json.dumps(result)


    @app.route('/boards', methods=['GET', 'POST'])
    def boards():
        result = {}
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            data = json.loads(request.data)
            board = Board(board_name = data['board_name'], description = data['description'])
            if len(Board.query.filter_by(board_name = board.board_name).all()) > 0:
                result['message'] = 'Board already exists'
            else:
                db.session.add(board)
                db.session.commit()
                result['message'] = 'Board was created'
                result['data'] =  board.to_json()
        return result


    @app.route('/threads/get', methods=['GET', 'POST'])
    def get_thread():
        result = {}
        if request.method == 'GET':
            param = request.args['filter']
            if not param == 'all':
                thread_id = request.args['thread_id']
                thread = Thread.query.filter_by(thread_id = thread_id).first()
                result['data'] = thread.to_json()
            else:
                print([threaD.to_json() for threaD in Thread.query.all()])
                result['data'] = [threaD.to_json() for threaD in Thread.query.all()]
        return result


    @app.route('/threads/post', methods = ['POST'])
    def post_thread():

        result = {
            'message': '',
            'data': ''
        }

        if request.method == 'POST':
            data = json.loads(request.data)
            user = User.query.get(data['user_email'])
            if not user == None and user.check_password(data['password']):
                thread = Thread(name = data['name'], content = data['content'], user_email = data['user_email'], board_name = data['board_name'])

                if len(Thread.query.filter_by(name = thread.name, board_name = data['board_name']).all()) > 0:
                    result['message'] = 'Thread already exists'
                else:
                    db.session.add(thread)
                    db.session.commit()
                    result['message'] = 'Thread created'
                    result['data'] = thread.to_json()
            else:
                result['message'] = 'User/Password combination is not valid'

        return result


    @app.route('/comments', methods=['GET', 'POST'])
    def comments():

        result = {
            'message': '',
            'data': ''
        }

        if request.method == 'GET':
            comment_id = request.args['comment_id']
            query = Comment.query.get(comment_id)
            if not query == None:
                result['data'] = query.to_json()

        elif request.method == 'POST':
            data = json.loads(request.data)
            comment = Comment(user_email = data['user_email'], thread_id = data['thread_id'], content = data['content'])
            db.session.add(comment)
            db.session.commit()
            result['message'] = 'Comment was created'
            result['data'] = comment.to_json()

        return result

    app.run()
