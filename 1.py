import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# CONFIG
st.set_page_config(page_title="Planejamento de Carreira", layout="wide")

# BANCO SQLite
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
    streak INTEGER,
    ultimo TEXT
)
""")

conn.commit()

# INIT DADOS
def get_progresso():
    c.execute("SELECT * FROM progresso WHERE id=1")
    r = c.fetchone()
    if not r:
        c.execute("INSERT INTO progresso VALUES (1,1,0,0,NULL)")
        conn.commit()
        return {"casa":1,"xp":0,"streak":0,"ultimo":None}
    return {"casa":r[1],"xp":r[2],"streak":r[3],"ultimo":r[4]}

def salvar_progresso(d):
    c.execute("UPDATE progresso SET casa=?, xp=?, streak=?, ultimo=? WHERE id=1",
              (d["casa"], d["xp"], d["streak"], d["ultimo"]))
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
    salvar_progresso(dados)
    st.rerun()

# REGISTRAR ATIVIDADE
st.subheader("Registrar Atividade")

atividade = st.selectbox("Tipo", [
    "Estudo", "Laboratório", "Projeto", "Inglês", "Networking"
])
obs = st.text_area("Observação")

if st.button("Salvar"):
    c.execute("INSERT INTO atividades VALUES (?,?,?)",
              (str(date.today()), atividade, obs))
    conn.commit()
    dados["xp"] += 30
    salvar_progresso(dados)
    st.success("Salvo!")

# CARREGAR DADOS
df = pd.read_sql("SELECT * FROM atividades", conn)

# 📊 POWER BI STYLE (Altair)
st.subheader("📊 Análise de Atividades")

if not df.empty:
    chart = df.groupby(["data","atividade"]).size().reset_index(name="qtd")

    st.bar_chart(
        chart.pivot(index="data", columns="atividade", values="qtd").fillna(0)
    )

# 🔥 HEATMAP (GitHub Style)
st.subheader("🔥 Heatmap de Estudos")

if not df.empty:
    df["data"] = pd.to_datetime(df["data"])
    heat = df.groupby(df["data"].dt.date).size()

    heat_df = heat.reset_index()
    heat_df.columns = ["data","qtd"]

    st.dataframe(heat_df)

# 🧠 IA SIMPLES
st.subheader("🧠 Sugestão de Estudo (IA)")

def sugerir(df):
    if df.empty:
        return "Comece com Estudo básico hoje."
    ult = df.iloc[-1]["atividade"]

    if ult == "Estudo":
        return "Faça um laboratório amanhã."
    elif ult == "Laboratório":
        return "Trabalhe em um projeto."
    elif ult == "Projeto":
        return "Revise teoria."
    else:
        return "Foque em estudo técnico."

st.info(sugerir(df))

# 🖨️ PDF
st.subheader("🖨️ Gerar Relatório PDF")

if st.button("Gerar PDF"):
    doc = SimpleDocTemplate("relatorio.pdf", pagesize=letter)
    styles = getSampleStyleSheet()

    conteudo = []
    conteudo.append(Paragraph(f"XP: {dados['xp']}", styles["Normal"]))
    conteudo.append(Paragraph(f"Semana: {dados['casa']}", styles["Normal"]))

    for _, row in df.iterrows():
        conteudo.append(Paragraph(f"{row['data']} - {row['atividade']}: {row['obs']}", styles["Normal"]))

    doc.build(conteudo)

    with open("relatorio.pdf", "rb") as f:
        st.download_button("Baixar PDF", f, "relatorio.pdf")
