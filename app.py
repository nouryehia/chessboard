from init import app

from src.api.user import user_api_bp as uapi

app.register_blueprint(uapi, url_prefix="/api/users")


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
