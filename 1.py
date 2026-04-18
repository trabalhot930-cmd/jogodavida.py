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
# CONFIGURAÇÃO DO CRONOGRAMA ATUALIZADO
# ─────────────────────────────────────────────
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
DATA_INICIO = date(2026, 4, 18) # Início hoje

# Mapeamento detalhado (Ajustado para 80 semanas)
TEMAS_MAP = [
    (1, 6, "AZ-900", "#0078d4", "Abr-Mai/26", "Azure Fundamentals"),
    (7, 12, "ISO-F", "#e53935", "Jun-Jul/26", "ISO 27001 Fund."),
    (13, 24, "CCNA", "#00b4ad", "Jun-Nov/26", "Cisco Networking"),
    (25, 32, "AZ-104", "#005ba1", "Ago-Out/26", "Azure Admin Associate"),
    (33, 40, "SC-900", "#3267d3", "Dez/26-Jan/27", "Security & Compliance"),
    (41, 50, "S+", "#cc6600", "Fev-Abr/27", "CompTIA Security+"),
    (51, 60, "CySA+", "#d32f2f", "Jun-Ago/27", "CompTIA CySA+"),
    (61, 70, "ISO-LI", "#1565c0", "Out-Dez/27", "ISO 27001 Lead Imp."),
    (71, 76, "62443", "#f57c00", "Jan-Mar/28", "ISA/IEC 62443"),
    (77, 80, "GICSP", "#2e7d32", "Mai-Jul/28", "Global Industrial Cyber"),
]

def get_info_casa(n):
    for inicio, fim, sigla, cor, data_txt, nome in TEMAS_MAP:
        if inicio <= n <= fim:
            return sigla, cor, data_txt, nome
    return str(n), "#3a6080", "", ""

ARQUIVO = "progresso_juan_v10.json"

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
# LOGIN E ESTILOS
# ─────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center; color:#7eb8ff;'>SISTEMA DE ACESSO</h1>", unsafe_allow_html=True)
    _, col_c, _ = st.columns([1,1,1])
    with col_c:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if u == USER_LOGIN and p == USER_PASS:
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("Acesso negado")
    st.stop()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #02060d !important; color: #c8dff0; font-family: 'Rajdhani'; }
    
    .casa { 
        display: inline-flex; flex-direction: column; align-items: center; justify-content: center; 
        width: 105px; height: 105px; border-radius: 12px; margin: 6px; border: 2.5px solid; 
        text-align: center; background: #0a1a2e; transition: 0.3s;
    }
    .casa-atual { border-color: #00f2ff !important; box-shadow: 0 0 20px #00f2ff; background: #112a45; font-weight: bold; }
    .casa-feita { border-color: #00ff41 !important; color: #00ff41; opacity: 0.6; }
    .casa-normal { border-color: #1a3a60; color: #4e6e8e; }
    
    .sigla-txt { font-size: 14px; font-weight: bold; margin-bottom: 2px; }
    .data-txt { font-size: 9px; opacity: 0.8; font-weight: 400; }
    .semana-txt { font-size: 10px; margin-top: 4px; color: #aaa; }
    
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INTERFACE PRINCIPAL
# ─────────────────────────────────────────────
st.title("🛡️ Cyber Security Roadmap v10 - Juan Felipe")

tab1, tab2, tab3 = st.tabs(["🗺️ TABULEIRO", "📅 LOGS DE ESTUDO", "🏅 CERTIFICAÇÕES"])

with tab1:
    col_t, col_s = st.columns([4, 1.2])
    
    with col_t:
        st.markdown('<div style="background:#061020; padding:20px; border-radius:20px; border:1px solid #1a3a6a">', unsafe_allow_html=True)
        # Tabuleiro em fileiras de 8 para melhor visualização com casas maiores
        for i in range(10): 
            reverso = i % 2 != 0
            intervalo = range(i*8 + 1, (i+1)*8 + 1)
            row_html = ""
            for n in (reversed(intervalo) if reverso else intervalo):
                sigla, cor, d_txt, nome_f = get_info_casa(n)
                
                c_cls = "casa casa-atual" if n == dados['casa'] else ("casa casa-feita" if n < dados['casa'] else "casa casa-normal")
                borda_color = cor if n >= dados['casa'] else "#00ff41"
                
                row_html += f"""
                <div class="{c_cls}" style="border-color: {borda_color}">
                    <div class="sigla-txt">{sigla}</div>
                    <div class="data-txt">{d_txt}</div>
                    <div class="semana-txt">Semana {n}</div>
                </div>
                """
            st.markdown(f'<div style="display:flex; justify-content:center; flex-wrap:wrap">{row_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s:
        sigla_at, _, _, nome_at = get_info_casa(dados['casa'])
        dt_inicio = DATA_INICIO + timedelta(weeks=dados['casa']-1)
        
        st.metric("PONTOS XP", f"{dados['xp']} pts")
        st.metric("PROGRESSO", f"{dados['casa']} / 80")
        
        st.markdown(f"""
        <div style="background:#112a45; padding:15px; border-radius:10px; border-left: 5px solid #00f2ff">
            <p style="margin:0; font-size:12px; color:#00f2ff">FOCO DA SEMANA:</p>
            <h3 style="margin:0">{sigla_at}</h3>
            <p style="margin:0; font-size:13px; opacity:0.8">{nome_at}</p>
            <p style="margin-top:10px; font-size:11px">📅 Início: {dt_inicio.strftime('%d/%m/%Y')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("CONCLUIR SEMANA ⚔️", use_container_width=True):
            if dados['casa'] < 80:
                dados['casa'] += 1
                dados['xp'] += 100
                salvar(dados); st.rerun()
        
        if st.button("VOLTAR ETAPA ◀", use_container_width=True):
            if dados['casa'] > 1:
                dados['casa'] -= 1
                dados['xp'] = max(0, dados['xp'] - 100)
                salvar(dados); st.rerun()

with tab2:
    st.subheader("📅 Diário de Bordo Técnico")
    c1, c2 = st.columns([1, 2])
    with c1:
        d_sel = st.date_input("Data do Registro", date.today())
        txt = st.text_area("O que foi evoluído hoje?", placeholder="Ex: Lab de sub-redes CCNA concluído.")
        if st.button("Salvar Log 💾", use_container_width=True):
            dados.setdefault("eventos", {})[str(d_sel)] = txt
            salvar(dados); st.success("Log salvo!")
    with c2:
        if "eventos" in dados and dados["eventos"]:
            for k in sorted(dados["eventos"].keys(), reverse=True):
                with st.expander(f"📝 Registro {k}"):
                    st.write(dados["eventos"][k])

with tab3:
    st.subheader("🏅 Mural de Conquistas (Bônus 500 XP)")
    # Lista única de objetivos principais
    objetivos_unicos = list(dict.fromkeys([t[2] for t in TEMAS_MAP]))
    concluidas = dados.get("concluidas", [])
    
    for obj in objetivos_unicos:
        check = obj in concluidas
        if st.checkbox(obj, value=check):
            if obj not in concluidas:
                concluidas.append(obj)
                dados["xp"] += 500
                salvar(dados); st.rerun()
        elif check:
            concluidas.remove(obj)
            dados["xp"] = max(0, dados["xp"] - 500)
            salvar(dados); st.rerun()
    dados["concluidas"] = concluidas
