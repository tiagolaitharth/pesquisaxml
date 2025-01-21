import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import os

# Função para buscar os dados de cada XML
def buscar_dados_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    numero_pedido = root.find('.//infAdic/infCpl').text if root.find('.//infAdic/infCpl') is not None else 'N/A'
    numero_nf = root.find('.//cobr/fat/nFat').text if root.find('.//cobr/fat/nFat') is not None else 'N/A'
    volumes = root.find('.//vol/qVol').text if root.find('.//vol/qVol') is not None else 'N/A'
    transportadora = root.find('.//transp/xNome').text if root.find('.//transp/xNome') is not None else 'N/A'

    return {
        'numero_pedido': numero_pedido,
        'numero_nf': numero_nf,
        'volumes': volumes,
        'transportadora': transportadora
    }

# Função para exibir os resultados
def exibir_resultados(resultados):
    for resultado in resultados:
        st.write(f"**Número do Pedido:** {resultado['numero_pedido']}")
        st.write(f"**Número da NF:** {resultado['numero_nf']}")
        st.write(f"**Volumes:** {resultado['volumes']}")
        st.write(f"**Transportadora:** {resultado['transportadora']}")
        st.write("---")

# Função para salvar os resultados em CSV
def salvar_em_csv(dados):
    df = pd.DataFrame(dados)
    df.to_csv('resultados.csv', index=False)

# Função principal para execução do Streamlit
def main():
    st.title("Leitor de Arquivos XML")

    # Opção para o usuário fazer upload dos arquivos XML
    uploaded_files = st.file_uploader("Selecione os arquivos XML", type="xml", accept_multiple_files=True)

    if uploaded_files:
        resultados = []

        # Processando cada arquivo XML
        for uploaded_file in uploaded_files:
            dados = buscar_dados_xml(uploaded_file)
            resultados.append(dados)

        if resultados:
            exibir_resultados(resultados)

            # Botão para salvar os resultados em CSV
            if st.button("Salvar em CSV"):
                salvar_em_csv(resultados)
                st.success("Resultados salvos em 'resultados.csv'.")
        else:
            st.warning("Nenhum arquivo XML carregado ou os dados não puderam ser extraídos.")
    else:
        st.info("Selecione arquivos XML para iniciar o processo.")

if __name__ == "__main__":
    main()
