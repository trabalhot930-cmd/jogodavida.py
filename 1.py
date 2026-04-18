import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Cyber Roadmap PRO", page_icon="🛡️", layout="wide")

USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
ARQUIVO = "progresso_v2.json"

# ─────────────────────────────────────────────
# ESTILO (FUNDO AZUL + CERT PRETO)
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1f44, #0d2b6b);
    color: #e6f0ff;
}
.stTextInput input {
    background-color: #0f2a5a;
    color: white;
}
.stButton button {
    background-color: #1f4ea3;
    color: white;
    border-radius: 8px;
}
.cert {
    background: white;
    color: black;
    padding: 5px 10px;
    border-radius: 6px;
    font-weight: bold;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAPA
# ─────────────────────────────────────────────
TEMAS_MAP = [
    (1, 6, "☁️ AZ-900", "Azure Fundamentals"),
    (7, 12, "📜 ISO-F", "ISO 27001"),
    (13, 24, "🌐 CCNA", "Cisco CCNA"),
    (25, 32, "⚙️ AZ-104", "Azure Admin"),
    (33, 40, "🛡️ SC-900", "Security"),
    (41, 50, "🔐 Security+", "CompTIA Security+"),
    (51, 60, "🧠 CySA+", "CompTIA CySA+"),
    (61, 70, "🏢 ISO-LI", "Lead Implementer"),
    (71, 75, "🏭 62443", "ISA 62443"),
    (76, 80, "⚡ GICSP", "Industrial Cyber"),
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
                dados = json.load(f)
        except:
            dados = {}
    else:
        dados = {}

    # Anti erro versão antiga
    dados.setdefault("casa", 1)
    dados.setdefault("xp", 0)
    dados.setdefault("eventos", {})
    dados.setdefault("concluidas", [])
    dados.setdefault("streak", 0)
    dados.setdefault("ultimo_estudo", None)

    return dados

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2)

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

def nivel(xp):
    return xp // 1000

def progresso(casa):
    return int((casa / 80) * 100)

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
    st.markdown("<h1 style='text-align:center;'>🔐 ACESSO SEGURO</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar", use_container_width=True):
            if user == USER_LOGIN and senha == USER_PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Login inválido")

    st.stop()

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
st.title("🛡️ Cyber Roadmap PRO")

c1, c2, c3, c4 = st.columns(4)
c1.metric("XP", dados["xp"])
c2.metric("Nível", nivel(dados["xp"]))
c3.metric("Streak 🔥", dados["streak"])
c4.metric("Progresso", f"{progresso(dados['casa'])}%")

st.progress(progresso(dados["casa"]) / 100)

sigla, nome = get_info_casa(dados["casa"])
st.info(f"🎯 Foco atual: {nome} ({sigla})")

# ─────────────────────────────────────────────
# AÇÕES
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Concluir Semana"):
        dados["casa"] += 1
        dados["xp"] += 100
        salvar(dados)
        st.rerun()

with col2:
    if st.button("⬅️ Voltar"):
        dados["casa"] = max(1, dados["casa"] - 1)
        dados["xp"] = max(0, dados["xp"] - 100)
        salvar(dados)
        st.rerun()

# ─────────────────────────────────────────────
# DIÁRIO
# ─────────────────────────────────────────────
st.subheader("📝 Diário")

data_log = st.date_input("Data", date.today())
texto = st.text_area("Estudo do dia")

if st.button("Salvar estudo"):
    dados["eventos"][str(data_log)] = texto
    atualizar_streak(dados)
    dados["xp"] += 50
    salvar(dados)
    st.success("Salvo!")
    st.rerun()

# ─────────────────────────────────────────────
# INGLÊS
# ─────────────────────────────────────────────
st.subheader("🌍 Inglês diário")

if st.button("Registrar inglês 🇺🇸"):
    atualizar_streak(dados)
    dados["xp"] += 20
    salvar(dados)
    st.success("Inglês registrado!")

# ─────────────────────────────────────────────
# CERTIFICAÇÕES + PÓS
# ─────────────────────────────────────────────
st.subheader("🏅 Certificações")

certs = [
    ("☁️ AZ-900", "Azure Fundamentals"),
    ("📜 ISO-F", "ISO 27001"),
    ("🌐 CCNA", "Cisco"),
    ("⚙️ AZ-104", "Azure Admin"),
    ("🛡️ SC-900", "Security"),
    ("🔐 Security+", "CompTIA"),
    ("🧠 CySA+", "Cyber Analyst"),
    ("🏢 ISO-LI", "Lead Implementer"),
    ("🏭 62443", "Industrial"),
    ("⚡ GICSP", "ICS Security"),
    ("🎓 PÓS", "Pós-graduação"),
]

for sigla, nome in certs:
    marcado = st.checkbox(f"{sigla} - {nome}", value=(sigla in dados["concluidas"]))

    if marcado and sigla not in dados["concluidas"]:
        dados["concluidas"].append(sigla)
        dados["xp"] += 500

    elif not marcado and sigla in dados["concluidas"]:
        dados["concluidas"].remove(sigla)
        dados["xp"] -= 500

salvar(dados)

# ─────────────────────────────────────────────
# ATIVIDADES
# ─────────────────────────────────────────────
st.subheader("🚀 Atividades Estratégicas")

atividades = [
    "📄 LinkedIn",
    "💻 Projetos",
    "🧪 Laboratórios",
    "📚 Estudo teórico",
    "🎤 Networking",
    "📊 Portfólio",
]

for a in atividades:
    if st.button(a):
        dados["xp"] += 30
        salvar(dados)
        st.success(f"{a} registrado!")
