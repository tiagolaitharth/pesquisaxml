import os
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st
import io

def carregar_arquivos():
    # Selecione os arquivos XML via upload no Streamlit
    arquivos_xml = st.file_uploader("Carregue os arquivos XML", type=["xml"], accept_multiple_files=True)

    if not arquivos_xml:
        st.warning("Por favor, faça o upload dos arquivos XML.")
        return None

    return arquivos_xml

def buscar_nfs_por_pedido(arquivos_xml, pedidos):
    nfs = []
    
    # Percorre cada arquivo XML carregado
    for arquivo in arquivos_xml:
        try:
            tree = ET.parse(arquivo)
            root = tree.getroot()
            
            # Extrair informações necessárias
            nf = root.find(".//NFe/infNFe/ide/nNF").text  # Número da NF
            pedido = root.find(".//NFe/infNFe/ide/nPedido").text  # Número do Pedido
            transportadora = root.find(".//NFe/infNFe/transp/xNome").text  # Nome da Transportadora
            volumes = int(root.find(".//NFe/infNFe/transp/vol/quantidade").text)  # Volume

            # Verifica se o número do pedido corresponde ao que foi buscado
            if pedido in pedidos:
                nfs.append({
                    "NF": nf,
                    "Pedido": pedido,
                    "Transportadora": transportadora,
                    "Volumes": volumes
                })
        except Exception as e:
            st.warning(f"Erro ao processar o arquivo {arquivo.name}: {e}")
    
    return nfs

def exibir_tabela(nfs):
    if nfs:
        df = pd.DataFrame(nfs)

        # Calcula o total de volumes e de NFs
        total_volumes = df["Volumes"].sum()
        total_nfs = df.shape[0]

        # Exibe a tabela e os totais
        st.write(df)
        st.write(f"**Total de Volumes**: {total_volumes}")
        st.write(f"**Total de NFs**: {total_nfs}")

        # Botão para download da tabela em CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Baixar Tabela em CSV",
            data=csv,
            file_name="tabela_nfs.csv",
            mime="text/csv"
        )
    else:
        st.write("Nenhuma NF encontrada para os pedidos informados.")

def main():
    # Cabeçalho
    st.title("Buscador de NFs por Pedido")

    # Seleção de pedidos a serem buscados
    pedidos_input = st.text_input("Digite os números dos pedidos separados por espaço:")
    
    if pedidos_input:
        pedidos = pedidos_input.split()
        
        # Carregar arquivos XML via upload
        arquivos_xml = carregar_arquivos()

        if arquivos_xml is not None:
            # Buscar NFs pelos pedidos fornecidos
            nfs = buscar_nfs_por_pedido(arquivos_xml, pedidos)
            
            # Exibir os resultados
            exibir_tabela(nfs)

if __name__ == "__main__":
    main()
