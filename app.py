import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Sistema de Análise de OS",
    page_icon="📊",
    layout="wide"
)

# Título da página
st.title('📊 Exibição de Dados - Relatório')

ordem_colunas = [
    "Número", "Nome", "Data", "Descrição", "Total das peças", "Preço total", 
    "Preço de custo", "Total de serviços", "Lucro", "Equipamento", "Município", 
    "Técnico", "Nome - Vendedor", "Situação"
]

# Função para limpar e converter valores monetários
def limpar_valor(valor):
    if pd.isna(valor):
        return 0.0
    if isinstance(valor, str):
        valor = valor.replace('.', '').replace(',', '.')
        try:
            return float(valor)
        except:
            return 0.0
    return float(valor)

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("📁 Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Carregar os dados do arquivo enviado
    dados = pd.read_csv(uploaded_file, delimiter=";", dtype={'Número': str})
    
    # Ajustar a ordem das colunas
    colunas_presentes = [col for col in ordem_colunas if col in dados.columns]
    dados = dados[colunas_presentes]

    # Substituir NaN por valores adequados: "" para texto, 0 para números
    for coluna in dados.columns:
        if dados[coluna].dtype == 'object':  # Coluna de texto
            dados[coluna].fillna("", inplace=True)
        else:  # Coluna numérica
            dados[coluna].fillna(0, inplace=True)

    # Criar abas
    tab1, tab2, tab3 = st.tabs(["🔍 Filtros", "📊 Visualização", "💰 Totais"])

    with tab1:
        st.header("Configuração de Filtros")
        
        # Opções para habilitar ou desabilitar os filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_municipio = st.checkbox('Filtrar por Município', value=False)
            filtro_descricao = st.checkbox('Filtrar por Descrição', value=False)
            filtro_equipamento = st.checkbox('Filtrar por Equipamento', value=False)
            filtro_numero = st.checkbox('Filtrar por Número', value=False)
            
        with col2:
            filtro_nome_pessoa = st.checkbox('Filtrar por Nome Cliente', value=False)
            filtro_nome = st.checkbox('Filtrar por Nome Vendedor', value=False)
            filtro_data = st.checkbox('Filtrar por Data', value=False)
            filtro_situacao = st.checkbox('Filtrar por Situação', value=False)
            
        with col3:
            filtro_tecnico = st.checkbox('Filtrar por Técnico', value=False)
            filtro_garantia = st.checkbox('Filtrar por Garantia', value=False)
            filtro_problema = st.checkbox('Filtrar por Problema', value=False)

        # Filtros para exibir os dados, com base nas opções ativadas
        municipio = descricao = equipamento = numero = nome = data = situacao = garantia = problema = tecnico = None

        if filtro_municipio:
            municipio = st.selectbox('Escolha o município', dados['Município'].dropna().unique())
        
        if filtro_descricao:
            opcoes_descricao = ['Verificação de Equipamento', 'Manutencao FDM', 'Manutencao SLA', 
                               'Treinamento HH', 'Impressão de Peças FDM', 'Impressão de Peças SLA',
                               'Garantia', 'Entrega Técnica', 'Manutenção Interna']
            
            # Filtrar as opções que existem no DataFrame
            opcoes_validas = [opcao for opcao in opcoes_descricao if opcao in dados['Descrição'].dropna().unique()]
            
            # Exibir o selectbox com as opções válidas
            descricao = st.selectbox('Escolha a descrição', opcoes_validas)
            
            if filtro_municipio and municipio:
                # Filtrar os dados com base na descrição e município
                numeros_correspondentes = dados[
                    (dados['Descrição'] == descricao) & 
                    (dados['Município'] == municipio)
                ]['Número'].unique()
                
                # Filtrar o DataFrame apenas pelos números encontrados (MANTÉM TODOS OS REGISTROS COM MESMO NÚMERO)
                dados_filtrados_descricao = dados[dados['Número'].isin(numeros_correspondentes)].copy()
                
                st.info(f"Encontrados {len(numeros_correspondentes)} números de OS para '{descricao}' em {municipio}")
            else:
                dados_filtrados_descricao = dados[dados['Descrição'] == descricao].copy()
                st.info(f"Filtrando por descrição: {descricao}")

        if filtro_equipamento:
            equipamento = st.selectbox('Escolha o Equipamento', dados['Equipamento'].dropna().unique())
        
        if filtro_numero:
            numero = st.selectbox('Escolha o Número', dados['Número'].dropna().unique())
        
        if filtro_nome_pessoa:
            nomePessoa = st.selectbox('Escolha o Nome do Cliente', dados['Nome'].dropna().unique())
        
        if filtro_nome:
            nome = st.selectbox('Escolha o Nome do Vendedor', dados['Nome - Vendedor'].dropna().unique())
        
        if filtro_data:
            data = st.selectbox('Escolha a Data', dados['Data'].dropna().unique())
        
        if filtro_situacao:
            situacao = st.selectbox('Escolha a Situação', dados['Situação'].dropna().unique())
        
        if filtro_garantia:
            garantia = st.selectbox('Escolha a Garantia', dados['Garantia'].dropna().unique())
        
        if filtro_problema:
            problema = st.selectbox('Escolha o Problema', dados['Problema'].dropna().unique())
        
        if filtro_tecnico:
            tecnico = st.selectbox('Escolha o Técnico', dados['Técnico'].dropna().unique())

        # Opção para remover colunas
        st.subheader("Configuração de Colunas")
        colunas_disponiveis = dados.columns.tolist()
        colunas_a_remover = st.multiselect('Escolha as colunas a remover', colunas_disponiveis)

    with tab2:
        st.header("Visualização de Dados")
        
        # Aplicar remoção de colunas
        dados_visualizacao = dados.copy()
        if colunas_a_remover:
            dados_visualizacao = dados_visualizacao.drop(columns=colunas_a_remover)
            st.success(f"Colunas removidas: {', '.join(colunas_a_remover)}")

        # Filtrar os dados conforme a escolha (MANTENDO A LÓGICA ORIGINAL)
        filtro = dados_visualizacao.copy()

        if filtro_municipio and municipio:
            filtro = filtro[filtro["Município"] == municipio]
        
        if filtro_descricao and descricao:
            if filtro_municipio and municipio:
                # Usar o filtro já preparado que mantém todos os registros com mesmo número
                filtro = dados_visualizacao[dados_visualizacao['Número'].isin(numeros_correspondentes)]
            else:
                filtro = filtro[filtro["Descrição"] == descricao]
        
        if filtro_equipamento and equipamento:
            filtro = filtro[filtro["Equipamento"] == equipamento]
        
        if filtro_numero and numero:
            filtro = filtro[filtro["Número"] == numero]
        
        if filtro_nome_pessoa and nomePessoa:
            filtro = filtro[filtro["Nome"] == nomePessoa]
        
        if filtro_nome and nome:
            filtro = filtro[filtro["Nome - Vendedor"] == nome]
        
        if filtro_data and data:
            filtro = filtro[filtro["Data"] == data]
        
        if filtro_situacao and situacao:
            filtro = filtro[filtro["Situação"] == situacao]
        
        if filtro_garantia and garantia:
            filtro = filtro[filtro["Garantia"] == garantia]
        
        if filtro_problema and problema:
            filtro = filtro[filtro["Problema"] == problema]
        
        if filtro_tecnico and tecnico:
            filtro = filtro[filtro["Técnico"] == tecnico]

        # Exibir os dados filtrados - SEMPRE AGRUPANDO POR NÚMERO
        st.subheader("Dados Agrupados por Número de OS")
        
        # Ordenar por número para facilitar visualização
        filtro_ordenado = filtro.sort_values('Número')
        
        # Mostrar estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de OS", filtro_ordenado['Número'].nunique())
        with col2:
            st.metric("Total de Registros", len(filtro_ordenado))
        with col3:
            if 'Município' in filtro_ordenado.columns:
                st.metric("Municípios", filtro_ordenado['Município'].nunique())

        st.dataframe(filtro_ordenado, use_container_width=True)

    with tab3:
        st.header("Cálculo de Totais")
        
        # Colunas de interesse para cálculo de totais
        colunas_interesse = [
            "Total das peças", "Total de serviços", "Preço total", 
            "Quantidade/Horas", "Lucro", "Preço de custo"
        ]
        
        # Usar os dados já filtrados da aba 2
        dados_totais = filtro_ordenado.copy()
        
        st.subheader("Totais Financeiros")
        
        # Calcular totais
        totais = {}
        for coluna in colunas_interesse:
            if coluna in dados_totais.columns:
                dados_totais[coluna] = dados_totais[coluna].apply(limpar_valor)
                total_coluna = dados_totais[coluna].sum()
                totais[coluna] = total_coluna
        
        # Exibir totais em colunas
        col1, col2 = st.columns(2)
        
        with col1:
            for i, (coluna, total) in enumerate(totais.items()):
                if i % 2 == 0:
                    if coluna == "Quantidade/Horas":
                        st.metric(f"Total de {coluna}", f"{total:,.2f}")
                    else:
                        st.metric(f"Total de {coluna}", f"R$ {total:,.2f}")
        
        with col2:
            for i, (coluna, total) in enumerate(totais.items()):
                if i % 2 == 1:
                    if coluna == "Quantidade/Horas":
                        st.metric(f"Total de {coluna}", f"{total:,.2f}")
                    else:
                        st.metric(f"Total de {coluna}", f"R$ {total:,.2f}")
        
        # Análise adicional se houver Preço total e Preço de custo
        if 'Preço total' in totais and 'Preço de custo' in totais:
            st.subheader("Análise de Rentabilidade")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                lucro_bruto = totais['Preço total'] - totais['Preço de custo']
                st.metric("Lucro Bruto", f"R$ {lucro_bruto:,.2f}")
            
            with col2:
                if totais['Preço total'] > 0:
                    margem = (lucro_bruto / totais['Preço total']) * 100
                    st.metric("Margem (%)", f"{margem:.1f}%")
            
            with col3:
                if totais['Preço de custo'] > 0:
                    markup = (lucro_bruto / totais['Preço de custo']) * 100
                    st.metric("Markup (%)", f"{markup:.1f}%")

        # Mostrar totais por número de OS
        st.subheader("Totais por Número de OS")
        if 'Número' in dados_totais.columns and 'Preço total' in dados_totais.columns:
            totais_por_os = dados_totais.groupby('Número').agg({
                'Preço total': 'sum',
                'Total das peças': 'sum',
                'Total de serviços': 'sum'
            }).round(2)
            
            totais_por_os.columns = ['Total Geral', 'Total Peças', 'Total Serviços']
            st.dataframe(totais_por_os.sort_values('Total Geral', ascending=False))

else:
    st.info("👆 Faça upload de um arquivo CSV para começar a análise")

# Rodapé
st.markdown("---")
st.markdown("Sistema de Análise de Ordens de Serviço")