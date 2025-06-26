import streamlit as st
from database import create_user, verify_user

def login_form():
    """Affiche le formulaire de connexion"""
    with st.form("Connexion"):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
        
        if submitted:
            user = verify_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Identifiants incorrects")

def register_form():
    """Affiche le formulaire d'inscription"""
    with st.form("Inscription"):
        username = st.text_input("Nom d'utilisateur")
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password")
        submitted = st.form_submit_button("S'inscrire")
        
        if submitted:
            if password != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
                return
                
            if create_user(email, username, password):
                st.success("Compte créé avec succès! Veuillez vous connecter.")
            else:
                st.error("Cet email ou nom d'utilisateur est déjà utilisé")