from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializa o navegador
driver = webdriver.Chrome()

try:
    # 1. Abra a página de login
    driver.get("https://portal.ssparisi.com.br/prime/login.php")
    time.sleep(5)  # Aguarde o carregamento da página

    # 2. Preencha o usuário
    campo_usuario = driver.find_element(By.ID, "User")
    campo_usuario.send_keys("mauro@conttrolare.com.br")

    # 3. Preencha a senha
    campo_senha = driver.find_element(By.ID, "Pass")
    campo_senha.send_keys("Juni4724")

    # 4. Clique no botão de login
    botao_login = driver.find_element(By.ID, "SubLogin")
    botao_login.click()
    time.sleep(2)  # Aguarde para garantir que o login seja processado

    # 5. Clique no botão de Banco Online
    botao_banco_online = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "sidebar-sub-toggle"))
    )
    botao_banco_online.click()
    time.sleep(1)

    # 6. Abra uma nova guia
    driver.switch_to.new_window('tab')

    # 7. Navegue para a página de extratos
    driver.get("https://portal.ssparisi.com.br/prime/app/ctrl/GestaoBankExtratoSS.php")
    time.sleep(4)

    # 8. Aguarde a mudança no valor do campo
    valor_inicial = "Digite/Escolha..."
    WebDriverWait(driver, 20).until(
        lambda d: d.find_element(By.ID, "autocompleter-empresa-autocomplete").get_attribute("value") != valor_inicial
    )
    print("O valor do campo mudou!")

    # 9. Clique no botão "Bancos"
    botao_bancos = driver.find_element(By.ID, "headingBank")
    botao_bancos.click()
    time.sleep(1)

    # 10. Clique no botão "Ver Lançamentos"
    botao_ver_lancamentos = driver.find_element(By.ID, "account-7097")
    botao_ver_lancamentos.click()
    time.sleep(50)  # Aguarde o processamento final

except Exception as e:
    print("Ocorreu um erro durante a automação:", e)

finally:
    # Encerra o navegador
    driver.quit()
