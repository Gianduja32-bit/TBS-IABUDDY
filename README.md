# 🎓 Base d'apprentissage Streamlit

## 📋 Description

Ce projet contient une base simple pour apprendre à utiliser Streamlit.

## 🚀 Installation

1. Créer un environnement virtuel (optionnel mais recommandé):
```bash
python -m venv venv
source venv/bin/activate  # Sur Mac/Linux
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## ▶️ Lancement de l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse: `http://localhost:8501`

## 📚 Concepts de base Streamlit

### Affichage de texte
- `st.title()` - Titre principal
- `st.header()` - En-tête de section
- `st.write()` - Texte simple
- `st.markdown()` - Texte formaté en Markdown

### Entrées utilisateur
- `st.text_input()` - Champ de texte
- `st.button()` - Bouton cliquable
- `st.selectbox()` - Menu déroulant
- `st.slider()` - Curseur

### Organisation
- `st.columns()` - Créer des colonnes
- `st.sidebar` - Barre latérale
- `st.tabs()` - Onglets

### Messages
- `st.success()` - Message de succès (vert)
- `st.info()` - Information (bleu)
- `st.warning()` - Avertissement (jaune)
- `st.error()` - Erreur (rouge)

## 📖 Ressources pour apprendre

- [Documentation officielle Streamlit](https://docs.streamlit.io)
- [Galerie d'exemples](https://streamlit.io/gallery)
- [Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)

## 💡 Prochaines étapes

1. Modifiez `app.py` pour ajouter vos propres fonctionnalités
2. Essayez d'ajouter des graphiques avec `st.line_chart()` ou `st.bar_chart()`
3. Explorez les widgets interactifs
4. Ajoutez du CSS personnalisé avec `st.markdown()`

Bon apprentissage! 🚀
