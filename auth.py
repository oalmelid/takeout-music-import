import time
import uuid
import webbrowser
from threading import Thread

from flask import Flask, redirect, request, render_template
from urllib import parse

HOST = "localhost"
PORT = "8080"
HOME_URI = f"http://{HOST}:{PORT}/"
REDIRECT_URI = f"{HOME_URI}token"

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
def forward_to_deezer():
    uri = auth_uri()
    return redirect(uri)


@app.route("/token", methods=["GET"])
def auth_sucess():
    if request.args.get("error_reason") == "user_denied":
        return "Error: user declined auth"

    return render_template("token.html")


@app.route("/submit", methods=["GET"])
def receive_token():
    global TOKEN
    TOKEN = request.args.get("access_token")

    shutdown_func = request.environ.get("werkzeug.server.shutdown")

    if shutdown_func is None:
        raise RuntimeError("Not running with the Werkzeug Server")

    # Surprisingly this works, I guess werkzeug attempts a graceful shutdown.
    shutdown_func()
    return "Autentication complete, you may now close this tab."


def get_token():
    # Authentication token. The flask server is only spun up transiently to
    # obtain a token.
    TOKEN = None
    server_process = Thread(target=app.run, kwargs={"host": HOST, "port": PORT})
    server_process.start()
    webbrowser.open_new_tab(HOME_URI)

    while TOKEN is None:
        time.sleep(0.1)

    return TOKEN
