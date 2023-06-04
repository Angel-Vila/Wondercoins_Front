import requests
import json
import re
from unidecode import unidecode

enlace_wondercoins = "https://wondercoins.uca.es"
foto_default = "../static/logo-sinletras-sinfondo.jpg"


def monedas_inicio():
    """Lista de monedas que se pueden utilizar para la página principal (con imagen de anverso y tipo"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=image_obverse%2C%20type_full_value"
                     "%2C%20section_id&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    filtered = list(filter(lambda x: x["image_obverse"] != "null" and x["type_full_value"] != "", result))
    return filtered


def num_monedas():
    """Cantidad de monedas en la base de datos"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coin&sql_fullselect=SELECT%20COUNT(*)"
                     "%20AS%20cuenta%20FROM%20coins&lang=lg-spa&limit=10&"
                     "resolve_portal=false&resolve_dd_relations=false")
    return int(r.json()["result"][0]["cuenta"])


def info_moneda(id_moneda):
    """Toda la información de una moneda dado su código de identificación"""
    r = requests.get(f"http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     f"code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20catalogue_type_mint"
                     f"%2C%20mint%2C%20type%2C%20type_full_value%2C%20mint_name%2C%20weight%2C%20diameter%2C%20dies%"
                     f"2C%20image_obverse%2C%20image_reverse%2C%20number%2C%20uri%2C%20find_type%2C%20findspot"
                     f"%2C%20type_data%2C%20peculiarity_production%2C%20collection%2C%20bibliography_title"
                     f"%2C%20public_info%2C%20findspot_data"
                     f"&section_id={id_moneda}&lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    try:
        result = r.json()["result"][0]
        try:
            result["image_obverse"] = enlace_wondercoins + result["image_obverse"]
            result["image_reverse"] = enlace_wondercoins + result["image_reverse"]
        except (TypeError, AttributeError):
            result["image_obverse"] = foto_default
            result["image_reverse"] = foto_default
        try:
            result["mint"] = json.loads(result.get("mint").split(" | ")[0])
        except (TypeError, AttributeError):
            result["mint"] = ""
        try:
            result["catalogue_type_mint"] = json.loads(result["catalogue_type_mint"])
        except (TypeError, AttributeError):
            result["catalogue_type_mint"] = ""
        try:
            tipo = json.loads(result.get("type_data"))
            datos_tipo = tipo_moneda(tipo[0])
            result["l_anverso"] = datos_tipo["legend_obverse"]
            result["l_reverso"] = datos_tipo["legend_reverse"]
            result["d_anverso"] = datos_tipo["design_obverse"]
            result["d_reverso"] = datos_tipo["design_reverse"]
        except (TypeError, AttributeError):
            result["d_anverso"] = ""
            result["d_reverso"] = ""
            result["l_anverso"] = ""
            result["l_reverso"] = ""
        try:
            datos_hallazgo = info_hallazgo(json.loads(result["findspot_data"])[0])
            print(datos_hallazgo)
            result["map"] = datos_hallazgo["map"]
            result["popup"] = datos_hallazgo["popup"]
        except (TypeError, AttributeError):
            result["map"] = ""
            result["popup"] = ""
    except IndexError:
        result = []
    return result


def materiales():
    """Todos los materiales con monedas asociadas en la base de datos"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&sql_fullselect="
                     "SELECT%20DISTINCT(material)%20AS%20materiales%20FROM%20coins&lang=lg-spa&limit=0"
                     "&resolve_portal=false&resolve_dd_relations=false")
    lista = r.json()["result"]
    result = set()
    for i in lista:
        try:
            for j in i["materiales"].split("|"):
                result.add(j.strip())
        except AttributeError:
            continue
    return sorted(result)


def denominaciones():
    """Todas las denominaciones con monedas asociadas en la base de datos"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&sql_fullselect=SELECT%20DISTINCT(denomination)"
                     "%20FROM%20types&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    lista = r.json()["result"]
    result = set()
    for i in lista:
        try:
            for j in i["denomination"].split("|"):
                result.add(j.strip())
        except AttributeError:
            continue
    result.remove("")
    return sorted(result)


def catalogos():
    """Todos los catalogos con monedas en la base de datos"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&sql_fullselect=SELECT%20DISTINCT(catalogue)"
                     "%20FROM%20types&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    lista = r.json()["result"]
    result = set()
    for i in lista:
        try:
            result.add(i["catalogue"])
        except AttributeError:
            continue
    return sorted(result)


def info_tipo(id_tipo):
    """Toda la informacion necesaria de un tipo dado su id"""
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
        result["uri"] = result["uri"].split(",")
        autores = result["creators_names"].split("|") if result["creators_names"] is not None else []
        try:
            result["emisor"] = autores[0]
        except IndexError:
            result["emisor"] = ""
        try:
            result["autoridad"] = "|".join(autores[1:-1])
        except IndexError:
            result["autoridad"] = ""
        try:
            result["retrato"] = autores[-1] if len(autores) > 1 else ""
        except IndexError:
            result["retrato"] = ""
    except IndexError:
        result = []
    return result


def coins_tipo(vec_monedas):
    """La informacion de todas las monedas vinculadas a un tipo"""
    datos = []
    for i in vec_monedas:
        try:
            r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                             "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20"
                             f"mint%2C%20catalogue_type_mint%2C%20image_obverse%2C%20image_reverse&section_id={i}&"
                             "lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
            result = r.json()["result"][0]
            result["image_obverse"] = enlace_wondercoins + result["image_obverse"]
            result["image_reverse"] = enlace_wondercoins + result["image_reverse"]
            try:
                result["mint"] = json.loads(result["mint"].split("|")[0])
            except AttributeError:
                result["mint"] = ""
            try:
                result["catalogue_type_mint"] = json.loads(result["catalogue_type_mint"])
            except TypeError:
                result["catalogue_type_mint"] = ""
            datos.append(result)
        except IndexError:
            continue
    return datos


def tipo_moneda(t_moneda):
    """El tipo de una moneda dado su codigo"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=design_obverse%2C%20design_reverse%"
                     f"2C%20legend_obverse%2C%20legend_reverse&section_id={t_moneda}&lang=lg-spa&limit=10&"
                     f"resolve_portal=false"
                     "&resolve_dd_relations=false")
    result = r.json()["result"][0]
    return result


def busqueda(buscador):
    """Todas las monedas que cumplen los parametros del buscador"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20material"
                     "%2C%20mint%2C%20type_full_value&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in buscador.keys():
        if buscador[i] is not None and buscador[i] not in [0, ""]:
            print(buscador[i])
            busca = list(filter(lambda x, val=i: filtro(x[val], buscador[val]), busca))
    return list(map(lambda x: str(x["section_id"]), busca))


def filtro(x, parametro):
    """Funcion simple para comparar parametros"""
    if type(parametro) == int:
        return x == parametro
    else:
        return x is not None and unidecode(parametro.lower()) in unidecode(x.lower())


def busqueda_tipo(buscador):
    """Todos los tipos que cumplen los parametros del buscador"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=material%2C%20catalogue%2C%"
                     "20denomination%2C%20mint%2C%20date_in%2C%20date_out%2C%20section_id&lang=lg-spa&order="
                     "section_id%20ASC&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in buscador.keys():
        if buscador[i] is not None and buscador[i] not in [0, ""]:
            print(buscador[i])
            busca = list(filter(lambda x, val=i: filtro(x[val], buscador[val]), busca))
    return list(map(lambda x: str(x["section_id"]), busca))


def monedas_buscador_base(offset):
    """Las monedas que aparecen en el buscador sin busqueda realizada"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=number%2C%20image_obverse%2C%20"
                     "image_reverse%2C%20section_id%2C%20mint%2C%20catalogue_type_mint%2C%20type_data&lang=lg-spa&"
                     "order=section_id%20ASC&limit=100"
                     f"&offset={offset * 100}&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    for i in result:
        try:
            i["mint"] = json.loads(i["mint"].split("|")[0].strip())
            i["catalogue_type_mint"] = json.loads(i["catalogue_type_mint"])
        except AttributeError:
            i["mint"] = ""
            i["catalogue_type_mint"] = ""
        try:
            i["image_obverse"] = enlace_wondercoins + i["image_obverse"]
        except TypeError:
            i["image_obverse"] = foto_default
        try:
            i["image_reverse"] = enlace_wondercoins + i["image_reverse"]
        except TypeError:
            i["image_reverse"] = foto_default
    return result


def monedas_graficos_base(campo):
    """Las monedas que se usan en el grafico sin busqueda realizada"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     f"code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields={campo}&lang=lg-spa&"
                     "&limit=0&resolve_portal=false&resolve_dd_relations=false")
    return request_grafico(campo, r)


def request_grafico(campo, r):
    """Búsqueda de los campos necesarios para el grafico"""
    result = r.json()["result"]
    for i in result:
        i[campo] = i[campo].split("|")[0].strip() if i[campo] is not None else None
    datos = {i[campo]: result.count(i) for i in result}
    datos.pop(None) if None in datos else None
    datos.pop("") if "" in datos else None
    data = {"keys": list(datos.keys()), "data": list(datos.values())}
    data["keys"].append("Otros")
    data["data"].append(0)
    i = 0
    while i < len(data["keys"]) - 1:
        if int(data["data"][i]) < sum(int(x) for x in data["data"]) / 50:
            data["data"][-1] += int(data["data"][i])
            data["data"].pop(i)
            data["keys"].pop(i)
        else:
            i += 1
    return data


def monedas_buscador(id_monedas, offset):
    """Monedas que se muestran tras una busqueda"""
    if len(id_monedas) == 0:
        return []
    lista_monedas = id_monedas[offset * 100:offset * 100 + 100] if len(id_monedas) > offset * 100 + 100 \
        else id_monedas[offset * 100:]
    print(lista_monedas)
    lista_ids = ",".join(lista_monedas)
    print(lista_ids)
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=number%2C%20image_obverse%2C%20"
                     "image_reverse%2C%20section_id%2C%20mint%2C%20catalogue_type_mint%2C%20type_data&lang=lg-spa&"
                     f"order=section_id%20ASC&limit=100&section_id={lista_ids}"
                     f"&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    for i in result:
        try:
            i["mint"] = json.loads(i["mint"].split("|")[0].strip())
            i["catalogue_type_mint"] = json.loads(i["catalogue_type_mint"])
        except AttributeError:
            continue
        i["number"] = "SIN NUMERO" if i["number"] is None else i["number"]
        try:
            i["image_obverse"] = enlace_wondercoins + i["image_obverse"]
        except TypeError:
            i["image_obverse"] = foto_default
        try:
            i["image_reverse"] = enlace_wondercoins + i["image_reverse"]
        except TypeError:
            i["image_reverse"] = foto_default
    return result


def tesoros():
    """Lista de tesoros"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=hoards&ar_fields="
                     "section_id%2C%20name&lang=lg-spa&order=section_id%20ASC&limit=0"
                     "&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    return result


def info_tesoro(id_tesoro):
    """Informacion de un tesoro dado su id"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=hoards&ar_fields="
                     "section_id%2C%20name%2C%20indexation%2C%20coins%2C%20date_in%2C%20date_out%2C%20public_info%"
                     f"2C%20place%2C%20map%2C%20bibliography_data%2C%20georef&section_id={id_tesoro}&lang="
                     f"lg-spa&limit=0"
                     "&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    return filtro_monedas(result)


def datos_grafico(vec_monedas, campo):
    """Peticion de los datos para crear un grafico"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&sql_fullselect="
                     f"SELECT%20{campo}%20FROM%20coins&lang=lg-spa&limit=0&section_id={','.join(vec_monedas)}"
                     "&resolve_portal=false&resolve_dd_relations=false")
    return request_grafico(campo, r)


def cantidad_tesoro(monedas):
    """Numbero de monedas en un tesoro"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=type&"
                     f"section_id={','.join(monedas)}&lang=lg-spa&limit=0&"
                     f"resolve_portal=false&resolve_dd_relations=false")
    part = r.json()["result"]
    denominations = []
    for i in part:
        try:
            tipo = i.get("type").split("_")[0]
            print(tipo)
            r2 = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                              "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=denomination&"
                              f"section_id={tipo}&lang=lg-spa&limit=100&resolve_portal=false"
                              f"&resolve_dd_relations=false")
            den = r2.json()["result"]["denomination"]
            denominations.append(den)
        except AttributeError:
            continue
    return denominations


def info_hallazgo(id_hallazgo):
    """Informacion de un hallazgo dado su id"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields="
                     "name%2C%20indexation%2C%20place%2C%20georef%2C%20public_info%2C%20coins%2C%20bibliography_data%2C"
                     f"%20map&lang=lg-spa&limit=10&section_id={id_hallazgo}"
                     f"&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    print(result["coins"])
    return filtro_monedas(result)


def filtro_monedas(result):
    """Muestra de monedas para un hallazgo o un tesoro, y curacion de datos"""
    filtro = re.compile('^>')
    try:
        id_biblio = json.loads(result["bibliography_data"])
        result["biblio"] = bibliografia(id_biblio[0])
    except TypeError:
        result["biblio"] = ""
    result["public_info"] = re.sub(filtro, "", result["public_info"])
    try:
        result["georef"] = json.loads(result["georef"])[0]
        aux = json.loads(result["georef"]["text"]).encode("ascii", "ignore")
        result["popup"] = re.sub(filtro, "", aux.decode())
    except TypeError:
        result["popup"] = "Localizacion indeterminada"
    result["map"] = json.loads(result["map"])
    try:
        result["coins"] = json.loads(result["coins"])
        result["tamanno"] = len(result["coins"])
        result["muestra"] = coins_tipo(result["coins"][:9]) if len(result["coins"]) > 9 else coins_tipo(result["coins"])
    except TypeError:
        result["muestra"] = []
        result["tamanno"] = 0
    return result


def hallazgos():
    """Lista de hallazgos con monedas asociadas"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields=section_id%2C%20coins%2C%20name"
                     "&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_hallazgos = list(filter(lambda x: x["coins"] is not None, result))
    return lista_hallazgos


def cecas_mapa():
    """Cecas localizadas en el mapa"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=mints&sql_fullselect=SELECT%20section_id%2C%20"
                     "name%2C%20map%2C%20relations_coins%20FROM%20mints&lang=lg-spa&limit=0&"
                     "resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_cecas = list(filter(lambda x: x["relations_coins"] is not None and x["name"] is not None
                                        and x["map"] != "{}", result))
    for i in lista_cecas:
        i["map"] = json.loads(i["map"])
    return lista_cecas


def hallazgos_mapa():
    """Hallazgos localizados en el mapa"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields=section_id%2C%20name%2C%20map%"
                     "2C%20coins&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_hallazgos = list(filter(lambda x: x["coins"] is not None and x["map"] != "{}", result))
    for i in lista_hallazgos:
        i["map"] = json.loads(i["map"])
    return lista_hallazgos


def tesoros_mapa():
    """Tesoros localizados en el mapa"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=hoards&ar_fields=section_id%2C%20name%2C%20map&"
                     "lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_tesoros = list(filter(lambda x: x["map"] != "{}", result))
    for i in lista_tesoros:
        i["map"] = json.loads(i["map"])
    return lista_tesoros


def info_ceca(id_ceca):
    """Informacion de la ceca dado su id"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=mints&ar_fields=name%2C%20indexation%"
                     f"2C%20place%2C%20georef_geojson%2C%20map%2C%20uri%2C%20relations_coins&section_id={id_ceca}&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    result["map"] = json.loads(result["map"])
    monedas = json.loads(result["relations_coins"])
    result["monedas"] = coins_ceca(monedas)
    return result


def coins_ceca(vec_coins):
    """Monedas vinculadas a una ceca en el mapa"""
    vec_result = []
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&"
                     "ar_fields=section_id%2C%20findspot_data%2C%20mint%2C%20catalogue_type_mint&"
                     f"section_id={','.join(vec_coins)}&lang=lg-spa&limit=0&"
                     "resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    for i in result:
        try:
            i["mint"] = json.loads(result.get("mint").split(" | ")[0])
        except (TypeError, AttributeError):
            i["mint"] = ""
        try:
            i["catalogue_type_mint"] = json.loads(i["catalogue_type_mint"])
        except (TypeError, AttributeError):
            i["catalogue_type_mint"] = ""
        i["findspot_data"] = json.loads(i["findspot_data"])
        r2 = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                          f"code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields=map"
                          f"&section_id={i['findspot_data'][0]}"
                          "&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
        i["coords"] = json.loads(r2.json()["result"][0]["map"])
        vec_result.append(i)
    return result


def datos_informe(vec_monedas):
    """Extraccion y curacion de datos para el informe"""
    datos = []
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20denomination%"
                     "2C%20type_data%2C%20weight%2C%20diameter%2C%20dies%2C%20type_full_value%2C%20number%2C%20mint&"
                     f"section_id={','.join(vec_monedas)}&lang=lg-spa&limit=10&resolve_portal=false&"
                     f"resolve_dd_relations=false")
    result = r.json()["result"]
    for i in result:
        tipo = json.loads(i["type_data"])[0]
        datos_tipo = tipo_moneda(tipo)
        print(i["mint"])
        pre_ceca = i["mint"].split(" | ")[0]
        ceca = json.loads(pre_ceca)[0].split("|")[0].strip()
        tipo_dato = i["type_full_value"].split(" | ")[0]
        for j in datos_tipo.keys():
            datos_tipo[j] = "" if datos_tipo[j] is None else datos_tipo[j]
        datos.append((i["section_id"], i["denomination"].split(" | ")[0],
                      datos_tipo["legend_obverse"] + "\n" + datos_tipo["design_obverse"],
                      datos_tipo["legend_reverse"] + "\n" + datos_tipo["design_reverse"],
                      ceca, i["weight"], i["diameter"], i["dies"], tipo_dato, i["number"]))
    return datos


def buscador_tipos_base(offset):
    """Informacion base en el buscador de tipos"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=section_id%"
                     "2C%20uri&lang=lg-spa&order=section_id%20ASC&limit=50&"
                     f"resolve_portal=false&resolve_dd_relations=false&offset={offset * 50}")
    result = r.json()["result"]
    for i in result:
        i["uri"] = i["uri"].split(",")[0]
    return result


def busqueda_tipos(parametros):
    """Busqueda de tipos dados unos parametros, devuelve un vector de ids"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=section_id%2C%20mint%2C%20"
                     "date_in%2C%20date_out%2C%20denomination%2C%20material%2C%20catalogue&lang=lg-spa&order="
                     "section_id%20ASC&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in parametros.keys():
        if parametros[i] is not None:
            print(parametros[i])
            busca = list(filter(lambda x, val=i: x[val] is not None and str(parametros[val]) in str(x[val]), busca))
    return list(map(lambda x: str(x["section_id"]), busca))


def tipos_buscador(vec_tipos, offset):
    """Listado de los tipos encontrados en el buscador"""
    if not vec_tipos:
        return []
    tipos = vec_tipos[offset * 50: offset * 50 + 50] if len(vec_tipos) > offset * 50 + 50 else vec_tipos[offset * 50:]
    print(len(tipos))
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=section_id%"
                     f"2C%20uri&section_id={','.join(tipos)}&lang=lg-spa&order=section_id%20ASC&limit=50&"
                     f"resolve_portal=false&resolve_dd_relations=false&")
    lista_tipos = r.json()["result"]
    for i in lista_tipos:
        i["uri"] = i["uri"].split(",")[0]
    return lista_tipos


def num_tipos():
    """Cantidad de tipos en la base de datos"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&sql_fullselect=SELECT%20COUNT(*)%20"
                     "FROM%20types&lang=lg-spa&order=section_id%20ASC&limit=10&resolve_portal=false&"
                     "resolve_dd_relations=false")
    return int(r.json()["result"][0]["COUNT(*)"])


def bibliografia(id_b):
    """Bibliografia ordenada y curada"""
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     f"records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=bibliographic_references&section_id={id_b}"
                     "&lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    return " | ".join([result["ref_publications_title"], result["ref_publications_authors"],
                       result["ref_publications_magazine"], result["ref_publications_editor"],
                       result["ref_publications_date"]])


if __name__ == "__main__":
    print(info_moneda(967))
