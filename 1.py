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
   # ─────────────────────────────────────────────
# DADOS ATUALIZADOS DO PLANEJAMENTO (2026-2029)
# ─────────────────────────────────────────────

FASES = {
    "2026: BASE + INÍCIO DA PÓS": {
        "range": (1, 12), "cor": "#1a6abf", "emoji": "🚀",
        "metas": [
            ("AZ",  "#0078d4", "Azure Fundamentals (AZ-900)", "Abr/2026"),
            ("ISO", "#e53935", "ISO/IEC 27001 Fundamentals", "Mai/2026"),
            ("PÓS", "#7b1fa2", "Pós-graduação (Início)",      "Jun/2026"),
            ("CCNA","#00b4ad", "Cisco CCNA",                  "Jul/2026"),
            ("SC",  "#3267d3", "Microsoft (SC-900)",          "Out/2026"),
            ("EN",  "#00695c", "Inglês (30-40 min/dia)",      "Diário"),
        ]
    },
    "2027: SEGURANÇA + OT + GOVERNANÇA": {
        "range": (13, 28), "cor": "#2e7d32", "emoji": "🛡️",
        "metas": [
            ("S+",  "#cc6600", "CompTIA Security+",           "Fev/2027"),
            ("LI",  "#1565c0", "ISO 27001 Lead Implementer",  "Mai/2027"),
            ("624", "#f57c00", "ISA/IEC 62443 Fundamentals",  "Ago/2027"),
            ("MT",  "#4a148c", "MITRE ATT&CK for ICS",        "Out/2027"),
            ("Cy",  "#d32f2f", "CompTIA CySA+",               "Dez/2027"),
        ]
    },
    "2028: ESPECIALIZAÇÃO + FINAL PÓS": {
        "range": (29, 42), "cor": "#e65100", "emoji": "⚙️",
        "metas": [
            ("GI",  "#2e7d32", "Global ICS Prof. (GICSP)",    "Mar/2028"),
            ("LA",  "#bf360c", "ISO 27001 Lead Auditor",      "Ago/2028"),
            ("🎓",  "#6a1c77", "Conclusão Pós-graduação",     "Dez/2028"),
        ]
    },
    "2029: CONSOLIDAÇÃO": {
        "range": (43, 50), "cor": "#6a1c77", "emoji": "👑",
        "metas": [
            ("CIS", "#b71c1c", "CISSP (Meta Final)",          "Jun/2029"),
            ("EN+", "#01579b", "Inglês: Fluência Funcional",  "2029"),
        ]
    }
}

# Mapeia as casas específicas do tabuleiro para mostrar os troféus
CERT_MAP = {
    4:  ("AZ",  "#0078d4", "AZ-900"),
    8:  ("ISO", "#e53935", "ISO 27001"),
    12: ("CCNA","#00b4ad", "CCNA"),
    16: ("SC",  "#3267d3", "SC-900"),
    20: ("S+",  "#cc6600", "Security+"),
    24: ("624", "#f57c00", "ISA 62443"),
    30: ("Cy",  "#d32f2f", "CySA+"),
    36: ("GI",  "#2e7d32", "GICSP"),
    45: ("LA",  "#bf360c", "Lead Auditor"),
    50: ("🏆",  "#8a30c0", "CISSP"),
}
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
