from PrimeiroSite import banco_de_dados, login_manager
from datetime import datetime
from flask_login import UserMixin
import pytz



@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(id_usuario)


class Usuario(banco_de_dados.Model, UserMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    nome = banco_de_dados.Column(banco_de_dados.String, nullable=False)
    email = banco_de_dados.Column(banco_de_dados.String, nullable=False, unique=True)
    senha = banco_de_dados.Column(banco_de_dados.String, nullable=False)
    foto_perfil = banco_de_dados.Column(banco_de_dados.String, nullable=False, default='padrao.jpg')
    foto_fundo = banco_de_dados.Column(banco_de_dados.String, nullable=False, default='padrao.png')
    posts = banco_de_dados.relationship('Post', backref='autor', lazy=True)
    comentarios = banco_de_dados.relationship('Comentario', backref='autor_post', lazy=True)


class Post(banco_de_dados.Model):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True}
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    titulo = banco_de_dados.Column(banco_de_dados.String, nullable=False)
    corpo = banco_de_dados.Column(banco_de_dados.Text, nullable=False)
    data = banco_de_dados.Column(banco_de_dados.DateTime, nullable=False, default=datetime.now)
    id_autor = banco_de_dados.Column(banco_de_dados.Integer, banco_de_dados.ForeignKey('usuario.id'), nullable=False)
    comentarios = banco_de_dados.relationship('Comentario',backref='post',lazy=True,cascade='all, delete')


class Comentario(banco_de_dados.Model):
    __tablename__ = 'comentarios'
    __table_args__ = {'extend_existing': True}
    id = banco_de_dados.Column(banco_de_dados.Integer,primary_key=True)
    texto = banco_de_dados.Column(banco_de_dados.Text,nullable=False)
    data = banco_de_dados.Column(banco_de_dados.DateTime, nullable=False, default=datetime.now)
    id_autor = banco_de_dados.Column(banco_de_dados.Integer, banco_de_dados.ForeignKey('usuario.id'), nullable=False)
    id_post = banco_de_dados.Column(banco_de_dados.Integer,banco_de_dados.ForeignKey('post.id'),nullable=False)

