import streamlit as st
import pandas as pd
import altair as alt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Carreira RPG Pro", layout="wide")

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
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
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
# HEADER
# =========================
st.title("🚀 Carreira RPG SaaS - Tracker Pessoal")

st.caption(f"⭐ XP: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# ABAS
# =========================
tab1, tab2 = st.tabs(["🎮 Dashboard RPG", "🛣️ Roadmap Carreira"])

# =========================
# TAB 1 - DASHBOARD RPG
# =========================
with tab1:

    st.subheader("📌 Registrar estudo por certificação")

    col1, col2 = st.columns(2)

    with col1:
        cert = st.selectbox(
            "Certificação",
            list(st.session_state.progress.keys())
        )

        atividade = st.selectbox(
            "Tipo de atividade",
            ["Estudo", "Laboratório", "Revisão", "Projeto", "Simulado"]
        )

    with col2:
        data = st.date_input("Data", value=pd.Timestamp.today())
        obs = st.text_area("Observação do dia")

    if st.button("Salvar registro"):
        st.session_state.db.append({
            "data": str(data),
            "certificacao": cert,
            "atividade": atividade,
            "obs": obs
        })

        st.session_state.xp += 10
        st.success("+10 XP ganho!")

    df = pd.DataFrame(st.session_state.db)

    # =========================
    # KPIs
    # =========================
    st.subheader("📊 KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Registros", len(df))
    col2.metric("XP", st.session_state.xp)
    col3.metric("Level", st.session_state.xp // 100 + 1)

    # =========================
    # PROGRESSO CERTIFICAÇÕES
    # =========================
    st.subheader("🎮 Progresso das Certificações")

    for c, v in st.session_state.progress.items():
        st.write(f"**{c}**")
        st.progress(v / 100)

    # =========================
    # FILTRO POR CERTIFICAÇÃO
    # =========================
    st.subheader("📚 Histórico por Certificação")

    if not df.empty:

        filtro = st.selectbox(
            "Selecionar certificação",
            df["certificacao"].unique()
        )

        df_f = df[df["certificacao"] == filtro].copy()
        df_f["data"] = pd.to_datetime(df_f["data"])

        st.dataframe(df_f, use_container_width=True)

        # =========================
        # GRÁFICO
        # =========================
        chart = alt.Chart(df_f).mark_line(point=True).encode(
            x="data:T",
            y="count():Q",
            color="atividade:N",
            tooltip=["atividade", "obs"]
        )

        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("Nenhum registro ainda.")

    # =========================
    # DISCIPLINA SCORE
    # =========================
    st.subheader("🏆 Score de Disciplina")

    score = len(df) * 5 + st.session_state.xp

    st.metric("Seu score", score)

    st.progress(min(score / 300, 1.0))

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:

    st.title("🛣️ Roadmap de Carreira 2026–2029")

    st.subheader("📅 2026 — BASE + INÍCIO DA PÓS")

    st.markdown("""
- AZ-900 (Abril/2026)  
- ISO 27001 Fundamentals (Maio/2026)  
- CCNA (Julho/2026)  
- SC-900 (Outubro/2026)  

🎓 Pós-graduação: Início Junho/2026  
🌍 Inglês: diário (30–40 min)
""")

    st.divider()

    st.subheader("📅 2027 — SEGURANÇA + OT")

    st.markdown("""
- Security+ (Fevereiro/2027)  
- ISO 27001 Lead Implementer (Maio/2027)  
- ISA/IEC 62443 (Agosto/2027)  
- MITRE ATT&CK ICS (contínuo)  
- CySA+ (Dezembro/2027)  

🌍 Inglês técnico
""")

    st.divider()

    st.subheader("📅 2028 — ESPECIALIZAÇÃO")

    st.markdown("""
- GICSP (Março/2028)  
- ISO 27001 Lead Auditor (Agosto/2028)  

🎓 Pós-graduação: conclusão Dez/2028  
🌍 Inglês: entrevistas e conversação
""")

    st.divider()

    st.subheader("📅 2029 — CONSOLIDAÇÃO")

    st.markdown("""
- CISSP (Junho/2029)  

🌍 Inglês fluente funcional  
💼 entrevistas internacionais
""")
       
