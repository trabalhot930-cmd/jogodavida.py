import streamlit as st
import json
import os
from datetime import datetime, date
import calendar
from PIL import Image, ImageDraw

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Plano de Carreira - Juan Felipe",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- COORDENADAS PARA O PEÃO NA IMAGEM (X, Y) ---
# Você deve ajustar esses números conforme as casas da sua imagem .jpeg
COORDS_MAPA = {
    1: (180, 520), 5: (390, 440), 10: (550, 480), 
    20: (800, 380), 30: (600, 200), 40: (280, 300), 50: (120, 210)
}

# --- DADOS DAS FASES ---
FASES = {
    "FASE 1: DECOLAGEM": {
        "range": (1, 12), "cor": "#1a6abf", "emoji": "🚀",
        "metas": [
            ("S+",  "#cc6600", "CompTIA Security+",     "Abr/2026 – Mai/2026"),
            ("AZ",  "#0078d4", "Azure AZ-900",           "Mai/2026"),
            ("AX",  "#e53935", "Axians ISO 27001/27019", "Mai/2026"),
            ("PÓS", "#7b1fa2", "Pós PUC (Início)",       "Jun/2026"),
            ("EN",  "#00695c", "Inglês Técnico",          "Contínuo"),
        ]
    },
    "FASE 2: CONSTRUÇÃO": {
        "range": (13, 25), "cor": "#2e7d32", "emoji": "🏗️",
        "metas": [
            ("Py",  "#3776ab", "Python + GitHub Ativo",  "2026 – 2027"),
            ("PB",  "#f57c00", "Power BI Dashboards",    "2026 – 2027"),
            ("SQL", "#b5880a", "SQL Avançado",           "2026 – 2027"),
        ]
    },
    "FASE 3: ESTRATÉGIA": { "range": (26, 38), "cor": "#e65100", "emoji": "⚙️", "metas": [] },
    "FASE 4: CONSOLIDAÇÃO": { "range": (39, 50), "cor": "#6a1c77", "emoji": "👑", "metas": [] }
}

ARQUIVO = "progresso_jf.json"

# --- FUNÇÕES ---
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO) as f:
            return json.load(f)
    return {"casa": 1, "xp": 0, "concluidas": [], "eventos": {}}

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def desenhar_peao(img_path, casa_atual):
    try:
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        # Pega a coord da casa ou a mais próxima definida
        coord = COORDS_MAPA.get(casa_atual, (180, 520))
        x, y = coord
        raio = 25
        draw.ellipse((x-raio, y-raio, x+raio, y+raio), fill="red", outline="white", width=4)
        return img
    except:
        return None

# --- ESTILOS CSS --- (Mantive os seus que estão excelentes)
st.markdown("""
<style>
    /* Seus estilos CSS aqui... */
    .titulo-principal { font-family: 'Rajdhani'; font-size: 2rem; color: #7eb8ff; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if "dados" not in st.session_state:
    st.session_state.dados = carregar()
dados = st.session_state.dados

# --- UI PRINCIPAL ---
st.markdown('<div class="titulo-principal">🏆 Plano Estratégico de Carreira</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:#4a80b0;">JUAN FELIPE · CASA {dados["casa"]}</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO", "📅 CALENDÁRIO", "🏅 CERTIFICAÇÕES"])

with tab1:
    col_mapa, col_stats = st.columns([2, 1])
    
    with col_mapa:
        # Tenta carregar a imagem do WhatsApp que você subiu
        imagem_caminho = "tabuleiro_carreira.png" # Certifique-se de subir com esse nome no GitHub
        tabuleiro_com_peao = desenhar_peao(imagem_caminho, dados["casa"])
        
        if tabuleiro_com_peao:
            st.image(tabuleiro_com_peao, use_container_width=True, caption="Seu progresso visual")
        else:
            st.warning("⚠️ Suba o arquivo 'tabuleiro_carreira.png' para o GitHub para ver o peão no mapa!")
        
        # Aqui entra o seu código de renderização das casas (Row 1, Row 2...)
        # [SEU CÓDIGO DAS CASAS HTML AQUI]

    with col_stats:
        st.metric("XP TOTAL", f"{dados['xp']} pts")
        if st.button("🚀 AVANÇAR PRÓXIMA CASA", use_container_width=True):
            dados["casa"] = min(dados["casa"] + 1, 50)
            dados["xp"] += 100
            salvar(dados)
            st.rerun()

# [RESTANTE DO SEU CÓDIGO DE CALENDÁRIO E CERTIFICAÇÕES]
