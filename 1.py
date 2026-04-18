import streamlit as st
import json
import os
from PIL import Image, ImageDraw
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Jogo da Carreira: Juan Felipe", layout="wide")

# --- BANCO DE DADOS DE COORDENADAS (AJUSTE CONFORME O MAPA) ---
# Aqui você define onde o peão aparece para cada número de casa
COORDS = {
    1: (180, 520),   # INÍCIO
    5: (390, 440),   # Caminho inicial
    10: (550, 480),  # Perto da ponte
    20: (800, 380),  # Python / GitHub
    30: (600, 200),  # Power BI
    40: (280, 300),  # GICSP
    50: (120, 210),  # CISSP / META FINAL
}

# --- METAS POR FASE ---
metas_fases = {
    "FASE 1: DECOLAGEM": [
        "CompTIA Security+",
        "Azure AZ-900",
        "Pós PUC (Início)",
        "Inglês Técnico"
    ],
    "FASE 2: CONSTRUÇÃO": [
        "Python Automação",
        "SQL Avançado",
        "Power BI Dashboards",
        "Git/GitHub Ativo"
    ],
    "FASE 3: ESTRATÉGIA": [
        "Certificação GICSP",
        "Gestão de Projetos",
        "Redes Industriais"
    ],
    "FASE 4: CONSOLIDAÇÃO": [
        "Teoria CISSP",
        "Simulados Finais",
        "Liderança Corporativa",
        "META FINAL: CISSP"
    ]
}

# --- FUNÇÕES DE ARQUIVO ---
ARQUIVO_PROG = "progresso_tabuleiro.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_PROG):
        with open(ARQUIVO_PROG, "r") as f:
            return json.load(f)
    return {"casa_atual": 1, "xp_total": 0, "conquistas": []}

def salvar_dados(dados):
    with open(ARQUIVO_PROG, "w") as f:
        json.dump(dados, f, indent=4)

def desenhar_peao(img_fundo, casa):
    img_copy = img_fundo.copy()
    draw = ImageDraw.Draw(img_copy)
    
    # Busca a coordenada da casa, se não tiver, usa a última conhecida ou a 1
    coord = COORDS.get(casa, COORDS[1])
    x, y = coord
    
    # Desenha o peão (Círculo Vermelho)
    raio = 20
    draw.ellipse((x - raio, y - raio, x + raio, y + raio), fill="red", outline="white", width=3)
    return img_copy

# --- LÓGICA PRINCIPAL ---
dados = carregar_dados()

# Tentativa de carregar a imagem
try:
    image = Image.open("tabuleiro_carreira.png")
except FileNotFoundError:
    st.error("Erro: O arquivo 'tabuleiro_carreira.png' não foi encontrado na pasta.")
    st.stop()

# --- INTERFACE STREAMLIT ---
st.title("🏆 Plano Estratégico de Carreira")
st.subheader("Juan Felipe da Silva")

col_tab, col_controles = st.columns([2, 1])

with col_tab:
    # Exibe o tabuleiro com o peão na posição atual
    img_resultado = desenhar_peao(image, dados["casa_atual"])
    st.image(img_resultado, use_container_width=True)
    
    st.write(f"### Você está na Casa: {dados['casa_atual']} / 50")
    st.progress(min(dados["casa_atual"] / 50, 1.0))

with col_controles:
    st.header("🎮 Jogar")
    
    # Botão para avançar
    if st.button("🚀 Concluí uma Meta (Avançar 1 Casa)"):
        if dados["casa_atual"] < 50:
            dados["casa_atual"] += 1
            dados["xp_total"] += 100
            salvar_dados(dados)
            st.success("Parabéns pelo progresso!")
            st.rerun()
        else:
            st.balloons()
            st.success("Você atingiu o TOPO da carreira!")

    # Botão para resetar (Cuidado!)
    if st.sidebar.button("Resetar Jogo"):
        dados = {"casa_atual": 1, "xp_total": 0, "conquistas": []}
        salvar_dados(dados)
        st.rerun()

    st.divider()
    st.write("### 📈 Status")
    st.metric("XP Acumulado", f"{dados['xp_total']} XP")
    
    # Mostrar metas da fase atual
    if dados["casa_atual"] <= 12: fase = "FASE 1: DECOLAGEM"
    elif dados["casa_atual"] <= 25: fase = "FASE 2: CONSTRUÇÃO"
    elif dados["casa_atual"] <= 38: fase = "FASE 3: ESTRATÉGIA"
    else: fase = "FASE 4: CONSOLIDAÇÃO"
    
    st.info(f"**Fase Atual:** {fase}")
    st.write("**Próximos Desafios:**")
    for m in metas_fases[fase]:
        st.write(f"- {m}")

st.divider()
st.caption("Desenvolvido por Juan Felipe - Rumo ao CISSP")
