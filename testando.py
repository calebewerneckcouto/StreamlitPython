import pandas as pd
import streamlit as st

# Título da página
st.title('Exibição de Dados - Relatório')

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Carregar os dados do arquivo enviado
    dados = pd.read_csv(uploaded_file, delimiter=";")

    # Substituir NaN por valores adequados
    for coluna in dados.columns:
        if dados[coluna].dtype == 'object':  # Coluna de texto
            dados[coluna].fillna("", inplace=True)
        else:  # Coluna numérica
            dados[coluna].fillna(0, inplace=True)

    # Filtro por Descrição
    descricao = st.selectbox('Escolha a Descrição', dados['Descrição'].dropna().unique())

    # Filtrar os nomes com base na descrição selecionada
    nomes_correspondentes = dados[dados['Descrição'] == descricao]['Nome'].unique()

    # Filtrar o DataFrame apenas pelos nomes encontrados (independente da descrição)
    dados_filtrados = dados[dados['Nome'].isin(nomes_correspondentes)]

    # Contar quantas vezes cada nome aparece no dataset
    contagem_nomes = dados_filtrados['Nome'].value_counts().reset_index()
    contagem_nomes.columns = ['Nome', 'Quantidade']
    
    # Exibir os dados filtrados
    st.write(f"Exibindo todos os registros dos nomes associados à descrição **{descricao}**:")
    st.dataframe(dados_filtrados)

    

else:
    st.write("Por favor, faça o upload de um arquivo CSV.")
