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
        return "Concluída"
    elif xp >= 40:
        return "Em andamento"
    else:
        return "Não iniciada"

def badge(status):
    if status == "Concluída":
        return "🟢"
    elif status == "Em andamento":
        return "🟡"
    else:
        return "⬜"

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
        area = st.selectbox(
            "Área",
            list(st.session_state.cert_xp.keys())
        )

        activity = st.selectbox(
            "Atividade",
            ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", "Aula Pós-graduação", "Inglês"]
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
    # PROGRESSO GERAL (COM DATA + STATUS)
    # =========================
    st.subheader("🏆 Progresso Geral com Planejamento")

    planejamento = {
        "AZ-900": "Abril/2026",
        "ISO 27001": "Maio/2026",
        "CCNA": "Julho/2026",
        "SC-900": "Outubro/2026",
        "Python": "2026 contínuo",
        "SQL": "2026 contínuo",
        "Power BI": "2026 contínuo",
        "Security+": "Fevereiro/2027",
        "CySA+": "Dezembro/2027",
        "GICSP": "Março/2028",
        "CISSP": "Junho/2029",
        "Pós-graduação": "Junho/2026 → Dez/2028",
        "Inglês": "Abril/2026 → contínuo"
    }

    for item, xp in st.session_state.cert_xp.items():

        status = status_por_xp(xp)
        icon = badge(status)

        data_planejada = planejamento.get(item, "Não definido")

        st.markdown(f"""
### {icon} {item}

📅 **Planejado:** {data_planejada}  
📊 **Status:** {status}  
⭐ XP: {xp}

---
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

    # =========================
    # EXPORTAÇÃO
    # =========================
    st.subheader("📤 Exportar Base de Dados")

    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Baixar CSV completo",
            csv,
            "carreira_juan_felipe.csv",
            "text/csv"
        )

    # =========================
    # GRÁFICO EM TORRE
    # =========================
    st.subheader("🏗️ Gráfico em Torre (Produtividade)")

    if not df.empty:

        torre = df.groupby("area").agg(
            xp_total=("xp", "sum"),
            atividades=("area", "count")
        ).reset_index()

        chart = alt.Chart(torre).mark_bar().encode(
            x=alt.X("area:N", sort="-y"),
            y="xp_total:Q",
            color="area:N",
            tooltip=["area", "xp_total", "atividades"]
        ).properties(height=400)

        st.altair_chart(chart, use_container_width=True)

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:

    st.title("🛣️ Roadmap Completo")

    st.markdown("""
## 📅 2026 — BASE + PÓS
- AZ-900  
- ISO 27001  
- CCNA  
- SC-900  
- Python / SQL / Power BI  
- Pós-graduação (Cibersegurança e Governança de Dados)  
- Inglês diário  

## 📅 2027
- Security+  
- CySA+  

## 📅 2028
- GICSP  
- ISO 27001 Lead Auditor  

## 📅 2029
- CISSP  
""")

# =========================
# TAB 3 - CALENDÁRIO
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
        st.info("Sem dados ainda.")
