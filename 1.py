import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide"
)

# =========================
# CREDENCIAIS DE ACESSO
# =========================
USUARIO_VALIDO = "Juan"
SENHA_VALIDA = "Ju@n1990"

# =========================
# ATIVIDADES COMPLEMENTARES COM PONTOS
# =========================
ATIVIDADES_COMPLEMENTARES = {
    "📝 Post no LinkedIn": {"xp": 15, "desc": "Post técnico sobre segurança ou cibersegurança"},
    "🔗 Conexão estratégica": {"xp": 5, "desc": "Conectar com recrutador ou especialista da área"},
    "📄 Atualizar LinkedIn": {"xp": 10, "desc": "Atualizar perfil com novas conquistas"},
    "🎯 Aplicar para vaga": {"xp": 20, "desc": "Candidatar-se a uma vaga alinhada com a meta"},
    "📚 Ler artigo técnico": {"xp": 8, "desc": "Ler artigo sobre OT Security, ISO 27001, etc"},
    "🎧 Ouvir podcast técnico": {"xp": 8, "desc": "Podcast sobre cibersegurança industrial"},
    "💻 Projeto GitHub": {"xp": 25, "desc": "Publicar projeto no GitHub com documentação"},
    "📊 Dashboard Power BI": {"xp": 30, "desc": "Criar dashboard com dados reais"},
    "🤝 Networking evento": {"xp": 20, "desc": "Participar de webinar ou evento online"},
    "📝 Escrever artigo": {"xp": 35, "desc": "Artigo técnico para LinkedIn ou Medium"},
    "🎓 Webinar assistido": {"xp": 10, "desc": "Assistir webinar da área"},
    "📋 Planejamento semanal": {"xp": 10, "desc": "Planejar a semana de estudos"},
    "🏆 Certificação concluída": {"xp": 100, "desc": "Completar certificação do roadmap"},
    "📁 Portfolio atualizado": {"xp": 20, "desc": "Atualizar portfolio com novos projetos"},
    "🗣️ Inglês - 1h estudo": {"xp": 15, "desc": "Estudar inglês por 1 hora"},
    "🔬 Laboratório prático": {"xp": 25, "desc": "Laboratório de OT Security ou rede"},
}

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
    "CISA ICS 101": {"emblema": "🏭📘", "cor": "#00A4EF", "titulo": "CISA ICS 101", "xp": 80, "ano": 2026},
    "CISA ICS 201": {"emblema": "🏭📗", "cor": "#0078D4", "titulo": "CISA ICS 201", "xp": 100, "ano": 2026},
}

# =========================
# STYLE
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body {
    background: linear-gradient(135deg, #0a0e27, #1a1f3a);
    color: #4d9fff;
}

.block-container {
    padding-top: 1rem;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, #4d9fff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
}

.red-text {
    color: #ff4444 !important;
    font-weight: bold;
}

.green-text {
    color: #00ff88 !important;
}

.date-box {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
    border-radius: 15px;
    padding: 15px 25px;
    text-align: center;
    border: 1px solid rgba(77,159,255,0.3);
    margin-bottom: 20px;
}

.date-box .data {
    font-size: 28px;
    font-weight: bold;
    font-family: 'Orbitron', monospace;
}

.date-box .dia {
    font-size: 16px;
    opacity: 0.8;
}

.stButton button {
    background: linear-gradient(135deg, #4d9fff, #7b2ff7) !important;
    color: white !important;
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
}

.cert-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(77,159,255,0.2);
}

.cert-card.atrasado {
    border-left: 3px solid #ff4444;
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

.atividade-complementar {
    background: linear-gradient(135deg, rgba(255,68,68,0.08), rgba(123,47,247,0.03));
    border-radius: 10px;
    padding: 10px;
    margin: 5px;
    border-left: 3px solid #ff8800;
    text-align: center;
}

.atividade-complementar:hover {
    background: linear-gradient(135deg, rgba(255,68,68,0.15), rgba(123,47,247,0.08));
    transform: translateY(-2px);
}

.kpi-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.plano-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    border: 1px solid rgba(77,159,255,0.2);
}

.timeline-item {
    border-left: 2px solid #4d9fff;
    padding-left: 20px;
    margin: 15px 0;
    position: relative;
}

.timeline-item::before {
    content: "●";
    position: absolute;
    left: -8px;
    top: 0;
    color: #4d9fff;
    font-size: 14px;
}

.css-1d391kg, .css-12oz5g7 {
    background: linear-gradient(135deg, #0a0e27, #0d1133) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #4d9fff, #7b2ff7) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZAÇÃO DO SESSION STATE
# =========================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "db" not in st.session_state:
    st.session_state.db = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "cert_xp" not in st.session_state:
    st.session_state.cert_xp = {cert: 0 for cert in EMBLEMAS.keys()}
if "cert_status" not in st.session_state:
    st.session_state.cert_status = {cert: "Não iniciada" for cert in EMBLEMAS.keys()}
if "atividades_complementares_db" not in st.session_state:
    st.session_state.atividades_complementares_db = []

# =========================
# FUNÇÃO DE LOGIN
# =========================
def fazer_login():
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 40px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 20px; border: 1px solid rgba(77,159,255,0.3); text-align: center;">
        <h1>🚀 MISSÃO CARREIRA</h1>
        <h3>Acesso Autorizado</h3>
    </div>
    """, unsafe_allow_html=True)
    
    usuario = st.text_input("👨‍🚀 Usuário")
    senha = st.text_input("🔒 Senha", type="password")
    
    if st.button("🚀 Entrar", use_container_width=True):
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            st.session_state.autenticado = True
            st.success("✅ Acesso concedido!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos!")

# =========================
# FUNÇÕES PRINCIPAIS
# =========================
def calc_xp(atividade):
    tabela = {
        "📚 Estudo": 10, "🔬 Laboratório": 20, "🏗️ Projeto": 30,
        "🔄 Revisão": 15, "📝 Simulado": 15, "🎓 Aula Pós": 25,
        "🌎 Inglês": 15, "🏅 Certificação": 50
    }
    return tabela.get(atividade, 10)

def get_badge(status):
    if status == "Concluída":
        return "🏆"
    elif status == "Em andamento":
        return "⚡"
    return "💤"

def verificar_atraso(cert, ano):
    if ano == "Contínuo":
        return False
    if isinstance(ano, int) and datetime.now().year > ano:
        if st.session_state.cert_xp.get(cert, 0) < EMBLEMAS[cert]["xp"]:
            return True
    return False

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
    
    if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluída"
    elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"

def adicionar_atividade_complementar(nome, xp):
    st.session_state.atividades_complementares_db.append({
        "data": pd.Timestamp.now(),
        "atividade": nome,
        "xp": xp
    })
    st.session_state.xp += xp

def get_atividades_hoje():
    hoje = datetime.now().date()
    return [a for a in st.session_state.db if a['data'].date() == hoje]

def get_atividades_complementares_hoje():
    hoje = datetime.now().date()
    return [a for a in st.session_state.atividades_complementares_db if a['data'].date() == hoje]

def get_xp_semana():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    total = sum(a['xp'] for a in st.session_state.db if a['data'].date() >= inicio_semana.date())
    total += sum(a['xp'] for a in st.session_state.atividades_complementares_db if a['data'].date() >= inicio_semana.date())
    return total

def get_xp_mes():
    hoje = datetime.now()
    total = sum(a['xp'] for a in st.session_state.db if a['data'].month == hoje.month and a['data'].year == hoje.year)
    total += sum(a['xp'] for a in st.session_state.atividades_complementares_db if a['data'].month == hoje.month and a['data'].year == hoje.year)
    return total

# =========================
# VERIFICAR LOGIN
# =========================
if not st.session_state.autenticado:
    fazer_login()
    st.stop()

# =========================
# DATA ATUAL - DESTAQUE
# =========================
hoje = datetime.now()
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

st.markdown(f"""
<div class="date-box">
    <div class="dia">{dias_semana[hoje.weekday()]}</div>
    <div class="data">{hoje.day} de {meses[hoje.month-1]} de {hoje.year}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.markdown("### *Juan Felipe da Silva - Especialista em Segurança Corporativa | Infraestrutura Crítica | Cibersegurança*")
st.markdown(f"*Abril de 2026 – Junho de 2028 | Usina Hidrelétrica de Belo Monte*")
st.markdown('<p class="green-text">💾 Seu progresso é salvo automaticamente!</p>', unsafe_allow_html=True)
st.markdown("---")

# =========================
# ABAS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎮 Dashboard", "📋 Atividades", "🎖️ Certificações", "🗺️ Roadmap", "📊 Plano Estratégico"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    # KPIs principais
    c1, c2, c3, c4 = st.columns(4)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
    total_certs = len(EMBLEMAS)
    
    c1.metric("🎮 Missões", len(st.session_state.db) + len(st.session_state.atividades_complementares_db))
    c2.metric("⭐ XP Total", st.session_state.xp)
    c3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
    c4.metric("✅ Certificações", f"{concluidas}/{total_certs}")
    
    st.markdown("---")
    
    # Resumo do dia
    st.markdown("## 📊 Resumo do Dia")
    col1, col2, col3 = st.columns(3)
    
    xp_hoje = sum(a['xp'] for a in get_atividades_hoje())
    xp_hoje += sum(a['xp'] for a in get_atividades_complementares_hoje())
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 36px;">⭐</div>
            <div style="font-size: 28px; font-weight: bold;">+{xp_hoje}</div>
            <div>XP Hoje</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 36px;">📆</div>
            <div style="font-size: 28px; font-weight: bold;">+{get_xp_semana()}</div>
            <div>XP Semana</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 36px;">📅</div>
            <div style="font-size: 28px; font-weight: bold;">+{get_xp_mes()}</div>
            <div>XP Mês</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Meta diária
    meta_diaria = 50
    progresso_meta = min(xp_hoje / meta_diaria, 1.0)
    st.progress(progresso_meta)
    st.caption(f"Meta diária: {xp_hoje}/{meta_diaria} XP")

# =========================
# TAB 2 - ATIVIDADES
# =========================
with tab2:
    st.markdown("## ⚡ ATIVIDADES DO DIA")
    
    # Atividades principais
    st.markdown("### 📚 Estudos e Certificações")
    with st.form("nova_atividade", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
            atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"])
        with col2:
            obs = st.text_area("Observação")
        
        if st.form_submit_button("🚀 Lançar Missão Principal", use_container_width=True):
            xp_ganho = calc_xp(atividade)
            adicionar_atividade(area, atividade, xp_ganho, obs)
            st.success(f"+{xp_ganho} XP!", icon="🎉")
            st.rerun()
    
    st.markdown("---")
    
    # Atividades Complementares
    st.markdown("### 🎯 Atividades Complementares (PONTUAM XP)")
    st.markdown("*Realize ações estratégicas para acelerar sua carreira*")
    
    # Grid de atividades complementares
    cols = st.columns(4)
    for i, (nome, info) in enumerate(ATIVIDADES_COMPLEMENTARES.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="atividade-complementar">
                <div style="font-size: 24px;">{nome[:2]}</div>
                <div style="font-size: 12px; font-weight: bold;">{nome}</div>
                <div style="font-size: 10px; opacity: 0.8;">{info['desc'][:35]}</div>
                <div style="color: #00ff88; font-weight: bold;">⭐ +{info['xp']} XP</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✅ Realizar", key=f"comp_{i}", use_container_width=True):
                adicionar_atividade_complementar(nome, info['xp'])
                st.success(f"+{info['xp']} XP - {nome} concluída!", icon="🎉")
                st.rerun()
    
    st.markdown("---")
    
    # Lista de atividades de hoje
    st.markdown("### 📝 Atividades Registradas Hoje")
    
    atividades_hoje = get_atividades_hoje()
    complementares_hoje = get_atividades_complementares_hoje()
    
    if atividades_hoje or complementares_hoje:
        for atv in atividades_hoje:
            emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
            st.markdown(f"""
            <div class="atividade-card">
                {emblema} **{atv['area'][:30]}** | {atv['atividade']} | ⭐ +{atv['xp']}<br>
                <small>📝 {atv['obs'][:50] if atv['obs'] else '-'}</small>
            </div>
            """, unsafe_allow_html=True)
        
        for atv in complementares_hoje:
            info = ATIVIDADES_COMPLEMENTARES.get(atv['atividade'], {})
            st.markdown(f"""
            <div class="atividade-card">
                🎯 **{atv['atividade']}** | ⭐ +{atv['xp']}<br>
                <small>✅ Atividade complementar concluída</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("✨ Nenhuma atividade hoje. Comece agora!")

# =========================
# TAB 3 - CERTIFICAÇÕES
# =========================
with tab3:
    st.markdown("## 🎖️ JORNADA DAS CERTIFICAÇÕES")
    
    certs_list = list(st.session_state.cert_xp.items())
    
    for i in range(0, len(certs_list), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < len(certs_list):
                cert, xp = certs_list[idx]
                info = EMBLEMAS[cert]
                status = st.session_state.cert_status[cert]
                atrasado = verificar_atraso(cert, info.get("ano", 2030))
                progresso = min(xp / info["xp"], 1.0)
                classe = "cert-card atrasado" if atrasado else "cert-card"
                
                with cols[j]:
                    st.markdown(f"""
                    <div class="{classe}">
                        <div style="text-align: center; font-size: 32px;">{info['emblema']}</div>
                        <div style="font-weight: bold; text-align: center; font-size: 11px;">{cert[:20]}</div>
                        <div style="text-align: center; font-size: 24px;">{get_badge(status)}</div>
                        <div style="text-align: center; font-size: 10px;">{xp}/{info['xp']} XP</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(progresso)
                    
                    opcoes = ["Não iniciada", "Em andamento", "Concluída"]
                    idx_status = opcoes.index(status) if status in opcoes else 0
                    novo_status = st.selectbox("", opcoes, index=idx_status, key=f"status_{cert}", label_visibility="collapsed")
                    if novo_status != status:
                        st.session_state.cert_status[cert] = novo_status
                        st.rerun()

# =========================
# TAB 4 - ROADMAP
# =========================
with tab4:
    st.markdown("## 🗺️ ROADMAP DAS CERTIFICAÇÕES")
    
    anos = {
        2026: "🌱 2026 - Fundação",
        2027: "⚡ 2027 - Especialização",
        2028: "🎯 2028 - Maestria Técnica",
        2029: "👑 2029 - Liderança"
    }
    
    for ano, titulo in anos.items():
        with st.expander(titulo, expanded=(ano == 2026)):
            certs_ano = [c for c, d in EMBLEMAS.items() if d.get("ano") == ano]
            if certs_ano:
                cols = st.columns(min(4, len(certs_ano)))
                for i, cert in enumerate(certs_ano):
                    info = EMBLEMAS[cert]
                    status = st.session_state.cert_status[cert]
                    xp_atual = st.session_state.cert_xp[cert]
                    percent = (xp_atual / info["xp"]) * 100
                    
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; background: rgba(77,159,255,0.1); border-radius: 10px;">
                            <div style="font-size: 32px;">{info['emblema']}</div>
                            <div style="font-weight: bold; font-size: 11px;">{cert[:20]}</div>
                            <div style="font-size: 20px;">{get_badge(status)}</div>
                            <div style="font-size: 10px;">{xp_atual}/{info['xp']} XP</div>
                            <div style="background: #333; border-radius: 5px; height: 4px; margin-top: 5px;">
                                <div style="background: {info['cor']}; width: {percent}%; height: 4px; border-radius: 5px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# =========================
# TAB 5 - PLANO ESTRATÉGICO
# =========================
with tab5:
    st.markdown("## 📊 PLANO ESTRATÉGICO DE CARREIRA")
    st.markdown("### *Juan Felipe da Silva*")
    st.markdown("#### Especialista em Segurança Corporativa | Infraestrutura Crítica | Cibersegurança")
    st.markdown("*Abril de 2026 – Junho de 2028 | Usina Hidrelétrica de Belo Monte*")
    st.markdown("---")
    
    # Visão Geral
    st.markdown("### 🎯 VISÃO GERAL")
    st.markdown("""
    <div class="plano-card">
    Profissional com mais de 10 anos de experiência em segurança corporativa e infraestrutura crítica, 
    atuando na Usina Hidrelétrica de Belo Monte (11.233 MW). Este documento mapeia os passos concretos 
    para a transição de <strong>Técnico Sênior (R$ 7.500)</strong> para <strong>Especialista/Coordenador de Cibersegurança (R$ 18.000 - R$ 25.000)</strong> 
    até meados de 2028, usando a própria Norte Energia como laboratório estratégico de aprendizado e construção de portfólio.
    </div>
    """, unsafe_allow_html=True)
    
    # Projeção Salarial
    st.markdown("### 💰 PROJEÇÃO SALARIAL")
    
    salarios = [
        {"periodo": "Hoje - Abr/2026", "cargo": "Técnico Sênior", "salario": "R$ 7.500", "cor": "#4d9fff"},
        {"periodo": "Dez/2026", "cargo": "Especialista", "salario": "R$ 10-11k", "cor": "#00ff88"},
        {"periodo": "2027", "cargo": "Especialista Sênior", "salario": "R$ 13-16k", "cor": "#ffaa00"},
        {"periodo": "Saída 2028", "cargo": "Coordenador/Consultor", "salario": "R$ 18-25k", "cor": "#ff4444"}
    ]
    
    cols = st.columns(4)
    for i, s in enumerate(salarios):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, {s['cor']}20, rgba(123,47,247,0.05)); border-radius: 10px;">
                <div style="font-size: 14px; font-weight: bold;">{s['periodo']}</div>
                <div style="font-size: 18px; font-weight: bold; color: {s['cor']};">{s['salario']}</div>
                <div style="font-size: 11px;">{s['cargo']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Linha do Tempo
    st.markdown("### 📅 LINHA DO TEMPO - PASSO A PASSO")
    
    fases = [
        {"periodo": "Abr–Jun 2026", "titulo": "Decolagem — colocar tudo em movimento", "cor": "#00ff88",
         "itens": [
            "✅ CISA ICS 101 — iniciar agora (Gratuito, online)",
            "✅ Iniciar estudo Security+ SY0-701 (10h/semana)",
            "✅ Pós PUC Minas em andamento",
            "✅ LinkedIn e currículo atualizados",
            "✅ Projeto 1 — Dashboard KPIs de segurança"
         ]},
        {"periodo": "Jul–Set 2026", "titulo": "Construção — projetos e base técnica", "cor": "#4d9fff",
         "itens": [
            "✅ CISA ICS 201 + Security+ intensivo",
            "✅ Python intermediário (Pandas, Matplotlib)",
            "✅ Projeto 2 — Automação de relatórios",
            "✅ GitHub ativo com projetos reais"
         ]},
        {"periodo": "Out–Dez 2026", "titulo": "Primeira grande conquista", "cor": "#ffaa00",
         "itens": [
            "🎯 Aprovação CompTIA Security+",
            "✅ IAM + Resposta a Incidentes (Pós)",
            "✅ SQL avançado + Power BI publicado",
            "✅ Proposta formal de reajuste interno (R$ 10-11k)"
         ]},
        {"periodo": "Jan–Jun 2027", "titulo": "Profundidade OT — o salto para especialista", "cor": "#ff8800",
         "itens": [
            "🎯 ISO 27001 Lead Implementer",
            "🎯 ISA/IEC 62443 Cybersecurity Specialist",
            "✅ Criptografia + DevSecOps + Ethical Hacking",
            "✅ Projeto 3 — Política TI/OT convergida"
         ]},
        {"periodo": "Jul–Dez 2027", "titulo": "Consolidação — especialista reconhecido", "cor": "#ff4444",
         "itens": [
            "
