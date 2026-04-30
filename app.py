import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ─────────────────────────────────────────────
#  CONFIG GLOBALE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EduStat — Université de Yaoundé I",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CSS PERSONNALISÉ
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a3a5c 0%, #2e6da4 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2rem; }
    .main-header p  { color: rgba(255,255,255,0.8); margin: 4px 0 0; font-size: 0.9rem; }

    .metric-card {
        background: #f0f4f8;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #2e6da4;
    }
    .conseil-box {
        background: #e8f5e9;
        border-left: 4px solid #2e7d32;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #1b5e20;
    }
    .alerte-box {
        background: #fff3e0;
        border-left: 4px solid #e65100;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #bf360c;
    }
    .danger-box {
        background: #ffebee;
        border-left: 4px solid #c62828;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #b71c1c;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DONNÉES : UE PAR FILIÈRE
# ─────────────────────────────────────────────
FILIERES = {
    "Informatique — Licence 1": {
        "S1": [
            ("Algorithmique & Programmation", 4),
            ("Mathématiques générales 1",     3),
            ("Architecture des ordinateurs",  3),
            ("Analyse 1",                     3),
            ("Anglais technique 1",           2),
            ("Physique générale",             2),
        ],
        "S2": [
            ("Structures de données",         4),
            ("Mathématiques générales 2",     3),
            ("Systèmes d'exploitation 1",     3),
            ("Analyse 2",                     3),
            ("Anglais technique 2",           2),
            ("Électronique de base",          2),
        ],
    },
    "Informatique — Licence 2": {
        "S1": [
            ("Bases de données 1",            4),
            ("Réseaux informatiques 1",       3),
            ("Probabilités & Statistiques",   3),
            ("Programmation orientée objet",  4),
            ("Systèmes d'exploitation 2",     3),
        ],
        "S2": [
            ("Bases de données 2",            4),
            ("Réseaux informatiques 2",       3),
            ("Recherche opérationnelle",      3),
            ("Génie logiciel 1",              4),
            ("Programmation web",             3),
        ],
    },
    "Informatique — Licence 3": {
        "S1": [
            ("Génie logiciel 2",              4),
            ("IA & Machine Learning",         4),
            ("Compilation",                   3),
            ("Sécurité informatique",         3),
            ("Projet informatique 1",         3),
        ],
        "S2": [
            ("Développement mobile",          4),
            ("Big Data & Cloud",              4),
            ("Infographie",                   3),
            ("Entrepreneuriat numérique",     2),
            ("Projet informatique 2",         4),
        ],
    },
    "Mathématiques — Licence 1": {
        "S1": [
            ("Algèbre linéaire 1",            4),
            ("Analyse réelle 1",              4),
            ("Géométrie différentielle",      3),
            ("Informatique pour maths",       2),
            ("Probabilités 1",                3),
        ],
        "S2": [
            ("Algèbre linéaire 2",            4),
            ("Analyse réelle 2",              4),
            ("Topologie générale",            3),
            ("Probabilités 2",                3),
            ("Physique mathématique",         2),
        ],
    },
    "Mathématiques — Licence 2": {
        "S1": [
            ("Analyse complexe",              4),
            ("Algèbre abstraite",             4),
            ("Équations différentielles",     3),
            ("Statistiques inférentielles",   3),
            ("Mécanique analytique",          3),
        ],
        "S2": [
            ("Analyse fonctionnelle",         4),
            ("Théorie des groupes",           4),
            ("Calcul numérique",              3),
            ("Théorie des probabilités",      3),
            ("Travaux dirigés avancés",       2),
        ],
    },
}

# Données globales simulées (taux de validation par UE — Info L1 S1)
GLOBAL_UE_TAUX = {
    "Algorithmique & Programmation": 48,
    "Mathématiques générales 1":     52,
    "Architecture des ordinateurs":  63,
    "Analyse 1":                     41,
    "Anglais technique 1":           78,
    "Physique générale":             57,
}

GLOBAL_FILIERE_TAUX = {
    "Info L1": 54, "Info L2": 61, "Info L3": 72,
    "Math L1": 48, "Math L2": 65,
}

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "historique" not in st.session_state:
    st.session_state.historique = []


# ─────────────────────────────────────────────
#  FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────
def statut_note(note):
    if note >= 16: return "Très bien", "#1b5e20"
    if note >= 14: return "Bien",      "#2e7d32"
    if note >= 12: return "Assez bien","#558b2f"
    if note >= 10: return "Passable",  "#f57c00"
    if note >= 8:  return "Rattrapage","#e65100"
    return "Échec", "#c62828"


def calcul_moyenne(notes, coefs):
    total_pts  = sum(n * c for n, c in zip(notes, coefs))
    total_coef = sum(coefs)
    return total_pts / total_coef if total_coef else 0


def generer_conseils(resultats_df, moy, habitudes=None):
    conseils = []
    alertes  = []

    # Analyse des UE
    faibles   = resultats_df[resultats_df["Note"] < 10]
    moyennes  = resultats_df[(resultats_df["Note"] >= 10) & (resultats_df["Note"] < 12)]
    fortes    = resultats_df[resultats_df["Note"] >= 14]

    if len(faibles) > 0:
        noms = ", ".join(faibles["UE"].tolist())
        alertes.append(f"⚠️ UE en échec : **{noms}**. Un rattrapage sera nécessaire. Consultez votre enseignant.")

    if len(moyennes) > 0:
        noms = ", ".join(moyennes["UE"].tolist())
        conseils.append(f"📘 UE à consolider : **{noms}**. Un travail régulier peut faire passer ces UE au-dessus de 12.")

    if len(fortes) > 0:
        noms = ", ".join(fortes["UE"].tolist())
        conseils.append(f"✅ Points forts : **{noms}**. Continuez sur cette lancée !")

    if moy >= 14:
        conseils.append("🏆 Excellente moyenne ! Vous êtes sur la voie du mention Bien/Très bien.")
    elif moy >= 12:
        conseils.append("👍 Bonne moyenne. Quelques efforts supplémentaires vous amèneront à la mention Bien.")
    elif moy >= 10:
        conseils.append("📊 Moyenne passable. Le semestre est validé, mais il reste des marges de progression.")
    else:
        alertes.append("🚨 Moyenne inférieure à 10. Un passage en jury de rattrapage est probable. Ne tardez pas à demander de l'aide.")

    # Analyse des habitudes
    if habitudes:
        sommeil = habitudes.get("sommeil", 7)
        etude   = habitudes.get("etude", 3)
        ecrans  = habitudes.get("ecrans", 3)
        jeux    = habitudes.get("jeux", 1)

        if sommeil < 6:
            alertes.append(f"😴 Vous dormez seulement **{sommeil}h/nuit**. Le manque de sommeil réduit la mémorisation de 40%. Visez 7–8h.")
        elif sommeil >= 8:
            conseils.append(f"😴 Votre temps de sommeil ({sommeil}h) est optimal pour la mémorisation. Bravo !")

        if etude < 2:
            alertes.append(f"📚 Seulement **{etude}h d'étude/jour** en dehors des cours. Les étudiants performants étudient au moins 3–4h par jour.")
        elif etude >= 4:
            conseils.append(f"📚 **{etude}h d'étude/jour** — excellent rythme de travail !")

        total_distractions = ecrans + jeux
        if total_distractions > 4:
            alertes.append(f"📱 Vous passez **{total_distractions}h/jour** sur les écrans/jeux. Cela réduit votre concentration. Essayez la méthode Pomodoro (25 min étude / 5 min pause).")
        
        # Corrélation distraction / notes
        if moy < 12 and total_distractions > 3:
            alertes.append(f"🎮 Corrélation détectée : moyenne faible ({moy:.1f}) + temps de distraction élevé ({total_distractions}h). Réduire les écrans pourrait améliorer vos résultats de 1 à 2 points.")

    return conseils, alertes


def export_csv(df_notes, df_habitudes=None):
    output = io.StringIO()
    df_notes.to_csv(output, index=False, encoding="utf-8-sig")
    if df_habitudes is not None:
        output.write("\n\nHabitudes de vie\n")
        df_habitudes.to_csv(output, index=False, encoding="utf-8-sig")
    return output.getvalue().encode("utf-8-sig")


# ─────────────────────────────────────────────
#  EN-TÊTE
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🎓 EduStat</h1>
  <p>Suivi académique & analyse de données — Université de Yaoundé I · Ngoa-Ekélé · FST</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR — PROFIL ÉTUDIANT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Mon profil")
    nom       = st.text_input("Nom & Prénoms", placeholder="Ex: NKEMDIRIM Jean")
    matricule = st.text_input("Matricule", placeholder="Ex: 21A001")
    filiere   = st.selectbox("Filière", list(FILIERES.keys()))
    semestre  = st.selectbox("Semestre", ["S1", "S2"])
    annee     = st.selectbox("Année académique", ["2024–2025", "2025–2026", "2026–2027"])

    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.info("EduStat collecte vos données académiques pour produire des analyses statistiques et des conseils personnalisés.")

# ─────────────────────────────────────────────
#  ONGLETS PRINCIPAUX
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Saisie des notes",
    "📊 Mes statistiques",
    "🏠 Habitudes de vie",
    "🌍 Vue globale",
    "📥 Export & Historique"
])


# ══════════════════════════════════════════════
#  ONGLET 1 — SAISIE DES NOTES
# ══════════════════════════════════════════════
with tab1:
    st.subheader(f"📝 Saisie des notes — {filiere} · {semestre}")
    ues = FILIERES[filiere][semestre]

    st.markdown("Entrez vos notes sur 20 pour chaque Unité d'Enseignement.")

    notes_input = {}
    with st.form("form_notes"):
        cols_header = st.columns([3, 1, 2, 2])
        cols_header[0].markdown("**Unité d'Enseignement**")
        cols_header[1].markdown("**Coef.**")
        cols_header[2].markdown("**Note /20**")
        cols_header[3].markdown("**Rattrapage /20**")
        st.markdown("---")

        for ue_nom, coef in ues:
            cols = st.columns([3, 1, 2, 2])
            cols[0].markdown(f"<span style='font-size:0.95rem'>{ue_nom}</span>", unsafe_allow_html=True)
            cols[1].markdown(f"<span style='color:#666'>{coef}</span>", unsafe_allow_html=True)
            note_val = cols[2].number_input(
                label=f"note_{ue_nom}", min_value=0.0, max_value=20.0,
                step=0.25, value=None, label_visibility="collapsed",
                key=f"note_{ue_nom}"
            )
            ratt_val = cols[3].number_input(
                label=f"ratt_{ue_nom}", min_value=0.0, max_value=20.0,
                step=0.25, value=None, label_visibility="collapsed",
                key=f"ratt_{ue_nom}"
            )
            notes_input[ue_nom] = {
                "coef": coef,
                "note": note_val,
                "rattrapage": ratt_val
            }

        submitted = st.form_submit_button("✅ Calculer ma moyenne", use_container_width=True, type="primary")

    if submitted:
        rows = []
        valid = True
        for ue_nom, v in notes_input.items():
            if v["note"] is None:
                st.error(f"Note manquante pour : **{ue_nom}**")
                valid = False
                break
            # Note finale = max(note, rattrapage) si rattrapage renseigné
            note_finale = v["note"]
            if v["rattrapage"] is not None:
                note_finale = max(v["note"], v["rattrapage"])
            rows.append({
                "UE": ue_nom,
                "Coefficient": v["coef"],
                "Note initiale": v["note"],
                "Rattrapage": v["rattrapage"] if v["rattrapage"] is not None else "—",
                "Note finale": note_finale,
                "Validée": "✅" if note_finale >= 10 else "❌",
                "Statut": statut_note(note_finale)[0]
            })

        if valid and rows:
            df = pd.DataFrame(rows)
            moy = calcul_moyenne(df["Note finale"].tolist(), df["Coefficient"].tolist())
            nb_validees = (df["Note finale"] >= 10).sum()
            taux_val = round(nb_validees / len(df) * 100, 1)

            # Statut global
            if moy >= 14: statut_global, color_s = "Mention Bien/TB", "#1b5e20"
            elif moy >= 12: statut_global, color_s = "Mention Assez Bien", "#2e7d32"
            elif moy >= 10: statut_global, color_s = "Semestre validé", "#f57c00"
            elif (df["Note finale"] < 10).sum() <= 2 and moy >= 8:
                statut_global, color_s = "Passage en jury", "#e65100"
            else:
                statut_global, color_s = "Redoublement probable", "#c62828"

            st.session_state["df_notes"]      = df
            st.session_state["moy"]           = moy
            st.session_state["taux_val"]      = taux_val
            st.session_state["statut_global"] = statut_global

            # Enregistrer dans l'historique
            st.session_state.historique.append({
                "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Étudiant": nom or "—",
                "Filière": filiere,
                "Semestre": semestre,
                "Moyenne": round(moy, 2),
                "Taux validation": f"{taux_val}%",
                "Statut": statut_global
            })

            st.success("✅ Calcul effectué ! Consultez l'onglet **Mes statistiques**.")


# ══════════════════════════════════════════════
#  ONGLET 2 — STATISTIQUES PERSONNELLES
# ══════════════════════════════════════════════
with tab2:
    st.subheader("📊 Mes statistiques personnelles")

    if "df_notes" not in st.session_state:
        st.info("👈 Saisissez vos notes dans l'onglet **Saisie des notes** pour voir vos statistiques.")
    else:
        df      = st.session_state["df_notes"]
        moy     = st.session_state["moy"]
        taux    = st.session_state["taux_val"]
        statut  = st.session_state["statut_global"]
        hab     = st.session_state.get("habitudes", None)

        # Métriques
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Moyenne générale", f"{moy:.2f} / 20")
        c2.metric("UE validées", f"{(df['Note finale'] >= 10).sum()} / {len(df)}")
        c3.metric("Taux de validation", f"{taux}%")
        c4.metric("Statut", statut)

        st.markdown("---")
        col_a, col_b = st.columns(2)

        # Graphique barres
        with col_a:
            st.markdown("#### Performance par UE")
            colors = ["#2e7d32" if n >= 14 else "#f57c00" if n >= 10 else "#c62828"
                      for n in df["Note finale"]]
            fig_bar = go.Figure(go.Bar(
                x=df["Note finale"], y=df["UE"],
                orientation="h",
                marker_color=colors,
                text=[f"{n:.2f}" for n in df["Note finale"]],
                textposition="outside"
            ))
            fig_bar.add_vline(x=10, line_dash="dash", line_color="#e65100",
                              annotation_text="Seuil validation (10)")
            fig_bar.update_layout(
                height=max(300, len(df) * 45),
                margin=dict(l=0, r=40, t=10, b=10),
                xaxis=dict(range=[0, 22], title="Note /20"),
                yaxis=dict(title=""),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Radar des compétences
        with col_b:
            st.markdown("#### Profil de compétences")
            vals = df["Note finale"].tolist()
            cats = df["UE"].tolist()
            vals_norm = [v / 20 * 100 for v in vals]
            fig_radar = go.Figure(go.Scatterpolar(
                r=vals_norm + [vals_norm[0]],
                theta=cats + [cats[0]],
                fill="toself",
                fillcolor="rgba(46,109,164,0.2)",
                line_color="#1a3a5c"
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                height=380,
                margin=dict(l=40, r=40, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Tableau détaillé
        st.markdown("#### Détail par UE")
        st.dataframe(df.drop(columns=["Note initiale"]) if "Rattrapage" in df.columns else df,
                     use_container_width=True, hide_index=True)

        # Conseils
        st.markdown("---")
        st.markdown("#### 🤖 Conseils personnalisés")
        conseils, alertes = generer_conseils(df, moy, habitudes=hab)

        for a in alertes:
            st.markdown(f'<div class="alerte-box">{a}</div>', unsafe_allow_html=True)
        for c in conseils:
            st.markdown(f'<div class="conseil-box">{c}</div>', unsafe_allow_html=True)

        # Courbe de progression (si historique > 1)
        if len(st.session_state.historique) > 1:
            st.markdown("---")
            st.markdown("#### 📈 Courbe de progression")
            df_hist = pd.DataFrame(st.session_state.historique)
            fig_prog = px.line(df_hist, x="Date", y="Moyenne",
                               markers=True, line_shape="spline",
                               color_discrete_sequence=["#1a3a5c"])
            fig_prog.add_hline(y=10, line_dash="dash", line_color="#e65100")
            fig_prog.update_layout(
                height=250, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_prog, use_container_width=True)


# ══════════════════════════════════════════════
#  ONGLET 3 — HABITUDES DE VIE
# ══════════════════════════════════════════════
with tab3:
    st.subheader("🏠 Collecte des habitudes de vie")
    st.markdown("Ces données nous aident à comprendre les facteurs qui influencent vos résultats.")

    with st.form("form_habitudes"):
        st.markdown("#### 😴 Sommeil")
        sommeil = st.slider("Nombre d'heures de sommeil par nuit", 3, 12, 7)

        st.markdown("#### 📚 Travail personnel")
        etude_hors_cours = st.slider("Heures d'étude par jour (hors cours)", 0, 12, 3)
        revisions_avant  = st.slider("Jours de révision avant un examen", 0, 30, 7)
        methode_travail  = st.multiselect("Méthode(s) de travail utilisée(s)", [
            "Fiches de révision", "Exercices pratiques", "Lecture passive",
            "Groupes de travail", "Tutoriels vidéo", "Mind mapping", "Flashcards"
        ], default=["Fiches de révision", "Exercices pratiques"])

        st.markdown("#### 📱 Distractions & activités")
        ecrans  = st.slider("Temps sur les réseaux sociaux / vidéos (h/jour)", 0, 12, 2)
        jeux    = st.slider("Temps sur les jeux vidéo (h/jour)", 0, 12, 1)
        sport   = st.slider("Activité physique / sport (h/semaine)", 0, 20, 3)
        autres  = st.text_area("Autres activités ou problèmes à signaler", 
                               placeholder="Ex: travail à temps partiel, problèmes de transport, difficultés financières...")

        st.markdown("#### 🍽️ Bien-être général")
        stress  = st.select_slider("Niveau de stress ressenti", 
                                   options=["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"],
                                   value="Modéré")
        repas   = st.radio("Prenez-vous régulièrement 3 repas par jour ?", ["Oui", "Non", "Parfois"])
        transport = st.slider("Temps de trajet domicile–campus (minutes)", 0, 180, 30)

        submitted_hab = st.form_submit_button("💾 Enregistrer mes habitudes", use_container_width=True, type="primary")

    if submitted_hab:
        st.session_state["habitudes"] = {
            "sommeil": sommeil, "etude": etude_hors_cours,
            "revisions": revisions_avant, "ecrans": ecrans,
            "jeux": jeux, "sport": sport, "stress": stress,
            "repas": repas, "transport": transport,
            "methodes": methode_travail, "autres": autres
        }
        st.success("✅ Habitudes enregistrées ! Les conseils dans **Mes statistiques** en tiennent maintenant compte.")

        # Analyse immédiate des habitudes
        total_distractions = ecrans + jeux
        st.markdown("---")
        st.markdown("#### 📊 Analyse de vos habitudes")

        col1, col2, col3 = st.columns(3)
        col1.metric("Sommeil / nuit", f"{sommeil}h", 
                    delta="Optimal" if sommeil >= 7 else "Insuffisant",
                    delta_color="normal" if sommeil >= 7 else "inverse")
        col2.metric("Étude / jour", f"{etude_hors_cours}h",
                    delta="Bon rythme" if etude_hors_cours >= 3 else "À augmenter",
                    delta_color="normal" if etude_hors_cours >= 3 else "inverse")
        col3.metric("Distractions / jour", f"{total_distractions}h",
                    delta="Maîtrisé" if total_distractions <= 3 else "Trop élevé",
                    delta_color="normal" if total_distractions <= 3 else "inverse")

        # Graphique en anneau : répartition du temps
        autres_temps = max(0, 24 - sommeil - etude_hors_cours - total_distractions - transport / 60)
        labels_t = ["Sommeil", "Étude", "Distractions", "Transport", "Autre"]
        vals_t   = [sommeil, etude_hors_cours, total_distractions, round(transport/60, 1), round(autres_temps, 1)]
        fig_pie  = go.Figure(go.Pie(
            labels=labels_t, values=vals_t, hole=0.4,
            marker_colors=["#1a3a5c", "#2e7d32", "#c62828", "#f57c00", "#78909c"]
        ))
        fig_pie.update_layout(
            title="Répartition de votre journée (24h)", height=320,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ══════════════════════════════════════════════
#  ONGLET 4 — VUE GLOBALE
# ══════════════════════════════════════════════
with tab4:
    st.subheader("🌍 Statistiques globales — FST Yaoundé I")
    st.caption("Données illustratives basées sur les tendances observées. Mises à jour avec les vraies saisies.")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("#### Taux de réussite par filière")
        df_glob = pd.DataFrame({
            "Filière": list(GLOBAL_FILIERE_TAUX.keys()),
            "Taux (%)": list(GLOBAL_FILIERE_TAUX.values())
        })
        colors_glob = ["#2e7d32" if v >= 65 else "#f57c00" if v >= 50 else "#c62828"
                       for v in df_glob["Taux (%)"]]
        fig_glob = go.Figure(go.Bar(
            x=df_glob["Filière"], y=df_glob["Taux (%)"],
            marker_color=colors_glob,
            text=df_glob["Taux (%)"].apply(lambda x: f"{x}%"),
            textposition="outside"
        ))
        fig_glob.update_layout(
            height=300, yaxis=dict(range=[0, 100], title="Taux de réussite (%)"),
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_glob, use_container_width=True)

    with col_g2:
        st.markdown("#### Taux de validation par UE — Info L1 S1")
        df_ue_g = pd.DataFrame({
            "UE": list(GLOBAL_UE_TAUX.keys()),
            "Taux (%)": list(GLOBAL_UE_TAUX.values())
        }).sort_values("Taux (%)")
        colors_ue = ["#c62828" if v < 50 else "#f57c00" if v < 65 else "#2e7d32"
                     for v in df_ue_g["Taux (%)"]]
        fig_ue_g = go.Figure(go.Bar(
            x=df_ue_g["Taux (%)"], y=df_ue_g["UE"],
            orientation="h", marker_color=colors_ue,
            text=df_ue_g["Taux (%)"].apply(lambda x: f"{x}%"),
            textposition="outside"
        ))
        fig_ue_g.add_vline(x=50, line_dash="dash", line_color="#e65100")
        fig_ue_g.update_layout(
            height=300, xaxis=dict(range=[0, 100]),
            margin=dict(l=0, r=40, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_ue_g, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Données collectées (toutes saisies)")
    if st.session_state.historique:
        df_all = pd.DataFrame(st.session_state.historique)
        st.dataframe(df_all, use_container_width=True, hide_index=True)

        # Stats agrégées
        st.markdown("#### Analyse descriptive des données collectées")
        c1, c2, c3 = st.columns(3)
        c1.metric("Nombre de saisies", len(df_all))
        c2.metric("Moyenne générale", f"{df_all['Moyenne'].mean():.2f}")
        c3.metric("Taux de validation moyen", df_all['Taux validation'].str.replace('%','').astype(float).mean().round(1).astype(str) + "%")
    else:
        st.info("Aucune donnée collectée pour l'instant. Saisissez vos notes dans le premier onglet.")


# ══════════════════════════════════════════════
#  ONGLET 5 — EXPORT & HISTORIQUE
# ══════════════════════════════════════════════
with tab5:
    st.subheader("📥 Export des données & Historique")

    if "df_notes" not in st.session_state:
        st.info("👈 Saisissez vos notes pour pouvoir exporter.")
    else:
        df_notes = st.session_state["df_notes"]
        hab      = st.session_state.get("habitudes", None)

        st.markdown("#### Vos notes du semestre en cours")
        st.dataframe(df_notes, use_container_width=True, hide_index=True)

        # Export CSV notes
        csv_notes = df_notes.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇️ Télécharger mes notes (CSV)",
            data=csv_notes,
            file_name=f"EduStat_{nom or 'etudiant'}_{filiere.replace(' ','_')}_{semestre}.csv",
            mime="text/csv",
            use_container_width=True
        )

        if hab:
            st.markdown("#### Vos habitudes de vie enregistrées")
            df_hab = pd.DataFrame([hab])
            st.dataframe(df_hab, use_container_width=True, hide_index=True)

            csv_hab = df_hab.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="⬇️ Télécharger mes habitudes (CSV)",
                data=csv_hab,
                file_name=f"EduStat_habitudes_{nom or 'etudiant'}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Export rapport complet
        if hab:
            rapport_complet = f"""RAPPORT EDUSTAT — {nom or 'Étudiant'}
Filière   : {filiere}
Semestre  : {semestre}
Année     : {annee}
Date      : {datetime.now().strftime('%d/%m/%Y')}
══════════════════════════════════════
RÉSULTATS ACADÉMIQUES
Moyenne générale : {st.session_state['moy']:.2f}/20
UE validées      : {(df_notes['Note finale'] >= 10).sum()}/{len(df_notes)}
Taux validation  : {st.session_state['taux_val']}%
Statut           : {st.session_state['statut_global']}

HABITUDES DE VIE
Sommeil  : {hab['sommeil']}h/nuit
Étude    : {hab['etude']}h/jour
Écrans   : {hab['ecrans']}h/jour
Jeux     : {hab['jeux']}h/jour
Stress   : {hab['stress']}
══════════════════════════════════════
"""
            st.download_button(
                label="📄 Télécharger le rapport complet (TXT)",
                data=rapport_complet.encode("utf-8"),
                file_name=f"Rapport_EduStat_{nom or 'etudiant'}.txt",
                mime="text/plain",
                use_container_width=True
            )

    st.markdown("---")
    st.markdown("#### Historique des saisies")
    if st.session_state.historique:
        st.dataframe(pd.DataFrame(st.session_state.historique),
                     use_container_width=True, hide_index=True)
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.historique = []
            st.rerun()
    else:
        st.info("Aucune saisie enregistrée pour l'instant.")


# ─────────────────────────────────────────────
#  PIED DE PAGE
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.8rem;'>"
    "EduStat v1.0 · INF 232 EC2 · Université de Yaoundé I — Ngoa-Ekélé · FST"
    "</div>",
    unsafe_allow_html=True
)
