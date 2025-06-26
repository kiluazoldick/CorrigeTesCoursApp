import os
import json
from datetime import datetime
from config import STATS_DIR
import logging

def save_quiz_result(user_id, note_title, question_text, user_answer, correct_answer, score):
    """
    Sauvegarde le résultat d'une question de quiz pour un utilisateur spécifique
    """
    user_dir = os.path.join(STATS_DIR, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        
    stats_file = os.path.join(user_dir, f"{note_title}_stats.json")
    
    # Charger les stats existantes ou créer un nouveau dictionnaire
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
    else:
        stats = {"attempts": []}
    
    # Ajouter la nouvelle tentative
    attempt = {
        "timestamp": datetime.now().isoformat(),
        "question": question_text,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "score": score
    }
    
    stats["attempts"].append(attempt)
    
    # Sauvegarder les stats
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

def get_note_stats(user_id, note_title):
    """
    Récupère les statistiques pour une note d'un utilisateur spécifique
    """
    user_dir = os.path.join(STATS_DIR, str(user_id))
    stats_file = os.path.join(user_dir, f"{note_title}_stats.json")
    
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"attempts": []}

def get_all_stats(user_id):
    """
    Récupère toutes les statistiques d'un utilisateur spécifique
    """
    user_dir = os.path.join(STATS_DIR, str(user_id))
    all_stats = {}
    
    if not os.path.exists(user_dir):
        return all_stats
    
    for filename in os.listdir(user_dir):
        if filename.endswith('_stats.json'):
            note_title = filename.replace('_stats.json', '')
            with open(os.path.join(user_dir, filename), 'r', encoding='utf-8') as f:
                all_stats[note_title] = json.load(f)
    
    return all_stats

def delete_note_stats(user_id, note_title):
    """
    Supprime l'historique des stats pour une note d'un utilisateur spécifique
    """
    user_dir = os.path.join(STATS_DIR, str(user_id))
    stats_file = os.path.join(user_dir, f"{note_title}_stats.json")
    
    try:
        if os.path.exists(stats_file):
            os.remove(stats_file)
            return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression des stats de {note_title}: {e}")
    return False

def delete_all_stats(user_id):
    """
    Supprime tout l'historique des stats d'un utilisateur spécifique
    """
    try:
        user_dir = os.path.join(STATS_DIR, str(user_id))
        if os.path.exists(user_dir):
            for filename in os.listdir(user_dir):
                if filename.endswith('_stats.json'):
                    os.remove(os.path.join(user_dir, filename))
            return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression de toutes les stats: {e}")
    return False