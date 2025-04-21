import os
from config import NOTES_DIR  

def load_notes():
    notes = []
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(NOTES_DIR, filename), "r") as file:
                notes.append({"title": filename.replace(".txt", ""), "content": file.read()})
    return notes

def save_note(title, content):
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    with open(os.path.join(NOTES_DIR, f"{title}.txt"), "w") as file:
        file.write(content)

def delete_note(title):
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    if os.path.exists(filepath):
        os.remove(filepath)

def update_note(title, new_content):
    """
    Met à jour le contenu d'une note existante
    :param title: Titre de la note
    :param new_content: Nouveau contenu
    :return: True si la mise à jour est réussie, False sinon
    """
    filepath = os.path.join(NOTES_DIR, f"{title}.txt")
    if os.path.exists(filepath):
        with open(filepath, "w") as file:
            file.write(new_content)
        return True
    return False
