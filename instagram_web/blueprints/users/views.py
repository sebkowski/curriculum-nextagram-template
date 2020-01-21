from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
from peewee import IntegrityError
from flask_wtf.csrf import CSRFProtect
from models import *
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

# GET /users/new
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# POST /users/
@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    username = request.form.get('user_username')
    s = User(name=name, email=email, password=password, username=username)
    # try:
    if s.save():
        flash('user created')
        # return render_template('/home.html')
        return redirect(url_for('users.new'))
    else:
        for err in s.errors:
            flash(err)
        return redirect(url_for('users.new'))
    # except IntegrityError:
    #     flash('not sure what could be the error')
    #     return redirect(url_for('home'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
