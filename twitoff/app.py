from decouple import config
import uuid
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import insert_user, update_users
from .predict import predict_user


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def index():
        users = User.query.all()
        return render_template('base.html', title='index', users=users)

    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                insert_user(name)
                message = f'User {name} successfully added.'
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/predict', methods=['POST'])
    def predict(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'choose distinct users!'
        else:
            predicted = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely to be tweeted by {} than {}'.format(
                request.values['tweet_text'], user1 if predicted else user2,
                user2 if predicted else user1)
        return render_template('prediction.html', title='Prediction', message=message)


    @app.route('/update')
    def update():
        update_users()
        return render_template('base.html', users=User.query.all(), title='all tweets updated.')

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset.', users=[])

    return app