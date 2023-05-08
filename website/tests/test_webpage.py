from website.app import app
import requests
import website.peticiones


def test_inicio():
    response = app.test_client().get("/")
    print(response.status)
    assert response.status == "200 OK"


def test_monedas():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=coins&ar_fields=section_id&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    for i in result:
        response = app.test_client().get(f"/moneda/{i['section_id']}")
        assert response.status == "200 OK"


def test_tipos():
    r = requests.get("http://wwwondercoins.uca.es/dedalo/lib/dedalo/publication/server_api/v1/json/records?"
                     "code=12sdf58d91fgt_66sdfc-_ssddsDF_F*l&table=types&ar_fields=section_id&"
                     "lang=lg-spa&limit=0&resolve_portal=false&resolve_dd_relations=false")
    result = r.json()["result"]
    print(len(result))
    for i in result:
        print(i["section_id"])
        response = app.test_client().get(f"/tipo/{i['section_id']}")
        assert response.status == "200 OK"


def test_tesoros():
    tesoros = website.peticiones.tesoros()
    for i in tesoros:
        print(i["section_id"])
        response = app.test_client().get(f"/tesoro/{i['section_id']}")
        assert response.status == "200 OK"


def test_hallazgos():
    hallazgos = website.peticiones.hallazgos()
    for i in hallazgos:
        print(i["section_id"])
        response = app.test_client().get(f"/hallazgo/{i['section_id']}")
        assert response.status == "200 OK"


def test_cecas():
    cecas = website.peticiones.cecas_mapa()
    for i in cecas:
        print(i["section_id"])
        response = app.test_client().get(f"/ceca/{i['section_id']}")
        assert response.status == "200 OK"
