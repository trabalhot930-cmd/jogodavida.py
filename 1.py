import streamlit as st
import pandas as pd
import altair as alt
import os
import openai

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Carreira SaaS Pro", layout="wide")

# =========================
# OPENAI CONFIG (GIT SAFE)
# =========================
openai.api_key = os.getenv("OPENAI_API_KEY")

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
if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = None

if "db" not in st.session_state:
    st.session_state.db = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "progress" not in st.session_state:
    st.session_state.progress = {
        "AZ-900": 20,
        "ISO 27001": 10,
        "CCNA": 0,
        "Security+": 0,
        "CySA+": 0,
        "GICSP": 0,
        "CISSP": 0
    }

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    st.title("🔐 Login SaaS Carreira Pro")

    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user and pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()

    st.stop()

# =========================
# HEADER
# =========================
st.title("🚀 Carreira SaaS Pro")

st.caption(f"👤 Usuário: {st.session_state.get('user','guest')} | ⭐ XP: {st.session_state.xp}")

# =========================
# INPUT ATIVIDADES
# =========================
st.subheader("📌 Registrar atividade")

col1, col2 = st.columns(2)

with col1:
    atividade = st.selectbox(
        "Atividade",
        ["Estudo", "Laboratório", "Projeto", "Inglês", "Networking"]
    )

with col2:
    obs = st.text_area("Observação")

if st.button("Salvar"):
    st.session_state.db.append({
        "data": str(pd.Timestamp.today().date()),
        "atividade": atividade,
        "obs": obs
    })
    st.session_state.xp += 10
    st.success("Salvo!")

df = pd.DataFrame(st.session_state.db)

# =========================
# KPIs
# =========================
st.subheader("📊 KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total atividades", len(df))
col2.metric("XP", st.session_state.xp)
col3.metric("Level", st.session_state.xp // 100 + 1)

# =========================
# GRÁFICO
# =========================
st.subheader("📈 Evolução")

if not df.empty:
    df["data"] = pd.to_datetime(df["data"])

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="data:T",
        y="count():Q",
        color="atividade:N"
    )

    st.altair_chart(chart, use_container_width=True)

# =========================
# PROGRESSO CERTIFICAÇÕES (RPG)
# =========================
st.subheader("🎮 Progresso de Certificações")

for k, v in st.session_state.progress.items():
    st.write(f"**{k}**")
    st.progress(v / 100)

# =========================
# IA COACH SEMANAL
# =========================
st.subheader("🤖 IA Planejador Semanal")

def gerar_plano():
    if openai.api_key is None:
        return "⚠️ Configure OPENAI_API_KEY no Git Secrets"

    prompt = f"""
Você é um coach de carreira em segurança da informação.

Progresso do usuário:
{st.session_state.progress}

Atividades recentes:
{df.tail(5).to_string() if not df.empty else "Nenhuma"}

Crie um plano semanal detalhado (segunda a domingo)
com foco em certificações e prática.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um mentor de TI."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]

if st.button("Gerar plano semanal"):
    st.info(gerar_plano())

# =========================
# RANKING DE DISCIPLINA
# =========================
st.subheader("🏆 Ranking de Disciplina")

score = len(df) * 5 + st.session_state.xp

ranking = pd.DataFrame([
    {"Usuário": st.session_state.user, "Score": score},
    {"Usuário": "Aluno A", "Score": 120},
    {"Usuário": "Aluno B", "Score": 90},
    {"Usuário": "Aluno C", "Score": 60}
]).sort_values("Score", ascending=False)

st.dataframe(ranking, use_container_width=True)
st.bar_chart(ranking.set_index("Usuário"))
