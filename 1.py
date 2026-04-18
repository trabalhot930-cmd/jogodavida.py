import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from datetime import date

# CONFIG
st.set_page_config(page_title="Planejamento de Carreira", layout="wide")

# ESTILO (AZUL + BOTÃO VERMELHO)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1f44, #0d2b6b);
    color: #e6f0ff;
}

.stButton button {
    background-color: #d32f2f !important;
    color: white !important;
    font-weight: bold;
    border-radius: 8px;
}

.cert {
    background: white;
    color: black;
    padding: 5px;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# BANCO LOCAL (SEM ERRO)
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

# LOGIN
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if u == "Juan" and p == "Ju@n1990":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Erro")
    st.stop()

# TÍTULO
st.title("🛡️ Planejamento de Carreira")

# CERTIFICAÇÕES (LOGOS REAIS)
st.subheader("🏅 Certificações")

certs = [
    ("AZ-900", "https://img.icons8.com/color/96/azure-1.png"),
    ("ISO 27001", "https://img.icons8.com/color/96/security-checked.png"),
    ("CCNA", "https://img.icons8.com/color/96/cisco.png"),
    ("Security+", "https://img.icons8.com/color/96/security-lock.png"),
    ("CySA+", "https://img.icons8.com/color/96/artificial-intelligence.png"),
    ("GICSP", "https://img.icons8.com/color/96/factory.png"),
]

cols = st.columns(3)

for i, (nome, img) in enumerate(certs):
    with cols[i % 3]:
        st.image(img, width=60)
        st.markdown(f"<div class='cert'>{nome}</div>", unsafe_allow_html=True)

# REGISTRAR
st.subheader("🚀 Registrar Atividade")

atividade = st.selectbox("Tipo", [
    "Estudo", "Laboratório", "Projeto", "Inglês", "Networking"
])

obs = st.text_area("Observação")

if st.button("Salvar"):
    c.execute("INSERT INTO atividades VALUES (?,?,?)",
              (str(date.today()), atividade, obs))
    conn.commit()
    st.success("Salvo!")

# DADOS
df = pd.read_sql("SELECT * FROM atividades", conn)

# 📊 DASHBOARD POWER BI (ALTAIR)
st.subheader("📊 Dashboard")

if not df.empty:
    chart = alt.Chart(df).mark_bar().encode(
        x="data:T",
        y="count()",
        color="atividade:N",
        tooltip=["atividade", "count()"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

# 🔥 HEATMAP
st.subheader("🔥 Heatmap")

if not df.empty:
    df["data"] = pd.to_datetime(df["data"])

    heat = alt.Chart(df).mark_rect().encode(
        x='date(data):O',
        y='month(data):O',
        color='count()'
    )

    st.altair_chart(heat, use_container_width=True)

# 🧠 IA
st.subheader("🧠 Sugestão")

def sugerir(df):
    if df.empty:
        return "Comece com fundamentos hoje."
    ult = df.iloc[-1]["atividade"]

    if ult == "Estudo":
        return "Faça laboratório amanhã."
    elif ult == "Laboratório":
        return "Construa um projeto."
    else:
        return "Revise teoria."

st.info(sugerir(df))
