import streamlit as st
import pandas as pd
import altair as alt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Carreira SaaS RPG", layout="wide")

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

.card {
    background: white;
    color: black;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    margin-bottom: 6px;
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
        "AZ-900": 30,
        "ISO 27001": 15,
        "CCNA": 10,
        "Security+": 5,
        "CySA+": 0,
        "GICSP": 0,
        "CISSP": 0
    }

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    st.title("🔐 Carreira SaaS RPG")

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
st.title("🚀 Carreira SaaS RPG Dashboard")

st.caption(f"👤 {st.session_state.user} | ⭐ XP: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# INPUT
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

if st.button("Salvar atividade"):
    st.session_state.db.append({
        "data": str(pd.Timestamp.today().date()),
        "atividade": atividade,
        "obs": obs
    })
    st.session_state.xp += 10
    st.success("Atividade salva +10 XP!")

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
col2.metric("XP total", st.session_state.xp)
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
else:
    st.info("Sem dados ainda.")

# =========================
# PROGRESSO CERTIFICAÇÕES
# =========================
st.subheader("🎮 Certificações (RPG)")

for cert, value in st.session_state.progress.items():
    st.markdown(f"**{cert}**")
    st.progress(value / 100)

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

# =========================
# IA SIMULADA (SEM OPENAI)
# =========================
st.subheader("🧠 IA Coach (Offline)")

def coach():
    if df.empty:
        return "Comece com estudo diário e consistência."

    last = df.iloc[-1]["atividade"]

    if last == "Estudo":
        return "👉 Próximo passo: laboratório prático"
    if last == "Laboratório":
        return "👉 Transforme isso em projeto GitHub"
    if last == "Projeto":
        return "👉 Documente e publique"
    return "👉 Continue evoluindo com consistência"

st.info(coach())
