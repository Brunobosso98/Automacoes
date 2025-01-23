from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTextEdit, QProgressBar, QLabel, QLineEdit,
                           QComboBox, QSpinBox, QGroupBox)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import sys
import time
import json

class ScraperThread(QThread):
    progress_update = pyqtSignal(str)
    data_update = pyqtSignal(list)  # Para enviar dados para o gráfico
    finished = pyqtSignal()
    
    def __init__(self, url, min_diff):
        super().__init__()
        self.url = url
        self.min_diff = min_diff
    
    def run(self):
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome()
            wait = WebDriverWait(driver, 10)

            self.progress_update.emit("Abrindo o site...")
            driver.get(self.url)

            self.progress_update.emit("Coletando informações dos itens...")
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

            self.progress_update.emit("Carregando dados do JSON...")
            with open('AutomacaoDash/prices_orders_usd.json', 'r') as f:
                json_data = json.load(f)

            precos_json = {item['market_hash_name']: item['price'] * 6 for item in json_data['items']}

            self.progress_update.emit("Comparando preços...")
            resultados = []
            dados_grafico = []
            
            for nome, preco_site in zip(nomes_itens, preco_itens):
                if nome in precos_json:
                    preco_json = precos_json[nome]
                    diferenca_percentual = ((preco_json - preco_site) / preco_site) * 100
                    
                    if diferenca_percentual >= self.min_diff:
                        resultado = f"""Item: {nome}
Preço no site: R$ {preco_site:.2f}
Preço MarketCSGO: R$ {preco_json:.2f}
Diferença: {diferenca_percentual:.2f}%
{'-' * 50}"""
                        resultados.append(resultado)
                        dados_grafico.append((nome, diferenca_percentual))

            if not resultados:
                self.progress_update.emit("Não foram encontradas skins com a diferença mínima especificada.")
            else:
                resultado_final = "\n".join(resultados)
                self.progress_update.emit(resultado_final)
                
            self.data_update.emit(dados_grafico)
            
            driver.quit()
            self.finished.emit()
            
        except Exception as e:
            self.progress_update.emit(f"Erro: {str(e)}")
            self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DashSkins Comparador")
        self.setGeometry(100, 100, 1200, 800)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Layout esquerdo para controles e resultados
        left_layout = QVBoxLayout()
        
        # Grupo de configurações
        config_group = QGroupBox("Configurações")
        config_layout = QVBoxLayout()
        
        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setText("https://dashskins.com.br/deals?page=")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        config_layout.addLayout(url_layout)

        # Diferença mínima
        diff_layout = QHBoxLayout()
        diff_label = QLabel("Diferença mínima (%):")
        self.diff_spin = QSpinBox()
        self.diff_spin.setRange(1, 100)
        self.diff_spin.setValue(10)
        diff_layout.addWidget(diff_label)
        diff_layout.addWidget(self.diff_spin)
        config_layout.addLayout(diff_layout)

        config_group.setLayout(config_layout)
        left_layout.addWidget(config_group)

        # Botão para iniciar a busca
        self.start_button = QPushButton("Iniciar Busca")
        self.start_button.clicked.connect(self.start_scraping)
        left_layout.addWidget(self.start_button)

        # Área de texto para resultados
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        left_layout.addWidget(self.text_area)

        # Status label
        self.status_label = QLabel("Pronto para iniciar")
        left_layout.addWidget(self.status_label)

        main_layout.addLayout(left_layout)

        # Layout direito para o gráfico
        right_layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(6, 8))
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)
        main_layout.addLayout(right_layout)

        self.scraper_thread = None

    def start_scraping(self):
        self.start_button.setEnabled(False)
        self.text_area.clear()
        self.status_label.setText("Processando...")
        self.ax.clear()
        
        url = self.url_input.text()
        min_diff = self.diff_spin.value()
        
        self.scraper_thread = ScraperThread(url, min_diff)
        self.scraper_thread.progress_update.connect(self.update_progress)
        self.scraper_thread.data_update.connect(self.update_graph)
        self.scraper_thread.finished.connect(self.scraping_finished)
        self.scraper_thread.start()

    def update_progress(self, text):
        self.text_area.append(text)

    def update_graph(self, dados):
        self.ax.clear()
        if dados:
            nomes, diferencas = zip(*dados)
            bars = self.ax.bar(range(len(nomes)), diferencas)
            self.ax.set_xticks(range(len(nomes)))
            self.ax.set_xticklabels(nomes, rotation=45, ha='right')
            self.ax.set_ylabel('Diferença (%)')
            self.ax.set_title('Diferença de Preços por Item')
            
            # Adicionar valores acima das barras
            for bar in bars:
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.1f}%',
                         ha='center', va='bottom')
            
            plt.tight_layout()
            self.canvas.draw()

    def scraping_finished(self):
        self.start_button.setEnabled(True)
        self.status_label.setText("Busca finalizada!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

