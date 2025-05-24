import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Mon Projet PFA",
    page_icon="📚",
    layout="wide"
)

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/48/000000/student-center.png", width=100)
    st.title("Navigation")
    page = st.radio(
        "Choisissez une page:",
        ["Accueil", "À propos du projet", "Données", "Analyse", "Contact"]
    )

# Main content
if page == "Accueil":
    st.title("📚 Gestion des Candidatures")
    st.write("Bienvenue dans l'application de gestion des candidatures.")
    
    # Quick stats in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Candidatures", "150")
    with col2:
        st.metric("En attente", "45")
    with col3:
        st.metric("Traités", "105", "+12")

    # Add a sample chart
    st.subheader("Statistiques récentes")
    chart_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai'],
        'Candidatures': [30, 45, 60, 75, 90]
    })
    st.line_chart(chart_data.set_index('Mois'))

elif page == "À propos du projet":
    st.title("🎯 À propos du projet")
    st.write("""
    Ce projet vise à développer une application web pour la gestion efficace des candidatures.
    
    ### Objectifs principaux:
    - Simplifier le processus de candidature
    - Automatiser le tri et la classification
    - Fournir des analyses statistiques
    - Améliorer le suivi des candidatures
    """)

elif page == "Données":
    st.title("📊 Visualisation des données")
    st.write("Explorez les données des candidatures")
    
    # Sample data table
    data = pd.DataFrame({
        'ID': range(1, 6),
        'Nom': ['Dupont', 'Martin', 'Bernard', 'Petit', 'Robert'],
        'Status': ['En attente', 'Accepté', 'En attente', 'Refusé', 'Accepté'],
        'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05']
    })
    st.dataframe(data)

elif page == "Analyse":
    st.title("📈 Analyse des candidatures")
    
    # Add filters
    status = st.selectbox("Filtrer par status", ["Tous", "En attente", "Accepté", "Refusé"])
    date_range = st.date_input("Sélectionner une période")
    
    st.write("Résultats de l'analyse seront affichés ici...")

else:  # Contact page
    st.title("📧 Contact")
    with st.form("contact_form"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit = st.form_submit_button("Envoyer")
        
        if submit:
            st.success("Message envoyé! Nous vous contacterons bientôt.")
