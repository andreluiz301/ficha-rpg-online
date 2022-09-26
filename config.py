from flask import *
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  

path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'banco.db')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
jwt = JWTManager(app)