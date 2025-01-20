from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 10)

driver.get("https://demoqa.com/")

first_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[1]')))
first_element.click()

web_tables = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="item-3"]')))
web_tables.click()
time.sleep(1)

dados = pd.read_csv("AutomacaoForms/dados.csv")

for linha in dados.index:
    add_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="addNewRecordButton"]')))
    add_button.click()

    first_name = str(dados.loc[linha, "primeiro_nome"])
    last_name = str(dados.loc[linha, "sobrenome"])
    email = str(dados.loc[linha, "email"])
    age = str(dados.loc[linha, "idade"])
    salary = str(dados.loc[linha, "salario"])
    department = str(dados.loc[linha, "departamento"])

    wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(first_name)
    wait.until(EC.presence_of_element_located((By.ID, "lastName"))).send_keys(last_name)
    wait.until(EC.presence_of_element_located((By.ID, "userEmail"))).send_keys(email)
    wait.until(EC.presence_of_element_located((By.ID, "age"))).send_keys(age)
    wait.until(EC.presence_of_element_located((By.ID, "salary"))).send_keys(salary)
    wait.until(EC.presence_of_element_located((By.ID, "department"))).send_keys(department)
    
    submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit")))
    submit_button.click()
    time.sleep(1)


time.sleep(10)
driver.quit()
