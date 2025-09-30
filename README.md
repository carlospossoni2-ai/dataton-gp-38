# Recomendador de Vagas

## Descrição do projeto
Este projeto é um **sistema de recomendação de vagas** que permite que candidatos submetam seus currículos e recebam sugestões de vagas compatíveis.  
O sistema utiliza **Processamento de Linguagem Natural (NLP)** e **embeddings** para comparar o currículo do candidato com vagas cadastradas em um DataFrame.  

O app também disponibiliza um **currículo de exemplo** para download e visualização.

## Stack utilizada
- **Python 3.10+**
- **Streamlit**: Interface web interativa
- **Pandas / Numpy**: Manipulação de dados
- **NLTK / Spacy**: Pré-processamento de texto e lematização
- **Sentence Transformers**: Geração de embeddings e cálculo de similaridade
- **Pickle**: Armazenamento de embeddings pré-calculados
## Como Rodar o App Localmente
1. Clone o repositório:
-    git clone https://github.com/carlospossoni2-ai/dataton-gp-38.git
-    cd dataton-gp-38
  
Execute o setup do projeto:
-    ./setup.py
    
## Como treinar o modelo novamente
