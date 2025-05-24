import streamlit as st

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
    
    # Login link - using your Django app URL
    st.markdown(
        "<div style='text-align: center;'><h2>"
        "<a href='https://gestion-candidatures.onrender.com/login/' style='text-decoration: none; color: #FF4B4B;'>"
        "Se connecter 🔓</a></h2></div>",
        unsafe_allow_html=True
    )
    
    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <p style='color: #888; font-size: 0.8em;'>© 2025 Gestion des Candidatures. Tous droits réservés.</p>
    </div>
    """, unsafe_allow_html=True)
