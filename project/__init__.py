from .setup import app

from .src.api.user import user_api_bp as uapi

app.register_blueprint(uapi, url_prefix="/api/users")


@app.route('/')
def test():
    return '<h1>Hello!</h1>'

