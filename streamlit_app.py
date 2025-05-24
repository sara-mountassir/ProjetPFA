import streamlit as st
import requests

# Django app URL configuration
DJANGO_BASE_URL = "https://gestion-candidatures.onrender.com"
DJANGO_LOGIN_PATHS = ["/login/", "/accounts/login/", "/admin/login/"]

# Function to test URL availability
def test_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

# Find working login URL
working_login_url = None
for path in DJANGO_LOGIN_PATHS:
    url = DJANGO_BASE_URL + path
    if test_url(url):
        working_login_url = url
        break

# Set page config
st.set_page_config(
    page_title="Gestion des Candidatures",
    page_icon="📚",
    layout="centered"
)

# Center the content
col1, col2, col3 = st.columns([1,2,1])
with col2:
    # Logo and title
    st.image("https://img.icons8.com/color/96/000000/student-center.png", width=96)
    st.title("Gestion des Candidatures")
    
    # Welcome message
    st.write("Bienvenue dans votre espace de gestion des candidatures")
    
    # Add some space
    st.write("")
    
    if working_login_url:
        # Login link - using working Django app URL
        st.markdown(
            f"<div style='text-align: center;'><h2>"
            f"<a href='{working_login_url}' style='text-decoration: none; color: #FF4B4B;'>"
            f"Se connecter 🔓</a></h2></div>",
            unsafe_allow_html=True
        )
    else:
        # Show maintenance message if Django app is not available
        st.error("""
        🛰️ Le système de connexion est temporairement indisponible. 
        Veuillez réessayer dans quelques instants.
        """)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <p style='color: #888; font-size: 0.8em;'>© 2025 Gestion des Candidatures. Tous droits réservés.</p>
    </div>
    """, unsafe_allow_html=True)
