from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import PasswordField, EmailField, SubmitField, StringField, BooleanField,TextAreaField
from wtforms.validators import EqualTo, Email, Length, DataRequired, ValidationError
from PrimeiroSite.models import Usuario
from PrimeiroSite import app
from flask_login import current_user


class FormRegistro(FlaskForm):
    nome_usuario = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='E-mail Invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(5, 15)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha',message='Senhas devem ser iguais!')])
    botao_submit = SubmitField('Registrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já existente,Cadastre-se novamente ou faça Login para continuar')


class FormLogin(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(5, 15)])
    botao_submit = SubmitField('Login')
    lembrar_senha = BooleanField('Lembrar senha')


def validate_email(email):
    if current_user.email != email:
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já existente!!')


class FormEditPerfil(FlaskForm):
    nome_usuario = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='E-mail Invalido!')])
    foto_perfil = FileField('Mudar foto de perfil',validators=[FileAllowed(['jpg','png','jfif'],message='Formato não suportado. O arquivo precisa ser .jpg,  .png ou  .jfif')])
    foto_fundo = FileField('Mudar foto de fundo',validators=[FileAllowed(['jpg','png','jfif'],message='Formato não suportado. O arquivo precisa ser .jpg,  .png ou  .jfif')])
    botao_submit = SubmitField('Mudar Perfil')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já existente!!')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo ',validators=[DataRequired(),Length(2,100)])
    corpo = TextAreaField('Conteudo',validators=[DataRequired()])
    botao_submit = SubmitField('Enviar Post')


class FormComentar(FlaskForm):
    comentario = StringField('Titulo ',validators=[DataRequired(),Length(2,300)])
    botao_submit = SubmitField('Comentar')