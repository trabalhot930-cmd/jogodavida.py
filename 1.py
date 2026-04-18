import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# Configuração da página
st.set_page_config(
    page_title="Plano de Carreira - Juan Felipe",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DO PLANEJAMENTO (ESTRUTURA SEMANAL)
# ─────────────────────────────────────────────
DATA_INICIO_S1 = date(2026, 4, 18)  # Data de hoje

# Definição dos blocos de estudo conforme seu planejamento
ESTRUTURA_OBJETIVOS = [
    {"tema": "Azure Fundamentals (AZ-900)", "semanas": 4, "cor": "#0078d4", "emoji": "☁️", "prazo": "Abr/2026"},
    {"tema": "ISO/IEC 27001 Fundamentals", "semanas": 4, "cor": "#e53935", "emoji": "📄", "prazo": "Mai/2026"},
    {"tema": "Pós-graduação (Início)", "semanas": 4, "cor": "#7b1fa2", "emoji": "🎓", "prazo": "Jun/2026"},
    {"tema": "Cisco CCNA", "semanas": 12, "cor": "#00b4ad", "emoji": "🌐", "prazo": "Jul/2026"},
    {"tema": "Microsoft Security (SC-900)", "semanas": 8, "cor": "#3267d3", "emoji": "🔐", "prazo": "Out/2026"},
    {"tema": "CompTIA Security+", "semanas": 16, "cor": "#cc6600", "emoji": "🛡️", "prazo": "Fev/2027"},
    {"tema": "ISO 27001 Lead Implementer", "semanas": 12, "cor": "#1565c0", "emoji": "🏗️", "prazo": "Mai/2027"},
    {"tema": "ISA/IEC 62443 Fundamentals", "semanas": 12, "cor": "#f57c00", "emoji": "⚙️", "prazo": "Ago/2027"},
    {"tema": "MITRE ATT&CK for ICS", "semanas": 8, "cor": "#4a148c", "emoji": "🎯", "prazo": "Out/2027"},
    {"tema": "CompTIA CySA+", "semanas": 12, "cor": "#d32f2f", "emoji": "🔍", "prazo": "Dez/2027"},
    {"tema": "Global Industrial Cyber Security (GICSP)", "semanas": 15, "cor": "#2e7d32", "emoji": "🌍", "prazo": "Mar/2028"},
    {"tema": "ISO 27001 Lead Auditor", "semanas": 12, "cor": "#bf360c", "emoji": "⚖️", "prazo": "Ago/2028"},
    {"tema": "Conclusão Pós-graduação", "semanas": 12, "cor": "#6a1c77", "emoji": "🎓", "prazo": "Dez/2028"},
    {"tema": "META FINAL: CISSP", "semanas": 25, "cor": "#b71c1c", "emoji": "👑", "prazo": "Jun/2029"},
]

# Gerar o mapeamento semanal para o tabuleiro
MAPA_SEMANAL = []
contador = 1
for obj in ESTRUTURA_OBJETIVOS:
    for s in range(obj["semanas"]):
        MAPA_SEMANAL.append({
            "casa": contador,
            "tema": obj["tema"],
            "cor": obj["cor"],
            "emoji": obj["emoji"],
            "prazo": obj["prazo"]
        })
        contador += 1

TOTAL_CASAS = len(MAPA_SEMANAL)

# ─────────────────────────────────────────────
# PERSISTÊNCIA E LOGIN
# ─────────────────────────────────────────────
ARQUIVO = "progresso_roadmap.json"
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"

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

# Estilo Global (CSS)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {{ background: #050d1a !important; color: #c8dff0; font-family: 'Rajdhani'; }}
    .casa {{ display: inline-flex; flex-direction: column; align-items: center; justify-content: center; width: 80px; height: 80px; border-radius: 10px; font-size: 10px; margin: 4px; border: 2px solid; text-align: center; background: #0a1a2e; }}
    .casa-atual {{ border-color: #00f2ff !important; box-shadow: 0 0 15px #00f2ff; background: #112a45; animation: pulse 1.5s infinite; }}
    .casa-feita {{ border-color: #00ff41 !important; color: #00ff41; opacity: 0.6; }}
    .casa-normal {{ border-color: #1a3a60; color: #3a6080; }}
    @keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.03); }} }}
</style>
""", unsafe_allow_html=True)

if "dados" not in st.session_state:
    st.session_state.dados = carregar()
dados = st.session_state.dados

# ─────────────────────────────────────────────
# INTERFACE
# ─────────────────────────────────────────────
st.title("🏆 Cyber Roadmap Game - Juan Felipe")

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO SEMANAL", "📅 CALENDÁRIO & NOTAS", "🏅 CHECKLIST CONQUISTAS"])

# ABA 1: TABULEIRO
with tab1:
    col_t, col_s = st.columns([4, 1])
    
    with col_t:
        st.markdown('<div style="background:#061020; padding:20px; border-radius:15px; border:1px solid #1a3a6a">', unsafe_allow_html=True)
        # Renderizar o tabuleiro em linhas de 10
        for i in range(0, TOTAL_CASAS, 10):
            row_html = ""
            for n in range(i + 1, min(i + 11, TOTAL_CASAS + 1)):
                info = MAPA_SEMANAL[n-1]
                c_cls = "casa casa-atual" if n == dados['casa'] else ("casa casa-feita" if n < dados['casa'] else "casa casa-normal")
                borda = info['cor'] if n >= dados['casa'] else "#00ff41"
                
                row_html += f"""
                <div class="{c_cls}" style="border-color: {borda}">
                    <div style="font-size:12px">{info['emoji']}</div>
                    <div style="font-weight:bold">S{n}</div>
                    <div style="font-size:8px; line-height:1">{info['prazo']}</div>
                </div>
                """
            st.markdown(f'<div style="display:flex; justify-content:center; flex-wrap:wrap">{row_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s:
        info_atual = MAPA_SEMANAL[dados['casa']-1]
        data_atual = DATA_INICIO_S1 + timedelta(weeks=dados['casa']-1)
        
        st.metric("XP TOTAL", f"{dados['xp']} pts")
        st.metric("SEMANA", f"{dados['casa']} / {TOTAL_CASAS}")
        
        st.markdown("---")
        st.markdown(f"**Meta Atual:**\n### {info_atual['tema']}")
        st.caption(f"Inicia em: {data_atual.strftime('%d/%m/%Y')}")
        
        if st.button("Concluir Semana +100 XP ⚔️", use_container_width=True):
            if dados['casa'] < TOTAL_CASAS:
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
        nota = st.text_area("O que foi estudado hoje?", placeholder="Ex: Lab de SQL, curso da Hashtag...")
        if st.button("Salvar Log 💾", use_container_width=True):
            dados.setdefault("eventos", {})[str(data_sel)] = nota
            salvar(dados); st.success("Nota salva!")
    with c2:
        st.markdown("#### Histórico")
        if "eventos" in dados and dados["eventos"]:
            for d in sorted(dados["eventos"].keys(), reverse=True):
                with st.expander(f"📌 {d}"):
                    st.write(dados["eventos"][d])
                    if st.button("Remover", key=f"del_{d}"):
                        del dados["eventos"][d]
                        salvar(dados); st.rerun()

# ABA 3: CHECKLIST CONQUISTAS
with tab3:
    st.markdown("### 🏅 Certificações e Marcos")
    concluidas = dados.get("concluidas", [])
    
    # Criar checklist com base nos objetivos principais
    for obj in ESTRUTURA_OBJETIVOS:
        checked = obj["tema"] in concluidas
        if st.checkbox(f"{obj['emoji']} {obj['tema']} ({obj['prazo']})", value=checked, key=f"chk_{obj['tema']}"):
            if obj["tema"] not in concluidas:
                concluidas.append(obj["tema"])
                dados["xp"] += 500  # Bônus de conquista
                salvar(dados); st.rerun()
        elif checked:
            concluidas.remove(obj["tema"])
            dados["xp"] = max(0, dados["xp"] - 500)
            salvar(dados); st.rerun()
    
    dados["concluidas"] = concluidas
