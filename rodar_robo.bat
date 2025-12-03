@echo off
:: 1. Entra na pasta do projeto (O /d garante que mude de disco se precisar)
cd /d "C:\Users\Usuario 02\OneDrive - PROTOTYPE INDUSTRIA E COMERCIO DE EQUIPAMENTOS ELETRONICOS E PLASTICOS EIRELI\Documentos\dash_monitoramento_videowall"

:: 2. Ativa o ambiente virtual
call venv\Scripts\activate.bat

:: 3. Roda o script
python automatizacao.py

:: (Opcional) Tira o pause se quiser que a janela feche sozinha no final
:: pause