import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

st.set_page_config(layout="wide")

ARQUIVO = "dados.json"

# ─────────────────────────────────────────────
# ESTILO (mantendo seu padrão)
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body { background: #050d1a; color: #c8dff0; }

.casa {
    width: 100px; height: 100px;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    border-radius:10px;
    margin:4px;
    background:#0a1a2e;
    border:2px solid #1a3a60;
}

.casa-atual {
    border:2px solid #00f2ff;
    background:#1a4a8a;
}

.cert {
    background:white;
    color:black;
    padding:2px 6px;
    border-radius:6px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAPA (com ícones + pós)
# ─────────────────────────────────────────────
TEMAS_MAP = [
    (1, 6, "☁️ AZ-900", "Azure"),
    (7, 12, "📜 ISO-F", "ISO"),
    (13, 24, "🌐 CCNA", "Cisco"),
    (25, 32, "⚙️ AZ-104", "Azure Admin"),
    (33, 40, "🛡️ SC-900", "Security"),
    (41, 50, "🔐 Security+", "CompTIA"),
    (51, 60, "🧠 CySA+", "CySA"),
    (61, 70, "🏢 ISO-LI", "Implementer"),
    (71, 75, "🏭 62443", "Industrial"),
    (76, 80, "⚡ GICSP", "ICS"),
]

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO) as f:
            d = json.load(f)
    else:
        d = {}

    d.setdefault("casa", 1)
    d.setdefault("xp", 0)
    d.setdefault("eventos", {})
    d.setdefault("atividades", [])
    d.setdefault("streak", 0)
    d.setdefault("ultimo", None)

    return d

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2)

dados = carregar()

# ─────────────────────────────────────────────
# TABULEIRO ORIGINAL (mantido)
# ─────────────────────────────────────────────
st.title("🛡️ Roadmap Profissional")

for i in range(10):
    cols = st.columns(8)
    linha = list(range(i*8+1, (i+1)*8+1))
    if i % 2 != 0:
        linha.reverse()

    for idx, n in enumerate(linha):
        sigla = next((t[2] for t in TEMAS_MAP if t[0] <= n <= t[1]), str(n))

        cls = "casa"
        if n == dados["casa"]:
            cls += " casa-atual"

        cols[idx].markdown(
            f"<div class='{cls}'><div class='cert'>{sigla}</div><small>S{n}</small></div>",
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────
# CONTROLES
# ─────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    if st.button("Avançar"):
        dados["casa"] += 1
        dados["xp"] += 100
        salvar(dados)
        st.rerun()

with c2:
    if st.button("Voltar"):
        dados["casa"] = max(1, dados["casa"]-1)
        dados["xp"] -= 100
        salvar(dados)
        st.rerun()

# ─────────────────────────────────────────────
# INGLÊS DIÁRIO
# ─────────────────────────────────────────────
st.subheader("🌍 Inglês diário")

if st.button("Registrar inglês"):
    dados["xp"] += 20
    salvar(dados)
    st.success("Inglês registrado!")

# ─────────────────────────────────────────────
# ATIVIDADES COM OBS
# ─────────────────────────────────────────────
st.subheader("🚀 Atividades Estratégicas")

atividade = st.selectbox("Escolha", [
    "LinkedIn", "Projetos", "Laboratório",
    "Networking", "Portfólio", "Estudo"
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
    st.success("Salvo!")

# Histórico
for a in reversed(dados["atividades"]):
    with st.expander(f"{a['data']} - {a['atividade']}"):
        st.write(a["obs"])

# ─────────────────────────────────────────────
# RELATÓRIO
# ─────────────────────────────────────────────
st.subheader("🖨️ Relatório")

if st.button("Exportar"):
    st.download_button(
        "Baixar JSON",
        json.dumps(dados, indent=2),
        "relatorio.json"
    )
