from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from config import EMAIL, TELEFONE
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.get("https://dlp.hashtagtreinamentos.com/python/minicurso/minicurso-automacao/inscricao?curso=python&origemurl=hashtag_yt_org_minipython_8AMNaVt0z_M&utm_campaign=programacao&utm_content=python%2Fminicurso%2Fminicurso-automacao%2Finscricao&conversion=lespy-jan-25")

campo_nome = wait.until(EC.presence_of_element_located((By.ID, "firstname")))
campo_email = wait.until(EC.presence_of_element_located((By.ID, "email")))
campo_telefone = wait.until(EC.presence_of_element_located((By.ID, "phone")))

campo_nome.send_keys("Bruno Bosso Martins")
campo_email.send_keys(EMAIL)
campo_telefone.send_keys(TELEFONE)

botao_cadastrar = wait.until(EC.element_to_be_clickable((By.ID, "_form_1925_submit")))
botao_cadastrar.click()

botao_logar = wait.until(EC.element_to_be_clickable((By.ID, "botao-minicurso")))
botao_logar.click()

try:
    time.sleep(10)
except TimeoutException:
    print("Elemento não encontrado no tempo especificado")

driver.quit()


