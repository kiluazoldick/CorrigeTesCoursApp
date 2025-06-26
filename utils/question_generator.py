import os
import re
import json
import logging
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from config import QUESTIONS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Configuration API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= st.secrets["OPENROUTER_API_KEY"],
)

def generate_questions(user_id, note_title, note_content):
    """
    Génère des questions pour un utilisateur spécifique
    """
    try:
        # Créer le répertoire utilisateur s'il n'existe pas
        user_dir = os.path.join(QUESTIONS_DIR, str(user_id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        prompt = (
            f"À partir de ce texte, crée des questions  relativement ouvertes qui permettent l'apprentissage actif. "
            f"Tu choisiras un nombre de questions adéquat en fonction de la longueur du texte.\n"
            f"Pour chaque question, retourne un JSON avec deux clés : "
            f"'text' pour la question et 'reponse' pour la réponse correcte.\n"
            f"Texte : {note_content}\n"
            f"Retourne uniquement du JSON, rien d'autre."
        )

        # Envoyer la requête à l'API
        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Vérification de la réponse
        logging.info("Réponse brute de l'API : %s", response)
        generated_text = response.choices[0].message.content.strip()
        
        # Nettoyer la réponse JSON
        if generated_text.startswith("```json") and generated_text.endswith("```"):
            generated_text = generated_text.strip("```json").strip("```")
        if not generated_text:
            raise ValueError("Réponse vide retournée par l'API.")

        # Chargement du JSON
        try:
            questions = json.loads(generated_text)
        except json.JSONDecodeError as json_err:
            logging.error("Erreur lors de l'analyse du JSON : %s", json_err)
            raise ValueError("La réponse de l'API n'est pas un JSON valide.")

        # Sauvegarder les questions dans le répertoire utilisateur
        json_file_path = os.path.join(user_dir, f"{note_title}.json")
        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(questions, file, indent=4, ensure_ascii=False)
        
        logging.info("Questions sauvegardées dans : %s", json_file_path)
        return questions

    except Exception as e:
        logging.error("Erreur lors de la génération des questions : %s", e)
        return []

def evaluate_answer(question, user_answer, correct_answer):
    """
    Évalue la réponse de l'utilisateur en utilisant l'API
    """
    try:
        prompt = (
            f"Tu es un professeur qui évalue une réponse d'étudiant de manière bienveillante.\n"
            f"Question: {question}\n"
            f"Réponse correcte: {correct_answer}\n"
            f"Réponse de l'étudiant: {user_answer}\n\n"
            f"Règles d'évaluation:\n"
            f"- Une réponse courte mais qui contient les éléments essentiels mérite une très bonne note\n"
            f"- Si les mots-clés principaux sont présents, la note doit être élevée (4 ou 5)\n"
            f"- La forme de la réponse importe moins que le fond\n"
            f"- Une réponse concise et précise vaut autant qu'une réponse détaillée\n\n"
            f"- Si la reponse est vide, la note est  0\n"
            f"- Si il n'y a pas de réponse, la note est 0\n"
            f"- malgres le fait que tu sois bienveillant nhesite pas a 0\n si la réponse est vide\n"
            f"- dans tous les cas soit objectif dans la notation et surtout ne donne aucune note autre que 0\n si la réponse est vide\n"
            f"Retourne UNIQUEMENT un JSON valide avec ce format exact: {{\"score\": X}} où X est un nombre entre 0 et 5.\n"
            f"Utilise les guillemets doubles pour la clé \"score\"."
        )

        response = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
        )

        if not response or not response.choices:
            raise ValueError("L'API n'a pas retourné de choix valides.")

        raw_content = response.choices[0].message.content
        if not raw_content:
            raise ValueError("La réponse de l'API est vide.")

        # Nettoyage du JSON
        cleaned_content = re.sub(r"^```json\s*|\s*```$", "", raw_content.strip(), flags=re.MULTILINE)
        cleaned_content = cleaned_content.replace("'", '"')
        
        try:
            evaluation = json.loads(cleaned_content)
        except json.JSONDecodeError:
            # Fallback si le parsing échoue
            score_match = re.search(r'score["\']?\s*:\s*(\d+)', cleaned_content)
            if score_match:
                return {"score": int(score_match.group(1))}
            raise

        if "score" not in evaluation:
            raise ValueError("Le JSON retourné ne contient pas la clé 'score'")

        return {"score": evaluation["score"]}

    except Exception as e:
        logging.exception("Erreur lors de l'évaluation de la réponse")
        return {"score": 0}