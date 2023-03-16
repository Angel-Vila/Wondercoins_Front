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
