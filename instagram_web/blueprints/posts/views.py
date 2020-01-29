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

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates')

@posts_blueprint.route('/new')
def new():
   return render_template('posts/new.html')


# GET /users/new
