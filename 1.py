import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide"
)

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026},
    "AZ-104": {"emblema": "☁️⚙️", "cor": "#0078D4", "titulo": "Azure Administrator", "xp": 150, "ano": 2026},
    "AZ-500": {"emblema": "☁️🔐", "cor": "#005BA1", "titulo": "Azure Security", "xp": 150, "ano": 2026},
    "ISO 27001 Fundamentals": {"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation", "xp": 100, "ano": 2026},
    "ISO 27001 Auditor": {"emblema": "🔒🔍", "cor": "#FFC000", "titulo": "ISO Auditor", "xp": 150, "ano": 2027},
    "ISO 27001 Implementer": {"emblema": "🔒🛠️", "cor": "#FFA000", "titulo": "ISO Implementer", "xp": 150, "ano": 2027},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029},
    "IEC 62443": {"emblema": "🏭📏", "cor": "#808080", "titulo": "IEC 62443", "xp": 120, "ano": 2027},
    "MITRE ATT&CK ICS": {"emblema": "🎯🏭", "cor": "#A0A0A0", "titulo": "MITRE ICS", "xp": 120, "ano": 2028},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026},
    "CCNA": {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA", "xp": 150, "ano": 2026},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo"},
    "Cloud Security": {"emblema": "☁️🔒", "cor": "#00A4EF", "titulo": "Cloud Security", "xp": 150, "ano": 2028},
    "DevSecOps": {"emblema": "🔄🚀", "cor": "#6C3483", "titulo": "DevSecOps", "xp": 150, "ano": 2029}
}

# =========================
# STYLE
# =========================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0a0e27, #1a1f3a);
        color: #4d9fff;
    }
    h1, h2, h3 {
        background: linear-gradient(135deg, #4d9fff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .red-text { color: #ff4444 !important; font-weight: bold; }
    .cert-card {
        background: rgba(77, 159, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(77, 159, 255, 0.2);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .atrasado { border-left: 5px solid #ff4444 !important; }
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
# FUNÇÕES
# =========================
def calc_xp(activity):
    tabela = {
        "Estudo": 10, "Laboratório": 20, "Projeto": 30, "Revisão": 15,
        "Simulado": 15, "Aula Pós-graduação": 25, "Inglês": 15, "Certificação": 50
    }
    return tabela.get(activity, 10)

def get_badge(status):
    badges = {"Concluída": "🏆", "Em andamento": "⚡", "Não iniciada": "💤"}
    return badges.get(status, "💤")

def verificar_atraso(cert, ano):
    if ano == "Contínuo": return False
    if isinstance(ano, int) and datetime.now().year > ano:
        return st.session_state.cert_xp.get(cert, 0) < EMBLEMAS[cert]["xp"]
    return False

def delete_activity(index):
    # Precisamos deletar do banco original usando o índice correto
    atividade = st.session_state.db.pop(index)
    st.session_state.xp -= atividade["xp"]
    st.session_state.cert_xp[atividade["area"]] -= atividade["xp"]

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 Nave")
    st.markdown(f"👨‍🚀 **Juan Felipe**")
    st.markdown(f"⭐ **XP:** {st.session_state.xp}")
    st.markdown(f"🎖️ **Nível:** {st.session_state.xp // 100 + 1}")
    
    atrasadas = [c for c, d in EMBLEMAS.items() if verificar_atraso(c, d.get("ano"))]
    if atrasadas:
        st.markdown('<p class="red-text">⚠️ Atrasadas:</p>', unsafe_allow_html=True)
        for c in atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[c]["emblema"]} {c}</p>', unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Cibersegurança")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Dashboard", "🗺️ Roadmap", "📅 Trilhas", "🏅 Conquistas"])

with tab1:
    with st.expander("✨ Nova Missão"):
        c1, c2 = st.columns(2)
        with c1:
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
            atv = st.selectbox("Atividade", ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", "Aula Pós-graduação", "Inglês", "Certificação"])
        with c2:
            dt = st.date_input("Data")
            obs = st.text_input("Observações")
        
        if st.button("🚀 Lançar Missão", use_container_width=True):
            ganho = calc_xp(atv)
            st.session_state.db.append({
                "data": pd.to_datetime(dt),
                "area": area,
                "atividade": atv,
                "xp": ganho,
                "obs": obs
            })
            st.session_state.xp += ganho
            st.session_state.cert_xp[area] += ganho
            
            # Atualiza Status Automático
            if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
                st.session_state.cert_status[area] = "Concluída"
            elif st.session_state.cert_xp[area] > 0:
                st.session_state.cert_status[area] = "Em andamento"
            st.rerun()

    # KPIs
    concluidas = sum(1 for xp in st.session_state.cert_xp.values() if xp >= 100) # Exemplo simplificado
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Missões", len(st.session_state.db))
    k2.metric("XP Total", st.session_state.xp)
    k3.metric("Nível", st.session_state.xp // 100 + 1)
    k4.metric("Concluídas", f"{concluidas}/{len(EMBLEMAS)}")

    st.markdown("---")
    
    # Grid de Certificações
    certs_list = list(EMBLEMAS.keys())
    for i in range(0, len(certs_list), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(certs_list):
                cert = certs_list[i+j]
                info = EMBLEMAS[cert]
                xp_atual = st.session_state.cert_xp[cert]
                prog = min(xp_atual / info["xp"], 1.0)
                status = st.session_state.cert_status[cert]
                
                with cols[j]:
                    atraso_classe = "atrasado" if verificar_atraso(cert, info["ano"]) else ""
                    st.markdown(f"""
                    <div class="cert-card {atraso_classe}">
                        <div style="font-size:30px">{info['emblema']}</div>
                        <div style="font-size:12px; font-weight:bold; text-align:center">{cert}</div>
                        <div style="font-size:20px">{get_badge(status)}</div>
                        <div style="font-size:10px">{xp_atual}/{info['xp']} XP</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(prog)

    # Histórico e Gráfico
    if st.session_state.db:
        st.markdown("### 📈 Evolução")
        df = pd.DataFrame(st.session_state.db)
        evol = df.groupby('data')['xp'].sum().reset_index().sort_values('data')
        evol['Acumulado'] = evol['xp'].cumsum()
        
        chart = alt.Chart(evol).mark_line(point=True, color='#4d9fff').encode(
            x='data:T', y='Acumulado:Q', tooltip=['data', 'Acumulado']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
        
        with st.expander("📜 Ver Histórico Detalhado"):
            for idx, row in df.iloc[::-1].iterrows():
                c = st.columns([1, 2, 1, 1])
                c[0].write(row['data'].strftime('%d/%m/%y'))
                c[1].write(f"{EMBLEMAS[row['area']]['emblema']} {row['area']}")
                c[2].write(
