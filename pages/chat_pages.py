import streamlit as st
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

all_messages = [
        ('system', "Aqui está a questão do usuário: {user_query}"),
        ('system', "Sempre responda no idioma português"),
        ('system', "Toda vez que alguém fizer perguntas relacionadas ao Hub você deve responder em primeira pessoa no plural usando 'Somos','Fazemos”,'criamos”,'realizamos”,'executamos'."),
    ]
    
llm = ChatOpenAI(temperature=0.05, model="gpt-4o-mini-2024-07-18")


prompt = ChatPromptTemplate.from_messages(all_messages)

chain = prompt| llm | StrOutputParser()

# Verifica se o usuário está autenticado
# Página de chat
st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Exibir mensagens antigas
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.text_area("Você", message["text"])
    else:
        st.text_area("Bot", message["text"])

# Entrada do usuário
user_input = st.text_input("Digite sua mensagem:")
if st.button("Enviar"):
    if user_input:
        st.session_state["messages"].append({"role": "user", "text": user_input, "id": len(st.session_state["messages"])})
        # Resposta fictícia do bot
        bot_response = chain.invoke({'user_query':user_input})
        st.session_state["messages"].append({"role": "bot", "text": bot_response, "id": len(st.session_state["messages"]) + 1})
        st.rerun()
