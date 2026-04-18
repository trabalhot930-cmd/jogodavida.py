import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# Configuração da página
st.set_page_config(
    page_title="Cyber Roadmap v10 - Juan Felipe",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DO CRONOGRAMA ATUALIZADO
# ─────────────────────────────────────────────
USER_LOGIN = "Juan"
USER_PASS = "Ju@n1990"
DATA_INICIO = date(2026, 4, 18) # Início conforme sua solicitação

# Mapeamento detalhado ajustado para 80 casas
TEMAS_MAP = [
    (1, 6, "AZ-900", "#0078d4", "Abr-Mai/26", "Microsoft Azure Fundamentals"),
    (7, 12, "ISO-F", "#e53935", "Jun-Jul/26", "ISO/IEC 27001 Fundamentals"),
    (13, 24, "CCNA", "#00b4ad", "Jun-Nov/26", "Cisco CCNA"),
    (25, 32, "AZ-104", "#005ba1", "Ago-Out/26", "Microsoft Azure Administrator Associate"),
    (33, 40, "SC-900", "#3267d3", "Dez/26-Jan/27", "Microsoft Security, Compliance, and Identity Fundamentals"),
    (41, 50, "S+", "#cc6600", "Fev-Abr/27", "CompTIA Security+"),
    (51, 60, "CySA+", "#d32f2f", "Jun-Ago/27", "CompTIA CySA+"),
    (61, 70, "ISO-LI", "#1565c0", "Out-Dez/27", "ISO/IEC 27001 Lead Implementer"),
    (71, 76, "62443", "#f57c00", "Jan-Mar/28", "ISA/IEC 62443 Cybersecurity Fundamentals"),
    (77, 80, "GICSP", "#2e7d32", "Mai-Jul/28", "Global Industrial Cyber Security Professional"),
]

def get_info_casa(n):
    for inicio, fim, sigla, cor, data_txt, nome in TEMAS_MAP:
        if inicio <= n <= fim:
            return sigla, cor, data_txt, nome
    return str(n), "#3a6080", "", ""

# Persistência de dados
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
        if st.button("Entrar", use_container_width=True):
            if u == USER_LOGIN and p == USER_PASS:
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("Acesso negado")
    st.stop()

# Estilo CSS unificado para evitar bugs de renderização
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background: #02060d !important; color: #c8dff0; font-family: 'Rajdhani'; }
    
    .tabuleiro-container { background:#061020; padding:20px; border-radius:20px; border:1px solid #1a3a6a; display: flex; flex-direction: column; align-items: center; }
    .linha-tabuleiro { display: flex; justify-content: center; flex-wrap: wrap; width: 100%; }
    
    .casa { 
        display: inline-flex; flex-direction: column; align-items: center; justify-content: center; 
        width: 105px; height: 105px; border-radius: 12px; margin: 6px; border: 2.5px solid; 
        text-align: center; background: #0a1a2e;
    }
    .casa-atual { border-color: #00f2ff !important; box-shadow: 0 0 20px #00f2ff; background: #112a45; font-weight: bold; }
    .casa-feita { border-color: #00ff41 !important; color: #00ff41; opacity: 0.6; }
    .casa-normal { border-color: #1a3a60; color: #4e6e8e; }
    
    .sigla-txt { font-size: 14px; font-weight: bold; margin-bottom: 2px; }
    .data-txt { font-size: 9px; opacity: 0.8; }
    .semana-txt { font-size: 10px; margin-top: 4px; color: #aaa; }
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
        # Iniciando o container principal do tabuleiro
        html_tabuleiro = '<div class="tabuleiro-container">'
        
        for i in range(10): # 10 linhas de 8 casas = 80 casas
            reverso = i % 2 != 0
            intervalo = range(i*8 + 1, (i+1)*8 + 1)
            html_tabuleiro += '<div class="linha-tabuleiro">'
            
            lista_casas = list(reversed(intervalo)) if reverso else list(intervalo)
            for n in lista_casas:
                sigla, cor, d_txt, _ = get_info_casa(n)
                
                # Definindo a classe baseada no progresso
                status_classe = "casa-atual" if n == dados['casa'] else ("casa-feita" if n < dados['casa'] else "casa-normal")
                borda_color = cor if n >= dados['casa'] else "#00ff41"
                
                # Montando o HTML de cada casa individualmente para garantir a renderização
                html_tabuleiro += f'''
                <div class="casa {status_classe}" style="border-color: {borda_color}">
                    <div class="sigla-txt">{sigla}</div>
                    <div class="data-txt">{d_txt}</div>
                    <div class="semana-txt">Semana {n}</div>
                </div>
                '''
            html_tabuleiro += '</div>' # Fecha linha
            
        html_tabuleiro += '</div>' # Fecha container
        
        # O PONTO CRÍTICO: st.markdown com unsafe_allow_html=True renderiza o HTML em vez de mostrar o código
        st.markdown(html_tabuleiro, unsafe_allow_html=True)

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

# Manutenção das abas de Diário e Conquistas
with tab2:
    st.subheader("📅 Diário de Bordo Técnico")
    c1, c2 = st.columns([1, 2])
    with c1:
        d_sel = st.date_input("Data do Registro", date.today())
        txt = st.text_area("O que foi evoluído hoje?", key="nota_area")
        if st.button("Salvar Log 💾", use_container_width=True):
            dados.setdefault("eventos", {})[str(d_sel)] = txt
            salvar(dados); st.rerun()
    with c2:
        if "eventos" in dados and dados["eventos"]:
            for k in sorted(dados["eventos"].keys(), reverse=True):
                with st.expander(f"📝 Registro {k}"):
                    st.write(dados["eventos"][k])

with tab3:
    st.subheader("🏅 Mural de Conquistas")
    objetivos_unicos = list(dict.fromkeys([t[2] for t in TEMAS_MAP]))
    concluidas = dados.get("concluidas", [])
    
    for obj in objetivos_unicos:
        if st.checkbox(obj, value=(obj in concluidas), key=f"chk_{obj}"):
            if obj not in concluidas:
                concluidas.append(obj)
                dados["xp"] += 500
                salvar(dados); st.rerun()
        elif obj in concluidas:
            concluidas.remove(obj)
            dados["xp"] = max(0, dados["xp"] - 500)
            salvar(dados); st.rerun()
    dados["concluidas"] = concluidas
