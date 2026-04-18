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
# XP BASE
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

def bonus_status(status):
    if status == "Concluída":
        return 2.0   # XP DOBRADO
    elif status == "Em andamento":
        return 1.0
    else:
        return 0.5

# =========================
# HEADER
# =========================
st.title("📘 Planejamento de carreira Juan Felipe da Silva")
st.caption(f"⭐ XP Global: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# INPUT
# =========================
st.subheader("📌 Registrar atividade")

col1, col2, col3 = st.columns(3)

with col1:
    area = st.selectbox("Área", list(st.session_state.cert_xp.keys()))

with col2:
    activity = st.selectbox(
        "Atividade",
        ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", "Aula Pós-graduação", "Inglês"]
    )

with col3:
    status = st.selectbox(
        "Status da atividade",
        ["Não iniciada", "Em andamento", "Concluída"]
    )

data = st.date_input("Data", value=pd.Timestamp.today())
obs = st.text_area("Observação")

# =========================
# SAVE
# =========================
if st.button("Salvar atividade"):

    base_xp = calc_xp(activity)
    multiplier = bonus_status(status)
    xp_gain = int(base_xp * multiplier)

    st.session_state.db.append({
        "data": pd.to_datetime(data),
        "area": area,
        "atividade": activity,
        "status": status,
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
# PROGRESSO
# =========================
st.subheader("🏆 Progresso por Área")

for area_name, xp in st.session_state.cert_xp.items():

    if xp >= 120:
        icon = "🟢"
        txt = "Concluída"
    elif xp >= 40:
        icon = "🟡"
        txt = "Em andamento"
    else:
        icon = "⬜"
        txt = "Não iniciada"

    st.markdown(f"""
### {icon} {area_name}
**Status:** {txt}  
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
            y="atividades:Q"
        ),
        use_container_width=True
    )

# =========================
# EXPORTAÇÃO
# =========================
st.subheader("📤 Exportar dados")

if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Baixar CSV",
        csv,
        "carreira.csv",
        "text/csv"
    )
