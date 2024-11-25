import streamlit as st
import os

# Verifica se o usuário está autenticado
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Você precisa fazer login para acessar esta página.")
    st.stop()

# Configurar diretório de uploads
UPLOAD_FOLDER = "uploaded_files"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Página de upload
st.title("Upload e Listagem de Arquivos")

uploaded_file = st.file_uploader("Envie seu arquivo")

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Arquivo '{uploaded_file.name}' enviado com sucesso!")

# Listar arquivos
st.subheader("Arquivos já enviados:")
files = os.listdir(UPLOAD_FOLDER)
if files:
    for file in files:
        st.write(file)
else:
    st.write("Nenhum arquivo enviado até agora.")
