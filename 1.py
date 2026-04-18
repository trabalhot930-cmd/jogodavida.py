import streamlit as st
import json
import os
from datetime import datetime, date
import calendar

st.set_page_config(
    page_title="Plano de Carreira - Juan Felipe", Coloque as certificações  
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────
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

ARQUIVO = "progresso_jf.json"

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
# ESTILOS
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

/* Esconde itens desnecessários */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 1400px; }

/* Título principal */
.titulo-principal {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #7eb8ff;
    letter-spacing: 2px;
    text-align: center;
    margin-bottom: 0;
    text-transform: uppercase;
}
.subtitulo {
    font-size: 1rem;
    color: #4a80b0;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 1.5rem;
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
.card-fase {
    border-left: 4px solid;
    border-radius: 0 10px 10px 0;
    padding: 10px 14px;
    margin: 6px 0;
    background: rgba(10,20,50,0.6);
}

/* XP Bar */
.xp-container {
    background: #050d1a;
    border: 1px solid #1a3a6a;
    border-radius: 20px;
    height: 12px;
    overflow: hidden;
    margin: 6px 0;
}
.xp-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #1a5cbf, #4ab0ff);
    transition: width 0.5s;
}

/* Insígnia de certificação */
.insignia {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px; height: 40px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 10px;
    font-family: 'Share Tech Mono', monospace;
    margin: 3px;
    border: 1px solid rgba(255,255,255,0.2);
    text-align: center;
    line-height: 1.1;
    letter-spacing: 0;
    vertical-align: middle;
}
.insignia.done { filter: grayscale(0.3); box-shadow: 0 0 10px rgba(74,176,80,0.5); }
.insignia.pending { filter: grayscale(0.6) brightness(0.7); }

/* Tabuleiro */
.tabuleiro-container {
    background: #061020;
    border: 2px solid #1a3a6a;
    border-radius: 14px;
    padding: 16px;
    position: relative;
}
.casa {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px; height: 44px;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Share Tech Mono', monospace;
    margin: 3px;
    border: 2px solid;
    cursor: default;
    transition: transform 0.2s;
    position: relative;
    text-align: center;
}
.casa-normal { background: #0a1a2e; border-color: #1a3a60; color: #3a6080; }
.casa-feita  { background: #0a2a1a; border-color: #1a5a30; color: #2a8a4a; }
.casa-atual  { background: #1a4a8a; border-color: #4a90d9; color: #fff;
               box-shadow: 0 0 15px rgba(74,144,217,0.7); animation: pulse 1.5s infinite; }
.casa-cert   { border-width: 3px; font-size: 9px; }
.casa-inicio { background: #0a3a1a; border-color: #2a9a5a; color: #2a9a5a; }
.casa-fim    { background: #2a0a4a; border-color: #8a30c0; color: #c080ff; }

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 15px rgba(74,144,217,0.7); }
    50% { box-shadow: 0 0 25px rgba(74,144,217,1); }
}

/* Linha de casas */
.row-casas {
    display: flex;
    flex-wrap: nowrap;
    justify-content: flex-start;
    gap: 2px;
    margin: 4px 0;
    overflow-x: auto;
}
.row-casas.reverso { justify-content: flex-end; }

/* Labels de fase */
.label-fase {
    font-size: 9px;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 1px;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 2px;
}

/* Calendário */
.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 3px;
}
.cal-header {
    text-align: center;
    font-size: 11px;
    color: #4a70a0;
    padding: 4px;
    font-family: 'Share Tech Mono', monospace;
}
.cal-dia {
    background: #070f20;
    border: 1px solid #0f2040;
    border-radius: 6px;
    min-height: 60px;
    padding: 4px;
    font-size: 11px;
    color: #3a6080;
}
.cal-dia.hoje { border-color: #4a90d9; color: #7eb8ff; }
.cal-dia.tem-evento { border-color: #1a5a30; }
.cal-dia .num-dia { font-weight: 700; margin-bottom: 2px; }
.cal-evento { font-size: 9px; color: #4a9a6a; background: #0a2a1a;
              border-radius: 3px; padding: 1px 3px; margin: 1px 0;
              white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Métricas */
.metrica-box {
    background: rgba(10,30,80,0.6);
    border: 1px solid #1a3a7a;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}
.metrica-num { font-size: 2.2rem; font-weight: 700; color: #4ab0ff; font-family: 'Share Tech Mono'; }
.metrica-label { font-size: 11px; color: #4a70a0; letter-spacing: 1px; }

/* Botões */
.stButton > button {
    background: #1a4a8a !important;
    color: #7eb8ff !important;
    border: 1px solid #2a6aaa !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #2060b0 !important;
    border-color: #4a90d9 !important;
    box-shadow: 0 0 12px rgba(74,144,217,0.4) !important;
}

/* Checkbox */
.stCheckbox label { color: #c8dff0 !important; font-family: 'Rajdhani'; }

/* Selectbox / text_input */
.stSelectbox label, .stTextInput label, .stTextArea label { color: #7eb8ff !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #050d1a !important; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: #080f20 !important;
    color: #4a70a0 !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid #1a3060 !important;
    font-family: 'Rajdhani' !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}
.stTabs [aria-selected="true"] {
    background: #1a3a7a !important;
    color: #7eb8ff !important;
    border-color: #2a6aaa !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: rgba(5,13,26,0.8) !important;
    border: 1px solid #1a3060 !important;
    border-radius: 0 10px 10px 10px !important;
    padding: 1rem !important;
}

/* Divider */
hr { border-color: #1a3060 !important; }

/* Metric widget */
[data-testid="metric-container"] {
    background: rgba(10,30,80,0.4);
    border: 1px solid #1a3a6a;
    border-radius: 10px;
    padding: 10px;
}
[data-testid="metric-container"] label { color: #4a80b0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb { background: #1a3a6a; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTADO
# ─────────────────────────────────────────────
if "dados" not in st.session_state:
    st.session_state.dados = carregar()

dados = st.session_state.dados

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
st.markdown('<div class="titulo-principal">🏆 Plano Estratégico de Carreira</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">JUAN FELIPE DA SILVA · RUMO AO CISSP</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🗺️  TABULEIRO", "📅  CALENDÁRIO", "🏅  CERTIFICAÇÕES"])

# ═══════════════════════════════════════════
# TAB 1 – TABULEIRO
# ═══════════════════════════════════════════
with tab1:
    col_board, col_sidebar = st.columns([3, 1.2])

    with col_board:
        st.markdown('<div class="tabuleiro-container">', unsafe_allow_html=True)

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

        def render_casa(n):
            casa = dados["casa"]
            is_atual = (n == casa)
            is_feita = (n < casa)
            is_cert  = (n in CERT_MAP)
            is_inicio = (n == 1)
            is_fim    = (n == 50)

            if is_inicio:
                cls = "casa casa-inicio"
                label = "▶"
            elif is_fim:
                cls = "casa casa-fim"
                label = "★"
            elif is_atual:
                cls = "casa casa-atual"
                label = "JF"
                if is_cert:
                    c = CERT_MAP[n]
                    cls += " casa-cert"
            elif is_cert:
                c = CERT_MAP[n]
                bg = c[1]
                if is_feita:
                    cls = "casa casa-cert casa-feita"
                    label = "✓"
                    return f'<div class="{cls}" style="border-color:{bg};background:rgba(10,42,26,0.8)" title="{c[2]}">{label}</div>'
                else:
                    cls = "casa casa-cert"
                    label = c[0]
                    return f'<div class="{cls}" style="border-color:{bg};background:rgba(10,20,40,0.8);color:{bg}" title="{c[2]}">{label}</div>'
            elif is_feita:
                cls = "casa casa-feita"
                label = "✓"
            else:
                cls = "casa casa-normal"
                label = str(n)

            return f'<div class="{cls}">{label}</div>'

        # Row 1: casas 1-12
        st.markdown('<div style="margin-bottom:4px"><span class="label-fase" style="background:#0a2a0a;color:#2a8a4a">🚀 FASE 1: DECOLAGEM</span></div>', unsafe_allow_html=True)
        row1 = "".join(render_casa(n) for n in range(1, 13))
        st.markdown(f'<div class="row-casas">{row1}</div>', unsafe_allow_html=True)

        # Seta de transição
        st.markdown('<div style="text-align:right;color:#2a6a4a;font-size:20px;margin-right:18px">↓</div>', unsafe_allow_html=True)

        # Row 2: casas 13-25 (reverso)
        st.markdown('<div style="text-align:right;margin-bottom:4px"><span class="label-fase" style="background:#0a1a2a;color:#2a6a9a">🏗️ FASE 2: CONSTRUÇÃO</span></div>', unsafe_allow_html=True)
        row2 = "".join(render_casa(n) for n in range(25, 12, -1))
        st.markdown(f'<div class="row-casas reverso">{row2}</div>', unsafe_allow_html=True)

        st.markdown('<div style="color:#4a6a30;font-size:20px;margin-left:18px">↓</div>', unsafe_allow_html=True)

        # Row 3: casas 26-38
        st.markdown('<div style="margin-bottom:4px"><span class="label-fase" style="background:#2a1a0a;color:#9a6a2a">⚙️ FASE 3: ESTRATÉGIA</span></div>', unsafe_allow_html=True)
        row3 = "".join(render_casa(n) for n in range(26, 39))
        st.markdown(f'<div class="row-casas">{row3}</div>', unsafe_allow_html=True)

        st.markdown('<div style="text-align:right;color:#5a2a7a;font-size:20px;margin-right:18px">↓</div>', unsafe_allow_html=True)

        # Row 4: casas 39-50 (reverso)
        st.markdown('<div style="text-align:right;margin-bottom:4px"><span class="label-fase" style="background:#1a0a2a;color:#8a50aa">👑 FASE 4: CONSOLIDAÇÃO</span></div>', unsafe_allow_html=True)
        row4 = "".join(render_casa(n) for n in range(50, 38, -1))
        st.markdown(f'<div class="row-casas reverso">{row4}</div>', unsafe_allow_html=True)

        # Legenda insígnias
        st.markdown("<hr>", unsafe_allow_html=True)
        legend = "".join(
            f'<span class="insignia" style="background:{c[1]};color:#fff" title="{c[2]}">{c[0]}</span> '
            for c in CERT_MAP.values()
        )
        st.markdown(f'<div style="font-size:11px;color:#3a6080;margin-bottom:4px">MARCOS DE CERTIFICAÇÃO:</div>{legend}', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_sidebar:
        # Métricas
        fase_atual, fase_dados = get_fase(dados["casa"])
        pct = round(dados["casa"] / 50 * 100)

        st.markdown(f"""
        <div class="card-dark">
            <div style="font-size:12px;color:#4a80b0;letter-spacing:2px;margin-bottom:8px">STATUS ATUAL</div>
            <div style="display:flex;align-items:baseline;gap:8px">
                <span style="font-size:3rem;font-weight:700;color:#4ab0ff;font-family:'Share Tech Mono'">{dados['casa']}</span>
                <span style="color:#3a6080;font-size:1rem">/ 50</span>
            </div>
            <div class="xp-container"><div class="xp-fill" style="width:{pct}%"></div></div>
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#3a6080">
                <span>{pct}% completo</span>
                <span>{dados['xp']:,} XP</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        cor_fase = fase_dados["cor"]
        st.markdown(f"""
        <div class="card-fase" style="border-color:{cor_fase}">
            <div style="font-size:10px;color:#4a6080;letter-spacing:1px">FASE ATUAL</div>
            <div style="font-size:13px;font-weight:600;color:{cor_fase};margin:2px 0">{fase_dados['emoji']} {fase_atual}</div>
            <div style="font-size:10px;color:#3a5070">
                Casas {fase_dados['range'][0]} – {fase_dados['range'][1]}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Próximas metas
        st.markdown('<div style="font-size:11px;color:#4a80b0;letter-spacing:2px;margin:12px 0 6px">PRÓXIMAS METAS</div>', unsafe_allow_html=True)
        for sigla, cor, nome, prazo in fase_dados["metas"]:
            done = nome in dados.get("concluidas", [])
            opacity = "1" if not done else "0.5"
            check = "✓ " if done else ""
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;opacity:{opacity}">
                <span class="insignia {'done' if done else 'pending'}" style="background:{cor};color:#fff;width:30px;height:30px;font-size:9px">{sigla}</span>
                <div>
                    <div style="font-size:12px;color:{'#4a9a5a' if done else '#a8c8e8'}">{check}{nome}</div>
                    <div style="font-size:9px;color:#3a6080;font-family:'Share Tech Mono'">{prazo}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Botões
        c1, c2 = st.columns(2)
        with c1:
            if st.button("▶ Avançar", use_container_width=True):
                if dados["casa"] < 50:
                    dados["casa"] += 1
                    dados["xp"] = dados.get("xp", 0) + 100
                    today_key = str(date.today())
                    if today_key not in dados.get("eventos", {}):
                        dados.setdefault("eventos", {})[today_key] = []
                    dados["eventos"][today_key].append({
                        "titulo": f"Casa {dados['casa']} concluída",
                        "desc": "Avançou no tabuleiro"
                    })
                    salvar(dados)
                    st.rerun()
                else:
                    st.balloons()
        with c2:
            if st.button("◀ Voltar", use_container_width=True):
                if dados["casa"] > 1:
                    dados["casa"] -= 1
                    dados["xp"] = max(0, dados.get("xp", 0) - 100)
                    salvar(dados)
                    st.rerun()

        if st.button("🔄 Resetar Jogo", use_container_width=True):
            dados.update({"casa": 1, "xp": 0, "concluidas": [], "eventos": {}})
            salvar(dados)
            st.rerun()

        if dados["casa"] == 50:
            st.balloons()
            st.markdown('<div style="text-align:center;font-size:1.2rem;color:#c080ff;animation:pulse 1s infinite">🏆 CISSP CONQUISTADO!</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# TAB 2 – CALENDÁRIO
# ═══════════════════════════════════════════
with tab2:
    hoje = date.today()

    if "cal_mes" not in st.session_state:
        st.session_state.cal_mes = hoje.month
    if "cal_ano" not in st.session_state:
        st.session_state.cal_ano = hoje.year

    MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    col_prev, col_title, col_next = st.columns([1, 4, 1])
    with col_prev:
        if st.button("← Anterior"):
            if st.session_state.cal_mes == 1:
                st.session_state.cal_mes = 12
                st.session_state.cal_ano -= 1
            else:
                st.session_state.cal_mes -= 1
            st.rerun()
    with col_title:
        st.markdown(
            f'<div style="text-align:center;font-size:1.3rem;font-weight:700;color:#7eb8ff;letter-spacing:2px">'
            f'{MESES[st.session_state.cal_mes-1].upper()} {st.session_state.cal_ano}</div>',
            unsafe_allow_html=True
        )
    with col_next:
        if st.button("Próximo →"):
            if st.session_state.cal_mes == 12:
                st.session_state.cal_mes = 1
                st.session_state.cal_ano += 1
            else:
                st.session_state.cal_mes += 1
            st.rerun()

    # Cabeçalho dias da semana
    dias_sem = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
    header_html = "".join(f'<div class="cal-header">{d}</div>' for d in dias_sem)

    # Gerar dias do mês
    primeiro_dia = date(st.session_state.cal_ano, st.session_state.cal_mes, 1)
    dias_no_mes = calendar.monthrange(st.session_state.cal_ano, st.session_state.cal_mes)[1]
    inicio = primeiro_dia.weekday()
    inicio_ajust = (inicio + 1) % 7  # ajusta para Dom=0

    eventos = dados.get("eventos", {})

    dias_html = ""
    # Espaços vazios antes do dia 1
    for _ in range(inicio_ajust):
        dias_html += '<div style="min-height:60px"></div>'

    for d in range(1, dias_no_mes + 1):
        key = f"{st.session_state.cal_ano}-{st.session_state.cal_mes:02d}-{d:02d}"
        is_hoje = (d == hoje.day and st.session_state.cal_mes == hoje.month and st.session_state.cal_ano == hoje.year)
        evts = eventos.get(key, [])

        cls = "cal-dia"
        if is_hoje: cls += " hoje"
        if evts: cls += " tem-evento"

        evts_html = ""
        for e in evts[:2]:
            evts_html += f'<div class="cal-evento">{e["titulo"]}</div>'
        if len(evts) > 2:
            evts_html += f'<div class="cal-evento" style="color:#3a6a9a">+{len(evts)-2} mais</div>'

        hoje_dot = '🔵 ' if is_hoje else ''
        dias_html += f'<div class="{cls}"><div class="num-dia">{hoje_dot}{d}</div>{evts_html}</div>'

    st.markdown(
        f'<div class="cal-grid" style="grid-template-columns:repeat(7,1fr);gap:3px;margin-top:8px">'
        f'{header_html}{dias_html}</div>',
        unsafe_allow_html=True
    )

    # Formulário para adicionar evento
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#4a80b0;letter-spacing:2px;margin-bottom:8px">✏️ ADICIONAR ATIVIDADE</div>', unsafe_allow_html=True)

    col_dia, col_titulo, col_desc = st.columns([1, 2, 2])
    with col_dia:
        dia_sel = st.number_input("Dia", min_value=1, max_value=dias_no_mes, value=hoje.day, step=1)
    with col_titulo:
        titulo_evt = st.text_input("Título da atividade", placeholder="Ex: Estudei Security+")
    with col_desc:
        desc_evt = st.text_input("Descrição (opcional)", placeholder="Detalhes...")

    if st.button("➕ Salvar Atividade", use_container_width=True):
        if titulo_evt.strip():
            key = f"{st.session_state.cal_ano}-{st.session_state.cal_mes:02d}-{dia_sel:02d}"
            dados.setdefault("eventos", {}).setdefault(key, []).append({
                "titulo": titulo_evt.strip(),
                "desc": desc_evt.strip()
            })
            salvar(dados)
            st.success(f"✅ Atividade salva no dia {dia_sel}!")
            st.rerun()
        else:
            st.warning("Digite um título para a atividade.")

    # Listar eventos do mês
    mes_eventos = {k: v for k, v in eventos.items()
                   if k.startswith(f"{st.session_state.cal_ano}-{st.session_state.cal_mes:02d}")}

    if mes_eventos:
        st.markdown('<div style="font-size:12px;color:#4a80b0;letter-spacing:2px;margin:12px 0 6px">📋 ATIVIDADES DO MÊS</div>', unsafe_allow_html=True)
        for key in sorted(mes_eventos.keys()):
            dia_num = int(key.split("-")[2])
            for i, evt in enumerate(mes_eventos[key]):
                col_ev, col_del = st.columns([6, 1])
                with col_ev:
                    st.markdown(
                        f'<div style="background:#070f20;border:1px solid #1a3040;border-left:3px solid #1a5a30;'
                        f'border-radius:6px;padding:6px 10px;margin:2px 0">'
                        f'<span style="color:#2a7a4a;font-size:11px;font-family:\'Share Tech Mono\'">{dia_num:02d}/{st.session_state.cal_mes:02d}</span>'
                        f'<span style="color:#a8c8e8;margin-left:10px;font-size:13px">{evt["titulo"]}</span>'
                        f'{"<br><span style=\"color:#3a6080;font-size:11px\">"+evt["desc"]+"</span>" if evt.get("desc") else ""}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                with col_del:
                    if st.button("🗑️", key=f"del_{key}_{i}"):
                        dados["eventos"][key].pop(i)
                        if not dados["eventos"][key]:
                            del dados["eventos"][key]
                        salvar(dados)
                        st.rerun()

# ═══════════════════════════════════════════
# TAB 3 – CERTIFICAÇÕES
# ═══════════════════════════════════════════
with tab3:
    st.markdown('<div style="font-size:12px;color:#4a80b0;letter-spacing:2px;margin-bottom:12px">CLIQUE PARA MARCAR COMO CONCLUÍDA</div>', unsafe_allow_html=True)

    concluidas = dados.get("concluidas", [])
    total_certs = sum(len(v["metas"]) for v in FASES.values())
    total_feitas = len(concluidas)

    # Progresso geral
    pct_certs = round(total_feitas / total_certs * 100) if total_certs else 0
    st.markdown(f"""
    <div class="card-dark" style="margin-bottom:16px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <span style="color:#7eb8ff;font-weight:600">Progresso das Certificações</span>
            <span style="color:#4ab0ff;font-family:'Share Tech Mono';font-size:1.1rem">{total_feitas}/{total_certs}</span>
        </div>
        <div class="xp-container"><div class="xp-fill" style="width:{pct_certs}%"></div></div>
        <div style="font-size:11px;color:#3a6080;text-align:right">{pct_certs}% completo</div>
    </div>
    """, unsafe_allow_html=True)

    for fase_nome, fase_dados in FASES.items():
        cor = fase_dados["cor"]
        emoji = fase_dados["emoji"]
        metas = fase_dados["metas"]
        feitas_fase = sum(1 for _, _, nome, _ in metas if nome in concluidas)

        with st.expander(f"{emoji} {fase_nome}  —  {feitas_fase}/{len(metas)} concluídas", expanded=True):
            cols = st.columns(2)
            for idx, (sigla, cor_cert, nome, prazo) in enumerate(metas):
                done = nome in concluidas
                with cols[idx % 2]:
                    col_check, col_info = st.columns([1, 5])
                    with col_check:
                        checked = st.checkbox("", value=done, key=f"cert_{fase_nome}_{idx}")
                        if checked and nome not in concluidas:
                            concluidas.append(nome)
                            dados["concluidas"] = concluidas
                            dados["xp"] = dados.get("xp", 0) + 250
                            salvar(dados)
                            st.rerun()
                        elif not checked and nome in concluidas:
                            concluidas.remove(nome)
                            dados["concluidas"] = concluidas
                            dados["xp"] = max(0, dados.get("xp", 0) - 250)
                            salvar(dados)
                            st.rerun()
                    with col_info:
                        opacity = "1" if not done else "0.7"
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;opacity:{opacity};margin-bottom:4px">
                            <span class="insignia {'done' if done else ''}" 
                                  style="background:{cor_cert};color:#fff;width:36px;height:36px;font-size:9px">
                                {'✓' if done else sigla}
                            </span>
                            <div>
                                <div style="font-size:13px;color:{'#4a9a5a' if done else '#c8dff0'};
                                            {'text-decoration:line-through' if done else ''}">{nome}</div>
                                <div style="font-size:10px;color:#3a6080;font-family:'Share Tech Mono'">{prazo}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;font-size:10px;color:#1a3a6a;letter-spacing:2px;font-family:\'Share Tech Mono\'">'
    'DESENVOLVIDO POR JUAN FELIPE DA SILVA · RUMO AO CISSP · 2025–2029'
    '</div>',
    unsafe_allow_html=True
)
