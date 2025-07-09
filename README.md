# 🧠 CorrigeTesCoursApp – Plateforme d’apprentissage intelligent pour étudiants

CorrigeTesCoursApp est une application web de type **PWA** (Progressive Web App) développée avec **Python** et **Streamlit**. Elle permet aux étudiants de **saisir leurs cours**, **générer automatiquement des résumés**, **créer des quiz dynamiques** et de **suivre leur progression** à travers un tableau de bord interactif. L’application utilise des modèles d’intelligence artificielle via l’API **DeepSeek** de **OpenRouter** pour assister les apprenants de manière autonome, intuitive et efficace. 🎓🚀

---

## 🛠️ Fonctionnalités

### 📘 Gestion des Cours
- **Ajout & édition** : Enregistrez et modifiez vos cours facilement.
- **Interface fluide** : Champ de texte ergonomique.
- **Sauvegarde** : Données stockées localement en SQLite.

### 📑 Résumés IA automatisés
- Résumé clair et structuré généré à partir des cours.
- Basé sur un **modèle IA DeepSeek** intégré via API.
- Optimisé pour la langue française.

### ❓ Génération de Quiz
- Quiz à choix multiple générés automatiquement.
- Évaluation immédiate et notation automatique.
- Feedback par question pour améliorer l’apprentissage.

### 📊 Statistiques
- Visualisation des résultats passés.
- Score moyen par quiz.
- Suivi de progression global.

---

## ⚙️ Technologies utilisées

- **Langage** : Python 3.x
- **Framework** : Streamlit
- **Base de données** : SQLite
- **API IA** : OpenRouter (DeepSeek Model)
- **Outils complémentaires** :
  - dotenv
  - requests / requests-oauthlib
  - passlib
  - Docker (pour containerisation)

---

## 🚀 Installation

> 💡 Il est recommandé d’utiliser un environnement virtuel Python (`venv` ou `virtualenv`).

### Clonage du dépôt
```bash
git clone https://github.com/kiluazoldick/CorrigeTesCoursApp
cd CorrigeTesCoursApp
````

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Configuration de l’API IA

* Créez un compte sur [OpenRouter.ai](https://openrouter.ai)
* Obtenez une clé API pour le modèle DeepSeek
* Ajoutez-la dans un fichier `.env` :

```
OPENROUTER_API_KEY=your_key_here
```

### Lancer l’application

```bash
streamlit run app.py
```

### Alternative avec Docker

```bash
docker build -t corrigetescours .
docker run --env-file .env -dp 5000:5000 corrigetescours
```

---

## 📁 Structure du projet

```
CorrigeTesCoursApp/
├── app.py                 # Application principale
├── auth.py                # Authentification & sessions
├── config.py              # Variables globales
├── database.py            # Modèle de base de données
├── requirements.txt       # Dépendances
├── utils/                 # Fonctions utilitaires
├── notes/                 # Cours enregistrés
├── summaries/             # Résumés IA
├── questions/             # Quiz générés
├── stats/                 # Scores utilisateurs
├── Dockerfile             # Déploiement Docker
└── .env / .gitignore      # Fichiers de config
```

---

## 💡 Utilisation

### Dashboard

* Vue d’ensemble avec boutons d’accès rapide aux sections : Cours, Résumés, Quiz, Stats.

### Prise de Notes

* Interface d’ajout / édition des contenus de cours.

### Résumé Automatique

* Résumé généré en un clic à l’aide de l’IA.

### Quiz Intelligent

* Génération de QCM
* Évaluation automatique
* Feedback détaillé

### Statistiques

* Graphiques de progression
* Historique des performances

---

## 🤝 Contribution

Les contributions sont les bienvenues !
N’hésitez pas à :

* Signaler des bugs
* Améliorer le code ou l’interface
* Proposer des idées via pull request

---

## 📫 Contact

Auteur : **Nanga Doumer**
Email : \[nangadoumer@gmail.com]
GitHub : [@kiluazoldick](https://github.com/kiluazoldick)

---

## 📄 Licence

Ce projet est sous licence **MIT**.
Voir le fichier `LICENSE` pour plus de détails.

```
