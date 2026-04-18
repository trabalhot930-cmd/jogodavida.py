import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from datetime import date
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Carreira Pro Dashboard",
    layout="wide",
    page_icon="🛡️"
)

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #071a3a, #0c2f6e);
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
    padding: 0.5rem 1rem;
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
# BANCO DE DADOS
# =========================
conn = sqlite3.connect("carreira.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS atividades (
    data TEXT,
    atividade TEXT,
    obs TEXT
)
""")
conn.commit()

# =========================
# LOGIN SIMPLES
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login Sistema Carreira Pro")

    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == "Juan" and pwd == "Ju@n1990":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Credenciais inválidas")
    st.stop()

# =========================
# HEADER
# =========================
st.title("🛡️ Carreira Pro Dashboard")
st.caption("Planejamento + Métricas + Evolução Profissional")

# =========================
# REGISTRO
# =========================
st.subheader("🚀 Registrar atividade")

col1, col2 = st.columns(2)

with col1:
    atividade = st.selectbox("Tipo de atividade", [
        "Estudo", "Laboratório", "Projeto", "Inglês", "Networking"
    ])

with col2:
    obs = st.text_area("Observação")

if st.button("Salvar atividade"):
    c.execute(
        "INSERT INTO atividades VALUES (?,?,?)",
        (str(date.today()), atividade, obs)
    )
    conn.commit()
    st.success("Atividade registrada com sucesso!")

# =========================
# DADOS
# =========================
df = pd.read_sql("SELECT * FROM atividades", conn)

if not df.empty:
    df["data"] = pd.to_datetime(df["data"])

# =========================
# KPIs
# =========================
st.subheader("📊 KPIs")

col1, col2, col3 = st.columns(3)

total = len(df)
estudos = len(df[df["atividade"] == "Estudo"])
labs = len(df[df["atividade"] == "Laboratório"])

col1.metric("Total atividades", total)
col2.metric("Estudos", estudos)
col3.metric("Labs", labs)

# =========================
# FILTRO
# =========================
st.subheader("🎯 Filtros")

if not df.empty:
    filtro = st.multiselect(
        "Filtrar atividades",
        df["atividade"].unique(),
        default=df["atividade"].unique()
    )

    df = df[df["atividade"].isin(filtro)]

# =========================
# GRÁFICO EVOLUÇÃO
# =========================
st.subheader("📈 Evolução diária")

if not df.empty:
    chart = alt.Chart(df).mark_line(point=True).encode(
        x="data:T",
        y="count():Q",
        color="atividade:N",
        tooltip=["atividade", "count()"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

# =========================
# DISTRIBUIÇÃO
# =========================
st.subheader("📊 Distribuição de esforço")

if not df.empty:
    pie = alt.Chart(df).mark_arc().encode(
        theta="count()",
        color="atividade:N",
        tooltip=["atividade", "count()"]
    )

    st.altair_chart(pie, use_container_width=True)

# =========================
# IA SIMPLES (OPCIONAL OPENAI)
# =========================
st.subheader("🧠 IA de planejamento")

def sugestao(df):
    if df.empty:
        return "Comece com fundamentos (Estudo + prática diária)."

    ultimo = df.iloc[-1]["atividade"]

    if ultimo == "Estudo":
        return "Agora faça um laboratório prático."
    if ultimo == "Laboratório":
        return "Transforme isso em um projeto real."
    if ultimo == "Projeto":
        return "Documente e publique no GitHub."
    return "Mantenha consistência diária."

st.info(sugestao(df))

# =========================
# CERTIFICAÇÕES
# =========================
st.subheader("🏅 Trilha de certificações")

certs = [
    "AZ-900",
    "ISO 27001",
    "CCNA",
    "Security+",
    "CySA+",
    "GICSP"
]

cols = st.columns(3)

for i, cft in enumerate(certs):
    with cols[i % 3]:
        st.markdown(f"<div class='card'>{cft}</div>", unsafe_allow_html=True)
