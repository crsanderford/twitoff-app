import uuid
from flask import Flask, render_template
from .models import DB, User, Tweet


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
    DB.init_app(app)

    @app.route('/')
    def index():
        rand_name = str(uuid.uuid4())
        rand_u = User(name=rand_name)
        DB.session.add(rand_u)
        DB.session.commit()
        return 'index page.'

    @app.route('/hello')
    def hello():
        return render_template('base.html', title='hello...world.')

    return app

"""if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)"""