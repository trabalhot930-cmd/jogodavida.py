import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
from supabase import create_client

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Planejamento de Carreira", layout="wide")

# ─────────────────────────────────────────────
# ESTILO (AZUL + BOTÃO VERMELHO)
# ─────────────────────────────────────────────
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
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SUPABASE (COLOQUE SEUS DADOS)
# ─────────────────────────────────────────────
SUPABASE_URL = "https://SEU_PROJETO.supabase.co"
SUPABASE_KEY = "SUA_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
st.title("🛡️ Planejamento de Carreira")

# ─────────────────────────────────────────────
# CERTIFICAÇÕES (COM LOGOS)
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# REGISTRO
# ─────────────────────────────────────────────
st.subheader("🚀 Registrar Atividade")

atividade = st.selectbox("Tipo", [
    "Estudo", "Laboratório", "Projeto", "Inglês", "Networking"
])

obs = st.text_area("Observação")

if st.button("Salvar"):
    supabase.table("atividades").insert({
        "data": str(date.today()),
        "atividade": atividade,
        "obs": obs
    }).execute()

    st.success("Salvo!")

# ─────────────────────────────────────────────
# CARREGAR DADOS
# ─────────────────────────────────────────────
res = supabase.table("atividades").select("*").execute()
df = pd.DataFrame(res.data)

# ─────────────────────────────────────────────
# 📊 POWER BI STYLE (ALTAIR)
# ─────────────────────────────────────────────
st.subheader("📊 Dashboard")

if not df.empty:
    chart = alt.Chart(df).mark_bar().encode(
        x="data:T",
        y="count()",
        color="atividade:N",
        tooltip=["atividade", "count()"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

# ─────────────────────────────────────────────
# 🔥 HEATMAP
# ─────────────────────────────────────────────
st.subheader("🔥 Heatmap de Estudos")

if not df.empty:
    df["data"] = pd.to_datetime(df["data"])

    heat = alt.Chart(df).mark_rect().encode(
        x='date(data):O',
        y='month(data):O',
        color='count()'
    )

    st.altair_chart(heat, use_container_width=True)

# ─────────────────────────────────────────────
# 🧠 IA
# ─────────────────────────────────────────────
st.subheader("🧠 IA de Estudo")

def sugerir(df):
    if df.empty:
        return "Comece com fundamentos hoje."
    ult = df.iloc[-1]["atividade"]

    if ult == "Estudo":
        return "Faça laboratório amanhã."
    elif ult == "Laboratório":
        return "Construa um projeto."
    else:
        return "Volte para teoria."

st.info(sugerir(df))
