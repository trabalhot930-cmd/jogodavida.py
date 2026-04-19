import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json
import os

# =========================
# CONFIGURAÇÃO INICIAL
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CREDENCIAIS DE ACESSO
# =========================
USUARIO_VALIDO = "Juan"
SENHA_VALIDA = "Ju@n1990"

# =========================
# CONSTANTES DO SISTEMA
# =========================
META_DIARIA_XP = 50
XP_POR_TOPICO_CERT = 3
XP_POR_TOPICO_PUC = 5
XP_POR_HORA_ESTUDO = 5

# =========================
# CONTEÚDO DAS CERTIFICAÇÕES (OTIMIZADO)
# =========================
CONTEUDO_CERTIFICACOES = {
    "AZ-900": {
        "titulo": "Microsoft Azure Fundamentals",
        "descricao": "Certificação de entrada para Azure. Valida conhecimentos básicos de cloud computing.",
        "dominios": [
            {"nome": "Conceitos de Nuvem (25-30%)", "topicos": ["Benefícios da nuvem", "Modelos de serviço (IaaS, PaaS, SaaS)", "Modelos de implantação", "CAPEX vs OPEX"]},
            {"nome": "Serviços Principais (20-25%)", "topicos": ["Computação (VMs, Containers)", "Redes (VNet, VPN)", "Armazenamento (Blob, File)", "Banco de dados"]},
            {"nome": "Soluções de Segurança (15-20%)", "topicos": ["Segurança de rede", "Identidade (Azure AD)", "Proteção de dados", "Conformidade"]},
            {"nome": "Governança (10-15%)", "topicos": ["Cost Management", "Resource Groups", "Azure Monitor", "Azure Advisor"]}
        ],
        "recursos": ["Microsoft Learn (grátis)", "YouTube - John Savill", "GitHub Microsoft Learning"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "Udemy"],
        "semanas": 3, "horas": 30, "custo": "$99", "voucher": True
    },
    "SC-900": {
        "titulo": "Microsoft Security, Compliance & Identity",
        "descricao": "Certificação sobre segurança, compliance e identidade na Microsoft.",
        "dominios": [
            {"nome": "Conceitos de Segurança (25-30%)", "topicos": ["Zero Trust", "Defesa em profundidade", "Responsabilidade compartilhada", "Criptografia"]},
            {"nome": "Capacidades de Identidade (35-40%)", "topicos": ["Azure AD", "MFA e Conditional Access", "Identity Protection", "Privileged Identity Management"]},
            {"nome": "Capacidades de Segurança (20-25%)", "topicos": ["Microsoft Defender", "Microsoft Sentinel", "Defender para endpoint", "Defender Office 365"]},
            {"nome": "Capacidades de Compliance (10-15%)", "topicos": ["Service Trust Portal", "Compliance Manager", "Azure Policy", "LGPD e GDPR"]}
        ],
        "recursos": ["Microsoft Learn", "YouTube - John Savill", "Microsoft Security Docs"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "Whizlabs"],
        "semanas": 2, "horas": 25, "custo": "$99", "voucher": True
    },
    "Security+": {
        "titulo": "CompTIA Security+ (SY0-701)",
        "descricao": "Certificação fundamental de cibersegurança, reconhecida mundialmente.",
        "dominios": [
            {"nome": "Ameaças e Ataques (24%)", "topicos": ["Malware", "Ataques de rede", "Ataques de aplicação", "Ameaças internas", "OWASP Top 10"]},
            {"nome": "Tecnologias de Segurança (26%)", "topicos": ["Firewalls", "IDS/IPS", "SIEM", "Criptografia", "PKI", "MFA", "EDR/DLP"]},
            {"nome": "Arquitetura de Segurança (21%)", "topicos": ["Zero Trust", "Defesa em profundidade", "Segurança em nuvem", "Segurança de redes", "Hardening"]},
            {"nome": "Gestão de Acesso (16%)", "topicos": ["IAM", "SSO", "RBAC", "Kerberos/RADIUS", "PAM", "JIT"]},
            {"nome": "Riscos e Compliance (13%)", "topicos": ["Análise de risco", "BCP/DRP", "Resposta a incidentes", "LGPD/GDPR", "Forensics"]}
        ],
        "recursos": ["YouTube - Professor Messer", "CompTIA Objectives", "GitHub Study Guide"],
        "simulados": ["ExamCompass", "Professor Messer", "Jason Dion", "MeasureUp"],
        "semanas": 10, "horas": 80, "custo": "$392", "voucher": False
    },
    "CySA+": {
        "titulo": "CompTIA CySA+ (CS0-003)",
        "descricao": "Certificação de análise de segurança e resposta a incidentes.",
        "dominios": [
            {"nome": "Segurança de Software (22%)", "topicos": ["SSDLC", "SAST/DAST/IAST", "DevSecOps", "Análise de vulnerabilidades"]},
            {"nome": "Operações de Segurança (25%)", "topicos": ["SIEM", "SOAR", "Log management", "Threat hunting"]},
            {"nome": "Inteligência de Ameaças (20%)", "topicos": ["Threat Intelligence", "MITRE ATT&CK", "Indicadores de comprometimento", "Threat modeling"]},
            {"nome": "Resposta a Incidentes (18%)", "topicos": ["Ciclo de vida NIST", "Playbooks", "Forensics", "Comunicação"]},
            {"nome": "Gestão de Vulnerabilidades (15%)", "topicos": ["Scanning", "Vulnerability management", "Patch management", "Relatórios"]}
        ],
        "recursos": ["YouTube - Certify Breakfast", "CompTIA Objectives", "TryHackMe"],
        "simulados": ["Jason Dion", "Sybex", "ExamCompass"],
        "semanas": 8, "horas": 60, "custo": "$392", "voucher": False
    },
    "CISSP": {
        "titulo": "CISSP - Certified Information Systems Security Professional",
        "descricao": "Certificação mais reconhecida globalmente em cibersegurança.",
        "dominios": [
            {"nome": "Security and Risk Management (15%)", "topicos": ["CIA Triade", "Governança", "Gestão de riscos", "LGPD/GDPR"]},
            {"nome": "Asset Security (10%)", "topicos": ["Classificação de dados", "Retenção", "Handling de dados"]},
            {"nome": "Security Architecture (13%)", "topicos": ["Arquitetura de segurança", "Criptografia", "Modelos de segurança"]},
            {"nome": "Network Security (13%)", "topicos": ["Segurança de redes", "TLS/IPsec", "Segurança sem fio"]},
            {"nome": "IAM (13%)", "topicos": ["IAM", "SSO/MFA", "Federação", "PAM"]},
            {"nome": "Security Assessment (12%)", "topicos": ["Pentest", "Análise de vulnerabilidades", "Auditoria"]},
            {"nome": "Security Operations (13%)", "topicos": ["Resposta a incidentes", "BCP/DRP", "Forensics"]},
            {"nome": "Software Security (11%)", "topicos": ["DevSecOps", "SDLC seguro", "OWASP"]}
        ],
        "recursos": ["ISC2 Official Guide", "YouTube - Destination Certification", "LinkedIn Learning"],
        "simulados": ["ISC2 Official Tests", "Boson", "Pocket Prep"],
        "semanas": 16, "horas": 200, "custo": "$749", "voucher": False
    },
    "GICSP": {
        "titulo": "GICSP - Global Industrial Cyber Security Professional",
        "descricao": "Certificação especializada em segurança de sistemas industriais (OT/ICS).",
        "dominios": [
            {"nome": "OT/ICS Fundamentals (25%)", "topicos": ["Arquitetura ICS", "Protocolos industriais", "Ataques industriais", "TI vs OT"]},
            {"nome": "Riscos em OT (20%)", "topicos": ["Análise de risco industrial", "Vulnerabilidades ICS", "MITRE ATT&CK ICS"]},
            {"nome": "Segurança de Rede Industrial (20%)", "topicos": ["Segmentação", "Firewalls industriais", "Network monitoring", "IEC 62443"]},
            {"nome": "Controles de Segurança (20%)", "topicos": ["Hardening de PLCs", "Controle de acesso", "Patch management", "Backup industrial"]},
            {"nome": "Resposta a Incidentes OT (15%)", "topicos": ["Planos de resposta OT", "Forensics industrial", "Recuperação", "Simulações"]}
        ],
        "recursos": ["GIAC Official Course", "SANS ICS Security", "CISA ICS Training"],
        "simulados": ["GIAC Practice Tests", "CyberSecurity Training"],
        "semanas": 12, "horas": 120, "custo": "$949", "voucher": False
    },
    "Power BI": {
        "titulo": "Microsoft Power BI Data Analyst",
        "descricao": "Certificação para análise e visualização de dados com Power BI.",
        "dominios": [
            {"nome": "Preparação de Dados (20%)", "topicos": ["Power Query", "Limpeza de dados", "Tratamento de erros", "Combinação de tabelas"]},
            {"nome": "Modelagem de Dados (25%)", "topicos": ["Modelos star/snowflake", "Relacionamentos", "DAX", "Hierarquias"]},
            {"nome": "Visualização de Dados (30%)", "topicos": ["Gráficos", "Dashboards", "Drill-through", "Bookmarks"]},
            {"nome": "Análise de Dados (15%)", "topicos": ["Funções DAX", "Inteligência de tempo", "Segmentação", "Quick measures"]},
            {"nome": "Implantação (10%)", "topicos": ["Publicação", "Gateways", "RLS", "Workspaces"]}
        ],
        "recursos": ["Hashtag Treinamentos", "Microsoft Learn", "YouTube - SQLBI"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "MeasureUp"],
        "semanas": 6, "horas": 50, "custo": "$99", "voucher": False
    },
    "Python": {
        "titulo": "Python para Análise de Dados",
        "descricao": "Linguagem Python aplicada à automação e análise de dados.",
        "dominios": [
            {"nome": "Fundamentos (25%)", "topicos": ["Sintaxe", "Estruturas de controle", "Funções", "Listas/Dicionários"]},
            {"nome": "Manipulação de Dados (30%)", "topicos": ["Pandas", "Leitura de arquivos", "Filtros", "Tratamento de nulos"]},
            {"nome": "Visualização (20%)", "topicos": ["Matplotlib", "Seaborn", "Plotly"]},
            {"nome": "Automação (25%)", "topicos": ["Automação de planilhas", "E-mails", "Web scraping", "APIs"]}
        ],
        "recursos": ["Hashtag Treinamentos", "Curso em Vídeo", "DataCamp"],
        "simulados": ["HackerRank", "LeetCode", "Python Institute"],
        "semanas": 8, "horas": 60, "custo": "R$ 650", "voucher": False
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Linguagem SQL para consultas e manipulação de bancos de dados.",
        "dominios": [
            {"nome": "Consultas Básicas (30%)", "topicos": ["SELECT/WHERE", "ORDER BY", "Operadores", "Agregações"]},
            {"nome": "Joins (30%)", "topicos": ["INNER/LEFT/RIGHT JOIN", "Self JOIN", "Subconsultas", "CTEs"]},
            {"nome": "Manipulação (20%)", "topicos": ["INSERT/UPDATE/DELETE", "CREATE/ALTER/DROP", "Índices", "Transações"]},
            {"nome": "Funções Avançadas (20%)", "topicos": ["Window Functions", "GROUP BY", "Funções string/date", "Stored Procedures"]}
        ],
        "recursos": ["Hashtag Treinamentos", "SQLZoo", "Mode Analytics"],
        "simulados": ["HackerRank", "LeetCode", "StrataScratch"],
        "semanas": 6, "horas": 45, "custo": "R$ 650", "voucher": False
    }
}

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026},
    "ISO 27001 Fundamentals": {"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation", "xp": 100, "ano": 2026},
    "CCNA": {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA", "xp": 150, "ano": 2027},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo"}
}

# =========================
# EMENTA PUC MINAS (RESUMIDA)
# =========================
EMENTA_PUC = {
    "Arquitetura de Cibersegurança e Zero Trust": {
        "ementa": "Fundamentos de arquitetura de segurança. Paradigma Zero Trust. Defesa em profundidade.",
        "certificacoes": ["Security+", "CCNA"],
        "topicos": ["Zero Trust", "Defesa em profundidade", "Segurança em nuvem", "Firewalls", "IDS/IPS", "Segurança de endpoint"],
        "horas": 60
    },
    "Gestão de Riscos Cibernéticos": {
        "ementa": "Fundamentos de riscos. ISO 27005. NIST CSF. Gestão de riscos.",
        "certificacoes": ["ISO 27001", "CISSP"],
        "topicos": ["ISO 27005", "NIST CSF", "Análise de riscos", "Tratamento de riscos", "TPRM"],
        "horas": 45
    },
    "Resposta a Incidentes e Gestão de Crises": {
        "ementa": "Gestão de incidentes. NIST 800-61. SIEM, SOAR, EDR. SOC.",
        "certificacoes": ["CySA+", "CISSP"],
        "topicos": ["NIST 800-61", "SIEM", "SOAR", "EDR", "Playbooks", "SOC"],
        "horas": 50
    },
    "Segurança e Gestão da Identidade Digital": {
        "ementa": "IAM. RBAC, ABAC. Autenticação. Zero Trust.",
        "certificacoes": ["SC-900", "Security+"],
        "topicos": ["IAM", "RBAC/ABAC", "MFA/SSO", "Zero Trust", "Azure AD"],
        "horas": 45
    },
    "Criptografia e Segurança de Dados": {
        "ementa": "Criptografia simétrica/assimétrica. PKI. TLS/SSL.",
        "certificacoes": ["Security+", "CISSP"],
        "topicos": ["Criptografia simétrica", "Criptografia assimétrica", "PKI", "TLS/SSL", "Blockchain"],
        "horas": 55
    },
    "Ethical Hacking e Gestão de Vulnerabilidades": {
        "ementa": "Técnicas ofensivas. Pentest. MITRE ATT&CK.",
        "certificacoes": ["Security+", "CySA+"],
        "topicos": ["Pentest", "Red Team", "MITRE ATT&CK", "Ferramentas", "Gestão de vulnerabilidades"],
        "horas": 60
    }
}

# =========================
# STYLE PERSONALIZADO
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body {
    background: linear-gradient(135deg, #0a0e27, #1a1f3a);
    color: #4d9fff;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
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
.cert-card.atrasado { border-left: 3px solid #ff4444; }

.atividade-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.08), rgba(123,47,247,0.03));
    border-radius: 10px;
    padding: 10px;
    margin: 5px 0;
    border-left: 3px solid #4d9fff;
    transition: all 0.2s;
}
.atividade-card:hover {
    transform: translateX(5px);
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
}

.kpi-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08));
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.dominio-header {
    background: rgba(77,159,255,0.15);
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0 5px 0;
    font-weight: bold;
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
if "cert_topicos_concluidos" not in st.session_state:
    st.session_state.cert_topicos_concluidos = {}
if "disciplinas_progresso" not in st.session_state:
    st.session_state.disciplinas_progresso = {disciplina: 0 for disciplina in EMENTA_PUC.keys()}

# =========================
# FUNÇÕES DE BACKUP
# =========================
ARQUIVO_BACKUP = "backup_diario.json"

def salvar_backup():
    dados = {
        "db": st.session_state.db, "xp": st.session_state.xp,
        "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status,
        "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos,
        "disciplinas_progresso": st.session_state.disciplinas_progresso,
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
            st.session_state.cert_topicos_concluidos = dados.get("cert_topicos_concluidos", {})
            st.session_state.disciplinas_progresso = dados.get("disciplinas_progresso", st.session_state.disciplinas_progresso)
            return True
    return False

# =========================
# FUNÇÕES AUXILIARES
# =========================
def calc_xp(atividade):
    tabela = {"📚 Estudo": 10, "🔬 Laboratório": 20, "🏗️ Projeto": 30, "🔄 Revisão": 15,
              "📝 Simulado": 15, "🎓 Aula Pós": 25, "🌎 Inglês": 15, "🏅 Certificação": 50}
    return tabela.get(atividade, 10)

def get_badge(status):
    if status == "Concluída": return "🏆"
    elif status == "Em andamento": return "⚡"
    return "💤"

def verificar_atraso(cert, ano):
    if ano == "Contínuo": return False
    if isinstance(ano, int) and datetime.now().year > ano:
        if st.session_state.cert_xp.get(cert, 0) < EMBLEMAS[cert]["xp"]:
            return True
    return False

def adicionar_atividade(area, atividade, xp, obs):
    st.session_state.db.append({"data": datetime.now().isoformat(), "area": area, "atividade": atividade, "xp": xp, "obs": obs})
    st.session_state.xp += xp
    st.session_state.cert_xp[area] += xp
    if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluída"
    elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"
    salvar_backup()

def marcar_topico_certificacao(cert, dominio, topico, concluido):
    key = f"{cert}_{dominio}_{topico}"
    if concluido and key not in st.session_state.cert_topicos_concluidos:
        st.session_state.cert_topicos_concluidos[key] = True
        st.session_state.xp += XP_POR_TOPICO_CERT
        salvar_backup()
    elif not concluido and key in st.session_state.cert_topicos_concluidos:
        del st.session_state.cert_topicos_concluidos[key]
        st.session_state.xp -= XP_POR_TOPICO_CERT
        salvar_backup()

def get_atividades_hoje():
    hoje = datetime.now().date()
    resultado = []
    for a in st.session_state.db:
        try:
            data_atv = datetime.fromisoformat(a['data']).date() if isinstance(a['data'], str) else a['data'].date()
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
            data_atv = datetime.fromisoformat(a['data']) if isinstance(a['data'], str) else a['data']
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
            data_atv = datetime.fromisoformat(a['data']) if isinstance(a['data'], str) else a['data']
            if data_atv.month == hoje.month and data_atv.year == hoje.year:
                total += a['xp']
        except:
            pass
    return total

# =========================
# LOGIN
# =========================
def fazer_login():
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 40px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 20px; text-align: center;">
        <h1>🚀 MISSÃO CARREIRA</h1>
        <h3>Acesso Autorizado</h3>
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
# CARREGAR DADOS E VERIFICAR LOGIN
# =========================
carregar_backup()
if not st.session_state.autenticado:
    fazer_login()
    st.stop()

# =========================
# DATA ATUAL
# =========================
hoje = datetime.now()
st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08)); border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px;">
    <div style="font-size: 28px; font-weight: bold;">{hoje.strftime('%d/%m/%Y')}</div>
    <div>{hoje.strftime('%A')}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Cibersegurança")
st.markdown('<p class="green-text">💾 Seu progresso é salvo automaticamente!</p>', unsafe_allow_html=True)
st.markdown("---")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 NAVE")
    st.markdown(f"👨‍🚀 **Juan Felipe**")
    st.markdown(f"⭐ **XP:** {st.session_state.xp}")
    st.markdown(f"🎖️ **Nível:** {st.session_state.xp // 100 + 1}")
    st.markdown(f"📅 **Missões:** {len(st.session_state.db)}")
    st.markdown("---")
    
    atrasadas = [c for c, d in EMBLEMAS.items() if verificar_atraso(c, d.get("ano", 2030))]
    if atrasadas:
        st.markdown('<p class="red-text">⚠️ Atrasadas:</p>', unsafe_allow_html=True)
        for c in atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[c]["emblema"]} {c[:15]}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    xp_hoje = sum(a['xp'] for a in get_atividades_hoje())
    st.markdown(f"**📅 Hoje:** +{xp_hoje} XP")
    st.markdown(f"**📆 Semana:** +{get_xp_semana()} XP")
    st.markdown(f"**📅 Mês:** +{get_xp_mes()} XP")
    st.markdown("---")
    
    if st.button("📥 Backup", use_container_width=True):
        salvar_backup()
        st.success("Backup salvo!")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📚 Certificações", "🎓 Pós PUC", "🎖️ Progresso", "🗺️ Roadmap"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    st.markdown("## ⚡ ATIVIDADES DE HOJE")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        with st.form("nova_atividade", clear_on_submit=True):
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
            atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"])
            obs = st.text_area("Observação")
            if st.form_submit_button("🚀 Lançar", use_container_width=True):
                adicionar_atividade(area, atividade, calc_xp(atividade), obs)
                st.success("Missão concluída!", icon="🎉")
                st.rerun()
    with col2:
        st.markdown(f'<div class="kpi-card"><div style="font-size:36px;">⭐</div><div style="font-size:28px;">+{xp_hoje}</div><div>XP hoje</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div style="font-size:36px;">🎯</div><div style="font-size:28px;">{xp_hoje}/{META_DIARIA_XP}</div><div>Meta</div></div>', unsafe_allow_html=True)
        st.progress(min(xp_hoje / META_DIARIA_XP, 1.0))
    
    for atv in get_atividades_hoje():
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        st.markdown(f'<div class="atividade-card">{emblema} **{atv["area"][:30]}** | {atv["atividade"]} | ⭐ +{atv["xp"]}<br><small>📝 {atv["obs"][:50] if atv["obs"] else "-"}</small></div>', unsafe_allow_html=True)
    if not get_atividades_hoje():
        st.info("✨ Nenhuma atividade hoje. Comece agora!")
    
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
    c1.metric("Missões", len(st.session_state.db))
    c2.metric("XP", st.session_state.xp)
    c3.metric("Nível", st.session_state.xp // 100 + 1)
    c4.metric("Certificações", f"{concluidas}/{len(EMBLEMAS)}")
    c5.metric("Progresso", f"{(concluidas/len(EMBLEMAS)*100):.0f}%")

# =========================
# TAB 2 - CERTIFICAÇÕES
# =========================
with tab2:
    st.markdown("## 📚 PLANO DE ESTUDOS")
    cert_selecionada = st.selectbox("Selecione a certificação", list(CONTEUDO_CERTIFICACOES.keys()))
    
    if cert_selecionada in CONTEUDO_CERTIFICACOES:
        info = CONTEUDO_CERTIFICACOES[cert_selecionada]
        st.markdown(f"""
        <div class="cert-card">
            <h2>{EMBLEMAS[cert_selecionada]['emblema']} {cert_selecionada}</h2>
            <h3>{info['titulo']}</h3>
            <p>{info['descricao']}</p>
            <p><strong>⏱️ Duração:</strong> {info['semanas']} semanas ({info['horas']} horas) | <strong>💰 Custo:</strong> {info['custo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        sub1, sub2, sub3 = st.tabs(["📖 Conteúdo", "🎓 Recursos", "📝 Simulados"])
        with sub1:
            for dominio in info['dominios']:
                st.markdown(f'<div class="dominio-header">📌 {dominio["nome"]}</div>', unsafe_allow_html=True)
                for topico in dominio['topicos']:
                    key = f"{cert_selecionada}_{dominio['nome']}_{topico}"
                    if st.checkbox(topico, value=key in st.session_state.cert_topicos_concluidos, key=key):
                        marcar_topico_certificacao(cert_selecionada, dominio['nome'], topico, True)
                    else:
                        marcar_topico_certificacao(cert_selecionada, dominio['nome'], topico, False)
        with sub2:
            for r in info['recursos']:
                st.markdown(f"- 📹 {r}")
        with sub3:
            for s in info['simulados']:
                st.markdown(f"- ✅ {s}")

# =========================
# TAB 3 - PÓS PUC
# =========================
with tab3:
    st.markdown("## 🎓 PÓS-GRADUAÇÃO PUC MINAS")
    for disciplina, info in EMENTA_PUC.items():
        with st.expander(f"📖 {disciplina}"):
            st.markdown(f"*{info['ementa']}*")
            st.markdown(f"**Certificações relacionadas:** {', '.join(info['certificacoes'])}")
            for topico in info['topicos']:
                st.markdown(f"- {topico}")

# =========================
# TAB 4 - PROGRESSO
# =========================
with tab4:
    st.markdown("## 🎖️ PROGRESSO DAS CERTIFICAÇÕES")
    filtro = st.selectbox("Filtrar", ["Todas", "Em andamento", "Concluída", "Não iniciada"])
    certs = list(st.session_state.cert_xp.items())
    for i in range(0, len(certs), 4):
        cols = st.columns(4)
        for j in range(4):
            if i+j < len(certs):
                cert, xp = certs[i+j]
                info = EMBLEMAS[cert]
                status = st.session_state.cert_status[cert]
                if filtro != "Todas" and status != filtro:
                    continue
                atrasado = verificar_atraso(cert, info.get("ano", 2030))
                with cols[j]:
                    st.markdown(f'<div class="cert-card {"atrasado" if atrasado else ""}"><div style="text-align:center; font-size:32px;">{info["emblema"]}</div><div style="font-weight:bold; text-align:center;">{cert[:15]}</div><div style="text-align:center; font-size:24px;">{get_badge(status)}</div><div style="text-align:center; font-size:10px;">{xp}/{info["xp"]} XP</div></div>', unsafe_allow_html=True)
                    st.progress(min(xp/info["xp"], 1.0))
                    novo = st.selectbox("", ["Não iniciada", "Em andamento", "Concluída"], index=["Não iniciada", "Em andamento", "Concluída"].index(status), key=f"status_{cert}", label_visibility="collapsed")
                    if novo != status:
                        st.session_state.cert_status[cert] = novo
                        salvar_backup()
                        st.rerun()

# =========================
# TAB 5 - ROADMAP
# =========================
with tab5:
    st.markdown("## 🗺️ ROADMAP 2026-2029")
    roadmap = {
        2026: "🌱 Fundação - AZ-900, SC-900, Power BI, Python, SQL",
        2027: "⚡ Especialização - Security+, CySA+, CCNA",
        2028: "🎯 Maestria - GICSP",
        2029: "👑 Liderança - CISSP, Inglês"
    }
    for ano, desc in roadmap.items():
        with st.expander(f"{desc}", expanded=(ano==2026)):
            certs_ano = [c for c, d in EMBLEMAS.items() if d.get("ano") == ano]
            if certs_ano:
                cols = st.columns(min(4, len(certs_ano)))
                for i, cert in enumerate(certs_ano):
                    info = EMBLEMAS[cert]
                    st.markdown(f'<div style="text-align:center;"><div style="font-size:32px;">{info["emblema"]}</div><div>{cert}</div><div>{get_badge(st.session_state.cert_status[cert])}</div><div>{st.session_state.cert_xp[cert]}/{info["xp"]} XP</div></div>', unsafe_allow_html=True)

st.caption("🚀 Continue sua jornada, o universo te espera!")
