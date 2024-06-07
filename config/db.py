from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            static_folder='config/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3307/injcg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "comecaca"

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import User, Empresa, Cliente, Vendedor