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
# CRONOGRAMA ATUALIZADO (80 SEMANAS)
# ─────────────────────────────────────────────
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
DATA_INICIO = date(2026, 4, 18) 

# Mapeamento de temas conforme sua lista
TEMAS_MAP = [
    (1, 6, "AZ-900", "#0078d4", "Abr–Mai/26", "Microsoft Azure Fundamentals"),
    (7, 12, "ISO-F", "#e53935", "Jun–Jul/26", "ISO/IEC 27001 Fundamentals"),
    (13, 24, "CCNA", "#00b4ad", "Jun–Nov/26", "Cisco CCNA"),
    (25, 32, "AZ-104", "#005ba1", "Ago–Out/26", "Azure Administrator Associate"),
    (33, 40, "SC-900", "#3267d3", "Dez/26–Jan/27", "Security & Compliance"),
    (41, 50, "S+", "#cc6600", "Fev–Abr/27", "CompTIA Security+"),
    (51, 60, "CySA+", "#d32f2f", "Jun–Ago/27", "CompTIA CySA+"),
    (61, 70, "ISO-LI", "#1565c0", "Out–Dez/27", "ISO/IEC 27001 Lead Implementer"),
    (71, 75, "62443", "#f57c00", "Jan–Mar/28", "ISA/IEC 62443 Specialist"),
    (76, 80, "GICSP", "#2e7d32", "Mai–Jul/28", "Global Industrial Cyber"),
]

def get_info_casa(n):
    for inicio, fim, sigla, cor, data_txt, nome in TEMAS_MAP:
        if inicio <= n <= fim:
            return sigla, cor, data_txt, nome
    return str(n), "#3a6080", "", ""

ARQUIVO = "progresso_juan_v10.json"

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
# LOGIN
# ─────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>SISTEMA DE ACESSO</h1>", unsafe_allow_html=True)
    _, col_c, _ = st.columns([1,1,1])
    with col_c:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Entrar", use_container_width=True):
            if u == USER_LOGIN and p == USER_PASS:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# ─────────────────────────────────────────────
# ESTILOS E INTERFACE
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #050d1a !important; color: #c8dff0; font-family: 'Rajdhani'; }
    
    .casa { 
        display: inline-flex; flex-direction: column; align-items: center; justify-content: center; 
        width: 110px; height: 110px; border-radius: 12px; margin: 5px; border: 3px solid; 
        text-align: center; background: #0a1a2e;
    }
    .casa-atual { border-color: #00f2ff !important; box-shadow: 0 0 15px #00f2ff; background: #1a4a8a; }
    .casa-feita { border-color: #1a5a30 !important; background: #0a2a1a; color: #2a8a4a; opacity: 0.7; }
    .casa-normal { border-color: #1a3a60; background: #0a1a2e; color: #3a6080; }
    
    .sigla-txt { font-size: 16px; font-weight: bold; }
    .data-txt { font-size: 10px; opacity: 0.8; }
    .semana-txt { font-size: 9px; color: #555; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Cyber Security Roadmap - Juan Felipe")

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO", "📅 NOTAS", "🏅 CONQUISTAS"])

with tab1:
    col_t, col_s = st.columns([4, 1.2])
    
    with col_t:
        st.markdown('<div style="background:#061020; padding:15px; border-radius:15px; border:1px solid #1a3a6a">', unsafe_allow_html=True)
        # Tabuleiro em Zigue-zague (8 casas por linha)
        for i in range(10): # 10 linhas de 8 = 80 casas
            reverso = i % 2 != 0
            intervalo = range(i*8 + 1, (i+1)*8 + 1)
            row_html = '<div style="display:flex; justify-content:center; flex-wrap:wrap">'
            
            casas_da_linha = list(reversed(intervalo)) if reverso else list(intervalo)
            for n in casas_da_linha:
                sigla, cor, d_txt, _ = get_info_casa(n)
                
                # Classe de status
                if n == dados['casa']: c_cls = "casa casa-atual"
                elif n < dados['casa']: c_cls = "casa casa-feita"
                else: c_cls = "casa casa-normal"
                
                # Borda colorida se ainda não passou
                borda = f"border-color: {cor}" if n >= dados['casa'] else "border-color: #1a5a30"
                
                row_html += f'''
                <div class="{c_cls}" style="{borda}">
                    <div class="sigla-txt">{sigla}</div>
                    <div class="data-txt">{d_txt}</div>
                    <div class="semana-txt">S{n}</div>
                </div>
                '''
            row_html += '</div>'
            st.markdown(row_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s:
        sigla_at, _, _, nome_at = get_info_casa(dados['casa'])
        st.metric("XP TOTAL", f"{dados['xp']} pts")
        st.metric("SEMANA", f"{dados['casa']} / 80")
        
        st.info(f"**Foco Atual:**\n{nome_at}")
        
        if st.button("Avançar Semana ▶", use_container_width=True):
            if dados['casa'] < 80:
                dados['casa'] += 1
                dados['xp'] += 100
                salvar(dados); st.rerun()
        
        if st.button("Voltar Etapa ◀", use_container_width=True):
            if dados['casa'] > 1:
                dados['casa'] -= 1
                dados['xp'] = max(0, dados['xp'] - 100)
                salvar(dados); st.rerun()

with tab2:
    st.subheader("📝 Diário de Estudos")
    c1, c2 = st.columns([1, 2])
    with c1:
        dt = st.date_input("Data", date.today())
        txt = st.text_area("Notas:")
        if st.button("Salvar Log 💾"):
            dados.setdefault("eventos", {})[str(dt)] = txt
            salvar(dados); st.rerun()
    with c2:
        if "eventos" in dados:
            for k in sorted(dados["eventos"].keys(), reverse=True):
                with st.expander(f"📌 {k}"):
                    st.write(dados["eventos"][k])

with tab3:
    st.subheader("🏅 Checklist de Certificações")
    objetivos = list(dict.fromkeys([t[2] for t in TEMAS_MAP]))
    concluidas = dados.get("concluidas", [])
    
    for obj in objetivos:
        if st.checkbox(obj, value=(obj in concluidas)):
            if obj not in concluidas:
                concluidas.append(obj)
                dados["xp"] += 500
                salvar(dados); st.rerun()
        elif obj in concluidas:
            concluidas.remove(obj)
            dados["xp"] = max(0, dados["xp"] - 500)
            salvar(dados); st.rerun()
    dados["concluidas"] = concluidas
