import streamlit as st
import json
import os
from PIL import Image, ImageDraw
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Jogo da Carreira: Juan Felipe", layout="wide")

# --- BANCO DE DADOS DE DADOS (COORDENADAS E METAS) ---
# MAPA DE COORDENADAS X,Y PARA CADA CASA NO TABULEIRO ORIGINAL
# Nota: Você precisará ajustar essas coordenadas X,Y clicando na imagem e pegando os pixels reais.
COORDS = {
    1: (180, 520),  # INÍCIO / Técnico Sênior
    2: (230, 480),  # Início do caminho de terra
    3: (280, 440),
    4: (340, 410),  # Curva
    5: (390, 440),  # Próximo ao rio
    # ... adicione as outras casas ...
    10: (550, 480), # Ex: Ponte
    20: (800, 380), # Ex: Python / GitHub
    30: (600, 200), # Ex: Power BI
    40: (280, 300), # Ex: GICSP
    50: (120, 210), # CISSP / TOP (Meta Final)
}

# BANCO DE METAS POR FASE (BASEADO NO SEU MAPA)
metas_fases = {
    "FASE 1: DECCOLAGEM": [
        {"Ordem": 1, "Meta": "CompTIA Security+ (Estudo/Simulado)", "Status": "A Fazer"},
        {"Ordem": 2, "Meta": "Azure AZ-900 (Iniciante)", "Status": "A Fazer"},
        {"Ordem": 3, "Meta": "Pós PUC (Disciplinas Básicas)", "Status": "A Fazer"},
        {"Ordem": 4, "Meta": "Melhorar Inglês (Conversação)", "Status": "A Fazer"},
    ],
    "FASE 2: CONSTRUÇÃO": [
        {"Ordem": 1, "Meta": "Python Intermediário / Scripts de Automação", "Status": "A Fazer"},
        {"Ordem": 2, "Meta": "SQL Avançado (Análise de Dados)", "Status": "A Fazer"},
        {"Ordem": 3, "Meta": "Power BI (Dashboard do Escritório)", "Status": "A Fazer"},
        {"Ordem": 4, "Meta": "Aprender Git/GitHub", "Status": "A Fazer"},
    ],
    "FASE 3: ESTRATÉGIA": [
        {"Ordem": 1, "Meta": "Certificação GICSP (Foco em OT/ICS)", "Status": "A Fazer"},
        {"Ordem": 2, "Meta": "Gestão de Projetos Ágeis", "Status": "A Fazer"},
        {"Ordem": 3, "Meta": "Redes Industriais Profundas", "Status": "A Fazer"},
    ],
    "FASE 4: CONSOLIDAÇÃO": [
        {"Ordem": 1, "Meta": "Estudo Focado CISSP (Teoria)", "Status": "A Fazer"},
        {"Ordem": 2, "Meta": "Simulados CISSP Profundos", "Status": "A Fazer"},
        {"Ordem": 3, "Meta": "Liderança e Gestão de Pessoas", "Status": "A Fazer"},
        {"Ordem": 50, "Meta": "⭐️ META FINAL: Obter CISSP e Posição Executiva", "Status": "A Fazer"},
    ]
}

# --- FUNÇÕES DE PERSISTÊNCIA ---
ARQUIVO_PROG = "progresso_tabuleiro.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_PROG):
        with open(ARQUIVO_PROG, "r") as f:
            return json.load(f)
    return {"casa_atual": 1, "metas_completas": [], "xp_total": 0}

def salvar_dados(dados):
    with open(ARQUIVO_PROG, "w") as f:
        json.dump(dados, f, indent=4)

def desenhar_peao(imagem, casa):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # Pega as coordenadas X,Y para a casa atual (ou usa a casa 1 como padrão)
    coord = COORDS.get(casa, (180, 520))
    x, y = coord
    
    # Define o tamanho do peão (um círculo vermelho)
    raio = 20
    draw.ellipse((x - raio, y - raio, x + raio, y + raio), fill="red", outline="black", width=2)
    return img

# --- INICIALIZAÇÃO ---
dados = carregar_dados()
image = Image.open("tabuleiro_carreira.png") # Certifique-se que a imagem está na mesma pasta

# --- INTERFACE DO STREAMLIT ---
st.title("🏆 Jogo da Vida Profissional: Juan Felipe")
st.write("Acompanhe sua progressão do Técnico Sênior ao Topo (CISSP).")

# --- SIDEBAR: PAINEL DE CONTROLE DO JOGADOR ---
with st.sidebar:
    st.header("👤 Painel do Jogador")
    st.image("image_2.png", use_column_width=True) # Exibe o avatar original
    st.metric("Casa Atual", dados["casa_atual"])
    st.metric("XP Total", dados["xp_total"])
    
    # Campo para concluir metas e avançar
    st.divider()
    st.subheader("Registrar Conquista")
    
    # Cria uma lista de todas as metas pendentes para selecionar
    todas_as_metas = []
    for fase, metas in metas_fases.items():
        for meta in metas:
            if meta["Ordem"] not in dados["metas_completas"]:
                todas_as_metas.append(f"{fase} - {meta['Meta']}")

    meta_concluida = st.selectbox("Qual meta você conquistou?", ["Selecione..."] + todas_as_metas)
    
    if st.button("Confirmar Conquista (Avançar 1 Casa)"):
        if meta_concluida != "Selecione...":
            # Extrai o nome da meta
            nome_meta = meta_concluida.split(" - ")[1]
            # Adiciona ao XP e às metas completas
            dados["xp_total"] += 100
            # Adiciona o ID da meta (aqui usamos a 'Ordem' como ID simples)
            # Nota: Para um sistema real, use IDs únicos.
            # dados["metas_completas"].append(...) 

            # Avança a casa
            if dados["casa_atual"] < 50:
                dados["casa_atual"] += 1
                st.success(f"🏆 Boa, Juan! Avançou para a casa {dados['casa_atual']} e ganhou 100 XP!")
                # Lógica para mostrar as coordenadas da casa
                if dados["casa_atual"] in COORDS:
                    st.info(f"Coordenadas da Casa: {COORDS[dados['casa_atual']]}")
                else:
                    st.warning("Coordenadas para esta casa ainda não foram definidas.")
            else:
                st.balloons()
                st.success("PARABÉNS! VOCÊ CHEGOU AO TOPO DO TABULEIRO!")

            salvar_dados(dados)
            st.rerun() # Atualiza a página para mostrar o peão novo

# --- LAYOUT PRINCIPAL: O TABULEIRO E AS MISSÕES ---
col_tabuleiro, col_missoes = st.columns([2, 1])

with col_tabuleiro:
    st.subheader("🗺️ Mapa da Jornada")
    # Desenha o peão na imagem
    imagem_com_peao = desenhar_peao(image, dados["casa_atual"])
    # Exibe a imagem interativa
    st.image(imagem_com_peao, use_column_width=True, caption="Você é o peão vermelho!")
    st.divider()
    st.write(f"Você está na Casa {dados['casa_atual']}. Faltam {50 - dados['casa_atual']} passos para o CISSP!")

with col_missoes:
    st.subheader("📋 Log de Missões")
    
    # Define qual fase mostrar baseado na casa atual
    if dados["casa_atual"] <= 12: fase_ativa = "FASE 1: DECCOLAGEM"
    elif dados["casa_atual"] <= 25: fase_ativa = "FASE 2: CONSTRUÇÃO"
    elif dados["casa_atual"] <= 38: fase_ativa = "FASE 3: ESTRATÉGIA"
    else: fase_ativa = "FASE 4: CONSOLIDAÇÃO"
    
    st.markdown(f"**Atualmente em: {fase_ativa}**")
    
    # Converte a lista de dicionários em um DataFrame para mostrar bonito
    df_metas = pd.DataFrame(metas_fases[fase_ativa])
    # Tira a coluna de ordem para ficar mais limpo
    df_metas = df_metas[["Meta", "Status"]]
    st.table(df_metas)

# --- RODAPÉ: RESUMO DE CONQUISTAS ANTERIORES ---
st.divider()
st.subheader("🏅 Mural de Conquistas Anteriores")
if dados["metas_completas"]:
    st.info("Aqui você listará as certificações e marcos que já completou.")
else:
    st.warning("Nenhuma meta estratégica registrada como concluída ainda. Vamos estudar!")
