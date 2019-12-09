from decouple import config
import uuid
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import insert_user


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def index():
        #rand_name = str(uuid.uuid4())
        #rand_u = User(name=rand_name)
        #DB.session.add(rand_u)
        #DB.session.commit()
        users = User.query.all()
        return render_template('base.html', title='index', users=users)

    @app.route('/hello')
    def hello():
        return render_template('base.html', title='hello...world.')
    
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




    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset.', users=[])

    return app

"""if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)"""