#!/bin/bash

echo "🚀 Iniciando setup do ambiente..."

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Baixar modelo de português do spaCy
python -m spacy download pt_core_news_sm

echo "✅ Ambiente pronto! Agora você pode rodar:"
echo "streamlit run app/app.py"
