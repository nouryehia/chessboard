from .setup import app

from .src.api.user import user_api_bp as uapi

app.register_blueprint(uapi, url_prefix="/api/users")
