import os
import re
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from config import QUESTIONS_DIR, QUESTIONS_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Configuration API
api_key = os.getenv("DEEPSEEK_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def generate_questions(note_title, note_content):
    """
    Génère des questions à partir du contenu des notes en utilisant l'API DeepSeek.
    :param note_title: Titre de la note
    :param note_content: Contenu de la note
    :return: Une liste de questions générées
    """
    try:
        prompt = (
            f"À partir de ce texte, crée des questions relativement ouvertes qui permettent l'apprentissage actif. "
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

        # Sauvegarder les questions dans un fichier JSON
        json_file_path = os.path.join(QUESTIONS_DIR, f"{note_title}.json")
        with open(json_file_path, "w") as file:
            json.dump(questions, file, indent=4, ensure_ascii=False)
        logging.info("Questions sauvegardées dans : %s", json_file_path)
        return questions

    except Exception as e:
        logging.error("Erreur lors de la génération des questions : %s", e)
        return []

def save_questions(questions):
    """
    Sauvegarde les questions générées dans un fichier JSON.
    :param questions: Liste des questions
    """
    try:
        if not os.path.exists(os.path.dirname(QUESTIONS_FILE)):
            os.makedirs(os.path.dirname(QUESTIONS_FILE))
        with open(QUESTIONS_FILE, "w") as file:
            json.dump(questions, file, indent=4)
        logging.info("Questions sauvegardées dans le fichier principal : %s", QUESTIONS_FILE)
    except Exception as e:
        logging.error("Erreur lors de la sauvegarde des questions : %s", e)

def load_questions():
    """
    Charge les questions sauvegardées à partir du fichier JSON.
    :return: Liste des questions
    """
    try:
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r") as file:
                return json.load(file)
    except Exception as e:
        logging.error("Erreur lors du chargement des questions : %s", e)
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

        # Nettoyage plus robuste du JSON
        cleaned_content = re.sub(r"^```json\s*|\s*```$", "", raw_content.strip(), flags=re.MULTILINE)
        
        # Correction des guillemets simples en doubles si nécessaire
        cleaned_content = cleaned_content.replace("'", '"')
        
        try:
            evaluation = json.loads(cleaned_content)
        except json.JSONDecodeError:
            # Si le parsing échoue, tentative de correction du format
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