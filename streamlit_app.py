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
    st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        <p style='font-size: 1.2em; color: #666;'>Bienvenue dans votre espace de gestion des candidatures</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login button with styling
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <a href='https://projetpfa-jzgjbivvfqdgn7p9jawpnu.streamlit.app/login/' target='_self' style='text-decoration: none;'>
            <button style='
                background-color: #FF4B4B;
                color: white;
                padding: 15px 32px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s ease;
                width: 100%;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'
                onmouseover='this.style.backgroundColor="#FF3333"'
                onmouseout='this.style.backgroundColor="#FF4B4B"'>
                Se connecter 🔓
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <p style='color: #888; font-size: 0.8em;'>© 2025 Gestion des Candidatures. Tous droits réservés.</p>
    </div>
    """, unsafe_allow_html=True)

