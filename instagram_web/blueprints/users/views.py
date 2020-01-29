from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
from peewee import IntegrityError
from flask_wtf.csrf import CSRFProtect
from models import *
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_required, login_user
from instagram_web.util.helpers import *
# from config import S3_BUCKET

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
    profile_image = 'user.png'
    s = User(name=name, email=email, password=password, username=username, profile_image=profile_image)
    # try:
    if s.save():
        flash('user created')
        login_user(s)
        # return render_template('/home.html')
        return redirect(url_for('home'))
    else:
        for err in s.errors:
            flash(err)
        return redirect(url_for('users.new'))
    # except IntegrityError:
    #     flash('not sure what could be the error')
    #     return redirect(url_for('home'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template('users/show.html', user=user)
    else:
        flash('no such user')
        return redirect('/')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/edit', methods=['GET'])
def edit():

    return render_template('users/edit.html')



@users_blueprint.route('/edit', methods=['POST'])
def update():
    email = request.form.get('user_email')

    query = User.update(email=email).where(User.id==current_user.id)
    if query.execute():
        flash('email updated')
        return render_template('home.html')
    else:
        flash('not updated')
    return render_template('home.html')

@users_blueprint.route('/upload_profile_image', methods=['GET'])
def profile_image():
    if current_user.is_active == False:
        return redirect(url_for('home'))
    else:
        return render_template('users/test.html')


@users_blueprint.route('/upload_profile_image', methods=['POST'])
def update_profile_image():
	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file = request.files["user_file"]

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        s=User.update(profile_image=file.filename).where(User.id==current_user.id)
        if s.execute():
            flash('profile image updated')
            return render_template('home.html')
        else:
            flash('profile image not updated')
            return render_template('home.html')
    else:
        return redirect("/")







    
    # if query.execute():
    #     flash('profile image updated')
    # else:
    #     flash('not updated')
    # return render_template('home.html')
    

