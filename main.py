from flask import Flask, request
from models import *
from flask_login import current_user, login_user, login_required
import os.path, json


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    db.init_app(app)
    login.init_app(app)
    return app


def init_database(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':

    app = create_app()
    if not os.path.isfile('sqlite:///test.db'):
        init_database(app)
    login = LoginManager()

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


    @app.route('/posts/get', methods=['GET', 'POST'])
    def posts():
        result = {}
        if request.method == 'GET':
            post_id = request.args['post_id']
            post = Post.query.filter_by(post_id = post_id).first()
            result['data'] = post.to_json()
        return result


    @app.route('/posts/post', methods = ['POST'])
    @login_required
    def postThread():

        result = {
            'message': '',
            'data': ''
        }

        if request.method == 'POST':
            data = json.loads(request.data)
            post = Post(name = data['name'], content = data['content'], user_email = data['user_email'], board_name = data['board_name'])

            if len(Post.query.filter_by(name = post.name, board_name = data['board_name']).all()) > 0:
                result['message'] = 'Post already exists'
            else:
                db.session.add(post)
                db.session.commit()
                result['message'] = 'Post created'
                result['data'] = post.to_json()

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
            comment = Comment(user_email = data['user_email'], post_id = data['post_id'], content = data['content'])
            db.session.add(comment)
            db.session.commit()
            result['message'] = 'Comment was created'
            result['data'] = comment.to_json()

        return result


    app.run()
