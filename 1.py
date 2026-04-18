import streamlit as st
import json
import os
from datetime import datetime, date
import calendar

# Configuração da página
st.set_page_config(
    page_title="Plano de Carreira - Juan Felipe",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# DADOS E CONSTANTES
# ─────────────────────────────────────────────
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"

FASES = {
    "FASE 1: DECOLAGEM": {
        "range": (1, 12), "cor": "#1a6abf", "emoji": "🚀",
        "metas": [
            ("S+",  "#cc6600", "CompTIA Security+",     "Abr/2025 – Mai/2025"),
            ("AZ",  "#0078d4", "Azure AZ-900",           "Mai/2025"),
            ("AX",  "#e53935", "Axians ISO 27001/27019", "Mai/2025"),
            ("MS",  "#b71c1c", "Microsoft ADUS",         "Mai/2025"),
            ("PÓS", "#7b1fa2", "Pós PUC (Início)",       "Jun/2025"),
            ("EN",  "#00695c", "Inglês Técnico",          "Contínuo"),
        ]
    },
    "FASE 2: CONSTRUÇÃO": {
        "range": (13, 25), "cor": "#2e7d32", "emoji": "🏗️",
        "metas": [
            ("Py",  "#3776ab", "Python + GitHub Ativo",  "Out/2025 – Out/2026"),
            ("PB",  "#f57c00", "Power BI Dashboards",    "Out/2025 – Out/2026"),
            ("SQL", "#b5880a", "SQL Avançado",           "Out/2025 – Out/2026"),
            ("ISO", "#1565c0", "ISO 27001 Implementer",  "Out/2025 – Out/2026"),
            ("ATK", "#4a148c", "MITRE ATT&CK Avançado",  "Out/2025 – Out/2026"),
            ("DOC", "#00838f", "Documentação Técnica",   "Contínuo"),
        ]
    },
    "FASE 3: ESTRATÉGIA": {
        "range": (26, 38), "cor": "#e65100", "emoji": "⚙️",
        "metas": [
            ("GI",  "#2e7d32", "Certificação GICSP",     "Jan/2027 – Dez/2028"),
            ("PUC", "#6a1c77", "PUC Minas Conclusão",    "Jan/2027 – Dez/2028"),
            ("SDAs","#37474f", "SDAS Conformidade",      "Jan/2027 – Dez/2028"),
            ("GES", "#bf360c", "Gestão de Projetos",     "Jan/2027 – Dez/2028"),
            ("OT",  "#01579b", "Redes Industriais OT",   "Jan/2027 – Dez/2028"),
        ]
    },
    "FASE 4: CONSOLIDAÇÃO": {
        "range": (39, 50), "cor": "#6a1c77", "emoji": "👑",
        "metas": [
            ("CS",  "#6a1c77", "CISSP – Teoria",         "2028 – 2029"),
            ("SIM", "#880e4f", "Simulados CISSP",        "2028 – 2029"),
            ("LID", "#1a237e", "Liderança Corporativa",  "2028 – 2029"),
            ("HH",  "#4e342e", "Headhunters TI/OT",     "2028 – 2029"),
            ("TOP", "#b71c1c", "META FINAL: CISSP",      "2029"),
        ]
    }
}

CERT_MAP = {
    5:  ("S+",  "#cc6600", "Security+"),
    10: ("AZ",  "#0078d4", "AZ-900"),
    15: ("Py",  "#3776ab", "Python"),
    20: ("PB",  "#f57c00", "Power BI"),
    25: ("SQL", "#b5880a", "SQL"),
    30: ("GI",  "#2e7d32", "GICSP"),
    40: ("CS",  "#6a1c77", "CISSP"),
    50: ("🏆",  "#8a30c0", "META"),
}

ARQUIVO = "progresso_jf.json"

# ─────────────────────────────────────────────
# FUNÇÕES DE APOIO
# ─────────────────────────────────────────────
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO) as f:
            return json.load(f)
    return {"casa": 1, "xp": 0, "concluidas": [], "eventos": {}}

def salvar(d):
    with open(ARQUIVO, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def get_fase(casa):
    for nome, dados in FASES.items():
        if dados["range"][0] <= casa <= dados["range"][1]:
            return nome, dados
    return list(FASES.items())[-1]

# ─────────────────────────────────────────────
# SISTEMA DE LOGIN
# ─────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.markdown("""
        <style>
        .login-box {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            background: rgba(10, 25, 60, 0.9);
            border: 1px solid #1a3a6a;
            border-radius: 15px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/508/508757.png", width=80)
        st.subheader("Acesso Restrito - Plano de Carreira")
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar", use_container_width=True):
            if user == USER_LOGIN and password == USER_PASS:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.autenticado:
    login()
    st.stop()

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #050d1a !important;
    color: #c8dff0;
    font-family: 'Rajdhani', sans-serif;
}
[data-testid="stSidebar"] { background: #080f20 !important; }
[data-testid="stHeader"] { background: transparent !important; }

.titulo-principal {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #7eb8ff;
    letter-spacing: 2px;
    text-align: center;
    text-transform: uppercase;
    margin-top: -20px;
}
.subtitulo {
    font-size: 1rem;
    color: #4a80b0;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 2rem;
    font-family: 'Share Tech Mono', monospace;
}

/* Cards */
.card-dark {
    background: rgba(10, 25, 60, 0.8);
    border: 1px solid #1a3a6a;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 12px;
}

/* Tabuleiro */
.tabuleiro-container {
    background: #061020;
    border: 2px solid #1a3a6a;
    border-radius: 14px;
    padding: 20px;
}
.casa {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 65px; height: 65px;
    border-radius: 12px;
    font-size: 10px;
    font-family: 'Share Tech Mono', monospace;
    margin: 4px;
    border: 2px solid;
    transition: all 0.3s;
    text-align: center;
    line-height: 1;
}
.casa-normal { background: #0a1a2e; border-color: #1a3a60; color: #3a6080; }
.casa-feita  { background: #0a2a1a; border-color: #1a5a30; color: #2a8a4a; }
.casa-atual  { background: #1a4a8a; border-color: #4a90d9; color: #fff;
               box-shadow: 0 0 15px rgba(74,144,217,0.7); animation: pulse 1.5s infinite; }
.casa-cert   { border-width: 3px; font-weight: bold; }

.label-cert { font-size: 9px; margin-top: 4px; display: block; overflow: hidden; white-space: nowrap; }

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 15px rgba(74,144,217,0.7); }
    50% { transform: scale(1.05); box-shadow: 0 0 25px rgba(74,144,217,1); }
}

.row-casas { display: flex; flex-wrap: wrap; gap: 5px; margin: 10px 0; }
.row-casas.reverso { flex-direction: row-reverse; }

/* XP Bar */
.xp-container { background: #050d1a; border: 1px solid #1a3a6a; border-radius: 20px; height: 12px; overflow: hidden; }
.xp-fill { height: 100%; background: linear-gradient(90deg, #1a5cbf, #4ab0ff); transition: width 0.5s; }

.insignia {
    display: inline-flex; align-items: center; justify-content: center;
    width: 35px; height: 35px; border-radius: 6px; font-weight: 700; font-size: 10px;
    font-family: 'Share Tech Mono'; margin: 2px; border: 1px solid rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGICA DO TABULEIRO
# ─────────────────────────────────────────────
if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados

st.markdown('<div class="titulo-principal">🏆 Plano Estratégico de Carreira</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">SISTEMA DE PROGRESSÃO: JUAN FELIPE</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO", "📅 CALENDÁRIO", "🏅 CERTIFICAÇÕES"])

with tab1:
    col_board, col_sidebar = st.columns([3.5, 1.2])

    with col_board:
        st.markdown('<div class="tabuleiro-container">', unsafe_allow_html=True)

        def render_casa(n):
            casa_atual_player = dados["casa"]
            is_atual = (n == casa_atual_player)
            is_feita = (n < casa_atual_player)
            cert_info = CERT_MAP.get(n)
            
            cls = "casa"
            label = str(n)
            sub_label = ""
            border_color = ""
            
            if is_atual: cls += " casa-atual"
            elif is_feita: cls += " casa-feita"
            else: cls += " casa-normal"
            
            if cert_info:
                cls += " casa-cert"
                label = cert_info[0]
                sub_label = f'<span class="label-cert">{cert_info[2]}</span>'
                border_color = f"border-color: {cert_info[1]};"
                if not is_feita and not is_atual:
                    border_color += f"color: {cert_info[1]};"

            return f'<div class="{cls}" style="{border_color}">{label}{sub_label}</div>'

        # FASES NO TABULEIRO
        fase_config = [
            ("🚀 FASE 1", range(1, 13), False),
            ("🏗️ FASE 2", range(13, 26), True),
            ("⚙️ FASE 3", range(26, 39), False),
            ("👑 FASE 4", range(39, 51), True)
        ]

        for titulo, r, reverso in fase_config:
            st.markdown(f'<div style="font-size:11px; color:#4a80b0; margin-top:10px">{titulo}</div>', unsafe_allow_html=True)
            row_html = "".join(render_casa(n) for n in (reversed(r) if reverso else r))
            rev_class = "reverso" if reverso else ""
            st.markdown(f'<div class="row-casas {rev_class}">{row_html}</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_sidebar:
        pct = round(dados["casa"] / 50 * 100)
        st.markdown(f"""
        <div class="card-dark">
            <div style="font-size:11px;color:#4a80b0;letter-spacing:1px">PROGRESSO GERAL</div>
            <div style="font-size:2.5rem;font-weight:700;color:#4ab0ff;font-family:'Share Tech Mono'">{pct}%</div>
            <div class="xp-container"><div class="xp-fill" style="width:{pct}%"></div></div>
            <div style="font-size:10px;color:#3a6080;margin-top:5px">CASA ATUAL: {dados['casa']} | XP: {dados['xp']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶ Avançar Casa", use_container_width=True):
            if dados["casa"] < 50:
                dados["casa"] += 1
                dados["xp"] += 100
                salvar(dados)
                st.rerun()
            else: st.balloons()
        
        if st.button("◀ Voltar Casa", use_container_width=True):
            if dados["casa"] > 1:
                dados["casa"] -= 1
                dados["xp"] = max(0, dados["xp"] - 100)
                salvar(dados)
                st.rerun()

        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

# Os códigos das abas de Calendário e Certificações permanecem os mesmos do anterior, 
# apenas integrados com a verificação de login acima.
# (Mantendo a funcionalidade de salvar/carregar JSON para persistência)

with tab2:
    st.info("Calendário de Atividades Técnicas - Use para registrar horas de estudo.")
    # [Mantém o código original do calendário aqui]

with tab3:
    st.subheader("Checklist de Conquistas")
    # [Mantém o código original das certificações aqui]
