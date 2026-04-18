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
# EMOJIS E ÍCONES ÉPICOS - VERSÃO COMPLETA
# =========================
EMBLEMAS = {
    # AZURE COMPLETO
    "AZ-900": {
        "icone": "☁️",
        "cor": "#00A4EF",
        "emblema": "🌩️",
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
        "titulo": "DevSecOps",
        "descricao": "Segurança no Ciclo DevOps",
        "nivel": "Advanced",
        "xp_necessario": 150,
        "ano": 2029,
        "trimestre": "Q1"
    }
}

# =========================
# STYLE ÉPICO
# =========================
st.markdown("""
<style>
html, body {
    background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 50%, #dee2e6 100%);
    color: #1a1a2e;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold !important;
}

.stMarkdown, p, div, span, label {
    color: #2c3e50 !important;
}

.stButton button {
    background: linear-gradient(135deg, #2c3e50, #34495e) !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.cert-card {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: all 0.3s;
}

.cert-card:hover {
    transform: translateX(10px);
    box-shadow: 0 5px 25px rgba(0,0,0,0.15);
}

.cert-card.atrasado {
    border-left: 4px solid #dc3545;
    background: linear-gradient(135deg, #fff5f5, #ffffff);
}

.level-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-left: 10px;
}

.red-text {
    color: #dc3545 !important;
    font-weight: bold;
}

.trilha-card {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    border-left: 4px solid #2c3e50;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.css-1d391kg, .css-12oz5g7 {
    background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
}

.css-1d391kg p, .css-12oz5g7 p, .css-12oz5g7 div {
    color: #e6f0ff !important;
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
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 Nave Estelar")
    st.markdown(f"""
    ### 👨‍🚀 Comandante: Juan Felipe
    ### ⭐ XP Total: {st.session_state.xp}
    ### 🎖️ Nível: {st.session_state.xp // 100 + 1}
    ### 📅 Missões: {len(st.session_state.db)}
    """)
    
    xp_no_nivel = st.session_state.xp % 100
    st.progress(xp_no_nivel / 100 if xp_no_nivel > 0 else 0)
    st.caption(f"Próximo nível: {100 - xp_no_nivel} XP")
    
    st.markdown("---")
    
    certificacoes_atrasadas = []
    for cert, data in EMBLEMAS.items():
        if verificar_atraso(cert, data.get("ano", 2030)):
            certificacoes_atrasadas.append(cert)
    
    if certificacoes_atrasadas:
        st.markdown('<p class="red-text">⚠️ ATENÇÃO - CERTIFICAÇÕES ATRASADAS:</p>', unsafe_allow_html=True)
        for cert in certificacoes_atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[cert]["emblema"]} {cert}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Top 5 Especializações")
    
    ranking = sorted(st.session_state.cert_xp.items(), key=lambda x: x[1], reverse=True)
    for cert, xp in ranking[:5]:
        if cert in EMBLEMAS:
            emblema = EMBLEMAS[cert]["emblema"]
            xp_necessario = EMBLEMAS[cert]["xp_necessario"]
            percent = (xp / xp_necessario) * 100
            st.markdown(f"{emblema} **{cert[:15]}**: {percent:.0f}%")
            st.progress(min(xp / xp_necessario, 1.0))
    
    st.markdown("---")
    st.markdown("### 📊 Resumo por Trilha")
    
    trilhas = {
        "Azure": ["AZ-900", "AZ-104", "AZ-500"],
        "ISO 27001": ["ISO 27001 Fundamentals", "ISO 27001 Auditor", "ISO 27001 Implementer"],
        "Seguranca": ["Security+", "CySA+", "CISSP"],
        "OT Industrial": ["IEC 62443", "MITRE ATT&CK ICS", "GICSP"],
        "Dados": ["Python", "SQL", "Power BI"]
    }
    
    for trilha, certs in trilhas.items():
        xp_total = sum(st.session_state.cert_xp.get(cert, 0) for cert in certs)
        xp_max = sum(EMBLEMAS[cert]["xp_necessario"] for cert in certs)
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
    st.markdown("# 🚀 MISSAO CARREIRA")
    st.markdown("### Juan Felipe da Silva - Especialista em Ciberseguranca e Cloud")
    st.markdown('<p class="red-text">🎯 Meta: Completar todas as certificacoes ate 2029!</p>', unsafe_allow_html=True)
    st.markdown("---")

# =========================
# ABAS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Dashboard", "🗺️ Roadmap Completo", "📅 Trilhas", "🏅 Conquistas"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    
    with st.expander("✨ NOVA MISSAO", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.selectbox("🎯 Area de Especializacao", list(EMBLEMAS.keys()))
            activity = st.selectbox("⚔️ Tipo de Missao", 
                                   ["Estudo", "Laboratorio", "Projeto", "Revisao", "Simulado", 
                                    "Aula Pos-graduacao", "Ingles", "Certificacao"])
        
        with col2:
            data = st.date_input("📆 Data", value=pd.Timestamp.today())
            obs = st.text_area("📝 Observacoes de Bordo")
        
        if st.button("🚀 LANCAR MISSAO", use_container_width=True):
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
            st.success(f"Missao completa! +{xp_gain} XP conquistado!", icon="🎉")
            st.balloons()
            st.rerun()
    
    col1, col2, col3, col4 = st.columns(4)
    
    if st.session_state.db:
        df_temp = pd.DataFrame(st.session_state.db)
        dias_unicos = df_temp['data'].nunique()
        certificacoes_concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() 
                                      if cert in EMBLEMAS and xp >= EMBLEMAS[cert]["xp_necessario"])
        
        col1.metric("🎮 Missoes", len(st.session_state.db))
        col2.metric("⭐ XP Global", st.session_state.xp)
        col3.metric("🏆 Nivel", st.session_state.xp // 100 + 1)
        col4.metric("✅ Certificacoes", f"{certificacoes_concluidas}/{len(EMBLEMAS)}")
    else:
        col1.metric("🎮 Missoes", 0)
        col2.metric("⭐ XP Global", 0)
        col3.metric("🏆 Nivel", 1)
        col4.metric("✅ Certificacoes", f"0/{len(EMBLEMAS)}")
    
    st.markdown("---")
    st.markdown("## 🎖️ PROGRESSO DAS CERTIFICACOES")
    
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
                    <h3 style="margin: 0; color: #2c3e50;">
                        {emblema_data['emblema']} {cert} 
                        <span style="font-size: 14px; color: {emblema_data['cor']};">{emblema_data['titulo']}</span>
                        <span class="level-badge" style="background: {emblema_data['cor']}20; color: {emblema_data['cor']};">
                            {nivel_icon} {emblema_data['nivel']}
                        </span>
                    </h3>
                    <p style="margin: 5px 0 0 0; color: #6c757d;">{emblema_data['descricao']}</p>
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
                st.markdown(f'<p class="red-text">Progresso: {xp}/{xp_necessario} XP ({int(progress*100)}%) - ATRASADO!</p>', unsafe_allow_html=True)
            else:
                st.caption(f"Progresso: {xp}/{xp_necessario} XP ({int(progress*100)}%)")
        
        with col2:
            st.markdown(f"**Status:** {badge_icon} {status}")
        
        with col3:
            status_options = ["Nao iniciada", "Em andamento", "Concluida"]
            current_index = status_options.index(status) if status in status_options else 0
            new_status_manual = st.selectbox(
                "Alterar",
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
    st.markdown("## 📜 REGISTRO DE MISSOES")
    
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
        
        chart = alt.Chart(evolucao).mark_line(point=True, color='#2c3e50', strokeWidth=3).encode(
            x=alt.X("data:T", title="Data", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("xp_acumulado:Q", title="XP Acumulado"),
            tooltip=["data", "xp_acumulado"]
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
        
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 BAIXAR RELATORIO", csv, "jornada_completa.csv", "text/csv")

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:
    st.markdown("## 🗺️ ROADMAP ESTRATEGICO 2026-2029")
    
    anos = {
        2026: "🌱 ANO 1 - FUNDACAO",
        2027: "⚡ ANO 2 - ESPECIALIZACAO",
        2028: "🎯 ANO 3 - MAESTRIA TECNICA",
        2029: "👑 ANO 4 - LIDERANCA"
    }
    
    for ano, titulo in anos.items():
        with st.expander(titulo, expanded=(ano == 2026)):
            certs_ano = [cert for cert, data in EMBLEMAS.items() if data.get("ano") == ano]
            
            if certs_ano:
                cols = st.columns(min(len(certs_ano), 4))
                for i, cert in enumerate(certs_ano):
                    emblema = EMBLEMAS[cert]
                    status = st.session_state.cert_status.get(cert, "Nao iniciada")
                    badge = get_badge_icon(status)
                    xp_atual = st.session_state.cert_xp.get(cert, 0)
                    xp_necessario = emblema["xp_necessario"]
                    percent = (xp_atual / xp_necessario) * 100
                    
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 15px; background: white; border-radius: 10px; margin: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <div style="font-size: 48px;">{emblema['emblema']}</div>
                            <div style="font-size: 16px; font-weight: bold; color: #2c3e50;">{cert}</div>
                            <div style="font-size: 11px; color: #6c757d;">{emblema['titulo']}</div>
                            <div style="font-size: 24px;">{badge}</div>
                            <div style="font-size: 11px; color: #2c3e50;">{xp_atual}/{xp_necessario} XP</div>
                            <div style="background: #e9ecef; border-radius: 5px; height: 5px; margin-top: 5px;">
                                <div style="background: {emblema['cor']}; width: {percent}%; height: 5px; border-radius: 5px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# =========================
# TAB 3 - TRILHAS
# =========================
with tab3:
    st.markdown("## 🎯 TRILHAS DE ESPECIALIZACAO")
    
    trilhas_info = {
        "Azure": {
            "certs": ["AZ-900", "AZ-104", "AZ-500"],
            "desc": "Dominio completo do ecossistema Microsoft Azure",
            "objetivo": "Arquiteto de Solucoes Cloud"
        },
        "ISO 27001": {
            "certs": ["ISO 27001 Fundamentals", "ISO 27001 Auditor", "ISO 27001 Implementer"],
            "desc": "Implementacao e auditoria de SGSI completo",
            "objetivo": "Lead Auditor e Implementer"
        },
        "Seguranca": {
            "certs": ["Security+", "CySA+", "CISSP"],
            "desc": "Do fundamentals a arquitetura de seguranca",
            "objetivo": "Arquiteto de Ciberseguranca"
        },
        "OT Industrial": {
            "certs": ["IEC 62443", "MITRE ATT&CK ICS", "GICSP"],
            "desc": "Especializacao em seguranca industrial",
            "objetivo": "Especialista em ICS Security"
        },
        "Dados": {
            "certs": ["Python", "SQL", "Power BI"],
            "desc": "Analise e visualizacao de dados",
            "objetivo": "Data Analyst Expert"
        }
    }
    
    for trilha, info in trilhas_info.items():
        st.markdown(f"""
        <div class="trilha-card">
            <h3 style="color: #2c3e50;">{trilha}</h3>
            <p style="color: #6c757d;">{info['desc']}</p>
            <p><strong>Objetivo:</strong> {info['objetivo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, cert in enumerate(info["certs"]):
            if cert in EMBLEMAS:
                emblema = EMBLEMAS[cert]
                xp_atual = st.session_state.cert_xp.get(cert, 0)
                xp_necessario = emblema["xp_necessario"]
                percent = (xp_atual / xp_necessario) * 100
                status = st.session_state.cert_status.get(cert, "Nao iniciada")
                badge_icon = get_badge_icon(status)
                
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 10px; margin: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <div style="font-size: 40px;">{emblema['emblema']}</div>
                        <div style="font-weight: bold; color: #2c3e50;">{cert}</div>
                        <div style="font-size: 11px; color: #6c757d;">{emblema['titulo']}</div>
                        <div style="font-size: 24px;">{badge_icon}</div>
                        <div style="font-size: 12px; color: #2c3e50;">{percent:.0f}%</div>
                        <div style="background: #e9ecef; border-radius: 5px; height: 5px; margin-top: 5px;">
                            <div style="background: {emblema['cor']}; width: {percent}%; height: 5px; border-radius: 5px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        xp_total = sum(st.session_state.cert_xp.get(cert, 0) for cert in info["certs"] if cert in EMBLEMAS)
        xp_max = sum(EMBLEMAS[cert]["xp_necessario"] for cert in info["certs"] if cert in EMBLEMAS)
        progresso_trilha = (xp_total / xp_max) * 100 if xp_max > 0 else 0
        
        st.progress(progresso_trilha / 100)
        st.caption(f"Progresso da Trilha: {progresso_trilha:.0f}%")
        st.markdown("---")

# =========================
# TAB 4 - CONQUISTAS
# =========================
with tab4:
    st.markdown("## 🏅 HALL DA FAMA")
    
    conquistas = []
    
    if len(st.session_state.db) >= 20:
        conquistas.append({"nome": "Maratonista Epico", "desc": "Completou 20+ missoes", "icone": "🎯", "desbloqueado": True})
    elif len(st.session_state.db) >= 10:
        conquistas.append({"nome": "Maratonista", "desc": "Completou 10 missoes", "icone": "🏃", "desbloqueado": True})
    else:
        faltam = 10 - len(st.session_state.db)
        conquistas.append({"nome": "Maratonista", "desc": f"Complete mais {faltam} missoes", "icone": "🏃", "desbloqueado": False})
    
    certificacoes_concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() 
                                  if cert in EMBLEMAS and xp >= EMBLEMAS[cert]["xp_necessario"])
    
    if certificacoes_concluidas >= 1:
        conquistas.append({"nome": "Especialista", "desc": "Concluiu sua primeira certificacao", "icone": "🏆", "desbloqueado": True})
    else:
        conquistas.append({"nome": "Especialista", "desc": "Conclua sua primeira certificacao", "icone": "🏆", "desbloqueado": False})
    
    if st.session_state.db:
        dias_unicos = len(set([r['data'].date() for r in st.session_state.db]))
        if dias_unicos >= 5:
            conquistas.append({"nome": "Dedicado", "desc": "Estudou em 5+ dias diferentes", "icone": "📅", "desbloqueado": True})
        else:
            faltam = 5 - dias_unicos
            conquistas.append({"nome": "Dedicado", "desc": f"Estude em mais {faltam} dias", "icone": "📅", "desbloqueado": False})
    else:
        conquistas.append({"nome": "Dedicado", "desc": "Estude em 5 dias diferentes", "icone": "📅", "desbloqueado": False})
    
    if st.session_state.xp >= 500:
        conquistas.append({"nome": "Veterano", "desc": "Acumulou 500+ XP", "icone": "💪", "desbloqueado": True})
    else:
        faltam = 500 - st.session_state.xp
        conquistas.append({"nome": "Veterano", "desc": f"Acumule mais {faltam} XP", "icone": "💪", "desbloqueado": False})
    
    if st.session_state.xp >= 1000:
        conquistas.append({"nome": "Lendario", "desc": "Ultrapassou 1000 XP", "icone": "🌟", "desbloqueado": True})
    else:
        faltam = 1000 - st.session_state.xp
        conquistas.append({"nome": "Lendario", "desc": f"Acumule mais {faltam} XP", "icone": "🌟", "desbloqueado": False})
    
    if certificacoes_concluidas >= 3:
        conquistas.append({"nome": "Mestre das Certificacoes", "desc": "Concluiu 3 certificacoes", "icone": "📜", "desbloqueado": True})
    else:
        faltam = 3 - certificacoes_concluidas
        conquistas.append({"nome": "Mestre das Certificacoes", "desc": f"Conclua mais {faltam} certificacoes", "icone": "📜", "desbloqueado": False})
    
    cols = st.columns(3)
    for i, conquista in enumerate(conquistas):
        with cols[i % 3]:
            if conquista["desbloqueado"]:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #28a745, #20c997); border-radius: 15px; margin: 10px;">
                    <div style="font-size: 48px;">{conquista['icone']}</div>
                    <div style="font-size: 18px; font-weight: bold; color: white;">{conquista['nome']}</div>
                    <div style="font-size: 12px; color: white;">{conquista['desc']}</div>
                    <div style="font-size: 24px; margin-top: 10px;">✅</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: #e9ecef; border-radius: 15px; margin: 10px; opacity: 0.6;">
                    <div style="font-size: 48px;">{conquista['icone']}</div>
                    <div style="font-size: 18px; font-weight: bold; color: #6c757d;">{conquista['nome']}</div>
                    <div style="font-size: 12px; color: #6c757d;">{conquista['desc']}</div>
                    <div style="font-size: 24px; margin-top: 10px;">🔒</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #6c757d;">🚀 Continue sua jornada, o universo da tecnologia espera por voce! 🌟</p>
        <p style="color: #6c757d; font-size: 12px;">Cada missao completada e um passo mais perto da maestria!</p>
    </div>
    """, unsafe_allow_html=True)
