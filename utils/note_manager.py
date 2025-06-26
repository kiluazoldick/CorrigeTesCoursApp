import os
from config import NOTES_DIR  

def load_notes(user_id):
    """Charge les notes d'un utilisateur spécifique"""
    user_dir = os.path.join(NOTES_DIR, str(user_id))
    notes = []
    
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        return notes
    
    for filename in os.listdir(user_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(user_dir, filename), "r", encoding="utf-8") as file:
                notes.append({"title": filename.replace(".txt", ""), "content": file.read()})
    return notes

def save_note(user_id, title, content):
    """Sauvegarde une note pour un utilisateur spécifique"""
    user_dir = os.path.join(NOTES_DIR, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    with open(os.path.join(user_dir, f"{title}.txt"), "w", encoding="utf-8") as file:
        file.write(content)

def delete_note(user_id, title):
    """Supprime une note d'un utilisateur spécifique"""
    user_dir = os.path.join(NOTES_DIR, str(user_id))
    filepath = os.path.join(user_dir, f"{title}.txt")
    
    if os.path.exists(filepath):
        os.remove(filepath)

def update_note(user_id, title, new_content):
    """Met à jour le contenu d'une note pour un utilisateur spécifique"""
    user_dir = os.path.join(NOTES_DIR, str(user_id))
    filepath = os.path.join(user_dir, f"{title}.txt")
    
    if os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(new_content)
        return True
    return False