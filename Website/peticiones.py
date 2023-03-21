import requests
import json


def num_monedas():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=image_obverse&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    filtered = list(filter(lambda x: x["image_obverse"] != "null", result))
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
    print(lista)
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
        result["monedas"] = coins_tipo(json.loads(result.get("coin_references")))
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
        busca = list(filter(lambda x: x[i] == buscador[i], busca))
    return busca


if __name__ == "__main__":
    print(busqueda({"material": "Orichalcum"}))
