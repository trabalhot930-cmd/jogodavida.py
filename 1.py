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
    5:  ("S+",  "#cc6600", "CompTIA Security+"),
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
# FUNÇÕES DE PERSISTÊNCIA
# ─────────────────────────────────────────────
def carregar():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"casa": 1, "xp": 0, "concluidas": [], "eventos": {}}

def salvar(d):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

# ─────────────────────────────────────────────
# ESTILOS E LOGIN
# ─────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center; color:#7eb8ff;'>SISTEMA DE ACESSO</h1>", unsafe_allow_html=True)
    with st.container():
        col_l, col_c, col_r = st.columns([1,1,1])
        with col_c:
            u = st.text_input("Usuário")
            p = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if u == USER_LOGIN and p == USER_PASS:
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("Acesso negado")
    st.stop()

# Estilo Global
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;700&family=Share+Tech+Mono&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #050d1a !important; color: #c8dff0; font-family: 'Rajdhani'; }
    .card-dark { background: rgba(10, 25, 60, 0.8); border: 1px solid #1a3a6a; border-radius: 12px; padding: 1rem; margin-bottom: 10px; }
    .casa { display: inline-flex; flex-direction: column; align-items: center; justify-content: center; width: 68px; height: 68px; border-radius: 12px; font-size: 10px; margin: 4px; border: 2px solid; text-align: center; }
    .casa-atual { border-color: #4a90d9; background: #1a4a8a; box-shadow: 0 0 15px #4a90d9; animation: pulse 1.5s infinite; }
    .casa-feita { border-color: #1a5a30; background: #0a2a1a; color: #2a8a4a; }
    .casa-normal { border-color: #1a3a60; background: #0a1a2e; color: #3a6080; }
    .label-cert { font-size: 8px; font-weight: bold; margin-top: 2px; }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
</style>
""", unsafe_allow_html=True)

if "dados" not in st.session_state:
    st.session_state.dados = carregar()
dados = st.session_state.dados

# ─────────────────────────────────────────────
# INTERFACE PRINCIPAL
# ─────────────────────────────────────────────
st.title("🏆 Plano de Carreira - Juan Felipe")

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO", "📅 CALENDÁRIO & NOTAS", "🏅 CHECKLIST CONQUISTAS"])

# ABA 1: TABULEIRO
with tab1:
    col_t, col_s = st.columns([4, 1])
    with col_t:
        st.markdown('<div style="background:#061020; padding:15px; border-radius:15px; border:1px solid #1a3a6a">', unsafe_allow_html=True)
        # Lógica simplificada de 4 fileiras para visualização
        for i in range(4):
            reverso = i % 2 != 0
            intervalo = range(i*13 + 1, (i+1)*13 + 1)
            row_html = ""
            for n in (reversed(intervalo) if reverso else intervalo):
                if n > 50: continue
                cert = CERT_MAP.get(n)
                c_cls = "casa casa-atual" if n == dados['casa'] else ("casa casa-feita" if n < dados['casa'] else "casa casa-normal")
                label = cert[0] if cert else str(n)
                sub = f'<div class="label-cert">{cert[2]}</div>' if cert else ""
                row_html += f'<div class="{c_cls}">{label}{sub}</div>'
            st.markdown(f'<div style="display:flex; justify-content:{"flex-end" if reverso else "flex-start"}; flex-wrap:wrap">{row_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s:
        st.metric("XP TOTAL", f"{dados['xp']} pts")
        st.metric("CASA ATUAL", f"{dados['casa']} / 50")
        if st.button("Avançar ▶", use_container_width=True):
            if dados['casa'] < 50:
                dados['casa'] += 1
                dados['xp'] += 100
                salvar(dados); st.rerun()
        if st.button("Voltar ◀", use_container_width=True):
            if dados['casa'] > 1:
                dados['casa'] -= 1
                dados['xp'] = max(0, dados['xp'] - 100)
                salvar(dados); st.rerun()

# ABA 2: CALENDÁRIO & NOTAS
with tab2:
    st.markdown("### 📅 Diário de Bordo")
    hoje = date.today()
    c1, c2 = st.columns([1, 2])
    
    with c1:
        data_sel = st.date_input("Selecione o dia", hoje)
        nota = st.text_area("O que você estudou/concluiu hoje?", placeholder="Ex: Estudei 2h de SQL e fiz laboratório de Azure.")
        if st.button("Salvar Nota 💾", use_container_width=True):
            key = str(data_sel)
            dados.setdefault("eventos", {})[key] = nota
            salvar(dados)
            st.success("Nota salva!")
            
    with c2:
        st.markdown("#### Histórico de Atividades")
        if "eventos" in dados and dados["eventos"]:
            for d_key in sorted(dados["eventos"].keys(), reverse=True):
                with st.expander(f"📌 Dia {d_key}"):
                    st.write(dados["eventos"][d_key])
                    if st.button("Remover", key=f"del_{d_key}"):
                        del dados["eventos"][d_key]
                        salvar(dados); st.rerun()
        else:
            st.info("Nenhuma nota registrada ainda.")

# ABA 3: CHECKLIST CONQUISTAS
with tab3:
    st.markdown("### 🏅 Minhas Certificações")
    
    # Progresso Geral de Certs
    todas_metas = []
    for f in FASES.values():
        for m in f["metas"]: todas_metas.append(m[2])
    
    concluidas = dados.get("concluidas", [])
    total = len(todas_metas)
    pronto = len(concluidas)
    
    st.progress(pronto/total if total > 0 else 0)
    st.write(f"Concluídas: {pronto} de {total}")
    
    cols_f = st.columns(2)
    for idx, (nome_fase, info_fase) in enumerate(FASES.items()):
        with cols_f[idx % 2]:
            st.markdown(f"#### {info_fase['emoji']} {nome_fase}")
            for sigla, cor, nome_cert, prazo in info_fase["metas"]:
                checked = nome_cert in concluidas
                if st.checkbox(f"{nome_cert} ({prazo})", value=checked, key=f"chk_{nome_cert}"):
                    if nome_cert not in concluidas:
                        concluidas.append(nome_cert)
                        dados["xp"] += 500 # Bonus por cert
                        salvar(dados); st.rerun()
                elif checked:
                    concluidas.remove(nome_cert)
                    dados["xp"] = max(0, dados["xp"] - 500)
                    salvar(dados); st.rerun()
    dados["concluidas"] = concluidas
