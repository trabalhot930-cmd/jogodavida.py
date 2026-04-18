import streamlit as st
import json
import os
from datetime import datetime, date
import calendar

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Plano de Carreira - Juan Felipe",
    page_icon="🏆",
    layout="wide"
)

ARQUIVO = "progresso_jf.json"

USUARIO = "Juan"
SENHA = "Ju@nSilv@"

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state.logado = False

def tela_login():
    st.title("🔐 Login - Plano de Carreira")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == USUARIO and senha == SENHA:
            st.session_state.logado = True
            st.success("Login realizado!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")

if not st.session_state.logado:
    tela_login()
    st.stop()

# ─────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO) as f:
            return json.load(f)
    return {
        "casa": 1,
        "xp": 0,
        "concluidas": [],
        "eventos": {},
        "historico": []
    }

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

dados = carregar()

# ─────────────────────────────────────────────
# CERTIFICAÇÕES (ATUALIZADAS)
# ─────────────────────────────────────────────
CERT_MAP = {
    5:  ("AZ",  "#0078d4", "Azure AZ-900"),
    8:  ("AX",  "#e53935", "ISO 27001 Fundamentos"),
    12: ("CCNA","#1ba0d7", "Cisco CCNA"),
    18: ("S+",  "#cc6600", "Security+"),
    22: ("SC9", "#5c6bc0", "SC-900"),
    28: ("ISO", "#1565c0", "ISO 27001 Implementer"),
    32: ("ICS", "#2e7d32", "ISA 62443"),
    35: ("MIT", "#6a1b9a", "MITRE ICS"),
    40: ("CYSA","#8e24aa", "CySA+"),
    45: ("GI",  "#2e7d32", "GICSP"),
    50: ("🏆", "#8a30c0", "CISSP"),
}

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
st.title("🏆 Plano Estratégico de Carreira")
st.caption("Juan Felipe • Rumo ao CISSP + OT Security")

# ─────────────────────────────────────────────
# AÇÕES
# ─────────────────────────────────────────────
def registrar_progresso(acao):
    hoje = datetime.now().strftime("%Y-%m-%d %H:%M")
    dados["historico"].append({
        "data": hoje,
        "acao": acao,
        "casa": dados["casa"],
        "xp": dados["xp"]
    })

# ─────────────────────────────────────────────
# TABs
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🗺️ Tabuleiro", "📅 Calendário", "📊 Histórico"])

# ═══════════════════════════════════════════
# TABULEIRO
# ═══════════════════════════════════════════
with tab1:

    st.subheader(f"Casa atual: {dados['casa']} | XP: {dados['xp']}")

    cols = st.columns(10)

    for i in range(1, 51):
        col = cols[(i-1) % 10]

        if i == dados["casa"]:
            col.markdown(f"🟦 **{i}**")
        elif i < dados["casa"]:
            col.markdown(f"✅ {i}")
        elif i in CERT_MAP:
            col.markdown(f"🏅 {CERT_MAP[i][0]}")
        else:
            col.markdown(f"{i}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        if st.button("➡️ Avançar"):
            if dados["casa"] < 50:
                dados["casa"] += 1
                dados["xp"] += 100
                registrar_progresso("Avançou casa")

                # Evento automático
                dia = str(date.today())
                dados["eventos"].setdefault(dia, []).append({
                    "titulo": f"Casa {dados['casa']}"
                })

                # Se for certificação
                if dados["casa"] in CERT_MAP:
                    nome = CERT_MAP[dados["casa"]][2]
                    dados["concluidas"].append(nome)
                    registrar_progresso(f"Certificação: {nome}")
                    st.balloons()

                salvar(dados)
                st.rerun()

    with c2:
        if st.button("⬅️ Voltar"):
            if dados["casa"] > 1:
                dados["casa"] -= 1
                dados["xp"] = max(0, dados["xp"] - 100)
                registrar_progresso("Voltou casa")
                salvar(dados)
                st.rerun()

# ═══════════════════════════════════════════
# CALENDÁRIO
# ═══════════════════════════════════════════
with tab2:
    st.subheader("📅 Calendário de Atividades")

    hoje = date.today()
    eventos = dados.get("eventos", {})

    for dia, lista in sorted(eventos.items()):
        st.write(f"📆 {dia}")
        for e in lista:
            st.write(f" - {e['titulo']}")

# ═══════════════════════════════════════════
# HISTÓRICO
# ═══════════════════════════════════════════
with tab3:
    st.subheader("📊 Histórico de Progresso")

    for item in reversed(dados["historico"][-20:]):
        st.write(f"{item['data']} - {item['acao']} (Casa {item['casa']})")

# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
if st.button("🚪 Sair"):
    st.session_state.logado = False
    st.rerun()
