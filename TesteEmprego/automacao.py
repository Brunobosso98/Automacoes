from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import shutil
from datetime import datetime

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 20)


driver.get("https://portal.ssparisi.com.br/prime/login.php")

campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "User")))
campo_usuario.clear()
campo_usuario.send_keys("mauro@conttrolare.com.br")

campo_senha = wait.until(EC.presence_of_element_located((By.ID, "Pass")))
campo_senha.clear()
campo_senha.send_keys("Juni4724")

botao_login = wait.until(EC.element_to_be_clickable((By.ID, "SubLogin")))
botao_login.click()

botao_banco_online = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/ul/li[10]/a")))
botao_banco_online.click()
time.sleep(2)

botao_lancamento = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/ul/li[10]/ul/li[1]")))
botao_lancamento.click()
time.sleep(5)

campo_empresa = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="autocompleter-empresa-autocomplete"]')))
campo_empresa.send_keys("CONTTROL - SICREDI")

botao_bancos = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bankDiv"]')))
botao_bancos.click()

botao_lancamento = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="account-7097"]')))
botao_lancamento.click()
time.sleep(6)

campo_data = wait.until(EC.presence_of_element_located((By.ID, 'initialDate')))
campo_data.send_keys("01/12/2024")

campo_data = wait.until(EC.presence_of_element_located((By.ID, 'finalDate')))
campo_data.send_keys("05/01/2025")
time.sleep(6)

botao_processar = wait.until(EC.presence_of_element_located((By.ID, 'seeTransactions')))
botao_processar.click()
time.sleep(10)


botao_exportar = wait.until(EC.presence_of_element_located((By.ID, 'export-data')))
botao_exportar.click()
time.sleep(5)

botao_baixar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))
botao_baixar.click()
time.sleep(5)

download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
destino_dir = r"C:\Users\bruno\Documents\Teste.txt"

arquivos = [f for f in os.listdir(download_dir) if f.endswith('.txt')]
if arquivos:
  arquivo_mais_recente = max([os.path.join(download_dir, f) for f in arquivos], key=os.path.getmtime)

  caminho_destino = os.path.join(destino_dir)

  shutil.move(arquivo_mais_recente, caminho_destino)
  print(f"Arquivo movido com sucesso para: {caminho_destino}")

driver.quit()
