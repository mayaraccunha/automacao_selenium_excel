import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv # Biblioteca para gerenciar segredos

# Carrega variáveis de ambiente do arquivo .env (Segurança)
load_dotenv()

# --- CONFIGURAÇÕES GERAIS ---
USUARIO = os.getenv("ONSIGN_USER")
SENHA = os.getenv("ONSIGN_PASS")

# Caminhos dinâmicos (funcionam em qualquer computador)
DIRETORIO_ATUAL = os.getcwd()
CAMINHO_DOWNLOAD = os.path.join(DIRETORIO_ATUAL, "temp_downloads")
CAMINHO_SAIDA = os.path.join(DIRETORIO_ATUAL, "output")
ARQUIVO_FINAL = os.path.join(CAMINHO_SAIDA, "Relatorio_Consolidado.xlsx")
NOME_ABA = "Dados_Players"

# URLs
URL_LOGIN = "https://app.onsign.tv/login/"
URL_TARGET = "https://app.onsign.tv/players/"

# Garantir que as pastas existam
for path in [CAMINHO_DOWNLOAD, CAMINHO_SAIDA]:
    if not os.path.exists(path):
        os.makedirs(path)

print(">>> Iniciando Automação de Extração de Dados - Digital Signage <<<")

# Configurações do Navegador
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": CAMINHO_DOWNLOAD,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless") # Execução em background (sem abrir janela)
options.add_argument("--window-size=1920,1080")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    # 1. Login
    print("[1/5] Realizando login no sistema...")
    driver.get(URL_LOGIN)
    
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(USUARIO)
    driver.find_element(By.NAME, "password").send_keys(SENHA)
    
    # Busca genérica pelo botão de ação principal
    botao_entrar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
    botao_entrar.click()

    # 2. Navegação e Download
    print("[2/5] Acessando relatório de players...")
    time.sleep(3) # Aguarda carregamento pós-login
    driver.get(URL_TARGET)
    
    # Clicar no botão de exportação (Seletor genérico via classe)
    botao_exportar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-info")))
    botao_exportar.click()
    
    print("      Aguardando conclusão do download...")
    time.sleep(10) # Tempo de espera para o arquivo baixar completamente

    # 3. Identificação do Arquivo
    print("[3/5] Processando arquivo baixado...")
    arquivos = [os.path.join(CAMINHO_DOWNLOAD, f) for f in os.listdir(CAMINHO_DOWNLOAD)]
    if not arquivos:
        raise FileNotFoundError("O download falhou ou a pasta está vazia.")
    
    arquivo_recente = max(arquivos, key=os.path.getctime)
    print(f"      Arquivo capturado: {os.path.basename(arquivo_recente)}")

    # Leitura do arquivo (suporte a CSV e Excel)
    if arquivo_recente.endswith('.csv'):
        df = pd.read_csv(arquivo_recente)
    else:
        df = pd.read_excel(arquivo_recente)

    # 4. Tratamento de Dados (Data Cleaning)
    print("[4/5] Aplicando regras de negócio e limpeza...")
    
    # Regra: Remover dispositivos de teste/homologação da base final
    coluna_filtro = "Nome do Player"
    termo_exclusao = "Teste" # Termo genérico para exclusão
    
    if coluna_filtro in df.columns:
        linhas_antes = len(df)
        # Filtra removendo linhas que contêm o termo de exclusão
        df = df[~df[coluna_filtro].str.contains(termo_exclusao, na=False, case=False)]
        linhas_depois = len(df)
        print(f"      Limpeza concluída: {linhas_antes - linhas_depois} registros de teste removidos.")
    else:
        print(f"      Aviso: Coluna '{coluna_filtro}' não encontrada. Pular etapa de filtro.")

    # 5. Exportação para Data Warehouse / Excel Mestre
    print("[5/5] Atualizando base consolidada...")
    
    if not os.path.exists(ARQUIVO_FINAL):
        df.to_excel(ARQUIVO_FINAL, sheet_name=NOME_ABA, index=False)
    else:
        with pd.ExcelWriter(ARQUIVO_FINAL, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=NOME_ABA, index=False)

    print(f"\n>>> SUCESSO! Dados atualizados em: {ARQUIVO_FINAL}")

    # Limpeza da pasta temporária
    for f in os.listdir(CAMINHO_DOWNLOAD):
        os.remove(os.path.join(CAMINHO_DOWNLOAD, f))

except Exception as e:
    print(f"\n[ERRO CRÍTICO]: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
    print("Processo finalizado.")