import streamlit as st
import pandas as pd
import altair as alt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Planejamento de carreira Juan Felipe da Silva", layout="wide")

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
if "db" not in st.session_state:
    st.session_state.db = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "progress" not in st.session_state:
    st.session_state.progress = {
        "AZ-900": {"status": "Concluindo", "icon": "☁️"},
        "ISO 27001": {"status": "Em andamento", "icon": "🔐"},
        "CCNA": {"status": "Em andamento", "icon": "🌐"},
        "SC-900": {"status": "Não iniciado", "icon": "🛡️"},
        "Python": {"status": "Em andamento", "icon": "🐍"},
        "SQL": {"status": "Em andamento", "icon": "🗄️"},
        "Power BI": {"status": "Em andamento", "icon": "📊"},
        "Security+": {"status": "Não iniciado", "icon": "🔒"},
        "CySA+": {"status": "Não iniciado", "icon": "🧠"},
        "GICSP": {"status": "Não iniciado", "icon": "🏭"},
        "CISSP": {"status": "Não iniciado", "icon": "🎯"}
    }

# =========================
# HEADER
# =========================
st.title("📘 Planejamento de carreira Juan Felipe da Silva")

st.caption(f"⭐ XP: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# ABAS
# =========================
tab1, tab2, tab3 = st.tabs(["🎓 Dashboard", "🛣️ Roadmap", "📆 Calendário"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:

    st.subheader("📌 Registro de estudos")

    col1, col2 = st.columns(2)

    with col1:
        cert = st.selectbox(
            "Certificação / Curso",
            list(st.session_state.progress.keys())
        )

        atividade = st.selectbox(
            "Atividade",
            ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado"]
        )

    with col2:
        data = st.date_input("Data", value=pd.Timestamp.today())
        obs = st.text_area("Observação")

    if st.button("Salvar"):
        st.session_state.db.append({
            "data": pd.to_datetime(data),
            "certificacao": cert,
            "atividade": atividade,
            "obs": obs
        })

        st.session_state.xp += 10
        st.success("+10 XP!")

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
    # PROGRESSO (NOVO FORMATO)
    # =========================
    st.subheader("🎓 Progresso das Certificações")

    for cert, info in st.session_state.progress.items():
        st.markdown(f"""
        ### {info['icon']} {cert}  
        **Status:** {info['status']}
        """)

    # =========================
    # HISTÓRICO
    # =========================
    st.subheader("📚 Histórico filtrado")

    if not df.empty:

        filtro = st.selectbox("Filtrar por certificação", df["certificacao"].unique())

        df_f = df[df["certificacao"] == filtro]

        st.dataframe(df_f, use_container_width=True)

        timeline = df_f.groupby("data").size().reset_index(name="atividades")

        chart = alt.Chart(timeline).mark_line(point=True).encode(
            x="data:T",
            y="atividades:Q",
            tooltip=["data", "atividades"]
        )

        st.altair_chart(chart, use_container_width=True)

    # =========================
    # EXPORTAÇÃO
    # =========================
    st.subheader("📤 Exportar dados")

    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Baixar CSV do progresso",
            csv,
            "planejamento_carreira_juan_felipe.csv",
            "text/csv"
        )

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:

    st.title("🛣️ Roadmap de Carreira")

    st.subheader("📅 2026 — BASE + FORMAÇÃO")

    st.markdown("""
- ☁️ AZ-900  
- 🔐 ISO 27001 Fundamentals  
- 🌐 CCNA  
- 🛡️ SC-900  

🐍 Python  
🗄️ SQL  
📊 Power BI  

🎓 Pós-graduação: início Junho/2026  
🌍 Inglês diário
""")

    st.divider()

    st.subheader("📅 2027 — SEGURANÇA + OT")

    st.markdown("""
- 🔒 Security+  
- ISO 27001 Lead Implementer  
- ISA/IEC 62443  
- CySA+
""")

    st.divider()

    st.subheader("📅 2028 — ESPECIALIZAÇÃO")

    st.markdown("""
- 🏭 GICSP  
- ISO 27001 Lead Auditor
""")

    st.divider()

    st.subheader("📅 2029 — CONSOLIDAÇÃO")

    st.markdown("""
- 🎯 CISSP  
- Inglês fluente profissional
""")

# =========================
# TAB 3 - CALENDÁRIO
# =========================
with tab3:

    st.title("📆 Calendário de Atividades")

    df = pd.DataFrame(st.session_state.db)

    if not df.empty:

        st.subheader("📊 Linha do tempo")

        timeline = df.groupby("data").size().reset_index(name="atividades")

        chart = alt.Chart(timeline).mark_bar().encode(
            x="data:T",
            y="atividades:Q",
            tooltip=["data", "atividades"]
        )

        st.altair_chart(chart, use_container_width=True)

        st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)

    else:
        st.info("Nenhuma atividade registrada ainda.")
