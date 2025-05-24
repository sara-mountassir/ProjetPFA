import streamlit as st
import webbrowser

# Redirect to Django login page
st.markdown("""
    <meta http-equiv="refresh" content="0; url=https://gestion-candidatures.onrender.com/login/">
    <script type="text/javascript">
        window.location.href = "https://gestion-candidatures.onrender.com/login/";
    </script>
""", unsafe_allow_html=True)

# Fallback message in case redirect doesn't work
st.write("Si vous n'êtes pas redirigé automatiquement, ")
st.markdown("[🔓 cliquez ici](https://gestion-candidatures.onrender.com/login/)")
