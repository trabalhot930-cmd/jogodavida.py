import streamlit as st
import pandas as pd
import json
import os

# Configuração da página
st.set_page_config(page_title="Board Game: Carreira Juan", layout="wide")

# Funções de Dados
def carregar_dados():
    if os.path.exists("progresso.json"):
        with open("progresso.json", "r") as f:
            return json.load(f)
    return {"casa_atual": 1, "conquistas": []}

def salvar_dados(dados):
    with open("progresso.json", "w") as f:
        json.dump(dados, f)

# Inicialização
dados = carregar_dados()

st.title("🏆 Plano Estratégico: Juan Felipe")
st.write("Acompanhe sua jornada do técnico sênior ao topo da carreira.")

# --- Sidebar para Controles ---
with st.sidebar:
    st.header("Painel de Controle")
    progresso = st.slider("Sua Casa no Tabuleiro", 1, 50, dados["casa_atual"])
    nova_conquista = st.text_input("Nova Conquista (ex: Certificação Security+)")
    
    if st.button("Salvar Progresso"):
        dados["casa_atual"] = progresso
        if nova_conquista:
            dados["conquistas"].append(nova_conquista)
        salvar_dados(dados)
        st.success("Progresso salvo!")

# --- Layout Principal ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mapa de Jornada")
    # Aqui você pode exibir a imagem que você gerou
    # st.image("sua_imagem_do_boardgame.jpg", use_column_width=True)
    
    # Barra de progresso visual
    porcentagem = (progresso / 50)
    st.progress(porcentagem)
    st.write(f"Você está na **Casa {progresso}** de 50. Faltam {50 - progresso} passos para o CISSP!")

with col2:
    st.subheader("Log de Conquistas")
    if dados["conquistas"]:
        for c in reversed(dados["conquistas"]):
            st.write(f"✅ {c}")
    else:
        st.info("Nenhuma conquista registrada ainda. Hora de estudar!")

# --- Marcos Estratégicos (Baseado na sua imagem) ---
st.divider()
fases = st.columns(4)

with fases[0]:
    st.info("**Fase 1: Decolagem**\n\nCompTIA Security+\nAzure AZ-900\nInglês")
with fases[1]:
    st.info("**Fase 2: Construção**\n\nPython Intermediário\nSQL Avançado\nPower BI")
with fases[2]:
    st.info("**Fase 3: Estratégia**\n\nGICSP (ICS/SCADA)\nGestão de Equipes")
with fases[3]:
    st.warning("**Fase 4: Topo**\n\nCISSP\nLiderança Executiva")
