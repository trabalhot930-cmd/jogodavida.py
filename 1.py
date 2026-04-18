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
        "CISSP": 0
    }

# =========================
# XP RULES
# =========================
def calc_xp(activity):
    return {
        "Estudo": 10,
        "Laboratório": 20,
        "Projeto": 30,
        "Revisão": 15,
        "Simulado": 15
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
# TAB 1
# =========================
with tab1:

    st.subheader("📌 Registrar atividade")

    col1, col2 = st.columns(2)

    with col1:
        cert = st.selectbox("Certificação / Curso", list(st.session_state.cert_xp.keys()))
        atividade = st.selectbox("Atividade", ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado"])

    with col2:
        data = st.date_input("Data", value=pd.Timestamp.today())
        obs = st.text_area("Observação")

    if st.button("Salvar atividade"):
        xp_gain = calc_xp(atividade)

        st.session_state.db.append({
            "data": pd.to_datetime(data),
            "certificacao": cert,
            "atividade": atividade,
            "xp": xp_gain,
            "obs": obs
        })

        st.session_state.xp += xp_gain
        st.session_state.cert_xp[cert] += xp_gain

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
    # BADGES + STATUS
    # =========================
    st.subheader("🏆 Certificações (Badges)")

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

        filtro = st.selectbox("Filtrar certificação", df["certificacao"].unique())

        df_f = df[df["certificacao"] == filtro]

        st.dataframe(df_f, use_container_width=True)

        chart = df_f.groupby("data").size().reset_index(name="atividades")

        st.altair_chart(
            alt.Chart(chart).mark_line(point=True).encode(
                x="data:T",
                y="atividades:Q",
                tooltip=["data", "atividades"]
            ),
            use_container_width=True
        )

# =========================
# TAB 2
# =========================
with tab2:

    st.title("🛣️ Roadmap")

    st.markdown("""
### 📅 2026
- AZ-900  
- ISO 27001  
- CCNA  
- Python / SQL / Power BI  

### 📅 2027
- Security+  
- CySA+  

### 📅 2028
- GICSP  

### 📅 2029
- CISSP  
""")

# =========================
# TAB 3
# =========================
with tab3:

    st.title("📆 Calendário")

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
