import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Planejamento de Carreira",
    page_icon="🛡️",
    layout="wide"
)

# ─────────────────────────────────────────────
# ESTILO
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    color: #000000 !important;
}
.stButton button {
    background-color: #d32f2f !important;
    color: white !important;
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIG USER
# ─────────────────────────────────────────────
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
ARQUIVO = "progresso.json"

# ─────────────────────────────────────────────
# MAPA
# ─────────────────────────────────────────────
TEMAS_MAP = [
    (1, 6, "☁️ AZ-900", "Azure Fundamentals"),
    (7, 12, "📜 ISO-F", "ISO 27001"),
    (13, 24, "🌐 CCNA", "Cisco CCNA"),
    (25, 32, "⚙️ AZ-104", "Azure Admin"),
    (33, 40, "🛡️ SC-900", "Security"),
    (41, 50, "🔐 Security+", "CompTIA"),
    (51, 60, "🧠 CySA+", "CySA"),
    (61, 70, "🏢 ISO-LI", "Implementer"),
    (71, 75, "🏭 62443", "Industrial"),
    (76, 80, "⚡ GICSP", "ICS"),
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
            with open(ARQUIVO) as f:
                d = json.load(f)
        except:
            d = {}
    else:
        d = {}

    d.setdefault("casa", 1)
    d.setdefault("xp", 0)
    d.setdefault("eventos", {})
    d.setdefault("concluidas", [])
    d.setdefault("streak", 0)
    d.setdefault("ultimo_estudo", None)
    d.setdefault("atividades", [])

    return d

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2)

def atualizar_streak(d):
    hoje = date.today()
    ultimo = d.get("ultimo_estudo")

    if ultimo:
        ultimo = datetime.strptime(ultimo, "%Y-%m-%d").date()
        if hoje == ultimo + timedelta(days=1):
            d["streak"] += 1
        elif hoje != ultimo:
            d["streak"] = 1
    else:
        d["streak"] = 1

    d["ultimo_estudo"] = str(hoje)

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
    st.title("🔐 Acesso Seguro")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == USER_LOGIN and senha == USER_PASS:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Login inválido")
    st.stop()

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
st.title("🛡️ Planejamento de Carreira")

c1, c2, c3, c4 = st.columns(4)
c1.metric("XP", dados["xp"])
c2.metric("Nível", dados["xp"] // 1000)
c3.metric("Streak 🔥", dados["streak"])
c4.metric("Progresso", f"{int((dados['casa']/80)*100)}%")

st.progress(dados["casa"]/80)

sigla, nome = get_info_casa(dados["casa"])
st.info(f"🎯 Foco atual: {nome} ({sigla})")

# ─────────────────────────────────────────────
# ALTERAR FOCO
# ─────────────────────────────────────────────
st.subheader("🎯 Ajustar Foco")

opcoes = [f"{t[2]} - {t[3]}" for t in TEMAS_MAP]
novo = st.selectbox("Escolher foco", opcoes)

if st.button("Alterar foco"):
    for i, f, sigla, nome in TEMAS_MAP:
        if f"{sigla} - {nome}" == novo:
            dados["casa"] = i
            salvar(dados)
            st.rerun()

# ─────────────────────────────────────────────
# AÇÕES
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if st.button("Avançar Semana"):
        dados["casa"] += 1
        dados["xp"] += 100
        salvar(dados)
        st.rerun()

with col2:
    if st.button("Voltar"):
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

if st.button("Salvar Estudo"):
    dados["eventos"][str(data_log)] = texto
    atualizar_streak(dados)
    dados["xp"] += 50
    salvar(dados)
    st.rerun()

# ─────────────────────────────────────────────
# INGLÊS
# ─────────────────────────────────────────────
st.subheader("🌍 Inglês")

if st.button("Registrar inglês"):
    atualizar_streak(dados)
    dados["xp"] += 20
    salvar(dados)

# ─────────────────────────────────────────────
# ATIVIDADES
# ─────────────────────────────────────────────
st.subheader("🚀 Atividades")

atividade = st.selectbox("Atividade", [
    "📘 Estudo",
    "🧪 Laboratório",
    "💻 Projeto",
    "🌐 Inglês",
    "📄 LinkedIn",
    "🤝 Networking"
])

obs = st.text_area("Observação")

if st.button("Salvar atividade"):
    dados["atividades"].append({
        "data": str(date.today()),
        "atividade": atividade,
        "obs": obs
    })
    dados["xp"] += 30
    salvar(dados)

# Histórico
for a in reversed(dados["atividades"]):
    with st.expander(f"{a['data']} - {a['atividade']}"):
        st.write(a["obs"])

# ─────────────────────────────────────────────
# GRÁFICO DE PILHA
# ─────────────────────────────────────────────
st.subheader("📊 Evolução por Atividade")

if dados["atividades"]:
    df = pd.DataFrame(dados["atividades"])
    df_group = df.groupby(["data", "atividade"]).size().unstack(fill_value=0)
    st.area_chart(df_group)

# ─────────────────────────────────────────────
# EXPORTAÇÃO
# ─────────────────────────────────────────────
st.subheader("🖨️ Relatório")

st.download_button(
    "Baixar progresso",
    json.dumps(dados, indent=2),
    "progresso.json"
)
