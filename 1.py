import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import pandas as pd

st.set_page_config(layout="wide")

ARQUIVO = "dados.json"

# ─────────────────────────────────────────────
# DATABASE (PRONTO PRA CLOUD)
# ─────────────────────────────────────────────
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            d = json.load(f)
    else:
        d = {}

    d.setdefault("casa", 1)
    d.setdefault("xp", 0)
    d.setdefault("streak", 0)
    d.setdefault("ultimo", None)
    d.setdefault("logs", [])
    d.setdefault("atividades", [])

    return d

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2)

dados = carregar()

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
        if u == "Juan" and p == "Ju@n1990":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Erro")

    st.stop()

# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Tabuleiro",
    "📊 Progresso",
    "📝 Registros",
    "🖨️ Relatório"
])

# ─────────────────────────────────────────────
# TABULEIRO CLICÁVEL
# ─────────────────────────────────────────────
with tab1:
    st.title("🗺️ Seu Tabuleiro")

    cols = st.columns(8)

    for i in range(1, 81):
        col = cols[(i-1) % 8]

        if col.button(f"S{i}", key=i):
            dados["casa"] = i
            dados["xp"] = i * 100
            salvar(dados)
            st.rerun()

    st.success(f"Você está na semana {dados['casa']}")

# ─────────────────────────────────────────────
# PROGRESSO + GRÁFICO
# ─────────────────────────────────────────────
with tab2:
    st.title("📊 Progresso")

    st.metric("XP", dados["xp"])
    st.metric("Semana", dados["casa"])

    # Criar dados fake evolutivos (ou histórico real depois)
    semanas = list(range(1, dados["casa"]+1))
    xp = [s * 100 for s in semanas]

    df = pd.DataFrame({
        "Semana": semanas,
        "XP": xp
    })

    st.line_chart(df.set_index("Semana"))

# ─────────────────────────────────────────────
# REGISTROS + OBSERVAÇÕES
# ─────────────────────────────────────────────
with tab3:
    st.title("📝 Registros de Atividades")

    atividade = st.selectbox("Atividade", [
        "LinkedIn",
        "Projetos",
        "Laboratório",
        "Networking",
        "Estudo",
        "Inglês"
    ])

    obs = st.text_area("Observação")

    if st.button("Salvar Registro"):
        dados["atividades"].append({
            "data": str(date.today()),
            "atividade": atividade,
            "obs": obs
        })
        dados["xp"] += 30
        salvar(dados)
        st.success("Registrado!")

    st.divider()

    for r in reversed(dados["atividades"]):
        with st.expander(f"{r['data']} - {r['atividade']}"):
            st.write(r["obs"])

# ─────────────────────────────────────────────
# RELATÓRIO (PRINT)
# ─────────────────────────────────────────────
with tab4:
    st.title("🖨️ Relatório")

    st.write(f"Semana atual: {dados['casa']}")
    st.write(f"XP total: {dados['xp']}")

    df = pd.DataFrame(dados["atividades"])

    if not df.empty:
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Baixar relatório CSV",
            csv,
            "relatorio.csv",
            "text/csv"
        )

    st.info("Use Ctrl+P para imprimir a tela")
