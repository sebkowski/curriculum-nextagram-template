from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
from peewee import IntegrityError
from flask_wtf.csrf import CSRFProtect
from models import *
from models.user import User
from flask_login import login_user, logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')



# GET /users/new
@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/delete',methods=['POST'])
@login_required
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))



# POST /sessions/
@sessions_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('user_email')
    password_to_check = request.form.get('user_password')

    user_info = User.get_or_none(User.email==email) 
    if not user_info: 
        flash('no user with this email')
        return redirect(url_for('sessions.new'))
    result = check_password_hash(user_info.password, password_to_check)
    

    if result:
        flash('logged in')
        session['user_id']=user_info.id
        # login_user(user_info)
        return redirect('/')
    else:
        flash('Wrong password')
        return redirect(url_for('sessions.new'))
