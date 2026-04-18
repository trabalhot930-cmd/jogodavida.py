import streamlit as st
import pandas as pd
import altair as alt

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
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = st.text_input("Digite seu nome")

if "db" not in st.session_state:
    st.session_state.db = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if not st.session_state.user:
    st.stop()

st.title("🌍 Ranking de Disciplina (Versão Local)")

st.success(f"Logado como: {st.session_state.user}")

# =========================
# MENU
# =========================
menu = st.sidebar.radio("Menu", ["Dashboard", "Ranking"])

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

    obs = st.text_area("Observação")

    if st.button("Salvar + XP"):
        st.session_state.db.append({
            "user": st.session_state.user,
            "cert": cert,
            "activity": activity,
            "date": str(pd.Timestamp.today().date()),
            "xp": 10,
            "obs": obs
        })

        st.session_state.xp += 10
        st.success("+10 XP!")

    df = pd.DataFrame(st.session_state.db)

    st.subheader("📊 Seu histórico")

    user_df = df[df["user"] == st.session_state.user] if not df.empty else df

    if not user_df.empty:
        st.dataframe(user_df)

        chart = alt.Chart(user_df).mark_bar().encode(
            x="cert:N",
            y="xp:Q",
            color="cert:N"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sem registros ainda.")

# =========================
# RANKING GLOBAL (LOCAL SIMULADO)
# =========================
if menu == "Ranking":

    st.subheader("🏆 Ranking de Disciplina")

    df = pd.DataFrame(st.session_state.db)

    if not df.empty:

        ranking = df.groupby("user")["xp"].sum().reset_index()
        ranking = ranking.sort_values("xp", ascending=False)

        st.dataframe(ranking, use_container_width=True)

        st.bar_chart(ranking.set_index("user"))

    else:
        st.info("Ainda não há dados para ranking.")
