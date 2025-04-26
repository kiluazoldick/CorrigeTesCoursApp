import os
import json
import logging
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from config import SUMMARY_DIR, SUMMARIES_FILE

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Chargement des variables d'environnement
load_dotenv()

# Configuration de l'API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

def generate_summary(note_title, note_content):
    """
    Génère un résumé à partir du contenu des notes en utilisant l'API DeepSeek.
    :param note_title: Titre de la note
    :param note_content: Contenu de la note
    :return: Le résumé généré
    """
    try:
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

        # Sauvegarde du résumé dans un fichier texte
        summary_file_path = os.path.join(SUMMARY_DIR, f"{note_title}.txt")
        with open(summary_file_path, "w", encoding="utf-8") as file:
            file.write(summary_text)

        logging.info("Résumé sauvegardé dans : %s", summary_file_path)
        return summary_text

    except Exception as e:
        logging.error("Erreur lors de la génération du résumé : %s", e)
        return ""


def load_summary(note_title):
    """
    Charge un résumé à partir du fichier correspondant.
    :param note_title: Titre de la note
    :return: Contenu du résumé
    """
    try:
        summary_file_path = os.path.join(SUMMARY_DIR, f"{note_title}.txt")
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


def save_all_summaries():
    """
    Sauvegarde tous les résumés dans un seul fichier JSON.
    """
    try:
        summaries = {}
        for filename in os.listdir(SUMMARY_DIR):
            if filename.endswith(".txt"):
                note_title = filename[:-4]  # Retirer l'extension .txt
                summary_path = os.path.join(SUMMARY_DIR, filename)
                with open(summary_path, "r", encoding="utf-8") as file:
                    summaries[note_title] = file.read()

        with open(SUMMARIES_FILE, "w", encoding="utf-8") as file:
            json.dump(summaries, file, ensure_ascii=False, indent=4)

        logging.info("Tous les résumés ont été sauvegardés dans : %s", SUMMARIES_FILE)

    except Exception as e:
        logging.error("Erreur lors de la sauvegarde de tous les résumés : %s", e)
