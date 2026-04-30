# 🎓 EduStat — Application de suivi académique
**Université de Yaoundé I · Ngoa-Ekélé · FST**
INF 232 EC2 — Collecte & Analyse descriptive de données

---

## Fonctionnalités
- ✅ Saisie des notes par UE avec coefficients (Info & Maths, L1/L2/L3)
- ✅ Calcul de la moyenne pondérée et taux de validation
- ✅ Gestion des rattrapages (note finale = max(note, rattrapage))
- ✅ Statistiques personnelles : barres, radar, tableau détaillé
- ✅ Conseils personnalisés basés sur les notes et habitudes
- ✅ Collecte des habitudes de vie (sommeil, étude, distractions)
- ✅ Vue globale des taux de réussite par filière
- ✅ Export CSV et rapport TXT
- ✅ Historique des saisies avec courbe de progression

---

## Déploiement sur Streamlit Cloud (gratuit)

### Étape 1 — Préparer GitHub
1. Créez un compte sur https://github.com
2. Créez un nouveau dépôt public (ex: `edustat-app`)
3. Uploadez les deux fichiers : `app.py` et `requirements.txt`

### Étape 2 — Déployer sur Streamlit Cloud
1. Allez sur https://share.streamlit.io
2. Connectez-vous avec votre compte GitHub
3. Cliquez **"New app"**
4. Sélectionnez votre dépôt, branche `main`, fichier `app.py`
5. Cliquez **"Deploy!"**

Votre application sera disponible à une URL du type :
`https://votre-nom-edustat-app-xxxx.streamlit.app`

### Étape 3 — Envoyer le lien au professeur
Envoyez le lien à : rollinfrancis28@gmail.com

---

## Lancement en local (test)
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Structure du projet
```
edustat/
├── app.py           ← Application principale
├── requirements.txt ← Dépendances Python
└── README.md        ← Ce fichier
```
