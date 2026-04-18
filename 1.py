import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# EMOJIS E ÍCONES ÉPICOS - COM EMBLEMAS ÚNICOS
# =========================
EMBLEMAS = {
    # AZURE COMPLETO
    "AZ-900": {
        "icone": "☁️",
        "cor": "#00A4EF",
        "emblema": "🌩️",
        "emblema_grande": "☁️✨",
        "titulo": "Azure Fundamentals",
        "descricao": "Fundamentos do Cloud Computing",
        "nivel": "Foundation",
        "xp_necessario": 120,
        "ano": 2026,
        "trimestre": "Q1"
    },
    "AZ-104": {
        "icone": "☁️",
        "cor": "#0078D4",
        "emblema": "⚙️",
        "emblema_grande": "☁️🔧",
        "titulo": "Azure Administrator",
        "descricao": "Administração de Infraestrutura Cloud",
        "nivel": "Associate",
        "xp_necessario": 150,
        "ano": 2026,
        "trimestre": "Q2"
    },
    "AZ-500": {
        "icone": "☁️",
        "cor": "#005BA1",
        "emblema": "🔐",
        "emblema_grande": "☁️🛡️",
        "titulo": "Azure Security Engineer",
        "descricao": "Segurança em Ambiente Azure",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2026,
        "trimestre": "Q3"
    },
    
    # ISO 27001 COMPLETO
    "ISO 27001 Fundamentals": {
        "icone": "🔒",
        "cor": "#FFD700",
        "emblema": "📘",
        "emblema_grande": "🔒📖",
        "titulo": "ISO 27001 Foundation",
        "descricao": "Fundamentos da Norma",
        "nivel": "Foundation",
        "xp_necessario": 100,
        "ano": 2026,
        "trimestre": "Q2"
    },
    "ISO 27001 Auditor": {
        "icone": "🔒",
        "cor": "#FFC000",
        "emblema": "🔍",
        "emblema_grande": "🔒🔍",
        "titulo": "ISO 27001 Lead Auditor",
        "descricao": "Auditoria de SGSI",
        "nivel": "Professional",
        "xp_necessario": 150,
        "ano": 2027,
        "trimestre": "Q1"
    },
    "ISO 27001 Implementer": {
        "icone": "🔒",
        "cor": "#FFA000",
        "emblema": "🛠️",
        "emblema_grande": "🔒⚙️",
        "titulo": "ISO 27001 Implementer",
        "descricao": "Implementação de SGSI",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2027,
        "trimestre": "Q2"
    },
    
    # SEGURANÇA COMPLETA
    "Security+": {
        "icone": "🛡️",
        "cor": "#FF0000",
        "emblema": "⚔️",
        "emblema_grande": "🛡️⚔️",
        "titulo": "Security+",
        "descricao": "Fundamentos de Cibersegurança",
        "nivel": "Professional",
        "xp_necessario": 120,
        "ano": 2027,
        "trimestre": "Q3"
    },
    "CySA+": {
        "icone": "🔍",
        "cor": "#FF4500",
        "emblema": "🕵️",
        "emblema_grande": "🔍🕵️",
        "titulo": "CySA+",
        "descricao": "Análise de Vulnerabilidades",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2027,
        "trimestre": "Q4"
    },
    "CISSP": {
        "icone": "👑",
        "cor": "#C0C0C0",
        "emblema": "🏆",
        "emblema_grande": "👑🏆",
        "titulo": "CISSP",
        "descricao": "Arquitetura de Segurança",
        "nivel": "Master",
        "xp_necessario": 200,
        "ano": 2029,
        "trimestre": "Q2"
    },
    
    # OT/INDUSTRIAL COMPLETO
    "IEC 62443": {
        "icone": "🏭",
        "cor": "#808080",
        "emblema": "📏",
        "emblema_grande": "🏭📏",
        "titulo": "IEC 62443 Foundation",
        "descricao": "Segurança em ICS/SCADA",
        "nivel": "Foundation",
        "xp_necessario": 120,
        "ano": 2027,
        "trimestre": "Q2"
    },
    "MITRE ATT&CK ICS": {
        "icone": "🏭",
        "cor": "#A0A0A0",
        "emblema": "🎯",
        "emblema_grande": "🎯🏭",
        "titulo": "MITRE ATT&CK for ICS",
        "descricao": "Táticas e Técnicas para ICS",
        "nivel": "Intermediate",
        "xp_necessario": 120,
        "ano": 2028,
        "trimestre": "Q1"
    },
    "GICSP": {
        "icone": "🏭",
        "cor": "#606060",
        "emblema": "⚙️",
        "emblema_grande": "🏭⚙️",
        "titulo": "GICSP",
        "descricao": "Segurança Industrial Global",
        "nivel": "Expert",
        "xp_necessario": 180,
        "ano": 2028,
        "trimestre": "Q3"
    },
    
    # DADOS
    "Python": {
        "icone": "🐍",
        "cor": "#3776AB",
        "emblema": "⚡",
        "emblema_grande": "🐍⚡",
        "titulo": "Python for Data",
        "descricao": "Automação e Análise de Dados",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2026,
        "trimestre": "Q3"
    },
    "SQL": {
        "icone": "🗄️",
        "cor": "#F29111",
        "emblema": "📊",
        "emblema_grande": "🗄️📊",
        "titulo": "Advanced SQL",
        "descricao": "Consultas e Modelagem de Dados",
        "nivel": "Intermediate",
        "xp_necessario": 120,
        "ano": 2026,
        "trimestre": "Q4"
    },
    "Power BI": {
        "icone": "📈",
        "cor": "#F2C811",
        "emblema": "🎨",
        "emblema_grande": "📈🎨",
        "titulo": "Power BI Expert",
        "descricao": "Dashboards e Analytics",
        "nivel": "Intermediate",
        "xp_necessario": 120,
        "ano": 2026,
        "trimestre": "Q4"
    },
    
    # REDES
    "CCNA": {
        "icone": "🌐",
        "cor": "#1BA0D7",
        "emblema": "🕸️",
        "emblema_grande": "🌐🕸️",
        "titulo": "CCNA",
        "descricao": "Redes e Infraestrutura",
        "nivel": "Associate",
        "xp_necessario": 150,
        "ano": 2026,
        "trimestre": "Q2"
    },
    "SC-900": {
        "icone": "🔐",
        "cor": "#0078D4",
        "emblema": "🎯",
        "emblema_grande": "🔐🎯",
        "titulo": "SC-900",
        "descricao": "Segurança e Compliance",
        "nivel": "Foundation",
        "xp_necessario": 100,
        "ano": 2026,
        "trimestre": "Q1"
    },
    
    # FORMAÇÃO ACADÊMICA
    "Pos-graduacao": {
        "icone": "🎓",
        "cor": "#800080",
        "emblema": "📜",
        "emblema_grande": "🎓📜",
        "titulo": "Pós-graduação",
        "descricao": "Cibersegurança e Governança de Dados",
        "nivel": "Advanced",
        "xp_necessario": 300,
        "ano": 2026,
        "trimestre": "Q2-Q4"
    },
    
    # IDIOMAS
    "Ingles": {
        "icone": "🇬🇧",
        "cor": "#1E90FF",
        "emblema": "💬",
        "emblema_grande": "🇬🇧💬",
        "titulo": "English Fluency",
        "descricao": "Proficiência Internacional",
        "nivel": "Essential",
        "xp_necessario": 250,
        "ano": "Contínuo",
        "trimestre": "2026-2029"
    },
    
    # CERTIFICAÇÕES COMPLEMENTARES
    "Cloud Security": {
        "icone": "☁️",
        "cor": "#00A4EF",
        "emblema": "🔒",
        "emblema_grande": "☁️🔒",
        "titulo": "Cloud Security",
        "descricao": "Segurança Multi-Cloud",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2028,
        "trimestre": "Q4"
    },
    "DevSecOps": {
        "icone": "🔄",
        "cor": "#6C3483",
        "emblema": "🚀",
        "emblema_grande": "🔄🚀",
        "titulo": "DevSecOps",
        "descricao": "Segurança no Ciclo DevOps",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2029,
        "trimestre": "Q1"
    }
}

# =========================
# STYLE PICA DAS GALÁXIAS - AZUL ÍNDICO + VERMELHO
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

/* Fundo galáctico */
html, body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
    color: #4d9fff;
}

.block-container {
    padding-top: 2rem;
    background: radial-gradient(circle at 20% 50%, rgba(77,159,255,0.08) 0%, rgba(0,0,0,0) 70%);
}

/* Títulos em azul índico brilhante */
h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, #4d9fff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold !important;
    text-shadow: 0 0 10px rgba(77,159,255,0.3);
}

/* Texto padrão em azul índico */
.stMarkdown, p, div, span, label, .stText, .stNumber {
    color: #4d9fff !important;
}

/* Texto em vermelho para alertas */
.red-text {
    color: #ff4444 !important;
    font-weight: bold;
    text-shadow: 0 0 5px rgba(255,68,68,0.5);
}

.red-badge {
    background: linear-gradient(135deg, #ff4444, #cc0000);
    padding: 5px 10px;
    border-radius: 20px;
    color: white;
    font-weight: bold;
    display: inline-block;
}

.warning-text {
    color: #ff8800 !important;
    font-weight: bold;
}

/* Botões galácticos */
.stButton button {
    background: linear-gradient(135deg, #4d9fff, #7b2ff7) !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(77,159,255,0.4);
}

/* Cards de certificação - estilo galáctico */
.cert-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(77,159,255,0.3);
    transition: all 0.3s;
}

.cert-card:hover {
    transform: translateX(10px);
    box-shadow: 0 5px 25px rgba(77,159,255,0.3);
    border: 1px solid rgba(77,159,255,0.6);
}

.cert-card.atrasado {
    border-left: 4px solid #ff4444;
    background: linear-gradient(135deg, rgba(255,68,68,0.1), rgba(123,47,247,0.05));
}

/* Badges de nível */
.level-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-left: 10px;
}

/* Trilha card */
.trilha-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-left: 4px solid #4d9fff;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    backdrop-filter: blur(5px);
}

/* Sidebar galáctica */
.css-1d391kg, .css-12oz5g7 {
    background: linear-gradient(135deg, #0a0e27, #0d1133) !important;
    border-right: 1px solid rgba(77,159,255,0.2);
}

.css-1d391kg p, .css-12oz5g7 p, .css-1d391kg div, .css-12oz5g7 div {
    color: #4d9fff !important;
}

/* Progress bar galáctica */
.stProgress > div > div {
    background: linear-gradient(90deg, #4d9fff, #7b2ff7) !important;
}

/* Animações */
@keyframes glow {
    0%, 100% { text-shadow: 0 0 5px rgba(77,159,255,0.5); }
    50% { text-shadow: 0 0 20px rgba(77,159,255,0.8); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.glow-text {
    animation: glow 2s infinite;
}

/* Métricas */
.metric-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(77,159,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "db" not in st.session_state:
    st.session_state.db = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "cert_xp" not in st.session_state:
    st.session_state.cert_xp = {cert: 0 for cert in EMBLEMAS.keys()}

if "cert_status" not in st.session_state:
    st.session_state.cert_status = {cert: "Não iniciada" for cert in EMBLEMAS.keys()}

# =========================
# FUNÇÕES AUXILIARES
# =========================
def calc_xp(activity):
    xp_table = {
        "Estudo": 10,
        "Laboratório": 20,
        "Projeto": 30,
        "Revisão": 15,
        "Simulado": 15,
        "Aula Pós-graduação": 25,
        "Inglês": 15,
        "Certificação": 50
    }
    return xp_table.get(activity, 10)

def status_por_xp(xp, cert):
    xp_necessario = EMBLEMAS[cert]["xp_necessario"]
    if xp >= xp_necessario:
        return "Concluída"
    elif xp >= xp_necessario * 0.3:
        return "Em andamento"
    else:
        return "Não iniciada"

def get_badge_icon(status):
    return {
        "Concluída": "🏆",
        "Em andamento": "⚡",
        "Não iniciada": "💤"
    }.get(status, "❓")

def get_nivel_icon(nivel):
    icons = {
        "Foundation": "🌱",
        "Essential": "📘",
        "Associate": "🥈",
        "Intermediate": "📊",
        "Professional": "💼",
        "Advanced": "🚀",
        "Expert": "🎯",
        "Master": "👑"
    }
    return icons.get(nivel, "⭐")

def delete_activity(index):
    activity = st.session_state.db[index]
    xp_to_remove = activity["xp"]
    
    st.session_state.xp -= xp_to_remove
    area = activity["area"]
    st.session_state.cert_xp[area] -= xp_to_remove
    st.session_state.db.pop(index)
    
    new_status = status_por_xp(st.session_state.cert_xp[area], area)
    st.session_state.cert_status[area] = new_status

def verificar_atraso(cert, ano_planejado):
    if ano_planejado == "Contínuo":
        return False
    ano_atual = datetime.now().year
    if isinstance(ano_planejado, int) and ano_atual > ano_planejado:
        xp_atual = st.session_state.cert_xp.get(cert, 0)
        xp_necessario = EMBLEMAS[cert]["xp_necessario"]
        if xp_atual < xp_necessario:
            return True
    return False

# =========================
# SIDEBAR GALÁCTICA
# =========================
with st.sidebar:
    st.markdown("## 🚀 **Nave Estelar**")
    st.markdown(f"""
    ### 👨‍🚀 **Comandante:** Juan Felipe
    ### ⭐ **XP Total:** {st.session_state.xp}
    ### 🎖️ **Nível:** {st.session_state.xp // 100 + 1}
    ### 📅 **Missões:** {len(st.session_state.db)}
    """)
    
    xp_no_nivel = st.session_state.xp % 100
    st.progress(xp_no_nivel / 100 if xp_no_nivel > 0 else 0)
    st.caption(f"Próximo nível: {100 - xp_no_nivel} XP")
    
    st.markdown("---")
    
    # Alertas em vermelho
    certificacoes_atrasadas = []
    for cert, data in EMBLEMAS.items():
        if verificar_atraso(cert, data.get("ano", 2030)):
            certificacoes_atrasadas.append(cert)
    
    if certificacoes_atrasadas:
        st.markdown('<p class="red-text">⚠️ **ATENÇÃO - CERTIFICAÇÕES ATRASADAS:**</p>', unsafe_allow_html=True)
        for cert in certificacoes_atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[cert]["emblema"]} {cert}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 **Top 5 Especializações**")
    
    ranking = sorted(st.session_state.cert_xp.items(), key=lambda x: x[1], reverse=True)
    for cert, xp in ranking[:5]:
        if cert in EMBLEMAS:
            emblema = EMBLEMAS[cert]["emblema"]
            xp_necessario = EMBLEMAS[cert]["xp_necessario"]
            percent = (xp / xp_necessario) * 100
            st.markdown(f"{emblema} **{cert[:15]}**: {percent:.0f}%")
            st.progress(min(xp / xp_necessario, 1.0))
    
    st.markdown("---")
    st.markdown("### 📊 **Resumo por Trilha**")
    
    trilhas = {
        "Azure": ["AZ-900", "AZ-104", "AZ-500"],
        "ISO 27001": ["ISO 27001 Fundamentals", "ISO 27001 Auditor", "ISO 27001 Implementer"],
        "Segurança": ["Security+", "CySA+", "CISSP"],
        "OT Industrial": ["IEC 62443", "MITRE ATT&CK ICS", "GICSP"],
        "Dados": ["Python", "SQL", "Power BI"]
    }
    
    for trilha, certs in trilhas.items():
        xp_total = sum(st.session_state.cert_xp.get(cert, 0) for cert in certs if cert in EMBLEMAS)
        xp_max = sum(EMBLEMAS[cert]["xp_necessario"] for cert in certs if cert in EMBLEMAS)
        percent = (xp_total / xp_max) * 100 if xp_max > 0 else 0
        
        if percent < 30:
            st.markdown(f'<span class="red-text">⚠️ {trilha}: {percent:.0f}%</span>', unsafe_allow_html=True)
        else:
            st.markdown(f"**{trilha}**: {percent:.0f}%")
        st.progress(percent / 100)

# =========================
# HEADER PRINCIPAL
# =========================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🚀 **MISSÃO CARREIRA**")
    st.markdown("### *Juan Felipe da Silva - Especialista em Cibersegurança e Cloud*")
    st.markdown('<p class="red-text glow-text">🎯 Meta: Completar todas as certificações até 2029!</p>', unsafe_allow_html=True)
    st.markdown("---")

# =========================
# ABAS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 **Dashboard Épico**", "🗺️ **Mapa da Jornada**", "📅 **Trilhas de Poder**", "🏅 **Conquistas Galácticas**"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    
    with st.expander("✨ **NOVA MISSÃO**", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.selectbox("🎯 **Área de Especialização**", list(EMBLEMAS.keys()))
            activity = st.selectbox("⚔️ **Tipo de Missão**", 
                                   ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", 
                                    "Aula Pós-graduação", "Inglês", "Certificação"])
        
        with col2:
            data = st.date_input("📆 **Data Estelar**", value=pd.Timestamp.today())
            obs = st.text_area("📝 **Observações de Bordo**")
        
        if st.button("🚀 **LANÇAR MISSÃO**", use_container_width=True):
            xp_gain = calc_xp(activity)
            st.session_state.db.append({
                "data": pd.to_datetime(data),
                "area": area,
                "atividade": activity,
                "xp": xp_gain,
                "obs": obs
            })
            st.session_state.xp += xp_gain
            st.session_state.cert_xp[area] += xp_gain
            new_status = status_por_xp(st.session_state.cert_xp[area], area)
            st.session_state.cert_status[area] = new_status
            st.success(f"✅ Missão completa! +{xp_gain} XP conquistado!", icon="🎉")
            st.balloons()
            st.rerun()
    
    col1, col2, col3, col4 = st.columns(4)
    
    if st.session_state.db:
        certificacoes_concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() 
                                      if cert in EMBLEMAS and xp >= EMBLEMAS[cert]["xp_necessario"])
        
        col1.metric("🎮 **Missões**", len(st.session_state.db))
        col2.metric("⭐ **XP Global**", st.session_state.xp)
        col3.metric("🏆 **Nível**", st.session_state.xp // 100 + 1)
        col4.metric("✅ **Certificações**", f"{certificacoes_concluidas}/{len(EMBLEMAS)}")
    else:
        col1.metric("🎮 **Missões**", 0)
        col2.metric("⭐ **XP Global**", 0)
        col3.metric("🏆 **Nível**", 1)
        col4.metric("✅ **Certificações**", f"0/{len(EMBLEMAS)}")
    
    st.markdown("---")
    st.markdown("## 🎖️ **JORNADA DAS CERTIFICAÇÕES**")
    
    for cert, xp in st.session_state.cert_xp.items():
        if cert not in EMBLEMAS:
            continue
            
        emblema_data = EMBLEMAS[cert]
        xp_necessario = emblema_data["xp_necessario"]
        status = st.session_state.cert_status[cert]
        badge_icon = get_badge_icon(status)
        nivel_icon = get_nivel_icon(emblema_data["nivel"])
        
        esta_atrasado = verificar_atraso(cert, emblema_data.get("ano", 2030))
        classe_atraso = "cert-card atrasado" if esta_atrasado else "cert-card"
        
        st.markdown(f"""
        <div class="{classe_atraso}">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="margin: 0;">
                        <span style="font-size: 32px;">{emblema_data['emblema_grande']}</span> {cert} 
                        <span style="font-size: 14px; color: {emblema_data['cor']};">{emblema_data['titulo']}</span>
                        <span class="level-badge" style="background: {emblema_data['cor']}20; color: {emblema_data['cor']};">
                            {nivel_icon} {emblema_data['nivel']}
                        </span>
                    </h3>
                    <p style="margin: 5px 0 0 0; opacity: 0.8;">{emblema_data['descricao']}</p>
                </div>
                <div style="font-size: 48px;">
                    {badge_icon}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            progress = min(xp / xp_necessario, 1.0)
            st.progress(progress)
            if esta_atrasado:
                st.markdown(f'<p class="red-text">📊 Progresso: {xp}/{xp_necessario} XP ({int(progress*100)}%) - ATRASADO!</p>', unsafe_allow_html=True)
            else:
                st.caption(f"📊 Progresso: {xp}/{xp_necessario} XP ({int(progress*100)}%)")
        
        with col2:
            st.markdown(f"**Status:** {badge_icon} {status}")
        
        with col3:
            status_options = ["Não iniciada", "Em andamento", "Concluída"]
            current_index = status_options.index(status) if status in status_options else 0
            new_status_manual = st.selectbox(
                "⚙️",
                status_options,
                index=current_index,
                key=f"status_{cert}",
                label_visibility="collapsed"
            )
            if new_status_manual != status:
                st.session_state.cert_status[cert] = new_status_manual
                st.rerun()
        
        st.markdown("---")
    
    # Histórico
    st.markdown("## 📜 **REGISTRO DE MISSÕES**")
    
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        df_f = df.sort_values("data", ascending=False).reset_index(drop=True)
        
        for idx, row in df_f.iterrows():
            if row['area'] not in EMBLEMAS:
                continue
                
            emblema_icon = EMBLEMAS[row['area']]['emblema']
            
            cols = st.columns([1, 1.5, 1, 0.8, 2, 0.5])
            with cols[0]:
                st.write(f"{emblema_icon} **{row['area'][:20]}**")
            with cols[1]:
                st.write(f"📅 {row['data'].strftime('%d/%m/%Y')}")
            with cols[2]:
                st.write(f"⚔️ {row['atividade']}")
            with cols[3]:
                st.write(f"⭐ +{row['xp']}")
            with cols[4]:
                st.write(f"📝 {row['obs'] if pd.notna(row['obs']) else '-'}")
            with cols[5]:
                for i, record in enumerate(st.session_state.db):
                    if (record['data'] == row['data'] and 
                        record['area'] == row['area'] and 
                        record['atividade'] == row['atividade'] and
                        record['xp'] == row['xp']):
                        if st.button("🗑️", key=f"del_{i}_{idx}"):
                            delete_activity(i)
                            st.rerun()
                        break
            st.markdown("---")
        
        # Gráfico
        evolucao = df.groupby('data').agg({'xp': 'sum'}).reset_index()
        evolucao = evolucao.sort_values('data')
        evolucao['xp_acumulado'] = evolucao['xp'].cumsum()
        
        chart = alt.Chart(evolucao).mark_line(point=True, color='#4d9fff', strokeWidth=3).encode(
            x=alt.X("data:T", title="Data", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("xp_acumulado:Q", title="XP Acumulado"),
            tooltip=["data", "xp_acumulado"]
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
        
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 **BAIXAR RELATÓRIO ESTELAR**", csv, "jornada_galactica.csv", "text/csv")

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:
    st.markdown("## 🗺️ **ROADMAP ESTRATÉGICO 2026-2029**")
    
    anos = {
        2026: "🌱 **ANO 1 - FUNDAÇÃO**",
        2027: "⚡ **ANO 2 - ESPECIALIZAÇÃO**",
        2028: "🎯 **ANO 3 - MAESTRIA TÉCNICA**",
        2029: "👑 **ANO 4 - LIDERANÇA**"
    }
    
    for ano, titulo in anos.items():
        with st.expander(titulo, expanded=(ano == 2026)):
            certs_ano = [cert for cert, data in EMBLEMAS.items() if data.get("ano") == ano]
            
            if certs_ano:
                cols = st.columns(min(len(certs_ano), 4))
                for i, cert in enumerate(certs_ano):
                    emblema = EMBLEMAS[cert]
                    status = st.session_state.cert_status.get(cert, "Não iniciada")
                    badge = get_badge_icon(status)
                    xp_atual = st.session_state.cert_xp.get(cert, 0)
                    xp_necessario = emblema["xp_necessario"]
                    percent = (xp_atual / xp_necessario) * 100
                    
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 10px; margin: 5px; border: 1px solid rgba(77,159,255,0.2);">
                            <div style="font-size: 48px;">{emblema['emblema_grande']}</div>
                            <div style="font-size: 16px; font-weight: bold; color: #4d9fff;">{cert}</div>
                            <div style="font-size: 11px; opacity: 0.7;">{emblema['titulo']}</div>
                            <div style="font-size: 24px;">{badge}</div>
                            <div style="font-size: 11px;">{xp_atual}/{xp_necessario} XP</div>
                            <div style="background: rgba(77,159,255,0.2); border-radius: 5px; height: 5px; margin-top: 5
