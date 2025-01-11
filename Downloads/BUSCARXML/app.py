import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

# Função para extrair dados do XML
def parse_xml(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        
        nf_data = {
            "Numero NF": root.findtext('NotaFiscal/Numero', default='N/A'),
            "Numero Pedido": root.findtext('Pedido/Numero', default='N/A'),
            "Volumes": root.findtext('NotaFiscal/Volumes', default='N/A'),
            "Transportadora": root.findtext('Transportadora/Nome', default='N/A')
        }
        return nf_data
    except Exception as e:
        return {"Error": str(e)}

# Configuração do Streamlit
st.title("Sistema de Leitura de XML")

# Upload de arquivos XML
uploaded_files = st.file_uploader(
    "Faça o upload de arquivos XML (vários arquivos podem ser selecionados)", 
    accept_multiple_files=True, 
    type="xml"
)

# Campo para digitar o número de pedidos
pedido_input = st.text_area("Digite os números dos pedidos, separados por linha:")
pedido_list = pedido_input.split("\n") if pedido_input else []

# Botão para processar os arquivos
if st.button("Processar XMLs"):
    if not uploaded_files:
        st.warning("Por favor, faça o upload de pelo menos um arquivo XML.")
    else:
        data = []
        for file in uploaded_files:
            xml_data = parse_xml(file)
            if xml_data.get("Numero Pedido") in pedido_list or not pedido_list:
                xml_data["Arquivo"] = file.name
                data.append(xml_data)
        
        if data:
            df = pd.DataFrame(data)
            st.write("Resultados encontrados:")
            st.dataframe(df)

            # Botão para salvar os resultados em CSV
            if st.button("Salvar lista em CSV"):
                csv_file = "resultado.csv"
                df.to_csv(csv_file, index=False)
                st.success(f"Arquivo CSV salvo como: {csv_file}")
                st.download_button("Baixar CSV", data=df.to_csv(index=False), file_name=csv_file)
        else:
            st.warning("Nenhuma informação correspondente foi encontrada.")
