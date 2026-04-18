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
# ESTILO SaaS CLEAN
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
}

.card {
    background: white;
    color: black;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
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

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    st.title("🔐 Carreira SaaS Pro")

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
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio("📌 Menu", ["Dashboard", "Roadmap"])

st.sidebar.success(f"Usuário: {st.session_state.user}")

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("🚀 Dashboard de Evolução")

    atividade = st.selectbox(
        "Atividade",
        ["Estudo", "Laboratório", "Projeto", "Inglês", "Networking"]
    )

    obs = st.text_area("Observação")

    if st.button("Salvar"):
        st.session_state.db.append({
            "data": str(date.today()),
            "atividade": atividade,
            "obs": obs
        })

    df = pd.DataFrame(st.session_state.db)

    st.subheader("📊 KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total", len(df))

    if not df.empty:
        col2.metric("Estudos", len(df[df["atividade"] == "Estudo"]))
        col3.metric("Labs", len(df[df["atividade"] == "Laboratório"]))
    else:
        col2.metric("Estudos", 0)
        col3.metric("Labs", 0)

    st.subheader("📈 Evolução")

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])

        chart = alt.Chart(df).mark_line(point=True).encode(
            x="data:T",
            y="count():Q",
            color="atividade:N"
        )

        st.altair_chart(chart, use_container_width=True)

    # IA simples
    st.subheader("🧠 IA Coach")

    def coach(df):
        if df.empty:
            return "Comece com consistência diária."

        last = df.iloc[-1]["atividade"]

        if last == "Estudo":
            return "Faça um laboratório prático agora."
        elif last == "Laboratório":
            return "Transforme em projeto GitHub."
        elif last == "Projeto":
            return "Documente e publique."
        else:
            return "Continue evoluindo."

    st.info(coach(df))

# =========================
# ROADMAP
# =========================
if menu == "Roadmap":

    st.title("🛡️ Roadmap de Carreira 2026–2029")

    # =========================
    # 2026
    # =========================
    st.subheader("📅 2026 — BASE + INÍCIO DA PÓS")

    st.markdown("### 🎯 Certificações")

    certs_2026 = [
        "AZ-900",
        "ISO 27001 Fundamentals",
        "CCNA",
        "SC-900"
    ]

    for c in certs_2026:
        st.markdown(f"<div class='card'>🏅 {c}</div>", unsafe_allow_html=True)

    st.markdown("""
    🎓 Pós-graduação: Início Junho/2026  
    🌍 Inglês: diário (30–40 min)
    """)

    st.divider()

    # =========================
    # 2027
    # =========================
    st.subheader("📅 2027 — SEGURANÇA + OT")

    certs_2027 = [
        "CompTIA Security+",
        "ISO 27001 Lead Implementer",
        "ISA/IEC 62443",
        "MITRE ATT&CK ICS",
        "CySA+"
    ]

    for c in certs_2027:
        st.markdown(f"<div class='card'>🛡️ {c}</div>", unsafe_allow_html=True)

    st.markdown("""
    🎓 Pós-graduação: continuidade  
    🌍 Inglês: técnico (documentação)
    """)

    st.divider()

    # =========================
    # 2028
    # =========================
    st.subheader("📅 2028 — ESPECIALIZAÇÃO")

    certs_2028 = [
        "GICSP",
        "ISO 27001 Lead Auditor"
    ]

    for c in certs_2028:
        st.markdown(f"<div class='card'>🔥 {c}</div>", unsafe_allow_html=True)

    st.markdown("""
    🎓 Pós-graduação: conclusão até Dez/2028  
    🌍 Inglês: conversação + entrevistas
    """)

    st.divider()

    # =========================
    # 2029
    # =========================
    st.subheader("📅 2029 — CONSOLIDAÇÃO")

    st.markdown("<div class='card'>🏆 CISSP</div>", unsafe_allow_html=True)

    st.markdown("""
    🌍 Inglês: fluência funcional  
    💼 foco: entrevistas e mercado internacional
    """)

# =========================
# FOOTER
# =========================
st.sidebar.markdown("---")
st.sidebar.info("🚀 Sistema SaaS Carreira Pro")
