import streamlit as st

# Set page config
st.set_page_config(
    page_title="Gestion des Candidatures",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for the login page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/white-abstract-background_23-2148806276.jpg");
        background-size: cover;
        background-position: center;
    }
    
    .login-container {
        background: rgba(10, 7, 7, 0.35);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        max-width: 430px;
        margin: 0 auto;
    }
    
    .login-tabs {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    
    .login-input {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        border-radius: 8px;
        color: white;
        padding: 12px;
        margin: 10px 0;
        width: 100%;
    }
    
    .login-button {
        background-color: #fff;
        color: #1937ce;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 10px;
        width: 100%;
    }
    
    .login-button:hover {
        background-color: #f0f0f0;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Login form
    with st.form("login_form"):
        st.text_input("Nom d'utilisateur ou email", key="username")
        st.text_input("Mot de passe", type="password", key="password")
        
        if st.form_submit_button("Se connecter", use_container_width=True):
            st.success("Redirection vers le tableau de bord...")
            st.write("""
            <meta http-equiv="refresh" content="2;url=https://gestion-candidatures.onrender.com/dashboard/">
            """, unsafe_allow_html=True)
    
    # Registration link
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <p style='color: #666;'>Pas encore de compte ? 
        <a href='https://gestion-candidatures.onrender.com/register/' style='color: #FF4B4B; text-decoration: none;'>
            Créer un compte
        </a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <p style='color: #888; font-size: 0.8em;'>© 2025 Gestion des Candidatures. Tous droits réservés.</p>
    </div>
    """, unsafe_allow_html=True)
