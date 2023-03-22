import requests
import json


def num_monedas():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=image_obverse%2C%20type_full_value"
                     "%2C%20section_id&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    filtered = list(filter(lambda x: x["image_obverse"] != "null" and x["type_full_value"] != "", result))
    return filtered


def info_moneda(id_moneda):
    dedalo_link = "https://wondercoins.uca.es"
    r = requests.get(f"http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     f"code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20catalogue_type_mint"
                     f"%2C%20mint%2C%20type%2C%20type_full_value%2C%20mint_name%2C%20weight%2C%20diameter%2C%20dies%"
                     f"2C%20image_obverse%2C%20image_reverse%2C%20number%2C%20uri%2C%20find_type%2C%20findspot&"
                     f"section_id={id_moneda}&lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    try:
        result = r.json()["result"][0]
        result["image_obverse"] = dedalo_link + result["image_obverse"]
        result["image_reverse"] = dedalo_link + result["image_reverse"]
    except IndexError:
        result = []
    return result


def materiales():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=material&sql_fullselect="
                     "SELECT%20DISTINCT(term)%20FROM%20material&lang=lg-spa&"
                     "limit=0&resolve_portal=false&resolve_dd_relations=false")
    lista = r.json()["result"]
    result = set()
    for i in lista:
        result.add(i["term"])
    return result


def info_tipo(id_tipo):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=mint%2C%20material%2C%20"
                     "denomination%2C%20date_in%2C%20date_out%2C%20creators_roles%2C%20creators_names%2C%20"
                     "design_obverse%2C%20design_reverse%2C%20legend_obverse%2C%20legend_reverse%2C%20uri%2C%20"
                     "coin_references&"
                     f"section_id={id_tipo}&lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    try:
        result = r.json()["result"][0]
        try:
            result["monedas"] = coins_tipo(json.loads(result.get("coin_references")))
        except TypeError:
            result["monedas"] = []
    except IndexError:
        result = []
    return result


def coins_tipo(vec_monedas):
    datos = []
    dedalo_link = "https://wondercoins.uca.es"
    for i in vec_monedas:
        r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                         "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20"
                         f"mint%2C%20catalogue_type_mint%2C%20image_obverse%2C%20image_reverse&section_id={i}&"
                         "lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
        result = r.json()["result"][0]
        result["image_obverse"] = dedalo_link + result["image_obverse"]
        result["image_reverse"] = dedalo_link + result["image_reverse"]
        result["mint"] = json.loads(result["mint"].split("|")[0])
        result["catalogue_type_mint"] = json.loads(result["catalogue_type_mint"])
        datos.append(result)
    return datos


def busqueda(buscador):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20material&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in buscador.keys():
        busca = list(filter(lambda x: x[i] == buscador[i], busca)) if buscador[i] != "" and buscador[i] is not None \
            else busca
    return list(map(lambda x: str(x["section_id"]), busca))


def monedas_buscador_base(offset):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=number%2C%20image_obverse%2C%20"
                     "image_reverse%2C%20section_id%2C%20findspot%2C%20material%2C%20type_data&lang=lg-spa&"
                     "order=section_id%20ASC&limit=100"
                     f"&offset={offset * 100}&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    dedalo_link = "https://wondercoins.uca.es"
    for i in result:
        try:
            i["image_obverse"] = dedalo_link + i["image_obverse"]
        except TypeError:
            i["image_obverse"] = "../static/logo-sinletras-sinfondo.jpg"
        try:
            i["image_reverse"] = dedalo_link + i["image_reverse"]
        except TypeError:
            i["image_reverse"] = "../static/logo-sinletras-sinfondo.jpg"
    return result


def monedas_buscador(id_monedas, offset):
    lista_monedas = id_monedas[offset * 100:offset * 100 + 100] if len(id_monedas) > offset * 100 + 100 \
        else id_monedas[offset * 100:]
    print(lista_monedas)
    lista_ids = ",".join(lista_monedas)
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=number%2C%20image_obverse%2C%20"
                     "image_reverse%2C%20section_id%2C%20findspot%2C%20material%2C%20type_data&lang=lg-spa&"
                     f"order=section_id%20ASC&limit=100&section_id={lista_ids}"
                     f"&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    dedalo_link = "https://wondercoins.uca.es"
    for i in result:
        try:
            i["image_obverse"] = dedalo_link + i["image_obverse"]
        except TypeError:
            i["image_obverse"] = "../static/logo-sinletras-sinfondo.jpg"
        try:
            i["image_reverse"] = dedalo_link + i["image_reverse"]
        except TypeError:
            i["image_reverse"] = "../static/logo-sinletras-sinfondo.jpg"
    return result


if __name__ == "__main__":
    print(monedas_buscador(busqueda({"material": "Bronce emplomado"}), 0))
