from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from models.user import User
from models.donate import Donation
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.helpers.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(sessions_blueprint)
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(donations_blueprint, url_prefix="/donations")

oauth.init_app(app)

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@app.route("/")
def home():
    users = User.select()
    total = sum([donation.amount for donation in Donation.select()])
    return render_template('home.html', users=users, total_donation=total)

