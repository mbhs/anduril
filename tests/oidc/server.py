from flask import Flask, render_template, redirect
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.secret_key = "secret"
app.config.update(OIDC_CLIENT_SECRETS="./secrets.json",
                  OIDC_SCOPES=["openid", "profile", "email"],
                  OIDC_ID_TOKEN_COOKIE_SECURE=False)

oidc = OpenIDConnect(app)


@app.route("/")
def index():
    if not oidc.user_loggedin:
        return """<a href="/login">Log in</a>"""
    else:
        first_name = oidc.user_getfield('first_name')
        last_name = oidc.user_getfield('last_name')
        username = oidc.user_getfield('username')
        return f"""Hello, {first_name} {last_name}, {username}<br><a href="/logout">Log out</a>"""


@app.route('/login')
@oidc.require_login
def login():
    return redirect("/")


@app.route('/logout')
def logout():
    oidc.logout()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
