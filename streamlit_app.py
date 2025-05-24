import streamlit as st

# Set page config
st.set_page_config(
    page_title="Gestion des Candidatures",
    page_icon="📚",
    layout="centered"
)

# Add custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    
    .big-link {
        display: inline-block;
        background-color: #FF4B4B;
        color: white !important;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 500;
        margin: 20px 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .big-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Center content
col1, col2, col3 = st.columns([1,2,1])

with col2:
    # Logo and title
    st.image("https://img.icons8.com/color/96/000000/student-center.png", width=96)
    st.title("Gestion des Candidatures")
    
    # Welcome message
    st.write("Bienvenue dans votre espace de gestion des candidatures")
    
    # Login link
    st.markdown(
        f'<a href="https://gestion-candidatures.onrender.com/login/" class="big-link">'
        f'Se connecter 🔓</a>',
        unsafe_allow_html=True
    )
    
    # Footer
    st.markdown(
        "<div style='text-align: center; margin-top: 30px;'>"
        "<p style='color: #888; font-size: 0.8em;'>© 2025 Gestion des Candidatures. "
        "Tous droits réservés.</p></div>",
        unsafe_allow_html=True
    )
