from flask import Flask
from flask_login import LoginManager
import os

from routes import initialize_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

initialize_routes(app, login_manager)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3030)