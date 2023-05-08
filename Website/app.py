import random
import datetime
import flask
from flask_cors import CORS
import peticiones
import generador_graficos
import generador_informes

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
    if not datos_tesoro:
        return flask.render_template("404.html")
    return flask.render_template("tesoro.html", datos=datos_tesoro)


@app.route("/hallazgos")
def hallazgos():
    lista_hallazgos = peticiones.hallazgos()
    return flask.render_template("hallazgos_lista.html", hallazgos=lista_hallazgos)


@app.route("/hallazgo/<int:id_hallazgo>")
def hallazgo(id_hallazgo):
    datos_hallazgo = peticiones.info_hallazgo(id_hallazgo)
    if not datos_hallazgo:
        return flask.render_template("404.html")
    return flask.render_template("hallazgo.html", datos=datos_hallazgo)


@app.route("/cecas")
def mapa_cecas():
    cecas = peticiones.cecas_mapa()
    return flask.render_template("mapa_cecas.html", cecas=cecas)


@app.route("/ceca/<int:id_ceca>")
def ceca(id_ceca):
    datos_ceca = peticiones.info_ceca(id_ceca)
    if not datos_ceca:
        return flask.render_template("404.html")
    return flask.render_template("ceca.html", datos=datos_ceca)


@app.route("/buscador", methods=["POST", "GET"])
def buscador():
    busqueda = {}
    pagina = 0
    if flask.request.method == "POST":
        if "Buscar" in flask.request.form:
            busqueda["material"] = flask.request.form.get("material")
            busqueda["type_full_value"] = flask.request.form.get("tipos")
            busqueda["mint"] = flask.request.form.get("ceca")
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
    else:
        monedas = peticiones.monedas_buscador(peticiones.busqueda(flask.session.get("search")), pagina)
        num_monedas = peticiones.busqueda(flask.session.get("search"))
        num_paginas = len(num_monedas) // 100 + 1 if len(num_monedas) % 100 != 0 else len(num_monedas) // 100
        num_monedas = len(num_monedas)
    print(len(monedas))
    return flask.render_template("searchbar.html", mats=materiales, n_pages=num_paginas, page=pagina, monedas=monedas,
                                 n_monedas=num_monedas)


@app.route("/buscador/reiniciar", methods=["POST", "GET"])
def reiniciar_busqueda():
    flask.session.pop("search") if "search" in flask.session.keys() else None
    return flask.redirect("/buscador")


@app.route("/buscador_tipos", methods=["POST", "GET"])
def buscador_tipos():
    busqueda = {}
    pagina = 0
    if flask.request.method == "POST":
        if "Buscar" in flask.request.form:
            busqueda["material"] = flask.request.form.get("material")
            busqueda["catalogue"] = flask.request.form.get("catalogo")
            busqueda["mint"] = flask.request.form.get("ceca")
            busqueda["denomination"] = flask.request.form.get("denominacion")
            busqueda["date_in"] = flask.request.form.get("date_in")
            busqueda["date_out"] = flask.request.form.get("date_out")
            flask.session["busqueda_tipos"] = busqueda
    pagina = int(flask.request.form.get("pagina")) if flask.request.form.get("pagina") is not None else pagina
    materiales = peticiones.materiales()
    denominaciones = peticiones.denominaciones()
    catalogos = peticiones.catalogos()
    if "busqueda_tipos" not in flask.session.keys():
        tipos = peticiones.buscador_tipos_base(pagina)
        num_tipos = peticiones.num_tipos()
        num_paginas = num_tipos // 100 + 1 if num_tipos % 100 != 0 else num_tipos // 100
    else:
        tipos = peticiones.tipos_buscador(peticiones.busqueda_tipos(flask.session.get("busqueda_tipos")), pagina)
        vec_tipos = peticiones.busqueda_tipos(flask.session.get("busqueda_tipos"))
        num_paginas = len(vec_tipos) // 100 + 1 if len(vec_tipos) % 100 != 0 else len(vec_tipos) // 100
        num_tipos = len(vec_tipos)
    return flask.render_template("search_tipos.html", mats=materiales, dems=denominaciones, cats=catalogos,
                                 n_pages=num_paginas, page=pagina, tipos=tipos, n_tipos=num_tipos)


@app.route("/buscador_tipos/reiniciar", methods=["POST", "GET"])
def reiniciar_busqueda_tipos():
    flask.session.pop("busqueda_tipos") if "busqueda_tipos" in flask.session.keys() else None
    return flask.redirect("/buscador_tipos")


@app.route("/graficos", methods=["POST", "GET"])
def graficos():
    busqueda = {}
    dato = "mint"
    if flask.request.method == "POST":
        if "Buscar" in flask.request.form:
            busqueda["material"] = flask.request.form.get("material")
            busqueda["type_full_value"] = flask.request.form.get("tipos")
            busqueda["mint"] = flask.request.form.get("ceca")
            dato = flask.request.form.get("valor")
            flask.session["search_graficos"] = busqueda
    materiales = peticiones.materiales()
    print(flask.session.get("search_graficos")) if "search_graficos" in flask.session.keys() else print("Vacio")
    if "search_graficos" not in flask.session.keys():
        datos = peticiones.monedas_graficos_base(dato)
    elif len(list(filter(lambda x: flask.session.get("search_graficos")[x] not in ["", 0],
                         flask.session.get("search_graficos").keys()))) == 0:
        datos = peticiones.monedas_graficos_base(dato)
    else:
        monedas = peticiones.busqueda(flask.session.get("search_graficos"))
        datos = peticiones.datos_grafico(monedas, dato)
    print(datos)
    flask.session["datos_grafico"] = datos
    grafico = generador_graficos.test(datos)
    return flask.render_template("graficos.html", graphJSON=grafico, mats=materiales)


@app.route("/graficos/reiniciar")
def reiniciar_graficos():
    flask.session.pop("search_graficos") if "search_graficos" in flask.session.keys() else None
    flask.session.pop("datos_grafico") if "datos_grafico" in flask.session.keys() else None
    return flask.redirect("/graficos")


@app.route("/graficos/callback", methods=["POST", "GET"])
def callback():
    print(flask.session.get("datos_grafico"))
    return generador_graficos.test(flask.session.get("datos_grafico"), flask.request.args.get("data"))


@app.route("/mapa")
def mapa():
    cecas = peticiones.cecas_mapa()
    hallazgos = peticiones.hallazgos_mapa()
    tesoros = peticiones.tesoros_mapa()
    return flask.render_template("mapa.html", cecas=cecas, hallazgos=hallazgos, tesoros=tesoros)


@app.route("/informes", methods=["POST", "GET"])
def informes():
    materiales = peticiones.materiales()
    if flask.request.method == "POST":
        busqueda = {"material": flask.request.form.get("material"), "type_full_value": flask.request.form.get("tipos"),
                    "mint": flask.request.form.get("ceca")}
        monedas = peticiones.busqueda(busqueda)
        generador_informes.generar_informe(peticiones.datos_informe(monedas))
        return flask.send_file("informes/prueba.pdf", download_name=f'informe_{datetime.datetime.now()}.pdf',
                               as_attachment=True)
    return flask.render_template("informes.html", mats=materiales)


if __name__ == "__main__":
    app.run(debug=True)
