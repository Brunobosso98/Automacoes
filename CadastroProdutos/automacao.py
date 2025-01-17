import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.get("https://dlp.hashtagtreinamentos.com/python/intensivao/login")

campo_email = wait.until(EC.presence_of_element_located((By.ID, "email")))
campo_senha = wait.until(EC.presence_of_element_located((By.ID, "password")))

campo_email.send_keys("pythonimpressionador@gmail.com")
campo_senha.send_keys("sua_senha")

botao_login = wait.until(EC.element_to_be_clickable((By.ID, "pgtpy-botao")))
botao_login.click()

time.sleep(5)

tabela = pd.read_csv("CadastroProdutos/produtos.csv")

for linha in tabela.index:
  codigo = str(tabela.loc[linha, "codigo"])
  marca = str(tabela.loc[linha, "marca"])
  tipo = str(tabela.loc[linha, "tipo"])
  categoria = str(tabela.loc[linha, "categoria"])
  preco_unitario = str(tabela.loc[linha, "preco_unitario"])
  custo = str(tabela.loc[linha, "custo"])
  obs = str(tabela.loc[linha, "obs"])

  wait.until(EC.presence_of_element_located((By.ID, "codigo"))).send_keys(codigo)
  wait.until(EC.presence_of_element_located((By.ID, "marca"))).send_keys(marca)
  wait.until(EC.presence_of_element_located((By.ID, "tipo"))).send_keys(tipo)
  wait.until(EC.presence_of_element_located((By.ID, "categoria"))).send_keys(categoria)
  wait.until(EC.presence_of_element_located((By.ID, "preco_unitario"))).send_keys(preco_unitario)
  wait.until(EC.presence_of_element_located((By.ID, "custo"))).send_keys(custo)
  
  if obs.strip() != "":
      wait.until(EC.presence_of_element_located((By.ID, "obs"))).send_keys(obs)

  time.sleep(2)

  botao_enviar = wait.until(EC.element_to_be_clickable((By.ID, "pgtpy-botao")))
  botao_enviar.click()

  time.sleep(5)

driver.quit()