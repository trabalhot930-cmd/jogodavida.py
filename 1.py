import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# CONFIG
st.set_page_config(page_title="Cyber Roadmap PRO", page_icon="🛡️", layout="wide")

USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
ARQUIVO = "progresso_v2.json"

# ESTILO (mantido + cert preta)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1f44, #0d2b6b);
    color: #e6f0ff;
}

.cert-box {
    background: white;
    color: black;
    padding: 4px 8px;
    border-radius: 6px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# MAPA (com ícones)
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

# FUNÇÕES
def get_info_casa(n):
    for i, f, sigla, nome in TEMAS_MAP:
        if i <= n <= f:
            return sigla, nome
    return "?", "?"

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r") as f:
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

# SESSION
if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados

# LOGIN
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>🔐 ACESSO SEGURO</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar", use_container_width=True):
            if usuario == USER_LOGIN and senha == USER_PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")
    st.stop()

# DASHBOARD
st.title("🛡️ Cyber Security Roadmap PRO")

c1, c2, c3, c4 = st.columns(4)
c1.metric("XP", dados["xp"])
c2.metric("Nível", dados["xp"] // 1000)
c3.metric("Streak 🔥", dados["streak"])
c4.metric("Progresso", f"{int((dados['casa']/80)*100)}%")

st.progress(dados["casa"]/80)

sigla, nome = get_info_casa(dados["casa"])
st.info(f"🎯 Foco atual: {nome} ({sigla})")

# AÇÕES
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
        dados["casa"] = max(1, dados["casa"] - 1)
        dados["xp"] = max(0, dados["xp"] - 100)
        salvar(dados)
        st.rerun()

# DIÁRIO
st.subheader("📝 Diário")

data_log = st.date_input("Data", date.today())
texto = st.text_area("Estudo do dia")

if st.button("Salvar Estudo"):
    dados["eventos"][str(data_log)] = texto
    atualizar_streak(dados)
    dados["xp"] += 50
    salvar(dados)
    st.rerun()

# INGLÊS
st.subheader("🌍 Inglês diário")

if st.button("Registrar inglês 🇺🇸"):
    atualizar_streak(dados)
    dados["xp"] += 20
    salvar(dados)
    st.success("Registrado!")

# CERTIFICAÇÕES (com pós)
st.subheader("🏅 Certificações")

certs = [
    ("☁️ AZ-900", "Azure"),
    ("📜 ISO-F", "ISO"),
    ("🌐 CCNA", "Cisco"),
    ("⚙️ AZ-104", "Admin"),
    ("🛡️ SC-900", "Security"),
    ("🔐 Security+", "CompTIA"),
    ("🧠 CySA+", "CySA"),
    ("🏢 ISO-LI", "Implementer"),
    ("🏭 62443", "Industrial"),
    ("⚡ GICSP", "ICS"),
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

# ATIVIDADES COM OBS
st.subheader("🚀 Atividades Estratégicas")

atividade = st.selectbox("Atividade", [
    "LinkedIn", "Projetos", "Laboratório",
    "Networking", "Portfólio", "Estudo"
])

obs = st.text_area("Observação da atividade")

if st.button("Salvar atividade"):
    dados["atividades"].append({
        "data": str(date.today()),
        "atividade": atividade,
        "obs": obs
    })
    dados["xp"] += 30
    salvar(dados)
    st.success("Atividade registrada!")

# HISTÓRICO
for a in reversed(dados["atividades"]):
    with st.expander(f"{a['data']} - {a['atividade']}"):
        st.write(a["obs"])

# EXPORTAÇÃO
st.subheader("🖨️ Relatório")

st.download_button(
    "Baixar progresso",
    json.dumps(dados, indent=2),
    "progresso.json"
)
