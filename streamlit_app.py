import streamlit as st

# Set page config
st.set_page_config(
    page_title="Mon Projet PFA",
    page_icon="📚",
    layout="wide"
)

# Main title
st.title("Mon Projet PFA")

# Welcome message
st.write("Bienvenue dans l'application Streamlit de mon projet.")

# Add a simple sidebar
with st.sidebar:
    st.header("Navigation")
    st.write("Welcome to the sidebar!")
