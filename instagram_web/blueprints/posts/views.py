from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
from peewee import IntegrityError
from flask_wtf.csrf import CSRFProtect
from models import *
from models.user import User
from models.post import Post
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_required, login_user
from instagram_web.util.helpers import *
# from config import S3_BUCKET

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates')

@posts_blueprint.route('/new')
def new():
   return render_template('posts/new.html')

@posts_blueprint.route('/', methods=['Post'])
def create():
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
        s = Post(image_path=file.filename, user_id=current_user.id)
        if s.save():
            flash('Posted!')
            return render_template('home.html')
        else:
            flash('Post failed')
            return render_template('home.html')
    else:
        return redirect("/")
   



# GET /users/new
