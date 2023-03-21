import random

import flask
from flask_cors import CORS
import peticiones
import generador_graficos

app = flask.Flask(__name__)
app.secret_key = "WwwWonderCoins"
CORS(app)


@app.route("/inicio")
@app.route("/")
def inicio():
    dedalo_link = "https://wondercoins.uca.es"
    num_monedas = peticiones.num_monedas()
    imagen = dedalo_link + random.choice(num_monedas)["image_obverse"]
    info_moneda = "Prueba"
    return flask.render_template("inicio.html", moneda=info_moneda, imagen=imagen)


@app.route("/moneda/<int:idmoneda>")
def moneda(idmoneda):
    info_moneda = peticiones.info_moneda(idmoneda)
    if len(info_moneda) < 1:
        return flask.render_template("404.html")
    return flask.render_template("moneda.html", moneda=info_moneda)


@app.route("/tipo/<int:idtipo>")
def tipo(idtipo):
    info_tipo = peticiones.info_tipo(idtipo)
    if not info_tipo:
        return flask.render_template("404.html")
    return flask.render_template("tipo.html", tipo=info_tipo)


@app.route("/tesoros")
def tesoros():
    return flask.render_template("tesoro.html")


@app.route("/buscador", methods=["POST", "GET"])
def buscador():
    busqueda = {}
    pagina = 0
    if flask.request.method == "POST":
        busqueda["material"] = flask.request.form.get("material")
        busqueda["m_id"] = flask.request.form.get("m_id")
        flask.session["search"] = busqueda
        print(flask.session["search"])
        pagina = int(flask.request.form.get("pagina"))
    materiales = peticiones.materiales()
    return flask.render_template("searchbar.html", mats=materiales, n_pages=10, page=pagina)


@app.route("/graficos")
def graficos():
    grafico = generador_graficos.test()
    return flask.render_template("graficos.html", graphJSON=grafico)


@app.route("/graficos/callback", methods=["POST", "GET"])
def callback():
    return generador_graficos.test(flask.request.args.get("data"))


if __name__ == "__main__":
    app.run(debug=True)
