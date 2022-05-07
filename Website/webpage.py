import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    app.run()
