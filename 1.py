import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# EMOJIS E ÍCONES ÉPICOS
# =========================
EMBLEMAS = {
    "AZ-900": {"icone": "☁️", "cor": "#00A4EF", "emblema": "🌩️", "emblema_grande": "☁️✨", "titulo": "Azure Fundamentals", "descricao": "Fundamentos do Cloud Computing", "nivel": "Foundation", "xp_necessario": 120, "ano": 2026, "trimestre": "Q1"},
    "AZ-104": {"icone": "☁️", "cor": "#0078D4", "emblema": "⚙️", "emblema_grande": "☁️🔧", "titulo": "Azure Administrator", "descricao": "Administração de Infraestrutura Cloud", "nivel": "Associate", "xp_necessario": 150, "ano": 2026, "trimestre": "Q2"},
    "AZ-500": {"icone": "☁️", "cor": "#005BA1", "emblema": "🔐", "emblema_grande": "☁️🛡️", "titulo": "Azure Security Engineer", "descricao": "Segurança em Ambiente Azure", "nivel": "Advanced", "xp_necessario": 150, "ano": 2026, "trimestre": "Q3"},
    "ISO 27001 Fundamentals": {"icone": "🔒", "cor": "#FFD700", "emblema": "📘", "emblema_grande": "🔒📖", "titulo": "ISO 27001 Foundation", "descricao": "Fundamentos da Norma", "nivel": "Foundation", "xp_necessario": 100, "ano": 2026, "trimestre": "Q2"},
    "ISO 27001 Auditor": {"icone": "🔒", "cor": "#FFC000", "emblema": "🔍", "emblema_grande": "🔒🔍", "titulo": "ISO 27001 Lead Auditor", "descricao": "Auditoria de SGSI", "nivel": "Professional", "xp_necessario": 150, "ano": 2027, "trimestre": "Q1"},
    "ISO 27001 Implementer": {"icone": "🔒", "cor": "#FFA000", "emblema": "🛠️", "emblema_grande": "🔒⚙️", "titulo": "ISO 27001 Implementer", "descricao": "Implementação de SGSI", "nivel": "Advanced", "xp_necessario": 150, "ano": 2027, "trimestre": "Q2"},
    "Security+": {"icone": "🛡️", "cor": "#FF0000", "emblema": "⚔️", "emblema_grande": "🛡️⚔️", "titulo": "Security+", "descricao": "Fundamentos de Cibersegurança", "nivel": "Professional", "xp_necessario": 120, "ano": 2027, "trimestre": "Q3"},
    "CySA+": {"icone": "🔍", "cor": "#FF4500", "emblema": "🕵️", "emblema_grande": "🔍🕵️", "titulo": "CySA+", "descricao": "Análise de Vulnerabilidades", "nivel": "Advanced", "xp_necessario": 150, "ano": 2027, "trimestre": "Q4"},
    "CISSP": {"icone": "👑", "cor": "#C0C0C0", "emblema": "🏆", "emblema_grande": "👑🏆", "titulo": "CISSP", "descricao": "Arquitetura de Segurança", "nivel": "Master", "xp_necessario": 200, "ano": 2029, "trimestre": "Q2"},
    "IEC 62443": {"icone": "🏭", "cor": "#808080", "emblema": "📏", "emblema_grande": "🏭📏", "titulo": "IEC 62443 Foundation", "descricao": "Segurança em ICS/SCADA", "nivel": "Foundation", "xp_necessario": 120, "ano": 2027, "trimestre": "Q2"},
    "MITRE ATT&CK ICS": {"icone": "🏭", "cor": "#A0A0A0", "emblema": "🎯", "emblema_grande": "🎯🏭", "titulo": "MITRE ATT&CK for ICS", "descricao": "Táticas e Técnicas para ICS", "nivel": "Intermediate", "xp_necessario": 120, "ano": 2028, "trimestre": "Q1"},
    "GICSP": {"icone": "🏭", "cor": "#606060", "emblema": "⚙️", "emblema_grande": "🏭⚙️", "titulo": "GICSP", "descricao": "Segurança Industrial Global", "nivel": "Expert", "xp_necessario": 180, "ano": 2028, "trimestre": "Q3"},
    "Python": {"icone": "🐍", "cor": "#3776AB", "emblema": "⚡", "emblema_grande": "🐍⚡", "titulo": "Python for Data", "descricao": "Automação e Análise de Dados", "nivel": "Advanced", "xp_necessario": 150, "ano": 2026, "trimestre": "Q3"},
    "SQL": {"icone": "🗄️", "cor": "#F29111", "emblema": "📊", "emblema_grande": "🗄️📊", "titulo": "Advanced SQL", "descricao": "Consultas e Modelagem de Dados", "nivel": "Intermediate", "xp_necessario": 120, "ano": 2026, "trimestre": "Q4"},
    "Power BI": {"icone": "📈", "cor": "#F2C811", "emblema": "🎨", "emblema_grande": "📈🎨", "titulo": "Power BI Expert", "descricao": "Dashboards e Analytics", "nivel": "Intermediate", "xp_necessario": 120, "ano": 2026, "trimestre": "Q4"},
    "CCNA": {"icone": "🌐", "cor": "#1BA0D7", "emblema": "🕸️", "emblema_grande": "🌐🕸️", "titulo": "CCNA", "descricao": "Redes e Infraestrutura", "nivel": "Associate", "xp_necessario": 150, "ano": 2026, "trimestre": "Q2"},
    "SC-900": {"icone": "🔐", "cor": "#0078D4", "emblema": "🎯", "emblema_grande": "🔐🎯", "titulo": "SC-900", "descricao": "Segurança e Compliance", "nivel": "Foundation", "xp_necessario": 100, "ano": 2026, "trimestre": "Q1"},
    "Pos-graduacao": {"icone": "🎓", "cor": "#800080", "emblema": "📜", "emblema_grande": "🎓📜", "titulo": "Pós-graduação", "descricao": "Cibersegurança e Governança de Dados", "nivel": "Advanced", "xp_necessario": 300, "ano": 2026, "trimestre": "Q2-Q4"},
    "Ingles": {"icone": "🇬🇧", "cor": "#1E90FF", "emblema": "💬", "emblema_grande": "🇬🇧💬", "titulo": "English Fluency", "descricao": "Proficiência Internacional", "nivel": "Essential", "xp_necessario": 250, "ano": "Contínuo", "trimestre": "2026-2029"},
    "Cloud Security": {"icone": "☁️", "cor": "#00A4EF", "emblema": "🔒", "emblema_grande": "☁️🔒", "titulo": "Cloud Security", "descricao": "Segurança Multi-Cloud", "nivel": "Advanced", "xp_necessario": 150, "ano": 2028, "trimestre": "Q4"},
    "DevSecOps": {"icone": "🔄", "cor": "#6C3483", "emblema": "🚀", "emblema_grande": "🔄🚀", "titulo": "DevSecOps", "descricao": "Segurança no Ciclo DevOps", "nivel": "Advanced", "xp_necessario": 150, "ano": 2029, "trimestre": "Q1"}
}

# =========================
# STYLE PICA DAS GALÁXIAS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"] {
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
    margin-bottom: 10px;
}
.cert-card.atrasado { border-left: 5px solid #ff4444; background: rgba(255, 68, 68, 0.05); }
.level-badge { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "db" not in st.session_state: st.session_state.db = []
if "xp" not in st.session_state: st.session_state.xp = 0
if "cert_xp" not in st.session_state: st.session_state.cert_xp = {cert: 0 for cert in EMBLEMAS.keys()}
if "cert_status" not in st.session_state: st.session_state.cert_status = {cert: "Não iniciada" for cert in EMBLEMAS.keys()}

# =========================
# FUNÇÕES
# =========================
def calc_xp(activity):
    xp_table = {"Estudo": 10, "Laboratório": 20, "Projeto": 30, "Revisão": 15, "Simulado": 15, "Aula Pós-graduação": 25, "Inglês": 15, "Certificação": 50}
    return xp_table.get(activity, 10)

def status_por_xp(xp, cert):
    req = EMBLEMAS[cert]["xp_necessario"]
    if xp >= req: return "Concluída"
    elif xp >= req * 0.3: return "Em andamento"
    return "Não iniciada"

def verificar_atraso(cert, ano_plan):
    if ano_plan == "Contínuo": return False
    if datetime.now().year > ano_plan and st.session_state.cert_xp[cert] < EMBLEMAS[cert]["xp_necessario"]: return True
    return False

def get_badge_icon(status):
    return {"Concluída": "🏆", "Em andamento": "⚡", "Não iniciada": "💤"}.get(status, "❓")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"## 🚀 **XP Total: {st.session_state.xp}**")
    st.progress(min((st.session_state.xp % 100) / 100, 1.0))
    st.markdown("---")
    st.markdown("### 📊 Status das Trilhas")
    for trilha, certs in {"Azure": ["AZ-900", "AZ-104", "AZ-500"], "Segurança": ["Security+", "CySA+", "CISSP"]}.items():
        xp_t = sum(st.session_state.cert_xp[c] for c in certs)
        xp_m = sum(EMBLEMAS[c]["xp_necessario"] for c in certs)
        st.write(f"{trilha}: {int((xp_t/xp_m)*100)}%")
        st.progress(xp_t/xp_m)

# =========================
# CONTEÚDO PRINCIPAL
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Dashboard", "🗺️ Mapa", "📅 Trilhas", "🏅 Conquistas"])

with tab1:
    with st.expander("✨ NOVA MISSÃO", expanded=True):
        c1, c2 = st.columns(2)
        with c1: area = st.selectbox("🎯 Área", list(EMBLEMAS.keys()))
        with c2: act = st.selectbox("⚔️ Atividade", ["Estudo", "Laboratório", "Projeto", "Simulado"])
        if st.button("🚀 LANÇAR"):
            gain = calc_xp(act)
            st.session_state.db.append({"data": datetime.now(), "area": area, "atividade": act, "xp": gain})
            st.session_state.xp += gain
            st.session_state.cert_xp[area] += gain
            st.session_state.cert_status[area] = status_por_xp(st.session_state.cert_xp[area], area)
            st.rerun()

    for cert, xp in st.session_state.cert_xp.items():
        emb = EMBLEMAS[cert]
        atraso = verificar_atraso(cert, emb["ano"])
        status = st.session_state.cert_status[cert]
        
        st.markdown(f"""
        <div class="cert-card {'atrasado' if atraso else ''}">
            <h3 style="margin:0">{emb['emblema_grande']} {cert} - {status}</h3>
            <p style="font-size:12px">{emb['descricao']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(xp/emb['xp_necessario'], 1.0))

with tab2:
    st.markdown("## 🗺️ Planejamento Temporal")
    for ano in [2026, 2027, 2028, 2029]:
        st.subheader(f"📅 {ano}")
        cols = st.columns(4)
        certs_ano = [c for c, d in EMBLEMAS.items() if d.get("ano") == ano]
        for i, c in enumerate(certs_ano):
            with cols[i % 4]:
