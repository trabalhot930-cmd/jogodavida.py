import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Carreira SaaS Pro",
    layout="wide",
    page_icon="🚀"
)

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
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

.card {
    background: white;
    color: black;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# BANCO SIMPLES (MODO MVP)
# =========================
if "db" not in st.session_state:
    st.session_state.db = []

# =========================
# LOGIN SIMPLES (SAAS DEMO)
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login SaaS Carreira Pro")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if email and senha:
            st.session_state.auth = True
            st.session_state.user = email
            st.rerun()
        else:
            st.error("Preencha os campos")

    st.stop()

# =========================
# HEADER
# =========================
st.title("🚀 Carreira SaaS Pro Dashboard")
st.caption(f"Usuário logado: {st.session_state.user}")

# =========================
# INPUT
# =========================
st.subheader("📌 Registrar atividade")

col1, col2 = st.columns(2)

with col1:
    atividade = st.selectbox(
        "Tipo de atividade",
        ["Estudo", "Laboratório", "Projeto", "Inglês", "Networking"]
    )

with col2:
    obs = st.text_area("Observação")

if st.button("Salvar atividade"):
    st.session_state.db.append({
        "data": str(date.today()),
        "atividade": atividade,
        "obs": obs
    })
    st.success("Atividade salva!")

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(st.session_state.db)

# =========================
# KPIs
# =========================
st.subheader("📊 KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total atividades", len(df))

if not df.empty:
    col2.metric("Estudos", len(df[df["atividade"] == "Estudo"]))
    col3.metric("Labs", len(df[df["atividade"] == "Laboratório"]))
else:
    col2.metric("Estudos", 0)
    col3.metric("Labs", 0)

# =========================
# DASHBOARD
# =========================
st.subheader("📈 Evolução")

if not df.empty:
    df["data"] = pd.to_datetime(df["data"])

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="data:T",
        y="count():Q",
        color="atividade:N",
        tooltip=["atividade"]
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)

# =========================
# DISTRIBUIÇÃO
# =========================
st.subheader("📊 Distribuição")

if not df.empty:
    pie = alt.Chart(df).mark_arc().encode(
        theta="count()",
        color="atividade:N"
    )

    st.altair_chart(pie, use_container_width=True)

# =========================
# IA COACH (SIMPLIFICADA)
# =========================
st.subheader("🧠 IA Coach")

def coach(df):
    if df.empty:
        return "Comece com estudo básico e consistência diária."

    last = df.iloc[-1]["atividade"]

    if last == "Estudo":
        return "Agora faça um laboratório prático real."
    elif last == "Laboratório":
        return "Transforme isso em um projeto GitHub."
    elif last == "Projeto":
        return "Documente e publique seu projeto."
    else:
        return "Mantenha consistência diária e evolução contínua."

st.info(coach(df))

# =========================
# CERTIFICAÇÕES ROADMAP
# =========================
st.subheader("🏅 Roadmap de Certificações")

certs = [
    "AZ-900",
    "ISO 27001",
    "Security+",
    "CCNA",
    "CySA+",
    "GICSP"
]

cols = st.columns(3)

for i, c in enumerate(certs):
    with cols[i % 3]:
        st.markdown(f"<div class='card'>{c}</div>", unsafe_allow_html=True)
