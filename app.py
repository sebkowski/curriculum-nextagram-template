import os
import config
import braintree
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from models.user import User
from flask_login import LoginManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

login_manager = LoginManager()
login_manager.init_app(app)



csrf = CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

gateway = braintree.BraintreeGateway(braintree.Configuration(braintree.Environment.Sandbox,
merchant_id=os.getenv('MerchantID'),
public_key=os.getenv('publicKEY'),
private_key=os.getenv('PrivateKEY')
))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
