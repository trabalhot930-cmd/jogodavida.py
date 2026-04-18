import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cyber Roadmap PRO",
    page_icon="🛡️",
    layout="wide"
)

USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
ARQUIVO = "progresso_v2.json"

DATA_INICIO = date(2026, 4, 18)

TEMAS_MAP = [
    (1, 6, "AZ-900", "Azure Fundamentals"),
    (7, 12, "ISO-F", "ISO 27001 Fundamentals"),
    (13, 24, "CCNA", "Cisco CCNA"),
    (25, 32, "AZ-104", "Azure Admin"),
    (33, 40, "SC-900", "Security Compliance"),
    (41, 50, "Security+", "CompTIA Security+"),
    (51, 60, "CySA+", "CompTIA CySA+"),
    (61, 70, "ISO-LI", "ISO Lead Implementer"),
    (71, 75, "62443", "ISA/IEC 62443"),
    (76, 80, "GICSP", "Industrial Cyber"),
]

# ─────────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────────
def get_info_casa(n):
    for i, f, sigla, nome in TEMAS_MAP:
        if i <= n <= f:
            return sigla, nome
    return "?", "?"

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "casa": 1,
        "xp": 0,
        "eventos": {},
        "concluidas": [],
        "streak": 0,
        "ultimo_estudo": None
    }

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2)

def calcular_nivel(xp):
    return xp // 1000

def progresso_percentual(casa):
    return int((casa / 80) * 100)

def atualizar_streak(dados):
    hoje = date.today()
    ultimo = dados.get("ultimo_estudo")

    if ultimo:
        ultimo = datetime.strptime(ultimo, "%Y-%m-%d").date()
        if hoje == ultimo:
            return
        elif hoje == ultimo + timedelta(days=1):
            dados["streak"] += 1
        else:
            dados["streak"] = 1
    else:
        dados["streak"] = 1

    dados["ultimo_estudo"] = str(hoje)

# ─────────────────────────────────────────────
# SESSION
# ─────────────────────────────────────────────
if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if u == USER_LOGIN and p == USER_PASS:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Acesso negado")
    st.stop()

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
st.title("🛡️ Cyber Security Roadmap PRO")

nivel = calcular_nivel(dados["xp"])
progresso = progresso_percentual(dados["casa"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("XP", dados["xp"])
c2.metric("Nível", nivel)
c3.metric("Streak 🔥", dados["streak"])
c4.metric("Progresso", f"{progresso}%")

st.progress(progresso / 100)

sigla, nome = get_info_casa(dados["casa"])
st.info(f"🎯 Foco atual: **{nome} ({sigla})**")

# ─────────────────────────────────────────────
# AÇÕES
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Concluir Semana"):
        if dados["casa"] < 80:
            dados["casa"] += 1
            dados["xp"] += 100
            salvar(dados)
            st.rerun()

with col2:
    if st.button("⬅️ Voltar"):
        if dados["casa"] > 1:
            dados["casa"] -= 1
            dados["xp"] = max(0, dados["xp"] - 100)
            salvar(dados)
            st.rerun()

# ─────────────────────────────────────────────
# DIÁRIO + STREAK
# ─────────────────────────────────────────────
st.subheader("📝 Diário")

data_log = st.date_input("Data", date.today())
texto = st.text_area("Estudo do dia")

if st.button("Salvar Estudo"):
    dados["eventos"][str(data_log)] = texto
    atualizar_streak(dados)
    dados["xp"] += 50
    salvar(dados)
    st.success("Salvo!")
    st.rerun()

# Histórico
for d in sorted(dados["eventos"].keys(), reverse=True):
    with st.expander(d):
        st.write(dados["eventos"][d])

# ─────────────────────────────────────────────
# CERTIFICAÇÕES
# ─────────────────────────────────────────────
st.subheader("🏅 Certificações")

objetivos = list(dict.fromkeys([t[2] for t in TEMAS_MAP]))
concluidas = dados["concluidas"]

for obj in objetivos:
    marcado = st.checkbox(obj, value=(obj in concluidas))

    if marcado and obj not in concluidas:
        concluidas.append(obj)
        dados["xp"] += 500

    elif not marcado and obj in concluidas:
        concluidas.remove(obj)
        dados["xp"] = max(0, dados["xp"] - 500)

dados["concluidas"] = concluidas
salvar(dados)

# ─────────────────────────────────────────────
# META SEMANAL INTELIGENTE
# ─────────────────────────────────────────────
st.subheader("🎯 Meta da Semana")

meta = dados["casa"] + 1
st.write(f"Objetivo: chegar na semana **{meta}**")

if dados["casa"] >= meta:
    st.success("Meta batida 🚀")
else:
    st.warning("Continue avançando...")

