import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# BANCO DE DADOS DE CERTIFICAÇÕES (EMBLEMAS)
# =========================
EMBLEMAS = {
    "AZ-900": {"icone": "☁️", "cor": "#00A4EF", "emblema": "🌩️", "emblema_grande": "☁️✨", "titulo": "Azure Fundamentals", "descricao": "Fundamentos do Cloud Computing", "nivel": "Foundation", "xp_necessario": 120, "ano": 2026},
    "AZ-104": {"icone": "☁️", "cor": "#0078D4", "emblema": "⚙️", "emblema_grande": "☁️🔧", "titulo": "Azure Administrator", "descricao": "Administração de Infra Cloud", "nivel": "Associate", "xp_necessario": 150, "ano": 2026},
    "AZ-500": {"icone": "☁️", "cor": "#005BA1", "emblema": "🔐", "emblema_grande": "☁️🛡️", "titulo": "Azure Security Engineer", "descricao": "Segurança em Ambiente Azure", "nivel": "Advanced", "xp_necessario": 150, "ano": 2026},
    "ISO 27001 Fundamentals": {"icone": "🔒", "cor": "#FFD700", "emblema": "📘", "emblema_grande": "🔒📖", "titulo": "ISO 27001 Foundation", "descricao": "Fundamentos da Norma", "nivel": "Foundation", "xp_necessario": 100, "ano": 2026},
    "Security+": {"icone": "🛡️", "cor": "#FF0000", "emblema": "⚔️", "emblema_grande": "🛡️⚔️", "titulo": "Security+", "descricao": "Cibersegurança", "nivel": "Professional", "xp_necessario": 120, "ano": 2027},
    "CISSP": {"icone": "👑", "cor": "#C0C0C0", "emblema": "🏆", "emblema_grande": "👑🏆", "titulo": "CISSP", "descricao": "Arquitetura de Segurança", "nivel": "Master", "xp_necessario": 200, "ano": 2029},
    "Python": {"icone": "🐍", "cor": "#3776AB", "emblema": "⚡", "emblema_grande": "🐍⚡", "titulo": "Python for Data", "descricao": "Automação e Dados", "nivel": "Advanced", "xp_necessario": 150, "ano": 2026},
    "Ingles": {"icone": "🇬🇧", "cor": "#1E90FF", "emblema": "💬", "emblema_grande": "🇬🇧💬", "titulo": "Fluency", "descricao": "Proficiência", "nivel": "Essential", "xp_necessario": 250, "ano": 2026}
}

# =========================
# ESTILO CSS (GALÁCTICO)
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        color: #4d9fff;
    }
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #4d9fff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .red-text { color: #ff4444 !important; font-weight: bold; }
    .cert-card {
        background: rgba(77, 159, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(77, 159, 255, 0.2);
        margin-bottom: 15px;
        transition: transform 0.3s;
    }
    .cert-card:hover { transform: scale(1.01); border-color: #4d9fff; }
    .atrasado { border-left: 5px solid #ff4444 !important; background: rgba(255, 68, 68, 0.05) !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZAÇÃO DO ESTADO
# =========================
if "db" not in st.session_state: st.session_state.db = []
if "xp" not in st.session_state: st.session_state.xp = 0
if "cert_xp" not in st.session_state: st.session_state.cert_xp = {c: 0 for c in EMBLEMAS.keys()}

# =========================
# LÓGICA DA SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"# 👨‍🚀 Comandante\n**Juan Felipe**")
    st.markdown(f"### ⭐ XP Total: {st.session_state.xp}")
    nivel = (st.session_state.xp // 100) + 1
    st.markdown(f"### 🎖️ Nível: {nivel}")
    st.progress(min((st.session_state.xp % 100) / 100, 1.0))
    st.markdown("---")
    st.markdown("### 🛠️ Atalhos de Missão")
    if st.button("Limpar Histórico"):
        st.session_state.db = []
        st.session_state.xp = 0
        st.session_state.cert_xp = {c: 0 for c in EMBLEMAS.keys()}
        st.rerun()

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Dashboard", "🗺️ Mapa da Jornada", "📅 Trilhas", "🏅 Conquistas"])

# TAB 1 - DASHBOARD
with tab1:
    st.markdown("## ⚡ Central de Comando")
    
    with st.expander("📝 REGISTRAR NOVA ATIVIDADE", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            area_sel = st.selectbox("🎯 Escolha a Certificação", list(EMBLEMAS.keys()))
        with c2:
            tipo_sel = st.selectbox("⚔️ Tipo de Missão", ["Estudo", "Laboratório", "Simulado", "Certificação"])
        
        if st.button("🚀 COMPUTAR XP"):
            ganho = {"Estudo": 10, "Laboratório": 20, "Simulado": 15, "Certificação": 100}.get(tipo_sel, 10)
            st.session_state.db.append({"data": datetime.now(), "area": area_sel, "xp": ganho})
            st.session_state.xp += ganho
            st.session_state.cert_xp[area_sel] += ganho
            st.success(f"+{ganho} XP em {area_sel}!")
            st.rerun()

    st.markdown("---")
    for cert, xp in st.session_state.cert_xp.items():
        emb = EMBLEMAS[cert]
        progresso = min(xp / emb["xp_necessario"], 1.0)
        is_atrasado = (datetime.now().year > emb["ano"] and progresso < 1.0)
        
        card_class = "cert-card atrasado" if is_atrasado else "cert-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between;">
                <span><b>{emb['emblema_grande']} {cert}</b> ({emb['nivel']})</span>
                <span>{int(progresso*100)}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progresso)
        if is_atrasado:
            st.markdown(f'<p class="red-text">⚠️ Meta de {emb["ano"]} não atingida!</p>', unsafe_allow_html=True)

# TAB 2 - MAPA DA JORNADA (CORREÇÃO DE INDENTAÇÃO AQUI)
with tab2:
    st.markdown("## 🗺️ Roadmap Galáctico")
    for ano in [2026, 2027, 2028, 2029]:
        st.subheader(f"📅 Ano {ano}")
        certs_ano = [c for c, d in EMBLEMAS.items() if d["ano"] == ano]
        
        if certs_ano:
            cols = st.columns(len(certs_ano))
            for i, c in enumerate(certs_ano):
                with cols[i]:
                    # Corrigido: Agora o código abaixo está dentro do bloco 'with'
                    status = "✅" if st.session_state.cert_xp[c] >= EMBLEMAS[c]["xp_necessario"] else "⏳"
                    st.markdown(f"""
                    <div style="text-align:center; padding:15px; border:1px solid #4d9fff; border-radius:10px;">
                        <span style="font-size:30px;">{EMBLEMAS[c]['emblema']}</span><br>
                        <b>{c}</b><br>
                        <span>{status}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Fase de consolidação e novos planos.")

# TAB 3 - TRILHAS
with tab3:
    st.markdown("### 📅 Cronograma Mensal")
    st.write("Em desenvolvimento: integração com calendários de estudo.")

# TAB 4 - CONQUISTAS
with tab4:
    st.markdown("## 🏅 Galeria de Troféus")
    concluidas = [c for c, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[c]["xp_necessario"]]
    
    if concluidas:
        cols = st.columns(3)
        for i, c in enumerate(concluidas):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(77,159,255,0.2); padding:20px; border-radius:15px;">
                    <h1 style="margin:0;">🏆</h1>
                    <h3>{c}</h3>
                    <p>Mestre Alcançado</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Nenhuma certificação completa ainda. Continue a missão!")

st.markdown("---")
st.caption("🚀 Sistema de Gestão de Carreira v2.0 - Juan Felipe da Silva")
