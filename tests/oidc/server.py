from flask import Flask, render_template
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.secret_key = "secret"
app.config.update(OIDC_CLIENT_SECRETS="./secrets.json",
                  OIDC_SCOPES=["openid", "profile", "email"],
                  OIDC_COOKIE_SECURE=False)

oidc = OpenIDConnect(app)


@app.route("/")
def index():
    if not oidc.user_loggedin:
        return """<a href="/login">Log in</a>"""
    else:
        return f"""Hello, {oidc.user_getfield('username')}"""


@app.route('/login')
@oidc.require_login
def login():
    return "Login"


if __name__ == "__main__":
    app.run(debug=True)
