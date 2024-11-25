import streamlit as st
import json

# Função para carregar usuários
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar usuários
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Função para verificar login
def authenticate(username, password, users):
    return username in users and users[username] == password

# Página inicial
def main():
    st.title("Login ou Cadastro")
    users = load_users()

    # Inicializa o estado de autenticação
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None

    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.rerun()

    if st.session_state["authenticated"]:
        st.success(f"Bem-vindo, {st.session_state['username']}!")
        st.sidebar.success("Use o MENU lateral para acessar as funcionalidades.")
        return

   

    choice = st.radio("Selecione uma opção", ["Login", "Cadastro"])

    if choice == "Cadastro":
        st.subheader("Cadastrar Novo Usuário")
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Cadastrar"):
            if username in users:
                st.error("Usuário já existe!")
            else:
                users[username] = password
                save_users(users)
                st.success("Usuário cadastrado com sucesso!")

    elif choice == "Login":
        st.subheader("Fazer Login")
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if authenticate(username, password, users):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

if __name__ == "__main__":
    main()
