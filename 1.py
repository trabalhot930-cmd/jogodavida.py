import streamlit as st
import pandas as pd
import altair as alt
from supabase import create_client
import os

# =========================
# SUPABASE
# =========================
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Ranking Global SaaS", layout="wide")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
html, body {
    background: linear-gradient(135deg, #061a3a, #0c2f6e);
    color: #e6f0ff;
}

.block-container {
    padding-top: 2rem;
}

.stButton button {
    background-color: #e53935 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN SIMPLES
# =========================
st.title("🌍 Ranking Global de Disciplina")

if "user" not in st.session_state:
    st.session_state.user = st.text_input("Digite seu nome")

user = st.session_state.user

if not user:
    st.stop()

st.success(f"Logado como: {user}")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio("Menu", ["Dashboard", "Ranking Global"])

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.subheader("📌 Registrar atividade")

    cert = st.selectbox(
        "Certificação / Curso",
        ["AZ-900", "CCNA", "Security+", "Python", "SQL", "Power BI", "ISO 27001"]
    )

    activity = st.selectbox(
        "Atividade",
        ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado"]
    )

    xp_gain = 10

    if st.button("Salvar + XP"):
        supabase.table("activities").insert({
            "user_name": user,
            "cert": cert,
            "activity": activity,
            "date": str(pd.Timestamp.today().date()),
            "xp": xp_gain
        }).execute()

        st.success("+10 XP registrado!")

    # =========================
    # HISTÓRICO DO USUÁRIO
    # =========================
    data = supabase.table("activities").select("*").eq("user_name", user).execute().data

    df = pd.DataFrame(data)

    st.subheader("📊 Seu histórico")

    if not df.empty:
        st.dataframe(df)

        st.bar_chart(df.groupby("cert")["xp"].sum())
    else:
        st.info("Sem registros ainda.")

# =========================
# RANKING GLOBAL
# =========================
if menu == "Ranking Global":

    st.subheader("🏆 Leaderboard Global")

    data = supabase.table("activities").select("*").execute().data
    df = pd.DataFrame(data)

    if not df.empty:

        ranking = df.groupby("user_name")["xp"].sum().reset_index()
        ranking = ranking.sort_values("xp", ascending=False)

        st.dataframe(ranking, use_container_width=True)

        chart = alt.Chart(ranking).mark_bar().encode(
            x="user_name:N",
            y="xp:Q",
            color="user_name:N"
        )

        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("Ainda não há dados no ranking global.")
