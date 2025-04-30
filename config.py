import os

# Dossier ou les notes seront sauvegardées
NOTES_DIR = "./notes/"
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Dossier où les résumés seront sauvegardés
SUMMARY_DIR = "./summaries/"
if not os.path.exists(SUMMARY_DIR):
    os.makedirs(SUMMARY_DIR)

# Fichier JSON où tous les résumés seront sauvegardés ensemble
SUMMARIES_FILE = "./summaries/all_summaries.json"

# Dossier ou les questions seront sauvegardées
QUESTIONS_DIR = "./questions/"
if not os.path.exists(QUESTIONS_DIR):
    os.makedirs(QUESTIONS_DIR)

# Chemin du fichier contenant les questions
QUESTIONS_FILE = os.path.join(QUESTIONS_DIR, "questions.json")

# Ajouter cette ligne avec les autres constantes
STATS_DIR = "./stats/"
if not os.path.exists(STATS_DIR):
    os.makedirs(STATS_DIR)
