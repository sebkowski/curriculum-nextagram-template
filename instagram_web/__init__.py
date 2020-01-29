from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(sessions_blueprint)
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(posts_blueprint, url_prefix="/posts")


@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@app.route("/")
def home():
    return render_template('home.html')
