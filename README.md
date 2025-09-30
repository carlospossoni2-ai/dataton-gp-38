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
1. Ative seu ambiente virtual (opcional, mas recomendado)
   - Windows: venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate

2. Instale as dependências do projeto
   pip install -r requirements.txt
   (ou instale apenas o Streamlit com: pip install streamlit)

3. (Opcional) Execute o script de setup automático
   ./setup.sh
   Esse script atualiza o pip, instala as dependências e já roda o app.

4. Caso não use o setup.sh, execute manualmente o aplicativo
   streamlit run app.py
   (ou streamlit run app/app.py se estiver em uma pasta app/)

5. Abra no navegador o endereço exibido no terminal (ex: http://localhost:8501)

6. Para encerrar a aplicação, pressione CTRL + C no terminal.
    
## Preparação dos Dados
Antes de treinar o modelo, os dados das vagas devem ser processados para criar um "currículo da vaga".  
Isso é feito pela função `criar_curriculo_vaga(df_vagas)` que:
- Combina informações de nível profissional, acadêmico, idiomas, áreas de atuação e competências;
- Tokeniza e organiza os dados em um formato pronto para análise de texto;
- Adiciona uma coluna `cv_vaga` ao DataFrame.

Exemplo de uso:
```python
from src.utils import criar_curriculo_vaga
df_vagas_curriculo = criar_curriculo_vaga(df_vagas_filtradas)
```

---

## Treinamento do Modelo
O modelo é treinado utilizando Sentence-BERT (`sentence-transformers`) para gerar embeddings semânticos das vagas.

Exemplo:
```python
from src.train_model import treinar_recomendador, set_seed

# Define seed para reprodutibilidade
SEED = 42
set_seed(SEED)

# Treina o modelo
model, embeddings_vagas = treinar_recomendador(df_vagas_curriculo, modelo_name="all-MiniLM-L6-v2", seed=SEED)
```

---

## Avaliação da Aderência
Para recomendar vagas a um candidato, utilize a função `recomendar_vagas`:
```python
from src.recommend import recomendar_vagas

df_result = recomendar_vagas(
    cv_candidato="Descrição completa do currículo do candidato",
    df_vagas=df_vagas_curriculo,
    model=model,
    embeddings_vagas=embeddings_vagas,
    limiar=0.7
)
```
O retorno é um DataFrame com:
- `id_vaga`
- `titulo_vaga`
- `similaridade` (pontuação de aderência)

---

## Como Treinar Novamente
1. Prepare os dados das vagas e candidatos.
2. Execute `criar_curriculo_vaga()` para gerar a coluna `cv_vaga`.
3. Execute `treinar_recomendador()` para gerar embeddings atualizados.
4. Salve o modelo com `joblib`:
```python
import joblib
joblib.dump(model, 'models/modelo_recomendador.pkl')
```

---

## Observações
- O modelo atual utiliza embeddings do Sentence-BERT, mas você pode experimentar outros modelos da biblioteca `sentence-transformers`.
- Para melhorar a precisão, recomenda-se usar dados atualizados e limpar possíveis inconsistências nos campos de vagas e currículos.
- O limite de similaridade (`limiar`) pode ser ajustado conforme a necessidade do RH.
