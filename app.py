import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET

# Função para processar o XML e extrair as informações
def processar_xml(uploaded_file):
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    # Extração dos dados
    nf_numero = root.find(".//nfeProc//infNFe//ide//nNF").text if root.find(".//nfeProc//infNFe//ide//nNF") else "N/A"
    transportadora = root.find(".//nfeProc//infNFe//emit//xNome").text if root.find(".//nfeProc//infNFe//emit//xNome") else "N/A"
    numero_pedido = root.find(".//nfeProc//infNFe//complemento").text if root.find(".//nfeProc//infNFe//complemento") else "N/A"
    volumes = root.find(".//nfeProc//infNFe//transp//vol//qVol").text if root.find(".//nfeProc//infNFe//transp//vol//qVol") else "0"
    
    return nf_numero, transportadora, numero_pedido, volumes

# Título da aplicação
st.title("Busca de Informações de NFs e Pedidos")

# Carregar arquivos via upload
uploaded_files = st.file_uploader("Escolha os arquivos XML", accept_multiple_files=True, type=["xml"])

# Verificar se os arquivos foram carregados
if uploaded_files:
    # Listas para armazenar as informações
    nfs = []
    transportadoras = []
    pedidos = []
    volumes = []

    # Processar os arquivos XML carregados
    for uploaded_file in uploaded_files:
        nf_numero, transportadora, numero_pedido, volume = processar_xml(uploaded_file)
        nfs.append(nf_numero)
        transportadoras.append(transportadora)
        pedidos.append(numero_pedido)
        volumes.append(volume)

    # Criar um DataFrame para exibir as informações
    data = {
        "Número da NF": nfs,
        "Transportadora": transportadoras,
        "Número do Pedido": pedidos,
        "Volume": volumes
    }

    df = pd.DataFrame(data)

    # Exibir a tabela
    st.subheader("Informações das Notas Fiscais")
    st.dataframe(df)

    # Botão para download da tabela em CSV
    st.download_button(
        label="Baixar Tabela em CSV",
        data=df.to_csv(index=False),
        file_name="notas_fiscais.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor, carregue os arquivos XML para análise.")
