import streamlit as st
import os
import time

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

embedding_size = 3072
embedding_model = 'text-embedding-3-large'
embeddings = OpenAIEmbeddings(model=embedding_model)

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = "text-embeddings"

pc = Pinecone(api_key=pinecone_api_key)

index_name = "test-index"  # change if desired

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

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
