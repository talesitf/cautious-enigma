import streamlit as st

# Verifica se o usuário está autenticado
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Você precisa fazer login para acessar esta página.")
    st.stop()

# Página de chat
st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Exibir mensagens antigas
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.text_area("Você", message["text"], key=message["id"], height=40)
    else:
        st.text_area("Bot", message["text"], key=message["id"], height=40)

# Entrada do usuário
user_input = st.text_input("Digite sua mensagem:")
if st.button("Enviar"):
    if user_input:
        st.session_state["messages"].append({"role": "user", "text": user_input, "id": len(st.session_state["messages"])})
        # Resposta fictícia do bot
        bot_response = f"Você disse: {user_input}"
        st.session_state["messages"].append({"role": "bot", "text": bot_response, "id": len(st.session_state["messages"]) + 1})
        st.rerun()
