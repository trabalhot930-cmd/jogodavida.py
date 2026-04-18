import streamlit as st
from supabase import create_client, Client
from datetime import datetime, date
import json

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Plano de Carreira", layout="wide")

SUPABASE_URL = "COLE_SUA_URL"
SUPABASE_KEY = "COLE_SUA_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

def login():
    st.title("🔐 Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })
        if res.user:
            st.session_state.user = res.user
            st.success("Logado!")
            st.rerun()
        else:
            st.error("Erro no login")

def cadastro():
    st.subheader("Criar conta")
    email = st.text_input("Novo email")
    senha = st.text_input("Nova senha", type="password")

    if st.button("Cadastrar"):
        supabase.auth.sign_up({
            "email": email,
            "password": senha
        })
        st.success("Conta criada!")

if not st.session_state.user:
    tab1, tab2 = st.tabs(["Login", "Cadastro"])
    with tab1:
        login()
    with tab2:
        cadastro()
    st.stop()

user = st.session_state.user

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
def carregar_dados():
    res = supabase.table("progresso").select("*").eq("user_id", user.id).execute()

    if res.data:
        return res.data[0]
    else:
        novo = {
            "user_id": user.id,
            "casa": 1,
            "xp": 0,
            "historico": [],
            "eventos": {}
        }
        supabase.table("progresso").insert(novo).execute()
        return novo

dados = carregar_dados()

# ─────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────
def salvar():
    supabase.table("progresso").update({
        "casa": dados["casa"],
        "xp": dados["xp"],
        "historico": dados["historico"],
        "eventos": dados["eventos"],
        "updated_at": datetime.now().isoformat()
    }).eq("user_id", user.id).execute()

# ─────────────────────────────────────────────
# CERT MAP
# ─────────────────────────────────────────────
CERT_MAP = {
    5: "AZ-900",
    12: "CCNA",
    18: "Security+",
    28: "ISO 27001",
    32: "ISA 62443",
    40: "CySA+",
    45: "GICSP",
    50: "CISSP"
}

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.title("🏆 Plano de Carreira")
st.caption(f"Logado como: {user.email}")

st.subheader(f"Casa {dados['casa']} | XP {dados['xp']}")

# Tabuleiro
cols = st.columns(10)
for i in range(1, 51):
    col = cols[(i-1) % 10]

    if i == dados["casa"]:
        col.markdown(f"🟦 **{i}**")
    elif i < dados["casa"]:
        col.markdown(f"✅ {i}")
    elif i in CERT_MAP:
        col.markdown(f"🏅 {CERT_MAP[i]}")
    else:
        col.markdown(str(i))

# ─────────────────────────────────────────────
# AÇÕES
# ─────────────────────────────────────────────
def registrar(acao):
    dados["historico"].append({
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "acao": acao
    })

col1, col2 = st.columns(2)

with col1:
    if st.button("➡️ Avançar"):
        if dados["casa"] < 50:
            dados["casa"] += 1
            dados["xp"] += 100
            registrar("Avançou")

            if dados["casa"] in CERT_MAP:
                registrar(f"Certificação: {CERT_MAP[dados['casa']]}")
                st.balloons()

            salvar()
            st.rerun()

with col2:
    if st.button("⬅️ Voltar"):
        if dados["casa"] > 1:
            dados["casa"] -= 1
            dados["xp"] = max(0, dados["xp"] - 100)
            registrar("Voltou")
            salvar()
            st.rerun()

# ─────────────────────────────────────────────
# HISTÓRICO
# ─────────────────────────────────────────────
st.divider()
st.subheader("📊 Histórico")

for h in reversed(dados["historico"][-10:]):
    st.write(f"{h['data']} - {h['acao']}")

# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
if st.button("🚪 Sair"):
    st.session_state.user = None
    st.rerun()
