from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from models import *
from models.user import User
from models.post import Post
from models.donate import Donation
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_required, login_user
from instagram_web.util.helpers import *
from app import gateway

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

# displaying the donation page
@donations_blueprint.route("/new")
def new():
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', client_token=client_token)

# form submission
@donations_blueprint.route("/create", methods=["POST"])
def create():
    amount = request.form.get('amount')
    nonce = request.form.get('nonce')
    
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success:
        flash('payment made')
        d=Donation(user_id=current_user.id, amount=amount)
        d.save()
        return redirect('/')
    else:
        flash("Payment failed")
        return redirect('/')