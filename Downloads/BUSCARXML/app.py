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
    
    # Selecione o diretório com arquivos XML
    pasta = st.text_input("Digite o caminho da pasta com arquivos XML:")
    
    if pasta and os.path.isdir(pasta):
        # Mostra os arquivos XML na pasta
        arquivos = [f for f in os.listdir(pasta) if f.endswith('.xml')]
        
        if arquivos:
            st.write(f"Arquivos XML encontrados: {', '.join(arquivos)}")
            
            # Campo para buscar pedidos ou NF
            busca = st.text_input("Digite o número do pedido ou NF para buscar:")
            
            resultados = []
            
            for arquivo in arquivos:
                if busca in arquivo:
                    xml_file = os.path.join(pasta, arquivo)
                    dados = buscar_dados_xml(xml_file)
                    resultados.append(dados)
                    
            if resultados:
                exibir_resultados(resultados)
                
                # Botão para salvar os resultados em CSV
                if st.button("Salvar em CSV"):
                    salvar_em_csv(resultados)
                    st.success("Resultados salvos em 'resultados.csv'.")
            else:
                st.warning("Nenhum arquivo encontrado com o número de pedido ou NF informado.")
        else:
            st.warning("Não há arquivos XML na pasta.")
    else:
        st.warning("Digite o caminho de uma pasta válida com arquivos XML.")

if __name__ == "__main__":
    main()
