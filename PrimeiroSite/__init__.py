from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import MetaData


app = Flask(__name__)
app.config['SECRET_KEY'] = '00208f9aeab6bb9ff101452be6b2bf1a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///primeirosite.db'
app.config['TIMEZONE'] = 'America/Sao_Paulo'
banco_de_dados = SQLAlchemy(app, session_options={"autoflush": False}, metadata=MetaData(naming_convention={"ix": "ix_%(column_0_label)s", "uq": "uq_%(table_name)s_%(column_0_name)s", "ck": "ck_%(table_name)s_%(constraint_name)s", "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", "pk": "pk_%(table_name)s"}))
cript = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para continuar!'
login_manager.login_message_category = 'alert-primary'
from PrimeiroSite import routes
