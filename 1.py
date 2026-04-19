import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json
import os

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
# SOFT SKILLS - ATIVIDADES PRÁTICAS
# =========================
SOFT_SKILLS_ATIVIDADES = {
    "Comunicacao e Apresentacao": {
        "descricao": "Capacidade de transmitir ideias claramente, fazer apresentacoes impactantes.",
        "atividades": [
            {"nome": "Apresentacao Tecnica", "descricao": "Apresentar um projeto para sua equipe", "xp": 30},
            {"nome": "Escrever Documentacao", "descricao": "Documentar um procedimento ou projeto", "xp": 20},
            {"nome": "Pitch de Ideia", "descricao": "Apresentar melhoria para a lideranca", "xp": 40},
            {"nome": "Dashboard para Gestao", "descricao": "Criar relatorio visual para tomada de decisao", "xp": 35}
        ]
    },
    "Lideranca de Equipes": {
        "descricao": "Capacidade de motivar, orientar e coordenar pessoas.",
        "atividades": [
            {"nome": "Mentorar Colega", "descricao": "Ensinar um processo ou tecnologia", "xp": 35},
            {"nome": "Liderar Reuniao", "descricao": "Conduzir uma reuniao de equipe", "xp": 30},
            {"nome": "Definir Metas", "descricao": "Estabelecer objetivos claros para a equipe", "xp": 40},
            {"nome": "Resolver Conflito", "descricao": "Mediar situacao de conflito", "xp": 50}
        ]
    },
    "Gestao de Projetos": {
        "descricao": "Planejar, executar e monitorar projetos.",
        "atividades": [
            {"nome": "Planejar Projeto", "descricao": "Criar cronograma com marcos", "xp": 40},
            {"nome": "Relatorio de Status", "descricao": "Produzir relatorio de progresso", "xp": 30},
            {"nome": "Gestao de Risco", "descricao": "Identificar e mitigar riscos", "xp": 45},
            {"nome": "Encerrar Projeto", "descricao": "Documentar licoes aprendidas", "xp": 60}
        ]
    },
    "Inteligencia Emocional": {
        "descricao": "Capacidade de reconhecer e gerenciar emocoes.",
        "atividades": [
            {"nome": "Gerenciar Estresse", "descricao": "Aplicar tecnica de respiracao", "xp": 20},
            {"nome": "Escuta Ativa", "descricao": "Praticar ouvir sem interromper", "xp": 25},
            {"nome": "Feedback Construtivo", "descricao": "Dar feedback usando tecnica SBI", "xp": 35},
            {"nome": "Reconhecer Erro", "descricao": "Admitir erro e pedir desculpas", "xp": 30}
        ]
    }
}

# =========================
# CONTEUDO DAS CERTIFICACOES
# =========================
CONTEUDO_CERTIFICACOES = {
    "AZ-900": {
        "titulo": "Microsoft Azure Fundamentals",
        "descricao": "Certificacao de entrada para Azure. Valida conhecimentos basicos de cloud.",
        "dominios": [
            {"nome": "Conceitos de nuvem", "topicos": ["Beneficios da nuvem", "Modelos de servico", "Modelos de implantacao", "CAPEX vs OPEX"]},
            {"nome": "Servicos principais", "topicos": ["Computacao", "Redes", "Armazenamento", "Banco de dados"]},
            {"nome": "Solucoes de seguranca", "topicos": ["Seguranca de rede", "Identidade", "Protecao de dados", "Conformidade"]}
        ],
        "recursos": ["Microsoft Learn", "YouTube - John Savill", "GitHub"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "Udemy"],
        "semanas": 3, "horas": 30, "custo": "$99", "voucher": True
    },
    "SC-900": {
        "titulo": "Microsoft Security, Compliance and Identity",
        "descricao": "Certificacao sobre seguranca, compliance e identidade.",
        "dominios": [
            {"nome": "Conceitos de seguranca", "topicos": ["Zero Trust", "Defesa em profundidade", "Criptografia"]},
            {"nome": "Capacidades de identidade", "topicos": ["Azure AD", "MFA", "Identity Protection", "PIM"]},
            {"nome": "Capacidades de seguranca", "topicos": ["Defender para nuvem", "Sentinel", "Defender endpoint"]}
        ],
        "recursos": ["Microsoft Learn", "YouTube - John Savill"],
        "simulados": ["Microsoft Assessment", "ExamTopics"],
        "semanas": 2, "horas": 25, "custo": "$99", "voucher": True
    },
    "AWS Cloud Practitioner": {
        "titulo": "AWS Cloud Practitioner",
        "descricao": "Certificacao fundamental da AWS.",
        "dominios": [
            {"nome": "Conceitos de nuvem", "topicos": ["Beneficios AWS", "Modelos de implantacao", "Infraestrutura global"]},
            {"nome": "Servicos principais", "topicos": ["EC2", "S3", "RDS", "VPC"]},
            {"nome": "Seguranca", "topicos": ["Responsabilidade compartilhada", "IAM", "Shield", "WAF"]}
        ],
        "recursos": ["AWS Skill Builder", "YouTube - Stephane Maarek", "AWS Free Tier"],
        "simulados": ["AWS Official Practice", "TutorialsDojo", "Udemy"],
        "semanas": 4, "horas": 30, "custo": "$100", "voucher": True
    },
    "Security+": {
        "titulo": "CompTIA Security+",
        "descricao": "Certificacao fundamental de ciberseguranca.",
        "dominios": [
            {"nome": "Ameacas e Ataques", "topicos": ["Malware", "Ataques de rede", "Ataques de aplicacao", "Vulnerabilidades"]},
            {"nome": "Tecnologias de Seguranca", "topicos": ["Firewalls", "IDS/IPS", "SIEM", "Criptografia"]},
            {"nome": "Arquitetura e Design", "topicos": ["Zero Trust", "Defesa em profundidade", "Seguranca em nuvem"]},
            {"nome": "Gestao de Acesso", "topicos": ["IAM", "SSO", "RBAC", "Autenticacao"]}
        ],
        "recursos": ["YouTube - Professor Messer", "CompTIA Objectives", "GitHub"],
        "simulados": ["ExamCompass", "Professor Messer", "Jason Dion", "MeasureUp"],
        "semanas": 10, "horas": 80, "custo": "$392", "voucher": False
    },
    "Scrum Fundamentals": {
        "titulo": "Scrum Fundamentals Certified",
        "descricao": "Certificacao basica de Scrum.",
        "dominios": [
            {"nome": "Fundamentos", "topicos": ["Manifesto Agil", "Principios ageis", "Scrum vs Waterfall"]},
            {"nome": "Papeis do Scrum", "topicos": ["Product Owner", "Scrum Master", "Development Team"]},
            {"nome": "Eventos", "topicos": ["Sprint Planning", "Daily Scrum", "Review", "Retrospective"]}
        ],
        "recursos": ["Scrum Guide", "YouTube - Scrum Framework", "Scrum.org"],
        "simulados": ["Scrum.org Assessment", "ScrumStudy", "Udemy"],
        "semanas": 1, "horas": 16, "custo": "R$ 500", "voucher": False
    },
    "Power BI": {
        "titulo": "Microsoft Power BI Data Analyst",
        "descricao": "Certificacao para analise e visualizacao de dados.",
        "dominios": [
            {"nome": "Preparacao de Dados", "topicos": ["Power Query", "Limpeza de dados", "Combinacao de tabelas"]},
            {"nome": "Modelagem de Dados", "topicos": ["Modelos star", "Relacionamentos", "DAX"]},
            {"nome": "Visualizacao", "topicos": ["Graficos", "Dashboards", "Drill-through"]}
        ],
        "recursos": ["Hashtag Treinamentos", "Microsoft Learn", "YouTube - SQLBI"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "MeasureUp"],
        "semanas": 6, "horas": 50, "custo": "$99", "voucher": False
    },
    "Python": {
        "titulo": "Python para Analise de Dados",
        "descricao": "Linguagem Python aplicada a automacao e analise.",
        "dominios": [
            {"nome": "Fundamentos", "topicos": ["Sintaxe", "Estruturas de controle", "Funcoes", "Listas e dicionarios"]},
            {"nome": "Manipulacao de Dados", "topicos": ["Pandas", "Leitura de arquivos", "Filtros", "Tratamento de nulos"]},
            {"nome": "Visualizacao", "topicos": ["Matplotlib", "Seaborn", "Plotly"]}
        ],
        "recursos": ["Hashtag Treinamentos", "Curso em Video", "DataCamp"],
        "simulados": ["HackerRank", "LeetCode", "Python Institute"],
        "semanas": 8, "horas": 60, "custo": "R$ 650", "voucher": False
    },
    "SQL": {
        "titulo": "SQL para Analise de Dados",
        "descricao": "Linguagem SQL para consultas e manipulacao.",
        "dominios": [
            {"nome": "Consultas Basicas", "topicos": ["SELECT", "WHERE", "ORDER BY", "Funcoes de agregacao"]},
            {"nome": "Joins", "topicos": ["INNER JOIN", "LEFT JOIN", "Self JOIN", "Subconsultas"]},
            {"nome": "Manipulacao", "topicos": ["INSERT", "UPDATE", "DELETE", "CREATE TABLE"]}
        ],
        "recursos": ["Hashtag Treinamentos", "SQLZoo", "Mode Analytics"],
        "simulados": ["HackerRank SQL", "LeetCode Database", "StrataScratch"],
        "semanas": 6, "horas": 45, "custo": "R$ 650", "voucher": False
    }
}

# =========================
# EMBLEMAS DAS CERTIFICACOES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026},
    "AWS Cloud Practitioner": {"emblema": "☁️📘", "cor": "#FF9900", "titulo": "AWS Cloud", "xp": 100, "ano": 2027},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027},
    "Scrum Fundamentals": {"emblema": "🔄📋", "cor": "#0A5C4A", "titulo": "Scrum", "xp": 60, "ano": 2026},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pos-graduacao", "xp": 300, "ano": 2026},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Ingles", "xp": 250, "ano": "Continuo"}
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
.red-text { color: #ff4444 !important; font-weight: bold; }
.green-text { color: #00ff88 !important; }
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
.cert-card.atrasado { border-left: 3px solid #ff4444; }
.atividade-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.08), rgba(123,47,247,0.03));
    border-radius: 10px;
    padding: 10px;
    margin: 5px 0;
    border-left: 3px solid #4d9fff;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}
.soft-card {
    background: linear-gradient(135deg, rgba(255,68,68,0.1), rgba(123,47,247,0.05));
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border-left: 3px solid #ff8800;
}
.dominio-header {
    background: rgba(77,159,255,0.15);
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0 5px 0;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZACAO DO SESSION STATE
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
    st.session_state.cert_status = {cert: "Nao iniciada" for cert in EMBLEMAS.keys()}
if "soft_skills_concluidas" not in st.session_state:
    st.session_state.soft_skills_concluidas = {}
if "cert_topicos_concluidos" not in st.session_state:
    st.session_state.cert_topicos_concluidos = {}

# =========================
# FUNCOES DE BACKUP
# =========================
ARQUIVO_BACKUP = "backup_diario.json"

def salvar_backup():
    dados = {
        "db": st.session_state.db,
        "xp": st.session_state.xp,
        "cert_xp": st.session_state.cert_xp,
        "cert_status": st.session_state.cert_status,
        "soft_skills_concluidas": st.session_state.soft_skills_concluidas,
        "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos,
        "data_backup": datetime.now().isoformat()
    }
    with open(ARQUIVO_BACKUP, "w") as f:
        json.dump(dados, f, default=str)
    return True

def carregar_backup():
    if os.path.exists(ARQUIVO_BACKUP):
        with open(ARQUIVO_BACKUP, "r") as f:
            dados = json.load(f)
            st.session_state.db = dados.get("db", [])
            st.session_state.xp = dados.get("xp", 0)
            st.session_state.cert_xp = dados.get("cert_xp", st.session_state.cert_xp)
            st.session_state.cert_status = dados.get("cert_status", st.session_state.cert_status)
            st.session_state.soft_skills_concluidas = dados.get("soft_skills_concluidas", {})
            st.session_state.cert_topicos_concluidos = dados.get("cert_topicos_concluidos", {})
            return True
    return False

# =========================
# FUNCOES PRINCIPAIS
# =========================
def calc_xp(atividade):
    tabela = {
        "Estudo": 10, "Laboratorio": 20, "Projeto": 30,
        "Revisao": 15, "Simulado": 15, "Aula Pos": 25,
        "Ingles": 15, "Certificacao": 50
    }
    return tabela.get(atividade, 10)

def get_badge(status):
    if status == "Concluida":
        return "🏆"
    elif status == "Em andamento":
        return "⚡"
    return "💤"

def verificar_atraso(cert, ano):
    if ano == "Continuo":
        return False
    if isinstance(ano, int) and datetime.now().year > ano:
        if st.session_state.cert_xp.get(cert, 0) < EMBLEMAS[cert]["xp"]:
            return True
    return False

def adicionar_atividade(area, atividade, xp, obs):
    st.session_state.db.append({
        "data": datetime.now().isoformat(),
        "area": area,
        "atividade": atividade,
        "xp": xp,
        "obs": obs
    })
    st.session_state.xp += xp
    st.session_state.cert_xp[area] += xp
    if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluida"
    elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"
    salvar_backup()

def adicionar_soft_skill(categoria, atividade, xp):
    key = f"{categoria}_{atividade}"
    if key not in st.session_state.soft_skills_concluidas:
        st.session_state.soft_skills_concluidas[key] = True
        st.session_state.xp += xp
        salvar_backup()
        return True
    return False

def marcar_topico_certificacao(cert, dominio, topico, concluido):
    key = f"{cert}_{dominio}_{topico}"
    if concluido and key not in st.session_state.cert_topicos_concluidos:
        st.session_state.cert_topicos_concluidos[key] = True
        st.session_state.xp += 3
        salvar_backup()
    elif not concluido and key in st.session_state.cert_topicos_concluidos:
        del st.session_state.cert_topicos_concluidos[key]
        st.session_state.xp -= 3
        salvar_backup()

def get_atividades_hoje():
    hoje = datetime.now().date()
    resultado = []
    for a in st.session_state.db:
        try:
            if isinstance(a['data'], str):
                data_atv = datetime.fromisoformat(a['data']).date()
            else:
                data_atv = a['data'].date()
            if data_atv == hoje:
                resultado.append(a)
        except:
            pass
    return resultado

def get_xp_semana():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    total = 0
    for a in st.session_state.db:
        try:
            if isinstance(a['data'], str):
                data_atv = datetime.fromisoformat(a['data'])
            else:
                data_atv = a['data']
            if data_atv.date() >= inicio_semana.date():
                total += a['xp']
        except:
            pass
    return total

def get_xp_mes():
    hoje = datetime.now()
    total = 0
    for a in st.session_state.db:
        try:
            if isinstance(a['data'], str):
                data_atv = datetime.fromisoformat(a['data'])
            else:
                data_atv = a['data']
            if data_atv.month == hoje.month and data_atv.year == hoje.year:
                total += a['xp']
        except:
            pass
    return total

# =========================
# FUNCAO DE LOGIN
# =========================
def fazer_login():
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 40px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 20px; text-align: center;">
        <h1>🚀 MISSAO CARREIRA</h1>
        <h3>Acesso Autorizado</h3>
    </div>
    """, unsafe_allow_html=True)
    usuario = st.text_input("Usuario")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar", use_container_width=True):
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Credenciais invalidas!")

# =========================
# CARREGAR DADOS E VERIFICAR LOGIN
# =========================
carregar_backup()
if not st.session_state.autenticado:
    fazer_login()
    st.stop()

# =========================
# DATA ATUAL E HEADER
# =========================
hoje = datetime.now()
st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08)); border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px;">
    <div style="font-size: 28px; font-weight: bold;">{hoje.strftime('%d/%m/%Y')}</div>
    <div>{hoje.strftime('%A')}</div>
</div>
""", unsafe_allow_html=True)

st.title("🚀 MISSAO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Ciberseguranca")
st.markdown('<p class="green-text">💾 Seu progresso e salvo automaticamente!</p>', unsafe_allow_html=True)
st.markdown("---")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 NAVE")
    st.markdown(f"**Usuario:** Juan Felipe")
    st.markdown(f"**XP:** {st.session_state.xp}")
    st.markdown(f"**Nivel:** {st.session_state.xp // 100 + 1}")
    st.markdown(f"**Missoes:** {len(st.session_state.db)}")
    st.markdown("---")
    
    atrasadas = [c for c, d in EMBLEMAS.items() if verificar_atraso(c, d.get("ano", 2030))]
    if atrasadas:
        st.markdown('<p class="red-text">⚠️ Atrasadas:</p>', unsafe_allow_html=True)
        for c in atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[c]["emblema"]} {c[:15]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    atividades_hoje = get_atividades_hoje()
    xp_hoje = sum(a['xp'] for a in atividades_hoje)
    st.markdown(f"**Hoje:** {len(atividades_hoje)} atividades | +{xp_hoje} XP")
    st.markdown(f"**Semana:** +{get_xp_semana()} XP")
    st.markdown(f"**Mes:** +{get_xp_mes()} XP")
    st.markdown("---")
    
    if st.button("Backup Manual", use_container_width=True):
        salvar_backup()
        st.success("Backup salvo!")
    st.markdown("---")
    if st.button("Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Certificacoes", "Soft Skills", "Progresso", "Roadmap"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    st.markdown("## Atividades de Hoje")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        with st.form("nova_atividade", clear_on_submit=True):
            area = st.selectbox("Certificacao", list(EMBLEMAS.keys()))
            atividade = st.selectbox("Tipo", ["Estudo", "Laboratorio", "Projeto", "Revisao", "Simulado", "Aula Pos", "Ingles", "Certificacao"])
            obs = st.text_area("Observacao")
            if st.form_submit_button("Lancar", use_container_width=True):
                xp_ganho = calc_xp(atividade)
                adicionar_atividade(area, atividade, xp_ganho, obs)
                st.success(f"+{xp_ganho} XP!", icon="🎉")
                st.rerun()
    
    with col2:
        st.markdown(f'<div class="kpi-card"><div style="font-size:36px;">⭐</div><div style="font-size:28px;">+{xp_hoje}</div><div>XP hoje</div></div>', unsafe_allow_html=True)
    
    with col3:
        meta = 50
        progresso = min(xp_hoje / meta, 1.0)
        st.markdown(f'<div class="kpi-card"><div style="font-size:36px;">🎯</div><div style="font-size:28px;">{xp_hoje}/{meta}</div><div>Meta</div></div>', unsafe_allow_html=True)
        st.progress(progresso)
    
    if atividades_hoje:
        for atv in atividades_hoje:
            emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
            st.markdown(f'<div class="atividade-card">{emblema} **{atv["area"][:30]}** | {atv["atividade"]} | ⭐ +{atv["xp"]}<br><small>📝 {atv["obs"][:50] if atv["obs"] else "-"}</small></div>', unsafe_allow_html=True)
    else:
        st.info("Nenhuma atividade hoje. Comece agora!")
    
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
    c1.metric("Missoes", len(st.session_state.db))
    c2.metric("XP", st.session_state.xp)
    c3.metric("Nivel", st.session_state.xp // 100 + 1)
    c4.metric("Certificacoes", f"{concluidas}/{len(EMBLEMAS)}")
    c5.metric("Progresso", f"{(concluidas/len(EMBLEMAS)*100):.0f}%")

# =========================
# TAB 2 - CERTIFICACOES
# =========================
with tab2:
    st.markdown("## Plano de Estudos por Certificacao")
    cert_selecionada = st.selectbox("Selecione a certificacao", list(CONTEUDO_CERTIFICACOES.keys()))
    
    if cert_selecionada in CONTEUDO_CERTIFICACOES:
        info = CONTEUDO_CERTIFICACOES[cert_selecionada]
        emblema = EMBLEMAS.get(cert_selecionada, {}).get('emblema', '📌')
        
        st.markdown(f"""
        <div class="cert-card">
            <h2>{emblema} {cert_selecionada}</h2>
            <h3>{info['titulo']}</h3>
            <p>{info['descricao']}</p>
            <p><strong>Duracao:</strong> {info['semanas']} semanas ({info['horas']} horas)</p>
            <p><strong>Custo:</strong> {info['custo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        sub_tab1, sub_tab2 = st.tabs(["Dominios e Topicoss", "Recursos e Simulados"])
        
        with sub_tab1:
            for dominio in info['dominios']:
                st.markdown(f'<div class="dominio-header">📌 {dominio["nome"]}</div>', unsafe_allow_html=True)
                for topico in dominio['topicos']:
                    key = f"{cert_selecionada}_{dominio['nome']}_{topico}"
                    concluido = key in st.session_state.cert_topicos_concluidos
                    if st.checkbox(f"📖 {topico}", value=concluido, key=key):
                        if not concluido:
                            marcar_topico_certificacao(cert_selecionada, dominio['nome'], topico, True)
                            st.rerun()
                    else:
                        if concluido:
                            marcar_topico_certificacao(cert_selecionada, dominio['nome'], topico, False)
                            st.rerun()
        
        with sub_tab2:
            st.markdown("### Recursos")
            for recurso in info['recursos']:
                st.markdown(f"- {recurso}")
            st.markdown("### Simulados")
            for simulado in info['simulados']:
                st.markdown(f"- {simulado}")

# =========================
# TAB 3 - SOFT SKILLS
# =========================
with tab3:
    st.markdown("## Desenvolvimento de Soft Skills")
    
    for categoria, info in SOFT_SKILLS_ATIVIDADES.items():
        with st.expander(f"📌 {categoria}", expanded=False):
            st.markdown(f"*{info['descricao']}*")
            st.markdown("---")
            cols = st.columns(2)
            for i, atividade in enumerate(info['atividades']):
                with cols[i % 2]:
                    key = f"soft_{categoria}_{atividade['nome']}"
                    if st.button(f"✅ {atividade['nome']} (+{atividade['xp']} XP)", key=key, use_container_width=True):
                        if adicionar_soft_skill(categoria, atividade['nome'], atividade['xp']):
                            st.success(f"+{atividade['xp']} XP - {atividade['nome']} concluida!")
                            st.rerun()
                        else:
                            st.info("Voce ja concluiu esta atividade!")
                    st.caption(f"📝 {atividade['descricao']}")

# =========================
# TAB 4 - PROGRESSO
# =========================
with tab4:
    st.markdown("## Progresso das Certificacoes")
    filtro = st.selectbox("Filtrar", ["Todas", "Em andamento", "Concluida", "Nao iniciada"])
    
    certs_list = list(st.session_state.cert_xp.items())
    for i in range(0, len(certs_list), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < len(certs_list):
                cert, xp = certs_list[idx]
                info = EMBLEMAS[cert]
                status = st.session_state.cert_status[cert]
                if filtro != "Todas" and status != filtro:
                    continue
                atrasado = verificar_atraso(cert, info.get("ano", 2030))
                progresso = min(xp / info["xp"], 1.0) if info["xp"] > 0 else 0
                classe = "cert-card atrasado" if atrasado else "cert-card"
                with cols[j]:
                    st.markdown(f'<div class="{classe}"><div style="text-align:center; font-size:32px;">{info["emblema"]}</div><div style="font-weight:bold; text-align:center; font-size:11px;">{cert[:20]}</div><div style="text-align:center; font-size:24px;">{get_badge(status)}</div><div style="text-align:center; font-size:10px;">{xp}/{info["xp"]} XP</div></div>', unsafe_allow_html=True)
                    st.progress(progresso)
                    opcoes = ["Nao iniciada", "Em andamento", "Concluida"]
                    idx_status = opcoes.index(status) if status in opcoes else 0
                    novo_status = st.selectbox("", opcoes, index=idx_status, key=f"status_{cert}", label_visibility="collapsed")
                    if novo_status != status:
                        st.session_state.cert_status[cert] = novo_status
                        salvar_backup()
                        st.rerun()

# =========================
# TAB 5 - ROADMAP
# =========================
with tab5:
    st.markdown("## Roadmap 2026-2029")
    
    roadmap = {
        2026: {"titulo": "Fundacao", "certs": ["AZ-900", "SC-900", "Scrum Fundamentals", "Power BI", "Python", "SQL", "Pos-graduacao"]},
        2027: {"titulo": "Especializacao", "certs": ["AWS Cloud Practitioner", "Security+"]},
        2028: {"titulo": "Maestria", "certs": []},
        2029: {"titulo": "Lideranca", "certs": ["Ingles"]}
    }
    
    for ano, info in roadmap.items():
        with st.expander(f"{info['titulo']} - {ano}", expanded=(ano == 2026)):
            if info['certs']:
                cols = st.columns(min(4, len(info['certs'])))
                for i, cert in enumerate(info['certs']):
                    if cert in EMBLEMAS:
                        emblema = EMBLEMAS[cert]
                        status = st.session_state.cert_status.get(cert, "Nao iniciada")
                        xp_atual = st.session_state.cert_xp.get(cert, 0)
                        percent = (xp_atual / emblema["xp"]) * 100 if emblema["xp"] > 0 else 0
                        with cols[i % 4]:
                            st.markdown(f"""
                            <div style="text-align:center; padding:10px; background:rgba(77,159,255,0.1); border-radius:10px;">
                                <div style="font-size:32px;">{emblema['emblema']}</div>
                                <div style="font-size:11px;">{cert[:15]}</div>
                                <div>{get_badge(status)}</div>
                                <div style="font-size:10px;">{xp_atual}/{emblema['xp']} XP</div>
                                <div style="background:#333; border-radius:5px; height:4px;"><div style="background:{emblema['cor']}; width:{percent}%; height:4px; border-radius:5px;"></div></div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info("Em planejamento")

st.caption("🚀 Continue sua jornada, o universo te espera!")
