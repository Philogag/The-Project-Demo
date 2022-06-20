from flask_login import LoginManager

from backend.service.master_user_service import get_session_user

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return get_session_user(user_id)


def init_login_manager(app):
    login_manager.init_app(app)
