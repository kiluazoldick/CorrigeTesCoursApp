import os
import json
import logging
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from config import SUMMARY_DIR

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Chargement des variables d'environnement
load_dotenv()

# Configuration de l'API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

def generate_summary(user_id, note_title, note_content):
    """
    Génère un résumé pour un utilisateur spécifique
    """
    try:
        # Créer le répertoire utilisateur s'il n'existe pas
        user_dir = os.path.join(SUMMARY_DIR, str(user_id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        prompt = (
            f"Lis attentivement ce texte et génère un résumé clair et précis.\n"
            f"Le résumé doit :\n"
            f"- Être concis mais complet\n"
            f"- Respecter le sens du texte d'origine\n"
            f"- Être bien structuré, sans introduction ni conclusion artificielle\n"
            f"- Utiliser un style neutre et académique\n\n"
            f"Texte à résumer :\n{note_content}\n\n"
            f"Retourne uniquement du texte brut, sans ajouter de balises, sans commencer par 'Résumé:' ou autres."
        )

        # Envoi de la requête
        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Vérification de la réponse
        logging.info("Réponse brute de l'API (résumé) : %s", response)
        summary_text = response.choices[0].message.content.strip()

        if not summary_text:
            raise ValueError("Résumé vide retourné par l'API.")

        # Sauvegarde du résumé dans le répertoire utilisateur
        summary_file_path = os.path.join(user_dir, f"{note_title}.txt")
        with open(summary_file_path, "w", encoding="utf-8") as file:
            file.write(summary_text)

        logging.info("Résumé sauvegardé dans : %s", summary_file_path)
        return summary_text

    except Exception as e:
        logging.error("Erreur lors de la génération du résumé : %s", e)
        return ""

def load_summary(user_id, note_title):
    """
    Charge un résumé pour un utilisateur spécifique
    """
    try:
        user_dir = os.path.join(SUMMARY_DIR, str(user_id))
        summary_file_path = os.path.join(user_dir, f"{note_title}.txt")
        
        with open(summary_file_path, "r", encoding="utf-8") as file:
            summary = file.read()
        
        logging.info("Résumé chargé depuis : %s", summary_file_path)
        return summary
    except FileNotFoundError:
        logging.error("Résumé introuvable pour le titre : %s", note_title)
        return ""
    except Exception as e:
        logging.error("Erreur lors du chargement du résumé : %s", e)
        return ""