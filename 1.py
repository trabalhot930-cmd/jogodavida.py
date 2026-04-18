import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# Configuração da página
st.set_page_config(
    page_title="Roadmap Alpha - Juan Felipe",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DO CRONOGRAMA SEMANAL (165 SEMANAS)
# ─────────────────────────────────────────────
DATA_INICIO = date(2026, 4, 1)

# Mapeamento de temas por período (Semanas aproximadas)
TEMAS_SEMANAIS = [
    (1, 4, "AZ-900: Cloud Fundamentals", "#0078d4"),
    (5, 8, "ISO 27001: Fundamentos", "#e53935"),
    (9, 13, "Pós-Graduação: Módulo 1", "#7b1fa2"),
    (14, 20, "Cisco CCNA: Networking", "#00b4ad"),
    (21, 26, "SC-900: Security & Compliance", "#3267d3"),
    (27, 40, "Inglês Técnico & Docs", "#00695c"),
    (41, 52, "CompTIA Security+: Core", "#cc6600"),
    (53, 65, "ISO 27001: Lead Implementer", "#1565c0"),
    (66, 78, "ISA/IEC 62443: Segurança OT", "#f57c00"),
    (79, 85, "MITRE ATT&CK for ICS", "#4a148c"),
    (86, 95, "CompTIA CySA+: Analista", "#d32f2f"),
    (96, 110, "GICSP: Industrial Cyber Security", "#2e7d32"),
    (111, 130, "ISO 27001: Lead Auditor", "#bf360c"),
    (131, 145, "Pós-Graduação: TCC / Conclusão", "#6a1c77"),
    (146, 165, "MASTER: Preparação CISSP", "#b71c1c"),
]

def get_tema_semana(n):
    for inicio, fim, nome, cor in TEMAS_SEMANAIS:
        if inicio <= n <= fim:
            return nome, cor
    return "Consolidação", "#333"

# ─────────────────────────────────────────────
# PERSISTÊNCIA
# ─────────────────────────────────────────────
ARQUIVO = "progresso_semanal_jf.json"

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"casa": 1, "xp": 0, "eventos": {}}

def salvar(d):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

# ─────────────────────────────────────────────
# ESTILOS INTERFACE
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #02060d !important; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background: #0a192f; border-radius: 5px; color: white; padding: 10px 20px; }
    
    .casa { 
        display: inline-flex; flex-direction: column; align-items: center; justify-content: center; 
        width: 100px; height: 100px; border-radius: 8px; font-size: 11px; margin: 5px; 
        border: 2px solid; text-align: center; transition: 0.3s;
    }
    .casa-atual { border-color: #00f2ff; background: #003366; box-shadow: 0 0 15px #00f2ff; font-weight: bold; }
    .casa-feita { border-color: #00ff41; background: #0a2612; color: #00ff41; opacity: 0.7; }
    .casa-normal { border-color: #1a3a6a; background: #050d1a; color: #4e6e8e; }
    .tema-label { font-size: 8px; margin-top: 5px; line-height: 1; }
</style>
""", unsafe_allow_html=True)

if "dados" not in st.session_state:
    st.session_state.dados = carregar()
dados = st.session_state.dados

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
st.title("🛡️ Cyber Security Warrior - Juan Felipe")
st.subheader("Foco Semanal: 2026 — 2029")

tab1, tab2 = st.tabs(["🗺️ TABULEIRO DE CARREIRA", "📝 NOTAS DA SEMANA"])

with tab1:
    col_info, col_btn = st.columns([3, 1])
    
    current_tema, current_cor = get_tema_semana(dados['casa'])
    data_casa = DATA_INICIO + timedelta(weeks=dados['casa']-1)
    
    with col_info:
        st.markdown(f"**Semana {dados['casa']}** | Iniciando em: {data_casa.strftime('%d/%m/%Y')}")
        st.markdown(f"<h2 style='color:{current_cor}'>{current_tema}</h2>", unsafe_allow_html=True)
    
    with col_btn:
        if st.button("Concluir Semana +100 XP ⚔️", use_container_width=True):
            if dados['casa'] < 165:
                dados['casa'] += 1
                dados['xp'] += 100
                salvar(dados); st.rerun()
        st.progress(dados['casa'] / 165)

    # Renderização do Tabuleiro (Grades de 10 por linha)
    st.write("---")
    num_casas = 165
    for row in range(0, num_casas, 10):
        cols_html = ""
        for n in range(row + 1, min(row + 11, num_casas + 1)):
            tema_n, cor_n = get_tema_semana(n)
            
            c_cls = "casa casa-atual" if n == dados['casa'] else ("casa casa-feita" if n < dados['casa'] else "casa casa-normal")
            style = f"border-color: {cor_n if n >= dados['casa'] else '#00ff41'}"
            
            cols_html += f"""
            <div class="{c_cls}" style="{style}">
                <div style="font-size:14px">S{n}</div>
                <div class="tema-label">{tema_n[:20]}...</div>
            </div>
            """
        st.markdown(f'<div style="display:flex; flex-wrap:wrap; justify-content:center">{cols_html}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 📝 Notas de Estudo e Logs de Segurança")
    data_nota = st.date_input("Data da nota", date.today())
    texto_nota = st.text_area("O que foi aprendido ou implementado nesta data?", height=150)
    
    if st.button("Salvar Log 💾"):
        key = str(data_nota)
        dados.setdefault("eventos", {})[key] = texto_nota
        salvar(dados)
        st.success("Log registrado com sucesso!")

    st.markdown("---")
    st.markdown("#### 📜 Histórico de Logs")
    if "eventos" in dados and dados["eventos"]:
        for d in sorted(dados["eventos"].keys(), reverse=True):
            with st.expander(f"📅 {d}"):
                st.write(dados["eventos"][d])
