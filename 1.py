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
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = st.text_input("Digite seu nome")

if "db" not in st.session_state:
    st.session_state.db = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "progress" not in st.session_state:
    st.session_state.progress = {
        "AZ-900": 30,
        "ISO 27001": 15,
        "CCNA": 10,
        "SC-900": 0,
        "Python": 0,
        "SQL": 0,
        "Power BI": 0,
        "Security+": 0,
        "CySA+": 0,
        "GICSP": 0,
        "CISSP": 0
    }

if not st.session_state.user:
    st.stop()

st.title("🚀 Carreira RPG Pro - Sistema Completo")

st.caption(f"👤 {st.session_state.user} | ⭐ XP: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# ABAS
# =========================
tab1, tab2, tab3 = st.tabs(["🎮 Dashboard", "🛣️ Roadmap", "📆 Calendário"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:

    st.subheader("📌 Registrar estudo")

    col1, col2 = st.columns(2)

    with col1:
        cert = st.selectbox(
            "Certificação / Curso",
            list(st.session_state.progress.keys())
        )

        activity = st.selectbox(
            "Atividade",
            ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado"]
        )

    with col2:
        data = st.date_input("Data", value=pd.Timestamp.today())
        obs = st.text_area("Observação do dia")

    if st.button("Salvar registro"):
        st.session_state.db.append({
            "user": st.session_state.user,
            "certificacao": cert,
            "atividade": activity,
            "data": str(data),
            "obs": obs,
            "xp": 10
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
    # PROGRESSO
    # =========================
    st.subheader("🎮 Progresso de Certificações")

    for k, v in st.session_state.progress.items():
        st.write(f"**{k}**")
        st.progress(v / 100)

    # =========================
    # HISTÓRICO FILTRADO
    # =========================
    st.subheader("📚 Histórico por Certificação")

    if not df.empty:

        filtro = st.selectbox("Filtrar certificação", df["certificacao"].unique())

        df_f = df[df["certificacao"] == filtro].copy()
        df_f["data"] = pd.to_datetime(df_f["data"])

        st.dataframe(df_f, use_container_width=True)

        chart = alt.Chart(df_f).mark_line(point=True).encode(
            x="data:T",
            y="xp:Q",
            color="atividade:N",
            tooltip=["atividade", "obs"]
        )

        st.altair_chart(chart, use_container_width=True)

        # =========================
        # EXPORT CSV
        # =========================
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Baixar progresso CSV",
            csv,
            "carreira_progresso.csv",
            "text/csv"
        )

    else:
        st.info("Nenhum registro ainda.")

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:

    st.title("🛣️ Roadmap de Carreira 2026–2029")

    st.subheader("📅 2026 — BASE + FORMAÇÃO")

    st.markdown("""
- AZ-900  
- ISO 27001 Fundamentals  
- CCNA  
- SC-900  

📘 Python (Formação continuada)  
📊 SQL (Formação continuada)  
📈 Power BI (Formação continuada)  

🎓 Pós-graduação: início Junho/2026  
🌍 Inglês: diário
""")

    st.divider()

    st.subheader("📅 2027 — SEGURANÇA + OT")

    st.markdown("""
- Security+  
- ISO 27001 Lead Implementer  
- ISA/IEC 62443  
- CySA+  
""")

    st.divider()

    st.subheader("📅 2028 — ESPECIALIZAÇÃO")

    st.markdown("""
- GICSP  
- ISO 27001 Lead Auditor  
- conclusão pós-graduação
""")

    st.divider()

    st.subheader("📅 2029 — CONSOLIDAÇÃO")

    st.markdown("""
- CISSP  
- Inglês fluente profissional
""")

# =========================
# TAB 3 - CALENDÁRIO
# =========================
with tab3:

    st.title("📆 Calendário de Atividades")

    df = pd.DataFrame(st.session_state.db)

    if not df.empty:

        df["data"] = pd.to_datetime(df["data"])

        timeline = df.groupby("data").size().reset_index(name="atividades")

        st.subheader("📊 Linha do tempo")

        chart = alt.Chart(timeline).mark_bar().encode(
            x="data:T",
            y="atividades:Q",
            tooltip=["data", "atividades"]
        )

        st.altair_chart(chart, use_container_width=True)

        st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)

    else:
        st.info("Nenhuma atividade registrada ainda.")
