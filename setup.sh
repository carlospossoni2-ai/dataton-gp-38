#!/bin/bash

echo "🚀 Iniciando setup do ambiente..."

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

echo "✅ Ambiente pronto! Agora você pode rodar:"
echo "streamlit run app/app.py"
