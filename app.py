import boto3
import streamlit as st
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# DynamoDB Table Name
DYNAMODB_TABLE = "test_streamlit_table"

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")  # Change the region if needed
table = dynamodb.Table(DYNAMODB_TABLE)

# Function to add a user to DynamoDB
def add_user_to_dynamodb(username, password):
    try:
        table.put_item(
            Item={
                "id": username,
                "password": password,
            }
        )
        return True
    except (NoCredentialsError, PartialCredentialsError):
        st.error("Unable to connect to DynamoDB. Check IAM permissions.")
        return False

# Function to authenticate user from DynamoDB
def authenticate_user_from_dynamodb(username, password):
    try:
        response = table.get_item(Key={"id": username})
        user = response.get("Item")
        if user and user["password"] == password:
            return True
        return False
    except (NoCredentialsError, PartialCredentialsError):
        st.error("Unable to connect to DynamoDB. Check IAM permissions.")
        return False

# Function for restricted access
def restricted_functionality():
    st.subheader("Restricted Access")
    st.write("You are now accessing a restricted feature because you are logged in.")

# Streamlit app for login and signup
def main():
    st.title("Login or Signup with DynamoDB")

    # Initialize session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None

    # If logged in, show logout button and restricted functionality
    if st.session_state["authenticated"]:
        st.sidebar.button("Logout", on_click=lambda: logout())
        st.success(f"Welcome {st.session_state['username']}!")
        restricted_functionality()
        return

    # Authentication form
    choice = st.radio("Select an option", ["Login", "Signup"])

    if choice == "Signup":
        st.subheader("Create a New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if add_user_to_dynamodb(username, password):
                st.success("User created successfully!")
            else:
                st.error("Failed to create user.")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user_from_dynamodb(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

# Function to handle logout
def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()

if __name__ == "__main__":
    main()
