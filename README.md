# 🤖 Automação de Extração de Dados - Digital Signage (ETL)

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Web_Automation-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![ETL](https://img.shields.io/badge/ETL-Pipeline-orange?style=for-the-badge)

Este projeto consiste em um **Robô de Extração de Dados (RPA)** desenvolvido para automatizar a rotina de monitoramento de players de mídia OOH (Out-of-Home).

O script acessa a plataforma de gestão (OnSign TV), realiza o download dos relatórios brutos, aplica regras de negócio (limpeza de dados) e consolida as informações em uma base estruturada Excel, pronta para ser consumida por ferramentas de BI.

---

## 🚀 Funcionalidades

* **Automação Web (Web Scraping):** Login seguro e navegação automática até a área de exportação de dados usando `Selenium`.
* **Tratamento de Dados:** * Sanitização de colunas.
    * Remoção automática de dispositivos de teste/homologação.
    * Padronização de dados usando `Pandas`.
* **Segurança:** Credenciais gerenciadas via variáveis de ambiente (`.env`), garantindo que senhas não fiquem expostas no código.
* **Gestão de Arquivos:** Sistema inteligente que gerencia downloads temporários e limpa resíduos após o processamento.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.13
* **Bibliotecas Principais:**
    * `Selenium`: Para interação com o navegador Chrome.
    * `Pandas`: Para manipulação e filtragem dos dados (Dataframe).
    * `Python-Dotenv`: Para gestão de segurança e variáveis de ambiente.
    * `OpenPyXL`: Para exportação e formatação do arquivo Excel final.

---

## 📂 Estrutura do Projeto

```text
├── output/              # Pasta onde o relatório final tratado é salvo
├── temp_downloads/      # Pasta temporária para downloads (limpa automaticamente)
├── venv/                # Ambiente virtual Python
├── .env                 # Arquivo de configuração (Senhas - Não versionado)
├── .gitignore           # Arquivos ignorados pelo Git
├── automatizacao.py     # Código fonte principal da automação
├── README.md            # Documentação do projeto
├── requirements.txt     # Lista de dependências do projeto
└── rodar_robo.bat       # Script para execução rápida no Windows