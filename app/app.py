import sys
import os
import re
import string
import unicodedata
import numpy as np
import pandas as pd
import nltk
import spacy
import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer, util

# -----------------------------
# Configuração da página Streamlit
# -----------------------------
st.set_page_config(page_title="Recomendador de Vagas", layout="centered")

# -----------------------------
# Inicializações
# -----------------------------
nltk.download('stopwords', quiet=True)
nlp = spacy.load("pt_core_news_sm")

# -----------------------------
# Funções de pré-processamento
# -----------------------------
def normalizar_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

def remover_pontuacao(text):
    punctuations = string.punctuation
    table = str.maketrans({key: ' ' for key in punctuations})
    text = text.translate(table)
    text = re.sub(r'\s+', ' ', text)
    return text

def normalizar_texto(texto):
    texto = texto.lower()
    texto = remover_pontuacao(texto)
    texto = normalizar_acentos(texto)
    texto = re.sub(r' +', ' ', texto)
    return ' '.join([w for w in texto.split()])

def tokenizar(texto):
    stop_words = nltk.corpus.stopwords.words('portuguese')
    if isinstance(texto, str):
        texto = normalizar_texto(texto)
        doc = nlp(texto)
        tokens = [
            token.lemma_
            for token in doc
            if token.lemma_ not in stop_words and not token.is_punct
        ]
        return ' '.join(tokens)
    else:
        return None

# -----------------------------
# Função de recomendação
# -----------------------------
def recomendar_vagas(cv_candidato, df_vagas, model, embeddings_vagas, limiar=0.7):
    """
    Recebe o currículo do candidato (cv_candidato), calcula similaridade com vagas
    e retorna as vagas com aderência acima do limiar.
    """
    cv_processado = tokenizar(cv_candidato)
    embedding_candidato = model.encode(cv_processado, convert_to_tensor=True)

    cosine_scores = util.cos_sim(embedding_candidato, embeddings_vagas)[0].cpu().numpy()
    idx_filtrados = np.where(cosine_scores >= limiar)[0]

    df_result = df_vagas.iloc[idx_filtrados].copy()
    df_result['similaridade'] = cosine_scores[idx_filtrados]
    df_result = df_result.sort_values(by='similaridade', ascending=False)

    return df_result[['titulo_vaga', 'nivel profissional', 'nivel_academico', 'nivel_ingles', 'areas_atuacao', 'cliente', 'analista_responsavel', 'tipo_contratacao', 'cidade', 'vaga_especifica_para_pcd', 'similaridade']]

# -----------------------------
# Carregar modelo e dados
# -----------------------------
@st.cache_resource
def carregar_modelo():
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

@st.cache_data
def carregar_dados():
    df_vagas = pd.read_csv("../src/vagas_curriculo.csv")
    with open("../src/embeddings_vagas.pkl", "rb") as f:
        embeddings_vagas = pickle.load(f)
    return df_vagas, embeddings_vagas

model = carregar_modelo()
df_vagas, embeddings_vagas = carregar_dados()

# -----------------------------
# Interface Streamlit
# -----------------------------
st.title("🔎 Recomendador de Vagas")
st.write("Suba seu currículo e veja as vagas mais compatíveis!")

# Formulário para dados do usuário
with st.form("formulario"):
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    cv_input = st.text_area("Cole seu currículo aqui", height=200)
    limiar = st.slider("Nível mínimo de similaridade", 0.0, 1.0, 0.5, 0.05)
    submitted = st.form_submit_button("🔍 Encontrar Vagas")

if submitted:
    if cv_input.strip():
        resultado = recomendar_vagas(cv_input, df_vagas, model, embeddings_vagas, limiar)
        if not resultado.empty:
            st.success(f"Vagas encontradas para {nome} ({email}):")
            st.dataframe(resultado.head(20), use_container_width=True)
        else:
            st.warning("Nenhuma vaga encontrada acima do limiar definido.")
    else:
        st.error("Por favor, insira o conteúdo do seu currículo.")

st.subheader("Exemplo de Currículo")
with open("curriculo_teste.pdf", "rb") as f:
    pdf_bytes = f.read()

st.download_button(
    label="Baixar currículo de exemplo",
    data=pdf_bytes,
    file_name="curriculo_exemplo.pdf",
    mime="application/pdf"
)
