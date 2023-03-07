import requests


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


if __name__ == "__main__":
    print(materiales())
