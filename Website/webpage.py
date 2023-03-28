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
    num_monedas = peticiones.monedas_inicio()
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
    lista_tesoros = peticiones.tesoros()
    return flask.render_template("tesoro_lista.html", lista_tesoros=lista_tesoros)


@app.route("/tesoro/<int:id_tesoro>")
def tesoro(id_tesoro):
    datos_tesoro = peticiones.info_tesoro(id_tesoro)
    return flask.render_template("tesoro.html", datos=datos_tesoro)


@app.route("/hallazgo/<int:id_hallazgo>")
def hallazgo(id_hallazgo):
    datos_hallazgo = peticiones.info_hallazgo(id_hallazgo)
    return flask.render_template("hallazgo.html", datos=datos_hallazgo)


@app.route("/cecas")
def mapa_cecas():
    cecas = peticiones.cecas_mapa()
    return flask.render_template("mapa_cecas.html", cecas=cecas)


@app.route("/ceca/<int:id_ceca>")
def ceca(id_ceca):
    datos_ceca = peticiones.info_ceca(id_ceca)
    return flask.render_template("ceca.html", datos=datos_ceca)


@app.route("/buscador", methods=["POST", "GET"])
def buscador():
    busqueda = {}
    pagina = 0
    if flask.request.method == "POST":
        if "Buscar" in flask.request.form:
            busqueda["material"] = flask.request.form.get("material")
            try:
                busqueda["section_id"] = int(flask.request.form.get("m_id"))
            except ValueError:
                busqueda["section_id"] = 0
            flask.session["search"] = busqueda
        pagina = int(flask.request.form.get("pagina")) if flask.request.form.get("pagina") is not None else pagina
    materiales = peticiones.materiales()
    print(flask.session.get("search")) if "search" in flask.session.keys() else print("Vacio")
    if "search" not in flask.session.keys():
        monedas = peticiones.monedas_buscador_base(pagina)
        num_monedas = peticiones.num_monedas()
        num_paginas = num_monedas // 100 + 1 if num_monedas % 100 != 0 else num_monedas // 100
        print(num_monedas, num_paginas)
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
