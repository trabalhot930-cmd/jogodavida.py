import streamlit as st
import pandas as pd
import altair as alt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Planejamento de carreira Juan Felipe da Silva",
    layout="wide"
)

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

if "cert_xp" not in st.session_state:
    st.session_state.cert_xp = {
        "AZ-900": 0,
        "ISO 27001": 0,
        "CCNA": 0,
        "SC-900": 0,
        "Python": 0,
        "SQL": 0,
        "Power BI": 0,
        "Security+": 0,
        "CySA+": 0,
        "GICSP": 0,
        "CISSP": 0,
        "Pós-graduação": 0,
        "Inglês": 0
    }

# =========================
# XP SYSTEM
# =========================
def calc_xp(activity):
    return {
        "Estudo": 10,
        "Laboratório": 20,
        "Projeto": 30,
        "Revisão": 15,
        "Simulado": 15,
        "Aula Pós-graduação": 25,
        "Inglês": 15
    }.get(activity, 10)

def status_por_xp(xp):
    if xp >= 120:
        return "Concluído"
    elif xp >= 40:
        return "Em andamento"
    else:
        return "Não iniciado"

def badge(status):
    if status == "Concluído":
        return "🥇"
    elif status == "Em andamento":
        return "🥈"
    else:
        return "🥉"

# =========================
# HEADER
# =========================
st.title("📘 Planejamento de carreira Juan Felipe da Silva")
st.caption(f"⭐ XP Global: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# ABAS
# =========================
tab1, tab2, tab3 = st.tabs(["🎓 Dashboard", "🛣️ Roadmap", "📆 Calendário"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:

    st.subheader("📌 Registrar atividade")

    col1, col2 = st.columns(2)

    with col1:
        area = st.selectbox(
            "Área de estudo",
            list(st.session_state.cert_xp.keys())
        )

        activity = st.selectbox(
            "Atividade",
            [
                "Estudo",
                "Laboratório",
                "Projeto",
                "Revisão",
                "Simulado",
                "Aula Pós-graduação",
                "Inglês"
            ]
        )

    with col2:
        data = st.date_input("Data", value=pd.Timestamp.today())
        obs = st.text_area("Observação")

    if st.button("Salvar atividade"):

        xp_gain = calc_xp(activity)

        st.session_state.db.append({
            "data": pd.to_datetime(data),
            "area": area,
            "atividade": activity,
            "xp": xp_gain,
            "obs": obs
        })

        st.session_state.xp += xp_gain
        st.session_state.cert_xp[area] += xp_gain

        st.success(f"+{xp_gain} XP!")

    df = pd.DataFrame(st.session_state.db)

    # =========================
    # KPIs
    # =========================
    st.subheader("📊 KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Registros", len(df))
    col2.metric("XP Global", st.session_state.xp)
    col3.metric("Level", st.session_state.xp // 100 + 1)

    # =========================
    # PROGRESSO (BADGES)
    # =========================
    st.subheader("🏆 Progresso Geral")

    for cert, xp in st.session_state.cert_xp.items():
        status = status_por_xp(xp)
        icon = badge(status)

        st.markdown(f"""
        ### {icon} {cert}  
        **Status:** {status}  
        **XP:** {xp}
        """)

    # =========================
    # HISTÓRICO
    # =========================
    st.subheader("📚 Histórico")

    if not df.empty:

        filtro = st.selectbox("Filtrar área", df["area"].unique())
        df_f = df[df["area"] == filtro]

        st.dataframe(df_f, use_container_width=True)

        timeline = df_f.groupby("data").size().reset_index(name="atividades")

        st.altair_chart(
            alt.Chart(timeline).mark_line(point=True).encode(
                x="data:T",
                y="atividades:Q",
                tooltip=["data", "atividades"]
            ),
            use_container_width=True
        )

    else:
        st.info("Sem registros ainda.")

# =========================
# TAB 2 - ROADMAP COMPLETO
# =========================
with tab2:

    st.title("🛣️ Roadmap de Carreira Completo")

    st.subheader("📅 2026 — BASE + INÍCIO DA PÓS")

    st.markdown("""
- AZ-900 — Abril/2026  
- ISO 27001 Fundamentals — Maio/2026  
- CCNA — Julho/2026  
- SC-900 — Outubro/2026  

📘 Python  
📊 SQL  
📈 Power BI  

🎓 Pós-graduação em Cibersegurança e Governança de Dados — início Junho/2026 (EAD)  
🌍 Inglês — início Abril/2026 (diário 30–40 min)
""")

    st.divider()

    st.subheader("📅 2027 — SEGURANÇA + GOVERNANÇA + OT")

    st.markdown("""
- Security+ — Fevereiro/2027  
- ISO 27001 Lead Implementer — Maio/2027  
- ISA/IEC 62443 — Agosto/2027  
- MITRE ATT&CK ICS — Outubro/2027  
- CySA+ — Dezembro/2027  

🎓 Pós-graduação (continuação)  
🌍 Inglês técnico
""")

    st.divider()

    st.subheader("📅 2028 — ESPECIALIZAÇÃO + FINAL DA PÓS")

    st.markdown("""
- GICSP — Março/2028  
- ISO 27001 Lead Auditor — Agosto/2028  

🎓 Pós-graduação (conclusão Dezembro/2028)  
🌍 Inglês avançado
""")

    st.divider()

    st.subheader("📅 2029 — CONSOLIDAÇÃO")

    st.markdown("""
- CISSP — Junho/2029  
🌍 Inglês fluente profissional
""")

# =========================
# TAB 3 - CALENDÁRIO
# =========================
with tab3:

    st.title("📆 Calendário de Atividades")

    df = pd.DataFrame(st.session_state.db)

    if not df.empty:

        timeline = df.groupby("data").size().reset_index(name="atividades")

        st.altair_chart(
            alt.Chart(timeline).mark_bar().encode(
                x="data:T",
                y="atividades:Q",
                tooltip=["data", "atividades"]
            ),
            use_container_width=True
        )

        st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)

    else:
        st.info("Nenhuma atividade registrada ainda.")
