import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# Configuração da página
st.set_page_config(
    page_title="Plano de Carreira - Juan Felipe",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# DADOS E CRONOGRAMA (LIMITE 80 CASAS)
# ─────────────────────────────────────────────
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
DATA_INICIO = date(2026, 4, 18) # Hoje

# Temas baseados no seu planejamento para as 80 semanas
TEMAS_MAP = [
    (1, 4, "AZ-900", "#0078d4", "Azure Fundamentals"),
    (5, 8, "ISO-F", "#e53935", "ISO 27001 Fund."),
    (9, 12, "PÓS", "#7b1fa2", "Início Pós-Graduação"),
    (13, 24, "CCNA", "#00b4ad", "Cisco Networking"),
    (25, 32, "SC-900", "#3267d3", "Security & Compliance"),
    (33, 48, "S+", "#cc6600", "CompTIA Security+"),
    (49, 60, "ISO-LI", "#1565c0", "ISO 27001 Lead Imp."),
    (61, 72, "62443", "#f57c00", "ISA/IEC 62443"),
    (73, 80, "MITRE", "#4a148c", "MITRE ATT&CK ICS"),
]

def get_info_casa(n):
    for inicio, fim, sigla, cor, nome in TEMAS_MAP:
        if inicio <= n <= fim:
            return sigla, cor, nome
    return str(n), "#3a6080", ""

ARQUIVO = "progresso_juan_80.json"

# ─────────────────────────────────────────────
# PERSISTÊNCIA
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

if "dados" not in st.session_state:
    st.session_state.dados = carregar()
dados = st.session_state.dados

# ─────────────────────────────────────────────
# ESTILOS E LOGIN
# ─────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center; color:#7eb8ff;'>SISTEMA DE ACESSO</h1>", unsafe_allow_html=True)
    with st.container():
        _, col_c, _ = st.columns([1,1,1])
        with col_c:
            u = st.text_input("Usuário")
            p = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if u == USER_LOGIN and p == USER_PASS:
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("Acesso negado")
    st.stop()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #050d1a !important; color: #c8dff0; font-family: 'Rajdhani'; }
    .casa { display: inline-flex; flex-direction: column; align-items: center; justify-content: center; width: 70px; height: 70px; border-radius: 12px; font-size: 10px; margin: 4px; border: 2px solid; text-align: center; }
    .casa-atual { border-color: #4a90d9; background: #1a4a8a; box-shadow: 0 0 15px #4a90d9; animation: pulse 1.5s infinite; }
    .casa-feita { border-color: #1a5a30; background: #0a2a1a; color: #2a8a4a; }
    .casa-normal { border-color: #1a3a60; background: #0a1a2e; color: #3a6080; }
    .label-cert { font-size: 8px; font-weight: bold; margin-top: 2px; }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INTERFACE PRINCIPAL
# ─────────────────────────────────────────────
st.title("🏆 Plano de Carreira - Juan Felipe")

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO", "📅 CALENDÁRIO & NOTAS", "🏅 CONQUISTAS"])

# ABA 1: TABULEIRO (PADRÃO ANTIGO - 80 CASAS)
with tab1:
    col_t, col_s = st.columns([4, 1])
    with col_t:
        st.markdown('<div style="background:#061020; padding:15px; border-radius:15px; border:1px solid #1a3a6a">', unsafe_allow_html=True)
        
        # Grid de 10 colunas por linha para as 80 casas
        for i in range(8):
            reverso = i % 2 != 0
            intervalo = range(i*10 + 1, (i+1)*10 + 1)
            row_html = ""
            for n in (reversed(intervalo) if reverso else intervalo):
                sigla, cor, nome_full = get_info_casa(n)
                
                c_cls = "casa casa-atual" if n == dados['casa'] else ("casa casa-feita" if n < dados['casa'] else "casa casa-normal")
                borda_style = f"border-color: {cor if n >= dados['casa'] else '#1a5a30'}"
                
                row_html += f'<div class="{c_cls}" style="{borda_style}">{sigla}<div class="label-cert">S{n}</div></div>'
            st.markdown(f'<div style="display:flex; justify-content:center; flex-wrap:wrap">{row_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s:
        sigla_atual, _, nome_atual = get_info_casa(dados['casa'])
        data_casa = DATA_INICIO + timedelta(weeks=dados['casa']-1)
        
        st.metric("XP TOTAL", f"{dados['xp']} pts")
        st.metric("SEMANA", f"{dados['casa']} / 80")
        st.markdown(f"**Foco:** {nome_atual}")
        st.caption(f"Início: {data_casa.strftime('%d/%m/%Y')}")
        
        if st.button("Avançar Semana ▶", use_container_width=True):
            if dados['casa'] < 80:
                dados['casa'] += 1
                dados['xp'] += 100
                salvar(dados); st.rerun()
        if st.button("Voltar Semana ◀", use_container_width=True):
            if dados['casa'] > 1:
                dados['casa'] -= 1
                dados['xp'] = max(0, dados['xp'] - 100)
                salvar(dados); st.rerun()

# ABA 2: CALENDÁRIO & NOTAS
with tab2:
    st.markdown("### 📅 Diário de Bordo")
    c1, c2 = st.columns([1, 2])
    with c1:
        data_sel = st.date_input("Selecione o dia", date.today())
        nota = st.text_area("Notas de estudo:")
        if st.button("Salvar Nota 💾", use_container_width=True):
            dados.setdefault("eventos", {})[str(data_sel)] = nota
            salvar(dados); st.success("Nota salva!")
    with c2:
        if "eventos" in dados and dados["eventos"]:
            for d_key in sorted(dados["eventos"].keys(), reverse=True):
                with st.expander(f"📌 Dia {d_key}"):
                    st.write(dados["eventos"][d_key])

# ABA 3: CHECKLIST CONQUISTAS
with tab3:
    st.markdown("### 🏅 Minhas Certificações")
    certs_lista = [t[2] for t in TEMAS_MAP]
    concluidas = dados.get("concluidas", [])
    
    for cert in certs_lista:
        checked = cert in concluidas
        if st.checkbox(cert, value=checked):
            if cert not in concluidas:
                concluidas.append(cert)
                dados["xp"] += 500
                salvar(dados); st.rerun()
        elif checked:
            concluidas.remove(cert)
            dados["xp"] = max(0, dados["xp"] - 500)
            salvar(dados); st.rerun()
    dados["concluidas"] = concluidas
