import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

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

.stButton button {
    background-color: #e53935 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE (FIX CRÍTICO)
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = None

if "db" not in st.session_state:
    st.session_state.db = []

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    st.title("🔐 Login - Carreira SaaS Pro")

    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user and pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Preencha os campos")

    st.stop()

# =========================
# HEADER
# =========================
st.title("🚀 Carreira SaaS Pro Dashboard")

st.caption(f"👤 Usuário logado: {st.session_state.get('user', 'guest')}")

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
    st.success("Salvo com sucesso!")

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
# GRÁFICO EVOLUÇÃO
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
else:
    st.info("Sem dados ainda para gráfico.")

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
# IA COACH (SEM ERRO OPENAI)
# =========================
st.subheader("🧠 IA Coach")

def coach(df):
    if df.empty:
        return "Comece com estudo diário e consistência."

    last = df.iloc[-1]["atividade"]

    if last == "Estudo":
        return "Agora faça um laboratório prático real."
    elif last == "Laboratório":
        return "Transforme isso em um projeto GitHub."
    elif last == "Projeto":
        return "Documente e publique seu projeto."
    else:
        return "Mantenha consistência e evolução contínua."

st.info(coach(df))

# =========================
# ROADMAP
# =========================
st.subheader("🏅 Roadmap Certificações")

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
        st.markdown(
            f"<div style='background:white;color:black;padding:10px;border-radius:10px;text-align:center;font-weight:bold'>{c}</div>",
            unsafe_allow_html=True
        )
