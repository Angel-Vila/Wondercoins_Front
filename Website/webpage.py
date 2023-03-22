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
    info_moneda = random.choice(num_monedas)
    imagen = dedalo_link + info_moneda["image_obverse"]
    pie_imagen = info_moneda["type_full_value"].split("|")[-1].strip()
    id_moneda = info_moneda["section_id"]
    return flask.render_template("inicio.html", moneda=pie_imagen, imagen=imagen, id_moneda=id_moneda)


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
        if "Buscar" in flask.request.form:
            busqueda["material"] = flask.request.form.get("material")
            busqueda["section_id"] = flask.request.form.get("m_id")
            flask.session["search"] = busqueda
        pagina = int(flask.request.form.get("pagina")) if flask.request.form.get("pagina") is not None else pagina
    materiales = peticiones.materiales()
    print(flask.session.get("search")) if "search" in flask.session.keys() else "Vacio"
    if "search" not in flask.session.keys():
        monedas = peticiones.monedas_buscador_base(pagina)
    else:
        monedas = peticiones.monedas_buscador(peticiones.busqueda(flask.session.get("search")), pagina)
    num_monedas = peticiones.busqueda(flask.session.get("search"))
    num_paginas = len(num_monedas) // 100 + 1 if len(num_monedas) % 100 != 0 else len(num_monedas) // 100
    print(len(num_monedas), num_paginas)
    return flask.render_template("searchbar.html", mats=materiales, n_pages=num_paginas, page=pagina, monedas=monedas)


@app.route("/buscador/reiniciar", methods=["POST", "GET"])
def reiniciar_busqueda():
    flask.session.pop("search")
    return flask.redirect("/buscador")


@app.route("/graficos")
def graficos():
    grafico = generador_graficos.test()
    return flask.render_template("graficos.html", graphJSON=grafico)


@app.route("/graficos/callback", methods=["POST", "GET"])
def callback():
    return generador_graficos.test(flask.request.args.get("data"))


if __name__ == "__main__":
    app.run(debug=True)
