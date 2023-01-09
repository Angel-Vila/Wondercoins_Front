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


if __name__ == "__main__":
    print(info_moneda(1))
