from flask import render_template, url_for, flash, redirect, request, abort
from PrimeiroSite.forms import FormLogin, FormRegistro, FormEditPerfil, FormCriarPost,FormComentar
from PrimeiroSite import app, banco_de_dados, cript, login_manager
from PrimeiroSite.models import Usuario, Post,Comentario
from sqlalchemy.orm import Session
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    form = FormComentar()
    posts = Post.query.order_by(Post.id.desc())
    comentarios = {post.id: sorted(post.comentarios, key=lambda c: c.data, reverse=True) for post in posts}
    return render_template('homepage.html', posts=posts,comentarios=comentarios,form=form)


@app.route('/usuários')
def usuarios():
    with app.app_context():
        lista_usuarios = {usuario.nome: usuario.email for usuario in Usuario.query.all()}
        print(lista_usuarios)
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario is not None and cript.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_senha.data)
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            p_next = request.args.get('next')
            if p_next:
                return redirect(p_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login! E-mail ou senha incorreto {form_login.email.data}', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/registro', methods=["GET", "POST"])
def register():
    form_registro = FormRegistro()
    if form_registro.validate_on_submit():
        senha_cript = cript.generate_password_hash(form_registro.senha.data)
        usuario = Usuario(nome=form_registro.nome_usuario.data, email=form_registro.email.data,
                          senha=senha_cript)
        with app.app_context():
            banco_de_dados.session.add(usuario)
            banco_de_dados.session.commit()
        flash(f'Conta criada com sucesso no e-mail {form_registro.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('register.html', form_registro=form_registro)


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for(f'static', filename=f'imgs_perfil/{current_user.foto_perfil}')
    foto_fundo = url_for(f'static', filename=f'imgs_fundo/{current_user.foto_fundo}')
    return render_template('perfil.html', foto_perfil=foto_perfil, foto_fundo=foto_fundo)


def salvarimagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_imagem = nome + codigo + extensao
    caminho = os.path.join(app.root_path, 'static/imgs_perfil', nome_imagem)
    qualidade = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(qualidade)
    imagem_reduzida = imagem_reduzida.resize((120, 120))
    imagem_reduzida.save(caminho)
    return nome_imagem


def salvarimagem_fundo(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_imagem = nome + codigo + extensao
    caminho = os.path.join(app.root_path, 'static/imgs_fundo', nome_imagem)

    imagem_resized = Image.open(imagem)
    imagem_resized = imagem_resized.resize((1200, 170))
    imagem_resized.save(caminho)
    return nome_imagem


@app.route('/perfil/editar', methods=["GET", "POST"])
@login_required
def editar_perfil():
    form_edit = FormEditPerfil()
    foto_perfil = url_for(f'static', filename=f'imgs_perfil/{current_user.foto_perfil}')
    foto_fundo = url_for(f'static', filename=f'imgs_fundo/{current_user.foto_fundo}')
    if form_edit.validate_on_submit():
        current_user.nome = form_edit.nome_usuario.data
        current_user.email = form_edit.email.data
        if form_edit.foto_perfil.data:
            imagem = salvarimagem(form_edit.foto_perfil.data)
            current_user.foto_perfil = imagem
        if form_edit.foto_fundo.data:
            imagem_fundo = salvarimagem_fundo(form_edit.foto_fundo.data)
            current_user.foto_fundo = imagem_fundo
        banco_de_dados.session.commit()
        flash('Mudanças feitas com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_edit.nome_usuario.data = current_user.nome
        form_edit.email.data = current_user.email
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form_edit=form_edit, foto_fundo=foto_fundo)


@app.route('/sair')
@login_required
def logout():
    logout_user()
    flash(f'Log-out feito com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/criar_post', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, autor=current_user)
        with app.app_context():
            banco_de_dados.session.add(post)
            banco_de_dados.session.commit()
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    return render_template('criar_post.html', form_criar_post=form_criar_post)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            banco_de_dados.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('exibir_post', post_id=post_id))
    else:
        form = None
    return render_template('post.html', form=form, post=post)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        with app.app_context():
            Session.object_session(post).expunge(post)
            banco_de_dados.session.delete(post)
            banco_de_dados.session.commit()
        flash('Post excluido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

def update(obj, session):
    session.add(obj)
    session.commit()
    return obj
@app.route('/comentar/<post_id>',methods=['GET','POST'])
@login_required
def comentar(post_id):
    form_comentar = FormComentar()
    post = Post.query.get_or_404(post_id)
    if form_comentar.validate_on_submit():
        comentario = Comentario(texto=form_comentar.comentario.data,autor_post=current_user,post=post)
        banco_de_dados.session.add(comentario)
        banco_de_dados.session.commit()
        return redirect(url_for('comentar', post_id=post_id))
    post = update(post, banco_de_dados.session)  # <- adicionado aqu
    return render_template('comentarios.html', post=post, form=form_comentar)