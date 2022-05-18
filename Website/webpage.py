import flask
from flask_cors import CORS
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = flask.Flask(__name__)
CORS(app)
app.config['GOOGLEMAPS_KEY'] = open("GOOGLE_API.txt").read()
GoogleMaps(app)


@app.route("/")
def index():
    mapa = Map(
        identifier="mapa",
        lat=36.53813063050466,
        lng=-6.202028173211203,
        region="es"
    )
    return flask.render_template("index.html", mapa=mapa)


if __name__ == "__main__":
    app.run(debug=True)
