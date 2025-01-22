import streamlit as st
import os
import xml.etree.ElementTree as ET
import pandas as pd

# Função para ler os arquivos XML e extrair as informações
def processar_arquivos_xml(arquivos, num_pedidos):
    dados = []
    for arquivo in arquivos:
        if arquivo.name.endswith(".xml"):
            try:
                tree = ET.parse(arquivo)
                root = tree.getroot()

                # Extraindo os dados necessários (exemplo, adapte conforme a estrutura do XML)
                for pedido in root.findall('.//det'):
                    numero_nf = pedido.find('.//nNF').text  # Ajuste para o seu XML
                    numero_pedido = pedido.find('.//nPedido').text  # Ajuste para o seu XML
                    transportadora = pedido.find('.//transportadora').text  # Ajuste para o seu XML
                    volumes = pedido.find('.//volumes').text  # Ajuste para o seu XML

                    if num_pedidos in numero_nf or num_pedidos in numero_pedido:
                        dados.append({
                            "Número da NF": numero_nf,
                            "Número do Pedido": numero_pedido,
                            "Transportadora": transportadora,
                            "Volumes": volumes,
                        })
            except ET.ParseError:
                st.error(f"Erro ao processar o arquivo {arquivo.name}")
    
    return dados

# Função para salvar a tabela como CSV
def salvar_como_csv(dados):
    df = pd.DataFrame(dados)
    csv = df.to_csv(index=False)
    return csv

# Interface do Streamlit
st.title("Busca de Informações de NFs e Pedidos")
st.write("Escolha os arquivos XML.")

# Seletor de arquivos XML
arquivos = st.file_uploader("Selecione os arquivos XML", type=["xml"], accept_multiple_files=True)

# Campo de entrada para o número do pedido ou NF
num_pedidos = st.text_input("Digite os números dos pedidos ou NFs separados por espaço")

# Botão para processar os arquivos
if st.button("Buscar"):
    if not arquivos or not num_pedidos:
        st.error("Por favor, selecione os arquivos e digite os números dos pedidos ou NFs.")
    else:
        num_pedidos_lista = num_pedidos.split()
        dados = []
        for numero in num_pedidos_lista:
            dados.extend(processar_arquivos_xml(arquivos, numero))
        
        if dados:
            df = pd.DataFrame(dados)
            st.write(df)
            
            # Botão para baixar a tabela como CSV
            csv = salvar_como_csv(dados)
            st.download_button(
                label="Baixar tabela em CSV",
                data=csv,
                file_name="dados_nf_pedido.csv",
                mime="text/csv"
            )
        else:
            st.warning("Nenhum dado encontrado para os números fornecidos.")
