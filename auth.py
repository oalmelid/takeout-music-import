import uuid
from flask import Flask, redirect, request
from urllib import parse

HOST = "localhost"
PORT = "8080"
REDIRECT_URI = f"http://{HOST}:{PORT}/token"

AUTH_ENDPOINT = "https://connect.deezer.com/oauth/auth.php"
CLIENT_ID = 461222

app = Flask(__name__)


def auth_uri(state, scope="manage_library", response_type="token", **kwargs):
    kwargs.update(
        {
            "state": state,
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
    # this is assumed to be single-client, single-flow, no interruptions.
    state = uuid.uuid4().hex
    uri = auth_uri(state)
    return redirect(uri)


@app.route("/token", methods=["GET"])
def receive_token():
    if request.args.get("error_reason") == "user_denied":
        return "Error: user declined auth"

    token = request.args.get("access_token")
    print(f"Got token: {token}")
    print(request.url)
    print(request.args)

    # Now to write some javascript to handle the token.
    return "OK"


if __name__ == "__main__":
    app.config.update(DEBUG=True)
    app.run(host=HOST, port=PORT)