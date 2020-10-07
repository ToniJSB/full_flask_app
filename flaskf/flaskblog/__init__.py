from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b3cbd5c4434006a5fc3d3f91c1cb4274'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Projects\\full_flask_app\\bloggerSite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flaskblog import routes