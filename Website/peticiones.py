import requests
import json


def num_monedas():
    r = requests.get("https://monedaiberica.org/dedalo/lib/dedalo/publication/server_api/v1/json/records?code"
                     "=654asdiKrhdTetQksluoQaW2&db_name=web_numisdata_mib&table=coins&sql_fullselect=SELECT%20MAX("
                     "section_id)%20FROM%20coins&lang=lg-eng&limit=10")
    result = r.json()["result"][0]["MAX(section_id)"]
    return result


def info_moneda(id_moneda):
    r = requests.get(f"https://monedaiberica.org/dedalo/lib/dedalo/publication/server_api/v1/json/records?code"
                     f"=654asdiKrhdTetQksluoQaW2&db_name=web_numisdata_mib&table=coins&section_id={id_moneda}"
                     f"&lang=lg-eng&limit=10")
    try:
        result = r.json()["result"][0]
    except IndexError:
        result = []
    return result


def materiales():
    r = requests.get("https://monedaiberica.org/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     "records?code=654asdiKrhdTetQksluoQaW2&table=coins&sql_fullselect="
                     "SELECT%20DISTINCT(material)%20FROM%20coins&lang=lg-spa&limit=0")
    lista = r.json()["result"]
    result = set()
    for i in lista:
        if i["material"] is not None:
            part = [j.strip() for j in i["material"].split("|")]
            for j in part:
                result.add(j)
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
        result["mint"] = json.loads(result["mint"])
        result["catalogue_type_mint"] = json.loads(result["catalogue_type_mint"])
        datos.append(result)
    return datos


if __name__ == "__main__":
    print(info_moneda(967))
