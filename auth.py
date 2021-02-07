import uuid
from flask import Flask, redirect, request, render_template
from urllib import parse

HOST = "localhost"
PORT = "8080"
REDIRECT_URI = f"http://{HOST}:{PORT}/token"

AUTH_ENDPOINT = "https://connect.deezer.com/oauth/auth.php"
CLIENT_ID = 461222

app = Flask(__name__)


def auth_uri(scope="manage_library", response_type="token", **kwargs):
    kwargs.update(
        {
            "client_id": CLIENT_ID,
            "scope": scope,
            "response_type": response_type,
            "redirect_uri": REDIRECT_URI,
        }
    )
    return f"{AUTH_ENDPOINT}?{parse.urlencode(kwargs)}"


@app.route("/", methods=["GET"])
def handle_root():
    return "This is a placeholder response"


@app.route("/deezer", methods=["GET"])
def auth_deezer():
    uri = auth_uri()
    return redirect(uri)


@app.route("/token", methods=["GET"])
def auth_sucess():
    if request.args.get("error_reason") == "user_denied":
        return "Error: user declined auth"

    return render_template("token.html")


@app.route("/submit", methods=["GET"])
def receive_token():
    global token
    token = request.args.get("access_token")
    return "Autentication complete"


if __name__ == "__main__":
    token = None
    app.config.update(DEBUG=True)
    app.run(host=HOST, port=PORT)
