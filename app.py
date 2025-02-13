import pandas as pd
import streamlit as st

# Título da página
st.title('Exibição de Dados - Relatório')

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Carregar os dados do arquivo enviado
    dados = pd.read_csv(uploaded_file, delimiter=";")

    # Substituir NaN por valores adequados: "" para texto, 0 para números
    for coluna in dados.columns:
        if dados[coluna].dtype == 'object':  # Coluna de texto
            dados[coluna].fillna("", inplace=True)
        else:  # Coluna numérica
            dados[coluna].fillna(0, inplace=True)

    # Opções para habilitar ou desabilitar os filtros
    filtro_municipio = st.checkbox('Filtrar por Município', value=True)
    filtro_descricao = st.checkbox('Filtrar por Descrição', value=True)
    filtro_equipamento = st.checkbox('Filtrar por Equipamento', value=True)
    filtro_numero = st.checkbox('Filtrar por Número', value=True)
    filtro_nome_pessoa = st.checkbox('Nome', value=True)
    filtro_nome = st.checkbox('Filtrar por Nome', value=True)
    filtro_data = st.checkbox('Filtrar por Data', value=True)
    filtro_situacao = st.checkbox('Filtrar por Situação', value=True)
    filtro_garantia = st.checkbox('Filtrar por Garantia', value=True)
    filtro_problema = st.checkbox('Filtrar por Problema', value=True)
    filtro_observacoes_recebimento = st.checkbox('Filtrar por Observações do recebimento', value=True)
    filtro_tecnico = st.checkbox('Filtrar por Técnico', value=True)
    filtro_observacoes_servico = st.checkbox('Filtrar por Observações do serviço', value=True)
    filtro_observacoes_internas = st.checkbox('Filtrar por Observações internas', value=True)
    filtro_data_conclusao = st.checkbox('Filtrar por Data de conclusão', value=True)
    filtro_data_saida = st.checkbox('Filtrar por Data de Saída', value=True)
    filtro_nome_vendedor = st.checkbox('Filtrar por Nome - Vendedor', value=True)
    filtro_categoria = st.checkbox('Filtrar por Descrição - Categoria', value=True)
    filtro_forma_pagamento = st.checkbox('Filtrar por Descrição - Forma de pagamento', value=True)

    # Opção para remover colunas
    colunas_disponiveis = dados.columns.tolist()
    colunas_a_remover = st.multiselect('Escolha as colunas a remover', colunas_disponiveis)

    # Remover as colunas selecionadas
    if colunas_a_remover:
        dados.drop(columns=colunas_a_remover, inplace=True)
        st.write("Colunas removidas com sucesso!")

    # Filtros para exibir os dados, com base nas opções ativadas
    municipio = descricao = equipamento = numero = nome = data = situacao = garantia = problema = observacoes_recebimento = tecnico = observacoes_servico = observacoes_internas = data_conclusao = data_saida = nome_vendedor = categoria = forma_pagamento = None

    if filtro_municipio:
        municipio = st.selectbox('Escolha o município', dados['Município'].dropna().unique())
    if filtro_descricao:
        descricao = st.selectbox('Escolha a descrição', dados['Descrição'].dropna().unique())
        nomes_correspondentes = dados[(dados['Descrição'] == descricao) & (dados['Município'] == municipio)]['Nome'].unique()

        # Filtrar o DataFrame apenas pelos nomes encontrados (independente da descrição)
        dados = dados[dados['Nome'].isin(nomes_correspondentes)]
        

    if filtro_equipamento:
        equipamento = st.selectbox('Escolha o Equipamento', dados['Equipamento'].dropna().unique())
    if filtro_numero:
        numero = st.selectbox('Escolha o Número', dados['Número - Nota Fiscal'].dropna().unique())
    if filtro_nome_pessoa:
        nomePessoa = st.selectbox('Escolha o Nome', dados['Nome'].dropna().unique())
    if filtro_nome:
        nome = st.selectbox('Escolha o Nome', dados['Nome - Vendedor'].dropna().unique())    
    if filtro_data:
        data = st.selectbox('Escolha a Data', dados['Data'].dropna().unique())
    if filtro_situacao:
        situacao = st.selectbox('Escolha a Situação', dados['Situação'].dropna().unique())
    if filtro_garantia:
        garantia = st.selectbox('Escolha a Garantia', dados['Garantia'].dropna().unique())
    if filtro_problema:
        problema = st.selectbox('Escolha o Problema', dados['Problema'].dropna().unique())
    if filtro_observacoes_recebimento:
        observacoes_recebimento = st.selectbox('Escolha as Observações do recebimento', dados['Observações do recebimento'].dropna().unique())
    if filtro_tecnico:
        tecnico = st.selectbox('Escolha o Técnico', dados['Técnico'].dropna().unique())
    if filtro_observacoes_servico:
        observacoes_servico = st.selectbox('Escolha as Observações do serviço', dados['Observações do serviço'].dropna().unique())
    if filtro_observacoes_internas:
        observacoes_internas = st.selectbox('Escolha as Observações internas', dados['Observações internas'].dropna().unique())
    if filtro_data_conclusao:
        data_conclusao = st.selectbox('Escolha a Data de Conclusão', dados['Data de conclusão'].dropna().unique())
    if filtro_data_saida:
        data_saida = st.selectbox('Escolha a Data de Saída', dados['Data de Saída'].dropna().unique())
    if filtro_nome_vendedor:
        nome_vendedor = st.selectbox('Escolha o Nome - Vendedor', dados['Nome - Vendedor'].dropna().unique())
    if filtro_categoria:
        categoria = st.selectbox('Escolha a Descrição - Categoria', dados['Descrição - Categoria'].dropna().unique())
    if filtro_forma_pagamento:
        forma_pagamento = st.selectbox('Escolha a Descrição - Forma de pagamento', dados['Descrição - Forma de pagamento'].dropna().unique())

    # Filtrar os dados conforme a escolha
    filtro = dados.copy()

    if filtro_municipio:
        filtro = filtro[filtro["Município"] == municipio]
    if filtro_descricao:
        filtro = filtro[filtro["Descrição"] == descricao]
    if filtro_equipamento:
        filtro = filtro[filtro["Equipamento"] == equipamento]
    if filtro_numero:
        filtro = filtro[filtro["Número - Nota Fiscal"] == numero]
    if filtro_nome_pessoa:
        filtro = filtro[filtro["Nome"] == nomePessoa]    
    if filtro_nome:
        filtro = filtro[filtro["Nome - Vendedor"] == nome]
    if filtro_data:
        filtro = filtro[filtro["Data"] == data]
    if filtro_situacao:
        filtro = filtro[filtro["Situação"] == situacao]
    if filtro_garantia:
        filtro = filtro[filtro["Garantia"] == garantia]
    if filtro_problema:
        filtro = filtro[filtro["Problema"] == problema]
    if filtro_observacoes_recebimento:
        filtro = filtro[filtro["Observações do recebimento"] == observacoes_recebimento]
    if filtro_tecnico:
        filtro = filtro[filtro["Técnico"] == tecnico]
    if filtro_observacoes_servico:
        filtro = filtro[filtro["Observações do serviço"] == observacoes_servico]
    if filtro_observacoes_internas:
        filtro = filtro[filtro["Observações internas"] == observacoes_internas]
    if filtro_data_conclusao:
        filtro = filtro[filtro["Data de conclusão"] == data_conclusao]
    if filtro_data_saida:
        filtro = filtro[filtro["Data de Saída"] == data_saida]
    if filtro_nome_vendedor:
        filtro = filtro[filtro["Nome - Vendedor"] == nome_vendedor]
    if filtro_categoria:
        filtro = filtro[filtro["Descrição - Categoria"] == categoria]
    if filtro_forma_pagamento:
        filtro = filtro[filtro["Descrição - Forma de pagamento"] == forma_pagamento]

    # Exibir os dados filtrados
    if filtro_descricao: 
        st.dataframe(dados)  # Exibe os dados filtrados de forma interativa
        
    else:
        st.dataframe(filtro)  # Exibe os dados filtrados de forma interativa

    # Colunas de interesse para cálculo de totais
    colunas_interesse = [
        "Total das peças", "Total de serviços", "Preço total", 
        "Quantidade/Horas", "Lucro", "Preço de custo"
    ]

    # Função para limpar e converter valores monetários
    def limpar_valor(valor):
        if isinstance(valor, str):
            valor = valor.replace('.', '').replace(',', '.')  # Remove pontos e troca vírgula por ponto
            return pd.to_numeric(valor, errors='coerce')
        return valor

    # Calcular e exibir os totais das colunas de interesse
    if filtro_descricao:  # Quando o filtro for por descrição    
        for coluna in colunas_interesse:
            if coluna in filtro.columns:
                dados[coluna] = dados[coluna].apply(limpar_valor)
                total_coluna = dados[coluna].sum()
                st.write(f"**Total de {coluna}:** R$ {total_coluna:,.2f}")
    else:   
        for coluna in colunas_interesse:
            if coluna in filtro.columns:
                filtro[coluna] = filtro[coluna].apply(limpar_valor)  # Aplicar a limpeza dos valores
                total_coluna = filtro[coluna].sum()  # Calcular o total para as demais consultas
                st.write(f"**Total de {coluna}:** R$ {total_coluna:,.2f}")
            else:
                st.write(f"**Total de {coluna}:** R$ 0.00")
