import requests
import json
import re


def monedas_inicio():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=image_obverse%2C%20type_full_value"
                     "%2C%20section_id&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    filtered = list(filter(lambda x: x["image_obverse"] != "null" and x["type_full_value"] != "", result))
    return filtered


def num_monedas():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coin&sql_fullselect=SELECT%20COUNT(*)"
                     "%20AS%20cuenta%20FROM%20coins&lang=lg-spa&limit=10&"
                     "resolve_portal=false&resolve_dd_relations=false")
    return int(r.json()["result"][0]["cuenta"])


def info_moneda(id_moneda):
    dedalo_link = "https://wondercoins.uca.es"
    r = requests.get(f"http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     f"code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20catalogue_type_mint"
                     f"%2C%20mint%2C%20type%2C%20type_full_value%2C%20mint_name%2C%20weight%2C%20diameter%2C%20dies%"
                     f"2C%20image_obverse%2C%20image_reverse%2C%20number%2C%20uri%2C%20find_type%2C%20findspot"
                     f"%2C%20type_data&"
                     f"section_id={id_moneda}&lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    try:
        result = r.json()["result"][0]
        try:
            result["image_obverse"] = dedalo_link + result["image_obverse"]
            result["image_reverse"] = dedalo_link + result["image_reverse"]
        except (TypeError, AttributeError):
            result["image_obverse"] = "../static/logo-sinletras-sinfondo.jpg"
            result["image_reverse"] = "../static/logo-sinletras-sinfondo.jpg"
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
            result["d_anverso"] = datos_tipo["legend_obverse"]
            result["d_reverso"] = datos_tipo["legend_reverse"]
            result["l_anverso"] = datos_tipo["design_obverse"]
            result["l_reverso"] = datos_tipo["design_reverse"]
        except (TypeError, AttributeError):
            result["d_anverso"] = ""
            result["d_reverso"] = ""
            result["l_anverso"] = ""
            result["l_reverso"] = ""
    except IndexError:
        result = []
    return result


def materiales():
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
    except IndexError:
        result = []
    return result


def coins_tipo(vec_monedas):
    datos = []
    dedalo_link = "https://wondercoins.uca.es"
    for i in vec_monedas:
        try:
            r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                             "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20"
                             f"mint%2C%20catalogue_type_mint%2C%20image_obverse%2C%20image_reverse&section_id={i}&"
                             "lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
            result = r.json()["result"][0]
            result["image_obverse"] = dedalo_link + result["image_obverse"]
            result["image_reverse"] = dedalo_link + result["image_reverse"]
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
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=design_obverse%2C%20design_reverse%"
                     f"2C%20legend_obverse%2C%20legend_reverse&section_id={t_moneda}&lang=lg-spa&limit=10&"
                     f"resolve_portal=false"
                     "&resolve_dd_relations=false")
    result = r.json()["result"][0]
    return result


def busqueda(buscador):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id%2C%20material"
                     "%2C%20mint%2C%20type_full_value&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in buscador.keys():
        if buscador[i] is not None and buscador[i] not in [0, ""]:
            print(buscador[i])
            busca = list(filter(lambda x: x[i] is not None and buscador[i] in x[i], busca))
    return list(map(lambda x: str(x["section_id"]), busca))


def busqueda_tipo(buscador):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=material%2C%20catalogue%2C%"
                     "20denomination%2C%20mint%2C%20date_in%2C%20date_out%2C%20section_id&lang=lg-spa&order="
                     "section_id%20ASC&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in buscador.keys():
        if buscador[i] is not None and buscador[i] not in [0, ""]:
            print(buscador[i])
            busca = list(filter(lambda x: x[i] is not None and buscador[i] in x[i], busca))
    return list(map(lambda x: str(x["section_id"]), busca))


def monedas_buscador_base(offset):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=number%2C%20image_obverse%2C%20"
                     "image_reverse%2C%20section_id%2C%20mint%2C%20catalogue_type_mint%2C%20type_data&lang=lg-spa&"
                     "order=section_id%20ASC&limit=100"
                     f"&offset={offset * 100}&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    dedalo_link = "https://wondercoins.uca.es"
    for i in result:
        try:
            i["mint"] = json.loads(i["mint"].split("|")[0].strip())
            i["catalogue_type_mint"] = json.loads(i["catalogue_type_mint"])
        except AttributeError:
            i["mint"] = ""
            i["catalogue_type_mint"] = ""
        try:
            i["image_obverse"] = dedalo_link + i["image_obverse"]
        except TypeError:
            i["image_obverse"] = "../static/logo-sinletras-sinfondo.jpg"
        try:
            i["image_reverse"] = dedalo_link + i["image_reverse"]
        except TypeError:
            i["image_reverse"] = "../static/logo-sinletras-sinfondo.jpg"
    return result


def monedas_graficos_base(campo):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     f"code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields={campo}&lang=lg-spa&"
                     "&limit=0&resolve_portal=false&resolve_dd_relations=false")
    return request_grafico(campo, r)


def request_grafico(campo, r):
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
    dedalo_link = "https://wondercoins.uca.es"
    for i in result:
        try:
            i["mint"] = json.loads(i["mint"].split("|")[0].strip())
            i["catalogue_type_mint"] = json.loads(i["catalogue_type_mint"])
        except AttributeError:
            continue
        i["number"] = "SIN NUMERO" if i["number"] is None else i["number"]
        try:
            i["image_obverse"] = dedalo_link + i["image_obverse"]
        except TypeError:
            i["image_obverse"] = "../static/logo-sinletras-sinfondo.jpg"
        try:
            i["image_reverse"] = dedalo_link + i["image_reverse"]
        except TypeError:
            i["image_reverse"] = "../static/logo-sinletras-sinfondo.jpg"
    return result


def tesoros():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=hoards&ar_fields="
                     "section_id%2C%20name&lang=lg-spa&order=section_id%20ASC&limit=0"
                     "&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    return result


def info_tesoro(id_tesoro):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=hoards&ar_fields="
                     "section_id%2C%20name%2C%20indexation%2C%20coins%2C%20date_in%2C%20date_out%2C%20public_info%"
                     f"2C%20place%2C%20map%2C%20bibliography_data%2C%20georef&section_id={id_tesoro}&lang="
                     f"lg-spa&limit=0"
                     "&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    return filtro_monedas(result)


def datos_grafico(vec_monedas, campo):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&sql_fullselect="
                     f"SELECT%20{campo}%20FROM%20coins&lang=lg-spa&limit=0&section_id={','.join(vec_monedas)}"
                     "&resolve_portal=false&resolve_dd_relations=false")
    return request_grafico(campo, r)


def cantidad_tesoro(monedas):
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
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields="
                     "name%2C%20indexation%2C%20place%2C%20georef%2C%20public_info%2C%20coins%2C%20bibliography_data%2C"
                     f"%20map&lang=lg-spa&limit=10&section_id={id_hallazgo}"
                     f"&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    print(result["coins"])
    return filtro_monedas(result)


def filtro_monedas(result):
    filtro = re.compile('<.*?>')
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
        result["muestra"] = coins_tipo(result["coins"][:9]) if len(result["coins"]) > 9 else coins_tipo(result["coins"])
    except TypeError:
        result["muestra"] = []
    return result


def hallazgos():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields=section_id%2C%20coins%2C%20name"
                     "&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_hallazgos = list(filter(lambda x: x["coins"] is not None, result))
    return lista_hallazgos


def cecas_mapa():
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
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=findspots&ar_fields=section_id%2C%20name%2C%20map%"
                     "2C%20coins&lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_hallazgos = list(filter(lambda x: x["coins"] is not None and x["map"] != "{}", result))
    for i in lista_hallazgos:
        i["map"] = json.loads(i["map"])
    return lista_hallazgos


def tesoros_mapa():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=hoards&ar_fields=section_id%2C%20name%2C%20map&"
                     "lang=lg-spa&limit=10&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    lista_tesoros = list(filter(lambda x: x["map"] != "{}", result))
    for i in lista_tesoros:
        i["map"] = json.loads(i["map"])
    return lista_tesoros


def info_ceca(id_ceca):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=mints&ar_fields=name%2C%20indexation%"
                     f"2C%20place%2C%20georef_geojson%2C%20map%2C%20uri%2C%20relations_coins&section_id={id_ceca}&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"][0]
    result["map"] = json.loads(result["map"])
    result["georef_geojson"] = json.loads(result["georef_geojson"])
    monedas = json.loads(result["relations_coins"])
    result["monedas"] = coins_ceca(monedas)
    return result


def coins_ceca(vec_coins):
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
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/"
                     "records?code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=section_id%"
                     "2C%20uri&lang=lg-spa&order=section_id%20ASC&limit=50&"
                     f"resolve_portal=false&resolve_dd_relations=false&offset={offset * 50}")
    result = r.json()["result"]
    for i in result:
        i["uri"] = i["uri"].split(",")[0]
    return result


def busqueda_tipos(parametros):
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=section_id%2C%20mint%2C%20"
                     "date_in%2C%20date_out%2C%20denomination%2C%20material%2C%20catalogue&lang=lg-spa&order="
                     "section_id%20ASC&limit=0&resolve_portal=false&resolve_dd_relations=false")
    busca = r.json()["result"]
    for i in parametros.keys():
        if parametros[i] is not None:
            print(parametros[i])
            busca = list(filter(lambda x: x[i] is not None and str(parametros[i]) in str(x[i]), busca))
    return list(map(lambda x: str(x["section_id"]), busca))


def tipos_buscador(vec_tipos, offset):
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
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&sql_fullselect=SELECT%20COUNT(*)%20"
                     "FROM%20types&lang=lg-spa&order=section_id%20ASC&limit=10&resolve_portal=false&"
                     "resolve_dd_relations=false")
    return int(r.json()["result"][0]["COUNT(*)"])


if __name__ == "__main__":
    print(tipos_buscador(busqueda_tipos({"material": "Plata"}), 0))
