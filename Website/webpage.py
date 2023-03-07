import random

import flask
from flask_cors import CORS
import peticiones

app = flask.Flask(__name__)
CORS(app)


@app.route("/")
def inicio():
    num_monedas = peticiones.num_monedas()
    info_moneda = {'image_obverse': None}
    while len(info_moneda) < 1 or info_moneda['image_obverse'] is None:
        id_moneda = random.randint(1, num_monedas)
        print(id_moneda)
        info_moneda = peticiones.info_moneda(id_moneda)
        print(info_moneda)
    url = f"https://monedaiberica.org/{info_moneda['image_obverse']}"
    return flask.render_template("inicio.html", moneda=info_moneda, imagen=url)


@app.route("/moneda/<int:idmoneda>")
def moneda(idmoneda):
    info_moneda = peticiones.info_moneda(idmoneda)
    if len(info_moneda) < 1:
        return flask.render_template("404.html")
    return flask.render_template("moneda.html", moneda=info_moneda)


@app.route("/buscador")
def buscador():
    materiales = peticiones.materiales()
    return flask.render_template("searchbar.html", mats=materiales)


@app.route("/graficos")
def graficos():
    return flask.render_template("graficos.html", imagen="./graficos/test.png")


if __name__ == "__main__":
    app.run(debug=True)
