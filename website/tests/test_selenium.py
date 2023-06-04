from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def test_inicio():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:5000")
    assert driver.title == "Archeomoneta - Inicio"
    imagen = driver.find_element(By.ID, "img-moneda")
    imagen.click()
    assert "Archeomoneta - Moneda " in driver.title
    textos = driver.find_elements(By.TAG_NAME, "p")
    for i in textos:
        print(i.text)


def test_buscador():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:5000/buscador")
    assert driver.title == "Archeomoneta - Buscador"
    buscador = driver.find_element(By.ID, "buscador")
    selector_id = buscador.find_element(By.ID, "m_id")
    selector_id.send_keys("691")
    boton = buscador.find_element(By.NAME, "Buscar")
    boton.click()
    moneda = driver.find_element(By.ID, "moneda-691")
    moneda.click()
    ventanas = driver.window_handles
    driver.switch_to.window(ventanas[1])
    timeout = 5
    try:
        pagina_cargada = EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
        WebDriverWait(driver, timeout).until(pagina_cargada)
        assert driver.title == "Archeomoneta - Moneda 691"
    except TimeoutException:
        print("Error: no se cargo la pagina")


def test_tipo():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:5000/tipo/1")
    assert driver.title == "Archeomoneta - RIC I (second edition) Augustus 1A"
    moneda_tipo = driver.find_element(By.ID, "link-moneda-967")
    moneda_tipo.click()
    ventanas = driver.window_handles
    driver.switch_to.window(ventanas[1])
    timeout = 5
    try:
        pagina_cargada = EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
        WebDriverWait(driver, timeout).until(pagina_cargada)
        assert driver.title == "Archeomoneta - Moneda 967"
    except TimeoutException:
        print("Error: no se cargo la pagina")


def test_informe():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", "./")
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("http://127.0.0.1:5000/informes")
    selector = Select(driver.find_element(By.ID, "materiales"))
    selector.select_by_visible_text("Plata")
    descarga = driver.find_element(By.NAME, "Generar informe")
    descarga.click()

