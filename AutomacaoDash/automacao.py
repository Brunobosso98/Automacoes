from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import re
import json

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.get("https://dashskins.com.br/deals?min=&max=&search=&item_type=&rarity=&itemset=&exterior=&weapon=&has_sticker=&has_charm=&has_stattrak=&is_souvenir=&is_instant=&limit=&page=1")

# botao_login = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/nav/div/div[2]/div[2]/div')))
# botao_login.click()
# time.sleep(5)


itens = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.image[alt]')))
nomes_itens = []
for item in itens:
    nome = item.get_attribute('alt')
    nome = nome.replace(f'StatTrak{chr(8482)}', 'StatTrak\\u2122')
    nome = nome.replace('龍王', '\\u9f8d\\u738b')
    nome = nome.replace('★', '\\u2605')
    nomes_itens.append(nome)


precos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'title.is-size-6.has-text-white-bis.has-text-centered')))
preco_itens = []
for preco in precos:
    valor = preco.text.replace('R$', '').strip()
    if ',' in valor:
        valor = valor.replace('.', '').replace(',', '.')
    preco_itens.append(float(valor))

# Printa os itens e seus preços
for nome, preco in zip(nomes_itens, preco_itens):
    print(f"{nome} - R$ {preco:.2f}")

# Carrega dados do arquivo JSON
with open('AutomacaoDash/prices_orders_usd.json', 'r') as f:
    json_data = json.load(f)

# Cria dicionário com preços do JSON em reais (multiplicado por 6)
precos_json = {item['market_hash_name']: item['price'] * 6 for item in json_data['items']}

# Abre arquivo para escrita
with open('AutomacaoDash/resultados.txt', 'w', encoding='utf-8') as arquivo:
    # Compara preços e mostra apenas os com diferença > 10%
    for nome, preco_site in zip(nomes_itens, preco_itens):
        if nome in precos_json:
            preco_json = precos_json[nome]
            diferenca_percentual = ((preco_json - preco_site) / preco_site) * 100
            
            if diferenca_percentual >= 10:
                resultado = f"""Item: {nome}
Preço no site: R$ {preco_site:.2f}
Preço MarketCSGO: R$ {preco_json:.2f}
Diferença: {diferenca_percentual:.2f}%
{'-' * 50}
"""
                arquivo.write(resultado + '\n')

driver.quit()

