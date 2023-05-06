import os
from os.path import join, dirname
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait  # wait until
from selenium.webdriver.support import expected_conditions as EC  # conditions for wait

from time import sleep
import pandas as pd


def activate_chrome_driver(path):
    """
    Activates Chrome driver for scraping based on the path to it.
    """
    service = Service(executable_path=path)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def setup_env():
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    LOGIN = os.environ.get("LOGIN")
    PASSWORD = os.environ.get("PASSWORD")
    PATH_DRIVER = os.environ.get("PATH_CHROME_DRIVER")

    return LOGIN, PASSWORD, PATH_DRIVER


def login_sigaa(driver, url, login, password):
    """
    Login Sigaa using Selenium
    """
    driver.get(url)

    # cookie consent
    cookie_consent = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.CLASS_NAME, "cookie-consent-modal")
    )
    ciente_button = cookie_consent.find_element(By.TAG_NAME, "button")
    ciente_button.click()

    login_form = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.NAME, "loginForm")
    )
    user_login_input = login_form.find_element(By.NAME, "user.login")
    user_login_input.send_keys(login)
    user_password_input = login_form.find_element(By.NAME, "user.senha")
    user_password_input.send_keys(password)
    sleep(1)
    login_form.submit()


def main():
    URL_SIGAA_LOGIN = "https://sig.ifc.edu.br/sigaa/verTelaLogin.do"
    LOGIN, PASSWORD, PATH_DRIVER = setup_env()

    driver = activate_chrome_driver(PATH_DRIVER)
    # LOGAR
    login_sigaa(driver, URL_SIGAA_LOGIN, LOGIN, PASSWORD)

    div_turmas = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.ID, "turmas-portal")
    )
    form_turmas = div_turmas.find_elements(By.TAG_NAME, "form")[1:]
    turmas = {}

    for turma in form_turmas:
        link_turma = turma.find_element(By.TAG_NAME, "a")
        nome_turma = link_turma.text
        turmas.update({nome_turma: []})
    print(turmas)

    for i in range(len(turmas)):
        div_turmas = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "turmas-portal")
        )
        form_turmas = div_turmas.find_elements(By.TAG_NAME, "form")[i + 1 :]
        link_turma = form_turmas[0].find_element(By.TAG_NAME, "a")
        print(link_turma.text)
        link_turma.click()

        div_barra_esquerda = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "barraEsquerda")
        )

        #
        item_menu = div_barra_esquerda.find_elements(By.CLASS_NAME, "itemMenu")
        for item in item_menu:
            print(item.text)
        tabela_relatorio = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.CLASS_NAME, "tabelaRelatorio")
        )
        #

        relatorio_data = pd.read_html(tabela_relatorio.get_attribute("outerHTML"))
        print(relatorio_data)

        for j in range(2):
            driver.back()


if __name__ == "__main__":
    main()
