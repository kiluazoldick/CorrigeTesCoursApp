import streamlit as st
import os, json
from utils.note_manager import load_notes, save_note, delete_note, update_note
from utils.question_generator import generate_questions, evaluate_answer
from utils.summary_generator import generate_summary
from config import QUESTIONS_DIR, SUMMARY_DIR
from utils.stats_manager import get_all_stats, save_quiz_result, delete_note_stats, delete_all_stats
from database import init_db
from auth import login_form, register_form

# Configuration de la page - doit être le premier élément
st.set_page_config(
    page_title="CorrigeTesCours",
    page_icon="📝",
    layout="wide"
)

# Initialisation de la base de données
init_db()

# Gestion de l'authentification
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# Si l'utilisateur n'est pas connecté, afficher les formulaires d'authentification
if not st.session_state.logged_in:
    st.title("Se connecter à CorrigeTesCours 🔐")
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        login_form()
    
    with tab2:
        register_form()
    
    st.stop()

# ================================================
# Application principale (utilisateur connecté)
# ================================================

# Sidebar 
st.sidebar.title(f"👋🏾Bonjour, {st.session_state.user['username']}")

menu = st.sidebar.radio(
    "📂 <span style='color: #0066CC;'>Choisissez une option :</span>", 
    ["Dashboard", "Notes","Résumé", "Quiz", "Performances"], 
    format_func=lambda x: f"🔹 {x}", 
    index=0,
    label_visibility="hidden", 
    key="menu_radio"
)

st.sidebar.markdown("---")

# Ajouter un bouton de déconnexion
if st.sidebar.button("🚪 Déconnexion"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# Main content
if menu == "Dashboard":
    # Header with custom styles
    st.markdown("<h1>Bienvenue sur CorrigeTesCours </h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader(f"Apprenez ses cours grâce au _Active Learning_, {st.session_state.user['username']}!")
    
    # Feature list with emojis and custom formatting
    st.markdown(
        """
        <div style='padding: 10px;'>
            <p><strong>CorrigeTesCours</strong> vous permet de :</p>
            <ul>
                <li>🗒️ <strong>Prendre des notes</strong> et les organiser.</li>
                <li>📋 <strong>Résumer ses notes</strong> pour un meilleur apprentissage.</li>
                <li>❓ <strong>Générer des questions</strong> pour vos cours.</li>
                <li>✅ <strong>Pratiquer l'apprentissage actif</strong> et suivre vos progrès.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

elif menu == "Notes":
    st.header("🗒️ Prise de Notes")
    
   
    
    user_id = st.session_state.user["id"]
    
    if "notes" not in st.session_state:
        st.session_state.notes = load_notes(user_id)
    
    if "editing_note" not in st.session_state:
        st.session_state.editing_note = None


    # Affichage des notes existantes
    st.write("### Vos notes :")
    if st.session_state.notes:
        for note in st.session_state.notes:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📝 {note['title']}")
            with col2:
                if st.button("✏️Voir/Modifier", key=f"edit_{note['title']}"):
                    st.session_state.editing_note = note
            with col3:
                if st.button("🗑️Supprimer", key=f"delete_{note['title']}"):
                    delete_note(user_id, note['title'])
                    st.session_state.notes = load_notes(user_id)
                    if st.session_state.editing_note and st.session_state.editing_note['title'] == note['title']:
                        st.session_state.editing_note = None
                    st.session_state.success_message = f"Note '{note['title']}' supprimée avec succès !"
                    st.rerun()
    else:
        st.info("Aucune note disponible pour le moment.")

    # Section d'édition/visualisation
    if st.session_state.editing_note:
        st.markdown("---")
        st.subheader(f"Modifier la note : {st.session_state.editing_note['title']}")
        edited_content = st.text_area(
            "Contenu de la note",
            value=st.session_state.editing_note['content'],
            height=300,
            key="edit_content"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sauvegarder les modifications"):
                if update_note(user_id, st.session_state.editing_note['title'], edited_content):
                    st.session_state.success_message = "Note mise à jour avec succès!"
                    st.session_state.notes = load_notes(user_id)
                    st.session_state.editing_note = None
                    st.rerun()
                else:
                    st.error("Erreur lors de la mise à jour de la note")
        with col2:
            if st.button("Annuler"):
                st.session_state.editing_note = None

                 # Gestion des messages de succès
    if "success_message" in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message

    # Section pour créer une nouvelle note
    st.markdown("---")
    st.subheader("Créer une nouvelle note")
    
    # Initialisation des champs
    if "new_note_title" not in st.session_state:
        st.session_state.new_note_title = ""
    if "new_note_content" not in st.session_state:
        st.session_state.new_note_content = ""
    
    note_title = st.text_input("Titre de la note", value=st.session_state.new_note_title, key="new_title")
    note_content = st.text_area("Contenu de la note", value=st.session_state.new_note_content, height=200, key="new_content")
    
    if st.button("Sauvegarder"):
        if note_title and note_content:
            save_note(user_id, note_title, note_content)
            st.session_state.notes = load_notes(user_id)
            
            # Réinitialisation du formulaire
            st.session_state.new_note_title = ""
            st.session_state.new_note_content = ""
            
            # Message de succès
            st.session_state.success_message = f"Note '{note_title}' sauvegardée avec succès !"
            st.rerun()
        else:
            st.warning("Veuillez fournir un titre et un contenu pour votre note.")
             
             # Gestion des messages de succès
    if "success_message" in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message


elif menu == "Résumé":
    st.header("📋 Mode Résumé")
    
    # Charger les notes disponibles
    user_id = st.session_state.user["id"]
    notes = load_notes(user_id)
    note_titles = [note["title"] for note in notes]
    selected_note = st.selectbox("Choisissez une note à résumer", note_titles)

    if selected_note:
        note_content = next(note["content"] for note in notes if note["title"] == selected_note)
        
        # Initialisation du résumé
        if "summary" not in st.session_state or st.session_state.get("current_summary_note") != selected_note:
            st.session_state.summary = ""
            st.session_state.current_summary_note = selected_note

        # Générer un nouveau résumé
        if st.button("📝 Générer le résumé"):
            try:
                with st.spinner("Génération du résumé en cours..."):
                    new_summary = generate_summary(user_id, selected_note, note_content)

                if new_summary:
                    st.session_state.summary = new_summary
                    st.success("Résumé généré avec succès !")
                else:
                    st.error("L'API n'a retourné aucun résumé.")
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

        # Afficher le résumé
        if st.session_state.summary:
            st.write("### Résumé :")
            st.text_area(
                "Voici votre résumé :",
                value=st.session_state.summary,
                height=300,
                disabled=False
            )
        else:
            st.info("Aucun résumé disponible. Cliquez sur 'Générer le résumé' pour commencer.")

elif menu == "Quiz":
    st.header("❓ Mode Quiz")
    
    # Charger les notes disponibles
    user_id = st.session_state.user["id"]
    notes = load_notes(user_id)
    note_titles = [note["title"] for note in notes]
    selected_note = st.selectbox("Choisissez une note", note_titles)

    if selected_note:
        note_content = next(note["content"] for note in notes if note["title"] == selected_note)
        json_file_path = os.path.join(QUESTIONS_DIR, str(user_id), f"{selected_note}.json")
        
        # Initialisation des questions
        if "questions" not in st.session_state or st.session_state.get("current_note") != selected_note:
            st.session_state.questions = []
            st.session_state.current_note = selected_note
            # Initialiser un dictionnaire pour stocker les réponses
            st.session_state.user_answers = {}

        # Générer de nouvelles questions
        if st.button("❓Générer des questions"):
            try:
                with st.spinner("Génération des questions en cours..."):
                    new_questions = generate_questions(user_id, selected_note, note_content)
                
                if new_questions:
                    st.session_state.questions = new_questions
                    st.session_state.user_answers = {}  # Réinitialiser les réponses
                    st.success("Questions générées avec succès !")
                else:
                    st.error("L'API n'a retourné aucune question.")
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

        # Afficher les questions
        if st.session_state.questions:
            st.write("### Questions :")
            
            # Afficher toutes les questions avec des champs de réponse
            for i, question in enumerate(st.session_state.questions, 1):
                st.write(f"**Question {i}:** {question['text']}")
                # Stocker la réponse dans session_state
                answer_key = f"answer_{i}"
                user_answer = st.text_area(
                    "Votre réponse",
                    key=answer_key,
                    height=100
                )
                st.session_state.user_answers[answer_key] = user_answer
                st.markdown("---")

            # Bouton unique pour vérifier toutes les réponses
            if st.button("📝 Vérifier toutes les réponses"):
                total_score = 0
                with st.spinner("Évaluation des réponses en cours..."):
                    for i, question in enumerate(st.session_state.questions, 1):
                        answer_key = f"answer_{i}"
                        user_answer = st.session_state.user_answers.get(answer_key, "")
                        
                        # Évaluer la réponse
                        evaluation = evaluate_answer(
                            question['text'],
                            user_answer,
                            question['reponse']
                        )
                        
                        # Sauvegarder le résultat
                        save_quiz_result(
                            user_id,
                            selected_note,
                            question['text'],
                            user_answer,
                            question['reponse'],
                            evaluation['score']
                        )
                        
                        total_score += evaluation['score']
                        
                        # Afficher le résultat pour cette question
                        with st.expander(f"Résultat Question {i}"):
                            st.write(f"**Votre réponse:** {user_answer}")
                            st.write(f"**Réponse correcte:** {question['reponse']}")
                            st.write(f"**Score:** {evaluation['score']}/5")
                
                # Afficher le score total
                avg_score = total_score / len(st.session_state.questions)
                st.success(f"Score total : {avg_score:.1f}/5")
                
                # Option pour recommencer
                if st.button("🔄 Recommencer le quiz"):
                    st.session_state.user_answers = {}
                    st.rerun()
        
        else:
            st.info("Aucune question disponible. Cliquez sur 'Générer des questions' pour commencer.")
           

elif menu == "Performances":
    st.header("📊 Performances d'apprentissage")
    
    user_id = st.session_state.user["id"]
    stats = get_all_stats(user_id)
    if not stats:
        st.info("Aucune statistique disponible pour le moment. Commencez à répondre à des quiz pour voir vos performances !")
    else:
        # Vue d'ensemble globale
        st.subheader("Vue d'ensemble")
        
        # Calculer les statistiques globales
        all_scores = []
        notes_avg_scores = {}
        for note_title, note_stats in stats.items():
            if note_stats["attempts"]:
                scores = [attempt["score"] for attempt in note_stats["attempts"]]
                notes_avg_scores[note_title] = sum(scores) / len(scores)
                all_scores.extend(scores)
        
        # Afficher le score moyen global
        if all_scores:
            global_avg = sum(all_scores) / len(all_scores)
            st.metric("Score moyen global", f"{global_avg:.1f}/5")
            
            # Graphique des scores moyens par note
            st.bar_chart(notes_avg_scores)
        
        # Détails par note
        st.subheader("Détails par note")
        for note_title, note_stats in stats.items():
            with st.expander(f"📝 {note_title}"):
                if note_stats["attempts"]:
                    col1, col2, col3 = st.columns(3)
                    
                    # Statistiques de base
                    scores = [attempt["score"] for attempt in note_stats["attempts"]]
                    avg_score = sum(scores) / len(scores)
                    with col1:
                        st.metric("Score moyen", f"{avg_score:.1f}/5")
                    with col2:
                        st.metric("Meilleur score", f"{max(scores)}/5")
                    with col3:
                        st.metric("Nombre de questions", len(scores))
                    
                    # Graphique d'évolution des scores
                    scores_df = {
                        "Question": range(1, len(scores) + 1),
                        "Score": scores
                    }
                    st.line_chart(scores_df, x="Question", y="Score")
                    
                    # Historique détaillé
                    st.write("### Historique détaillé")
                    for attempt in reversed(note_stats["attempts"]):
                        st.markdown(f"""
                        **📅 {attempt['timestamp'][:16].replace('T', ' à ')}**
                        - **Question:** {attempt['question']}
                        - **Votre réponse:** {attempt['user_answer']}
                        - **Réponse correcte:** {attempt['correct_answer']}
                        - **Score:** {attempt['score']}/5
                        ---
                        """)
                    
                    # Bouton pour supprimer l'historique de cette note
                    if st.button("🗑️ Supprimer l'historique", key=f"delete_{note_title}"):
                        if delete_note_stats(user_id, note_title):
                            st.success(f"Historique supprimé pour {note_title}")
                            st.rerun()
                        else:
                            st.error("Erreur lors de la suppression de l'historique")

        # Bouton pour supprimer tout l'historique
        st.markdown("---")
        if st.button("🗑️ Supprimer tout l'historique", type="secondary"):
            if delete_all_stats(user_id):
                st.success("Tout l'historique a été supprimé")
                st.rerun()
            else:
                st.error("Erreur lors de la suppression de l'historique")