import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026, "trimestre": "Q1"},
    "AZ-104": {"emblema": "☁️⚙️", "cor": "#0078D4", "titulo": "Azure Administrator", "xp": 150, "ano": 2026, "trimestre": "Q2"},
    "AZ-500": {"emblema": "☁️🔐", "cor": "#005BA1", "titulo": "Azure Security", "xp": 150, "ano": 2026, "trimestre": "Q3"},
    "ISO 27001 Fundamentals": {"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation", "xp": 100, "ano": 2026, "trimestre": "Q2"},
    "ISO 27001 Auditor": {"emblema": "🔒🔍", "cor": "#FFC000", "titulo": "ISO Auditor", "xp": 150, "ano": 2027, "trimestre": "Q1"},
    "ISO 27001 Implementer": {"emblema": "🔒🛠️", "cor": "#FFA000", "titulo": "ISO Implementer", "xp": 150, "ano": 2027, "trimestre": "Q2"},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027, "trimestre": "Q3"},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027, "trimestre": "Q4"},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029, "trimestre": "Q2"},
    "IEC 62443": {"emblema": "🏭📏", "cor": "#808080", "titulo": "IEC 62443", "xp": 120, "ano": 2027, "trimestre": "Q2"},
    "MITRE ATT&CK ICS": {"emblema": "🎯🏭", "cor": "#A0A0A0", "titulo": "MITRE ICS", "xp": 120, "ano": 2028, "trimestre": "Q1"},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028, "trimestre": "Q3"},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026, "trimestre": "Q3"},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026, "trimestre": "Q4"},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026, "trimestre": "Q4"},
    "CCNA": {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA", "xp": 150, "ano": 2026, "trimestre": "Q2"},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026, "trimestre": "Q1"},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026, "trimestre": "Q2-Q4"},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo", "trimestre": "2026-2029"},
    "Cloud Security": {"emblema": "☁️🔒", "cor": "#00A4EF", "titulo": "Cloud Security", "xp": 150, "ano": 2028, "trimestre": "Q4"},
    "DevSecOps": {"emblema": "🔄🚀", "cor": "#6C3483", "titulo": "DevSecOps", "xp": 150, "ano": 2029, "trimestre": "Q1"}
}

# =========================
# STYLE ÉPICO
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
    color: #4d9fff;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, #4d9fff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold !important;
    margin-top: 0;
    margin-bottom: 10px;
}

.red-text {
    color: #ff4444 !important;
    font-weight: bold;
    text-shadow: 0 0 5px rgba(255,68,68,0.3);
}

.green-text {
    color: #00ff88 !important;
    font-weight: bold;
}

.stButton button {
    background: linear-gradient(135deg, #4d9fff, #7b2ff7) !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    transition: all 0.3s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(77,159,255,0.4);
}

.cert-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 12px;
    padding: 10px;
    margin: 5px;
    border: 1px solid rgba(77,159,255,0.3);
    transition: all 0.3s;
    cursor: pointer;
}

.cert-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(77,159,255,0.2);
    border-color: #4d9fff;
}

.cert-card.atrasado {
    border-left: 3px solid #ff4444;
    background: linear-gradient(135deg, rgba(255,68,68,0.1), rgba(123,47,247,0.05));
}

.atividade-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.08), rgba(123,47,247,0.03));
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
    border-left: 3px solid #4d9fff;
    transition: all 0.2s;
}

.atividade-card:hover {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
    transform: translateX(5px);
}

.kpi-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(77,159,255,0.3);
}

.stProgress > div > div {
    background: linear-gradient(90deg, #4d9fff, #7b2ff7) !important;
}

.css-1d391kg, .css-12oz5g7 {
    background: linear-gradient(135deg, #0a0e27, #0d1133) !important;
    border-right: 1px solid rgba(77,159,255,0.2);
}

/* Scrollbar personalizada */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0a0e27;
}
::-webkit-scrollbar-thumb {
    background: #4d9fff;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #7b2ff7;
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
if "atividades_hoje" not in st.session_state:
    st.session_state.atividades_hoje = []

# =========================
# FUNÇÕES
# =========================
def calc_xp(atividade):
    tabela = {
        "📚 Estudo": 10,
        "🔬 Laboratório": 20,
        "🏗️ Projeto": 30,
        "🔄 Revisão": 15,
        "📝 Simulado": 15,
        "🎓 Aula Pós": 25,
        "🌎 Inglês": 15,
        "🏅 Certificação": 50
    }
    return tabela.get(atividade, 10)

def get_badge(status):
    if status == "Concluída":
        return "🏆"
    elif status == "Em andamento":
        return "⚡"
    return "💤"

def get_status_color(status):
    if status == "Concluída":
        return "#00ff88"
    elif status == "Em andamento":
        return "#ffaa00"
    return "#ff4444"

def verificar_atraso(cert, ano):
    if ano == "Contínuo":
        return False
    if isinstance(ano, int) and datetime.now().year > ano:
        if st.session_state.cert_xp.get(cert, 0) < EMBLEMAS[cert]["xp"]:
            return True
    return False

def delete_activity(index):
    atividade = st.session_state.db[index]
    st.session_state.xp -= atividade["xp"]
    st.session_state.cert_xp[atividade["area"]] -= atividade["xp"]
    st.session_state.db.pop(index)
    
    # Atualiza status
    area = atividade["area"]
    xp_atual = st.session_state.cert_xp[area]
    if xp_atual >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluída"
    elif xp_atual >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"
    else:
        st.session_state.cert_status[area] = "Não iniciada"

def adicionar_atividade(area, atividade, xp, obs):
    st.session_state.db.append({
        "data": pd.Timestamp.now(),
        "area": area,
        "atividade": atividade,
        "xp": xp,
        "obs": obs
    })
    st.session_state.xp += xp
    st.session_state.cert_xp[area] += xp
    
    # Atualiza status
    if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluída"
    elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"

def get_atividades_hoje():
    hoje = datetime.now().date()
    return [a for a in st.session_state.db if a['data'].date() == hoje]

def get_xp_semana():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    return sum(a['xp'] for a in st.session_state.db if a['data'].date() >= inicio_semana.date())

def get_xp_mes():
    hoje = datetime.now()
    return sum(a['xp'] for a in st.session_state.db if a['data'].month == hoje.month and a['data'].year == hoje.year)

def gerar_relatorio_html(data):
    atividades = [a for a in st.session_state.db if a['data'].date() == data]
    if not atividades:
        return None
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Missões - {data.strftime('%d/%m/%Y')}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #0a0e27, #1a1f3a);
                color: #4d9fff;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
                border-radius: 20px;
                padding: 30px;
                border: 1px solid rgba(77,159,255,0.3);
            }}
            h1 {{
                text-align: center;
                border-bottom: 2px solid #4d9fff;
                padding-bottom: 10px;
            }}
            .atividade {{
                background: rgba(77,159,255,0.1);
                margin: 10px 0;
                padding: 15px;
                border-radius: 10px;
                border-left: 3px solid #4d9fff;
            }}
            .total {{
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                margin-top: 30px;
                padding: 20px;
                background: rgba(77,159,255,0.15);
                border-radius: 10px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 11px;
                opacity: 0.7;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 RELATÓRIO DE MISSÕES</h1>
            <h2>📅 {data.strftime('%d/%m/%Y')}</h2>
            <p>👨‍🚀 Comandante: Juan Felipe da Silva</p>
            <hr>
    """
    
    total_xp = 0
    for atv in atividades:
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        total_xp += atv['xp']
        html += f"""
            <div class="atividade">
                <strong>{emblema} {atv['area']}</strong><br>
                ⚔️ {atv['atividade']}<br>
                ⭐ +{atv['xp']} XP<br>
                📝 {atv['obs'] if atv['obs'] else 'Sem observações'}
            </div>
        """
    
    html += f"""
            <div class="total">
                🌟 TOTAL DO DIA: +{total_xp} XP 🌟
            </div>
            <div class="footer">
                Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br>
                Missão Carreira - Juan Felipe da Silva
            </div>
        </div>
    </body>
    </html>
    """
    return html

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 NAVE ESTELAR")
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center;">
        <div style="font-size: 48px;">👨‍🚀</div>
        <h3 style="margin: 0;">Juan Felipe</h3>
        <p style="margin: 0; opacity: 0.8;">Comandante</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Métricas do Sidebar
    st.markdown("### 📊 Status")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**⭐ XP**")
        st.markdown(f"<h2 style='margin:0;'>{st.session_state.xp}</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"**🎖️ Nível**")
        st.markdown(f"<h2 style='margin:0;'>{st.session_state.xp // 100 + 1}</h2>", unsafe_allow_html=True)
    
    st.progress((st.session_state.xp % 100) / 100 if st.session_state.xp % 100 > 0 else 0)
    st.caption(f"Próximo nível: {100 - (st.session_state.xp % 100)} XP")
    
    st.markdown("---")
    
    # Alertas
    atrasadas = [c for c, d in EMBLEMAS.items() if verificar_atraso(c, d.get("ano", 2030))]
    if atrasadas:
        st.markdown('<p class="red-text">⚠️ CERTIFICAÇÕES ATRASADAS</p>', unsafe_allow_html=True)
        for c in atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[c]["emblema"]} {c[:20]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hoje
    st.markdown("### 📅 Hoje")
    atividades_hoje = get_atividades_hoje()
    xp_hoje = sum(a['xp'] for a in atividades_hoje)
    st.markdown(f"**Atividades:** {len(atividades_hoje)}")
    st.markdown(f"**XP Hoje:** +{xp_hoje}")
    
    # Semana
    st.markdown("### 📆 Esta Semana")
    st.markdown(f"**XP Semana:** +{get_xp_semana()}")
    
    # Mês
    st.markdown("### 📅 Este Mês")
    st.markdown(f"**XP Mês:** +{get_xp_mes()}")

# =========================
# HEADER PRINCIPAL
# =========================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🚀 MISSÃO CARREIRA")
    st.markdown("### *Juan Felipe da Silva - Especialista em Cibersegurança*")
    st.markdown('<p class="red-text" style="text-align: center;">🎯 META: COMPLETAR TODAS AS CERTIFICAÇÕES ATÉ 2029!</p>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# ATIVIDADES DO DIA - DESTAQUE
# =========================
st.markdown("## ⚡ ATIVIDADES DE HOJE")
st.markdown(f"📅 {datetime.now().strftime('%A, %d de %B de %Y')}")

col_atv1, col_atv2, col_atv3 = st.columns([2, 1, 1])

with col_atv1:
    with st.container():
        st.markdown("#### ➕ Registrar Nova Atividade")
        with st.form("nova_atividade", clear_on_submit=True):
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()), key="atv_area")
            atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"], key="atv_tipo")
            obs = st.text_area("Observação", key="atv_obs", placeholder="Ex: Estudei módulo 3 do AZ-900...")
            
            if st.form_submit_button("🚀 LANÇAR MISSÃO", use_container_width=True):
                xp_ganho = calc_xp(atividade)
                adicionar_atividade(area, atividade, xp_ganho, obs)
                st.success(f"✅ Missão lançada! +{xp_ganho} XP", icon="🎉")
                st.rerun()

with col_atv2:
    st.markdown("#### 📊 Resumo Hoje")
    xp_hoje = sum(a['xp'] for a in get_atividades_hoje())
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 36px;">⭐</div>
        <div style="font-size: 28px; font-weight: bold;">+{xp_hoje}</div>
        <div>XP hoje</div>
    </div>
    """, unsafe_allow_html=True)

with col_atv3:
    st.markdown("#### 🎯 Meta Diária")
    meta_diaria = 50
    progresso_meta = min(xp_hoje / meta_diaria, 1.0)
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 36px;">🎯</div>
        <div style="font-size: 28px; font-weight: bold;">{xp_hoje}/{meta_diaria}</div>
        <div>XP da meta</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progresso_meta)

# Lista de atividades de hoje
atividades_hoje = get_atividades_hoje()
if atividades_hoje:
    st.markdown("#### 📝 Atividades Registradas Hoje")
    for atv in atividades_hoje:
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        st.markdown(f"""
        <div class="atividade-card">
            <table style="width: 100%;">
                <tr>
                    <td style="width: 40px; font-size: 24px;">{emblema}</td>
                    <td style="width: 25%;"><strong>{atv['area'][:25]}</strong></td>
                    <td style="width: 25%;">{atv['atividade']}</td>
                    <td style="width: 15%; color: #00ff88;">⭐ +{atv['xp']}</td>
                    <td style="width: 25%; font-size: 12px; opacity: 0.7;">{atv['obs'][:30] if atv['obs'] else '-'}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("✨ Nenhuma atividade registrada hoje. Que tal começar agora?")

st.markdown("---")

# =========================
# KPIS PRINCIPAIS
# =========================
st.markdown("## 📊 PAINEL DE CONTROLE")

col1, col2, col3, col4, col5 = st.columns(5)

concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
total_certs = len(EMBLEMAS)
percent_certs = (concluidas / total_certs) * 100

col1.metric("🎮 Total Missões", len(st.session_state.db))
col2.metric("⭐ XP Total", st.session_state.xp)
col3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
col4.metric("✅ Certificações", f"{concluidas}/{total_certs}")
col5.metric("📊 Progresso", f"{percent_certs:.0f}%")

st.markdown("---")

# =========================
# CERTIFICAÇÕES EM GRID
# =========================
st.markdown("## 🎖️ JORNADA DAS CERTIFICAÇÕES")

# Filtros
col_filtro1, col_filtro2 = st.columns([2, 1])
with col_filtro2:
    filtro_status = st.selectbox("Filtrar por status", ["Todas", "Concluída", "Em andamento", "Não iniciada"])

# Grid de certificações
certs_list = list(st.session_state.cert_xp.items())

for i in range(0, len(certs_list), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx < len(certs_list):
            cert, xp = certs_list[idx]
            info = EMBLEMAS[cert]
            status = st.session_state.cert_status[cert]
            
            # Aplicar filtro
            if filtro_status != "Todas" and status != filtro_status:
                continue
            
            atrasado = verificar_atraso(cert, info.get("ano", 2030))
            progresso = min(xp / info["xp"], 1.0)
            
            classe = "cert-card atrasado" if atrasado else "cert-card"
            status_color = get_status_color(status)
            
            with cols[j]:
                st.markdown(f"""
                <div class="{classe}">
                    <div style="text-align: center; font-size: 36px;">{info['emblema']}</div>
                    <div style="font-weight: bold; text-align: center; font-size: 11px;">{cert[:22]}</div>
                    <div style="text-align: center; font-size: 20px;">{get_badge(status)}</div>
                    <div style="text-align: center; font-size: 10px;">{xp}/{info['xp']} XP</div>
                    <div style="text-align: center; font-size: 10px; color: {status_color};">{status}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.progress(progresso)
                
                # Seletor de status compacto
                opcoes = ["Não iniciada", "Em andamento", "Concluída"]
                idx_status = opcoes.index(status) if status in opcoes else 0
                novo_status = st.selectbox("", opcoes, index=idx_status, key=f"status_{cert}", label_visibility="collapsed")
                if novo_status != status:
                    st.session_state.cert_status[cert] = novo_status
                    st.rerun()

st.markdown("---")

# =========================
# GRÁFICOS E RELATÓRIOS
# =========================
st.markdown("## 📈 ANÁLISE DE EVOLUÇÃO")

if len(st.session_state.db) > 0:
    df = pd.DataFrame(st.session_state.db)
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values('data')
    
    # Gráfico 1: Evolução Acumulada
    st.markdown("### 📊 Evolução do XP Acumulado")
    
    evolucao = df.groupby('data').agg({'xp': 'sum'}).reset_index()
    evolucao['xp_acumulado'] = evolucao['xp'].cumsum()
    
    chart1 = alt.Chart(evolucao).mark_line(
        point=alt.OverlayMarkDef(filled=True, fill='white', size=80),
        strokeWidth=3,
        color='#4d9fff'
    ).encode(
        x=alt.X('data:T', title='Data', axis=alt.Axis(labelAngle=-45, format='%d/%m/%Y')),
        y=alt.Y('xp_acumulado:Q', title='XP Total Acumulado'),
        tooltip=['data:T', 'xp_acumulado:Q']
    ).properties(height=350, title='🚀 Trajetória de Crescimento')
    
    st.altair_chart(chart1, use_container_width=True)
    
    # Gráfico 2: Atividades por Certificação
    st.markdown("### 🎯 Distribuição de XP por Certificação")
    
    xp_por_cert = df.groupby('area').agg({'xp': 'sum'}).reset_index()
    xp_por_cert = xp_por_cert.sort_values('xp', ascending=False).head(10)
    
    chart2 = alt.Chart(xp_por_cert).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X('area:N', title='Certificação', sort='-y', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('xp:Q', title='XP Total'),
        color=alt.Color('area:N', legend=None, scale=alt.Scale(scheme='turbo')),
        tooltip=['area', 'xp']
    ).properties(height=350, title='📊 Top 10 Certificações por XP')
    
    st.altair_chart(chart2, use_container_width=True)
    
    # Gráfico 3: Atividades por Tipo
    st.markdown("### ⚔️ Distribuição por Tipo de Atividade")
    
    atividades_count = df['atividade'].value_counts().reset_index()
    atividades_count.columns = ['atividade', 'quantidade']
    
    chart3 = alt.Chart(atividades_count).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='quantidade', type='quantitative'),
        color=alt.Color(field='atividade', type='nominal', scale=alt.Scale(scheme='viridis')),
        tooltip=['atividade', 'quantidade']
    ).properties(height=350, title='🍩 Proporção de Tipos de Atividade')
    
    st.altair_chart(chart3, use_container_width=True)
    
    # Gráfico 4: Heatmap de Atividades por Mês
    st.markdown("### 🔥 Calor de Atividades")
    
    df['mes'] = df['data'].dt.strftime('%Y-%m')
    heatmap_data = df.groupby(['mes', 'area']).size().reset_index(name='atividades')
    heatmap_data = heatmap_data.sort_values('atividades', ascending=False).head(20)
    
    chart4 = alt.Chart(heatmap_data).mark_rect().encode(
        x=alt.X('mes:N', title='Mês', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('area:N', title='Certificação'),
        color=alt.Color('atividades:Q', scale=alt.Scale(scheme='inferno'), title='Atividades'),
        tooltip=['mes', 'area', 'atividades']
    ).properties(height=400, title='🌡️ Mapa de Calor das Atividades')
    
    st.altair_chart(chart4, use_container_width=True)
    
else:
    st.info("📊 Complete algumas missões para visualizar os gráficos de evolução!")

st.markdown("---")

# =========================
# RELATÓRIO DO DIA
# =========================
st.markdown("## 📄 RELATÓRIO E EXPORTAÇÃO")

col_rel1, col_rel2 = st.columns([2, 1])

with col_rel1:
    st.markdown("### Gerar Relatório Diário")
    data_relatorio = st.date_input("Selecione a data", value=datetime.now().date())
    
    if st.button("📄 GERAR RELATÓRIO", use_container_width=True):
        relatorio = gerar_relatorio_html(data_relatorio)
        if relatorio:
            st.markdown(f'<div class="kpi-card">', unsafe_allow_html=True)
            atividades_dia = [a for a in st.session_state.db if a['data'].date() == data_relatorio]
            st.markdown(f"**📅 {data_relatorio.strftime('%d/%m/%Y')}**")
            st.markdown(f"**Atividades:** {len(atividades_dia)}")
            st.markdown(f"**XP Total:** +{sum(a['xp'] for a in atividades_dia)}")
            
            st.download_button(
                label="📥 BAIXAR RELATÓRIO HTML",
                data=relatorio,
                file_name=f"relatorio_missoes_{data_relatorio.strftime('%Y%m%d')}.html",
                mime="text/html"
            )
            st.markdown(f'</div>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Nenhuma atividade encontrada em {data_relatorio.strftime('%d/%m/%Y')}")

with col_rel2:
    st.markdown("### Exportar Dados")
    if len(st.session_state.db) > 0:
        df_export = pd.DataFrame(st.session_state.db)
        csv = df_export.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 BAIXAR CSV COMPLETO",
            data=csv,
            file_name=f"historico_completo_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.caption(f"📊 {len(st.session_state.db)} registros exportados")

st.markdown("---")

# =========================
# HISTÓRICO RECENTE
# =========================
st.markdown("## 📜 HISTÓRICO DE MISSÕES")

if len(st.session_state.db) > 0:
    df_hist = pd.DataFrame(st.session_state.db)
    df_hist = df_hist.sort_values('data', ascending=False).reset_index(drop=True)
    
    # Filtro de data
    col_filtro1, col_filtro2 = st.columns([2, 1])
    with col_filtro2:
       
