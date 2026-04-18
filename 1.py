import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# CONFIG
st.set_page_config(page_title="Planejamento de Carreira", layout="wide")

# BANCO
conn = sqlite3.connect("carreira.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS atividades (
    data TEXT,
    atividade TEXT,
    obs TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS progresso (
    id INTEGER PRIMARY KEY,
    casa INTEGER,
    xp INTEGER,
    streak INTEGER
)
""")
conn.commit()

# INIT
def get_progresso():
    c.execute("SELECT * FROM progresso WHERE id=1")
    r = c.fetchone()
    if not r:
        c.execute("INSERT INTO progresso VALUES (1,1,0,0)")
        conn.commit()
        return {"casa":1,"xp":0,"streak":0}
    return {"casa":r[1],"xp":r[2],"streak":r[3]}

def salvar(d):
    c.execute("UPDATE progresso SET casa=?, xp=?, streak=? WHERE id=1",
              (d["casa"], d["xp"], d["streak"]))
    conn.commit()

dados = get_progresso()

# LOGIN
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if u == "Juan" and p == "Ju@n1990":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Erro")

    st.stop()

# DASHBOARD
st.title("🛡️ Planejamento de Carreira")

c1,c2,c3 = st.columns(3)
c1.metric("XP", dados["xp"])
c2.metric("Semana", dados["casa"])
c3.metric("Streak", dados["streak"])

# AÇÕES
if st.button("Avançar Semana"):
    dados["casa"] += 1
    dados["xp"] += 100
    salvar(dados)
    st.rerun()

# CERTIFICAÇÕES (COM EMBLEMAS)
st.subheader("🏅 Certificações")

certs = [
    "☁️ AZ-900",
    "📜 ISO 27001",
    "🌐 CCNA",
    "⚙️ AZ-104",
    "🛡️ SC-900",
    "🔐 Security+",
    "🧠 CySA+",
    "🏢 ISO Lead",
    "🏭 62443",
    "⚡ GICSP",
    "🎓 Pós-graduação"
]

for ctt in certs:
    st.markdown(f"### {ctt}")

# REGISTRAR ATIVIDADE
st.subheader("🚀 Registrar Atividade")

atividade = st.selectbox("Tipo", [
    "📘 Estudo",
    "🧪 Laboratório",
    "💻 Projeto",
    "🌐 Inglês",
    "🤝 Networking"
])

obs = st.text_area("Observação")

if st.button("Salvar"):
    c.execute("INSERT INTO atividades VALUES (?,?,?)",
              (str(date.today()), atividade, obs))
    conn.commit()
    dados["xp"] += 30
    salvar(dados)
    st.success("Salvo!")

# DADOS
df = pd.read_sql("SELECT * FROM atividades", conn)

# 📊 GRÁFICO
st.subheader("📊 Evolução")

if not df.empty:
    df_group = df.groupby(["data","atividade"]).size().unstack(fill_value=0)
    st.area_chart(df_group)

# 🔥 HEATMAP SIMPLES
st.subheader("🔥 Frequência de Estudo")

if not df.empty:
    heat = df.groupby("data").size()
    st.bar_chart(heat)

# 🧠 IA
st.subheader("🧠 Sugestão")

def sugerir(df):
    if df.empty:
        return "Comece com estudo hoje."
    ult = df.iloc[-1]["atividade"]
    if "Estudo" in ult:
        return "Faça laboratório amanhã."
    elif "Laboratório" in ult:
        return "Desenvolva um projeto."
    else:
        return "Volte para teoria."

st.info(sugerir(df))

# 🖨️ RELATÓRIO HTML (IMPRIMIR)
st.subheader("🖨️ Relatório")

html = f"""
<h2>Planejamento de Carreira</h2>
<p>XP: {dados['xp']}</p>
<p>Semana: {dados['casa']}</p>
"""

for _, row in df.iterrows():
    html += f"<p>{row['data']} - {row['atividade']} - {row['obs']}</p>"

st.download_button(
    "Baixar relatório (HTML)",
    html,
    "relatorio.html",
    "text/html"
)

st.info("Abra o HTML e pressione CTRL + P para salvar em PDF")
