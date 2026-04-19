import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

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
    "📝 Post no LinkedIn": {"xp": 15, "desc": "Post técnico sobre segurança"},
    "🔗 Conexão estratégica": {"xp": 5, "desc": "Conectar com recrutador"},
    "📄 Atualizar LinkedIn": {"xp": 10, "desc": "Atualizar perfil"},
    "🎯 Aplicar para vaga": {"xp": 20, "desc": "Candidatar-se a vaga"},
    "📚 Ler artigo técnico": {"xp": 8, "desc": "Artigo sobre OT Security"},
    "🎧 Ouvir podcast técnico": {"xp": 8, "desc": "Podcast cibersegurança"},
    "💻 Projeto GitHub": {"xp": 25, "desc": "Publicar projeto no GitHub"},
    "📊 Dashboard Power BI": {"xp": 30, "desc": "Criar dashboard"},
    "🤝 Networking evento": {"xp": 20, "desc": "Participar de webinar"},
    "📝 Escrever artigo": {"xp": 35, "desc": "Artigo técnico"},
    "🎓 Webinar assistido": {"xp": 10, "desc": "Assistir webinar"},
    "📋 Planejamento semanal": {"xp": 10, "desc": "Planejar semana"},
    "🏆 Certificação concluída": {"xp": 100, "desc": "Completar certificação"},
    "📁 Portfólio atualizado": {"xp": 20, "desc": "Atualizar portfólio"},
    "🗣️ Inglês - 1h estudo": {"xp": 15, "desc": "Estudar inglês"},
    "🔬 Laboratório prático": {"xp": 25, "desc": "Lab OT Security"},
    "📖 CISA ICS Module": {"xp": 30, "desc": "Completar módulo CISA"},
    "🎯 Simulado Security+": {"xp": 20, "desc": "Fazer simulado"}
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
    "CISA ICS 201": {"emblema": "🏭📗", "cor": "#0078D4", "titulo": "CISA ICS 201", "xp": 100, "ano": 2026}
}

# =========================
# STYLE
# =========================
st.markdown("""
<style>
html, body {
    background: linear-gradient(135deg, #0a0e27, #1a1f3a);
    color: #4d9fff;
}
h1, h2, h3 {
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
.stButton button {
    background: linear-gradient(135deg, #4d9fff, #7b2ff7) !important;
    color: white !important;
    border-radius: 10px;
}
.cert-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 12px;
    padding: 10px;
    margin: 5px;
    border: 1px solid rgba(77,159,255,0.3);
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
}
.atividade-complementar {
    background: linear-gradient(135deg, rgba(255,68,68,0.08), rgba(123,47,247,0.03));
    border-radius: 10px;
    padding: 10px;
    margin: 5px;
    border-left: 3px solid #ff8800;
    text-align: center;
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
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
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
# FUNÇÕES
# =========================
def calc_xp(atividade):
    tabela = {"📚 Estudo": 10, "🔬 Laboratório": 20, "🏗️ Projeto": 30, "🔄 Revisão": 15, "📝 Simulado": 15, "🎓 Aula Pós": 25, "🌎 Inglês": 15, "🏅 Certificação": 50}
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
    st.session_state.db.append({"data": pd.Timestamp.now(), "area": area, "atividade": atividade, "xp": xp, "obs": obs})
    st.session_state.xp += xp
    st.session_state.cert_xp[area] += xp
    if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluída"
    elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"

def adicionar_atividade_complementar(nome, xp):
    st.session_state.atividades_complementares_db.append({"data": pd.Timestamp.now(), "atividade": nome, "xp": xp})
    st.session_state.xp += xp

def get_atividades_hoje():
    hoje = datetime.now().date()
    return [a for a in st.session_state.db if a['data'].date() == hoje]

def get_complementares_hoje():
    hoje = datetime.now().date()
    return [a for a in st.session_state.atividades_complementares_db if a['data'].date() == hoje]

def get_xp_semana():
    hoje = datetime.now()
    inicio = hoje - timedelta(days=hoje.weekday())
    total = sum(a['xp'] for a in st.session_state.db if a['data'].date() >= inicio.date())
    total += sum(a['xp'] for a in st.session_state.atividades_complementares_db if a['data'].date() >= inicio.date())
    return total

def get_xp_mes():
    hoje = datetime.now()
    total = sum(a['xp'] for a in st.session_state.db if a['data'].month == hoje.month)
    total += sum(a['xp'] for a in st.session_state.atividades_complementares_db if a['data'].month == hoje.month)
    return total

def fazer_login():
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 40px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 20px; text-align: center;">
        <h1>🚀 MISSÃO CARREIRA</h1>
    </div>
    """, unsafe_allow_html=True)
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar", use_container_width=True):
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Credenciais inválidas!")

# =========================
# LOGIN
# =========================
if not st.session_state.autenticado:
    fazer_login()
    st.stop()

# =========================
# DATA ATUAL
# =========================
hoje = datetime.now()
st.markdown(f"""
<div class="date-box">
    <div class="data">{hoje.day} de {hoje.strftime('%B')} de {hoje.year}</div>
    <div>{hoje.strftime('%A')}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.markdown("### Juan Felipe da Silva")
st.markdown("---")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📋 Atividades", "🎖️ Certificações", "🗺️ Roadmap", "📅 Plano Estratégico"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
    c1.metric("Missões", len(st.session_state.db) + len(st.session_state.atividades_complementares_db))
    c2.metric("XP Total", st.session_state.xp)
    c3.metric("Nível", st.session_state.xp // 100 + 1)
    c4.metric("Certificações", f"{concluidas}/{len(EMBLEMAS)}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    xp_hoje = sum(a['xp'] for a in get_atividades_hoje()) + sum(a['xp'] for a in get_complementares_hoje())
    col1.metric("XP Hoje", f"+{xp_hoje}")
    col2.metric("XP Semana", f"+{get_xp_semana()}")
    col3.metric("XP Mês", f"+{get_xp_mes()}")
    
    meta = 50
    st.progress(min(xp_hoje / meta, 1.0))
    st.caption(f"Meta diária: {xp_hoje}/{meta} XP")

# =========================
# TAB 2 - ATIVIDADES
# =========================
with tab2:
    st.markdown("## Atividades do Dia")
    
    with st.form("nova_atividade", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
            atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"])
        with col2:
            obs = st.text_area("Observação")
        if st.form_submit_button("Lançar Missão", use_container_width=True):
            adicionar_atividade(area, atividade, calc_xp(atividade), obs)
            st.success("Missão concluída!")
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Atividades Complementares")
    
    cols = st.columns(4)
    for i, (nome, info) in enumerate(ATIVIDADES_COMPLEMENTARES.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="atividade-complementar">
                <div style="font-size: 20px;">{nome[:15]}</div>
                <div style="color: #00ff88;">⭐ +{info['xp']} XP</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Fazer", key=f"comp_{i}"):
                adicionar_atividade_complementar(nome, info['xp'])
                st.rerun()
    
    st.markdown("---")
    st.markdown("### Registro de Hoje")
    for atv in get_atividades_hoje():
        st.markdown(f"📌 {EMBLEMAS[atv['area']]['emblema']} **{atv['area']}** - {atv['atividade']} ⭐+{atv['xp']}")
    for atv in get_complementares_hoje():
        st.markdown(f"🎯 **{atv['atividade']}** ⭐+{atv['xp']}")

# =========================
# TAB 3 - CERTIFICAÇÕES
# =========================
with tab3:
    st.markdown("## Certificações")
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
                classe = "cert-card atrasado" if atrasado else "cert-card"
                with cols[j]:
                    st.markdown(f"""
                    <div class="{classe}">
                        <div style="text-align:center; font-size:32px;">{info['emblema']}</div>
                        <div style="text-align:center; font-weight:bold; font-size:11px;">{cert[:20]}</div>
                        <div style="text-align:center; font-size:24px;">{get_badge(status)}</div>
                        <div style="text-align:center; font-size:10px;">{xp}/{info['xp']} XP</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(min(xp / info["xp"], 1.0))
                    opcoes = ["Não iniciada", "Em andamento", "Concluída"]
                    novo = st.selectbox("", opcoes, index=opcoes.index(status), key=f"status_{cert}", label_visibility="collapsed")
                    if novo != status:
                        st.session_state.cert_status[cert] = novo
                        st.rerun()

# =========================
# TAB 4 - ROADMAP
# =========================
with tab4:
    st.markdown("## Roadmap 2026-2029")
    
    with st.expander("🌱 2026 - Fundação", expanded=True):
        certs = ["CISA ICS 101", "CISA ICS 201", "Security+", "AZ-900", "SC-900", "Python", "SQL", "Power BI"]
        cols = st.columns(4)
        for i, cert in enumerate(certs):
            if cert in EMBLEMAS:
                info = EMBLEMAS[cert]
                with cols[i % 4]:
                    st.markdown(f"{info['emblema']} {cert}")
    
    with st.expander("⚡ 2027 - Especialização"):
        certs = ["ISO 27001 Auditor", "ISO 27001 Implementer", "IEC 62443", "CySA+"]
        cols = st.columns(4)
        for i, cert in enumerate(certs):
            if cert in EMBLEMAS:
                info = EMBLEMAS[cert]
                with cols[i % 4]:
                    st.markdown(f"{info['emblema']} {cert}")
    
    with st.expander("🎯 2028 - Maestria"):
        certs = ["MITRE ATT&CK ICS", "GICSP", "Cloud Security"]
        cols = st.columns(3)
        for i, cert in enumerate(certs):
            if cert in EMBLEMAS:
                info = EMBLEMAS[cert]
                with cols[i]:
                    st.markdown(f"{info['emblema']} {cert}")
    
    with st.expander("👑 2029 - Liderança"):
        certs = ["CISSP", "DevSecOps"]
        cols = st.columns(2)
        for i, cert in enumerate(certs):
            if cert in EMBLEMAS:
                info = EMBLEMAS[cert]
                with cols[i]:
                    st.markdown(f"{info['emblema']} {cert}")

# =========================
# TAB 5 - PLANO ESTRATÉGICO
# =========================
with tab5:
    st.markdown("## Plano Estratégico de Carreira")
    st.markdown("### Juan Felipe da Silva")
    st.markdown("#### Especialista em Segurança Corporativa | Infraestrutura Crítica | Cibersegurança")
    st.markdown("---")
    
    st.markdown("### Projeção Salarial")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hoje", "R$ 7.500", "Técnico Sênior")
    col2.metric("Dez/2026", "R$ 10-11k", "Com Security+")
    col3.metric("2027", "R$ 13-16k", "Especialista")
    col4.metric("2028", "R$ 18-25k", "Coordenador")
    
    st.markdown("---")
    st.markdown("### Linha do Tempo")
    
    etapas = [
        ("Abr-Jun 2026", "DECOLAGEM", "Concluir CISA ICS 101/201 | Iniciar Security+ | Projeto Dashboard Power BI"),
        ("Jul-Set 2026", "CONSTRUÇÃO", "Simulados Security+ | Python | Automação de relatórios | GitHub"),
        ("Out-Dez 2026", "CONQUISTA", "APROVAÇÃO Security+ | Reajuste interno R$ 10-11k"),
        ("Jan-Jun 2027", "OT SECURITY", "ISO 27001 Lead Implementer | IEC 62443 | Política TI/OT"),
        ("Jul-Dez 2027", "CONSOLIDAÇÃO", "GICSP | Projetos avançados | Portfólio completo"),
        ("Jan-Jun 2028", "SAÍDA", "CISSP início | Aplicar para vagas R$ 18-25k")
    ]
    
    for periodo, titulo, desc in etapas:
        st.markdown(f"""
        <div class="timeline-item">
            <strong style="color: #00ff88;">{periodo}</strong><br>
            <strong>{titulo}</strong><br>
            <small>{desc}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Cargos-Alvo")
    
    cargos = [
        ("Analista de Segurança OT", "R$ 12-16k", "2026"),
        ("Especialista em Infraestrutura Crítica", "R$ 15-20k", "2027"),
        ("Coordenador de Cibersegurança", "R$ 18-25k", "2028"),
        ("Consultor TI/OT", "R$ 20-30k PJ", "2028")
    ]
    
    for cargo, salario, ano in cargos:
        st.markdown(f"- **{cargo}** - {salario} ({ano})")
    
    st.markdown("---")
    st.markdown('<p style="text-align:center;">🚀 Continue sua jornada, o universo te espera!</p>', unsafe_allow_html=True)
