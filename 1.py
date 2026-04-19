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
    "Comunicação e Apresentação": {
        "descricao": "Capacidade de transmitir ideias claramente, fazer apresentações impactantes.",
        "atividades": [
            {"nome": "🎤 Apresentação Técnica", "descricao": "Apresentar um projeto para sua equipe", "xp": 30},
            {"nome": "📝 Escrever Documentação", "descricao": "Documentar um procedimento", "xp": 20},
            {"nome": "🎯 Pitch de Ideia", "descricao": "Apresentar melhoria para liderança", "xp": 40},
            {"nome": "📊 Dashboard para Gestão", "descricao": "Criar relatório visual", "xp": 35},
            {"nome": "🗣️ Reunião em Inglês", "descricao": "Participar de reunião em inglês", "xp": 50}
        ]
    },
    "Liderança de Equipes": {
        "descricao": "Capacidade de motivar e coordenar pessoas.",
        "atividades": [
            {"nome": "👥 Mentorar Colega", "descricao": "Ensinar um processo a um colega", "xp": 35},
            {"nome": "📋 Liderar Reunião", "descricao": "Conduzir uma reunião", "xp": 30},
            {"nome": "🎯 Definir Metas", "descricao": "Estabelecer objetivos", "xp": 40},
            {"nome": "🔄 Delegar Tarefas", "descricao": "Distribuir atividades", "xp": 25},
            {"nome": "🏆 Reconhecer Time", "descricao": "Dar feedback positivo", "xp": 20}
        ]
    },
    "Gestão de Projetos": {
        "descricao": "Planejar, executar e monitorar projetos.",
        "atividades": [
            {"nome": "📅 Planejar Projeto", "descricao": "Criar cronograma", "xp": 40},
            {"nome": "💰 Controlar Orçamento", "descricao": "Monitorar gastos", "xp": 35},
            {"nome": "📊 Relatório de Status", "descricao": "Produzir relatório", "xp": 30},
            {"nome": "⚠️ Gestão de Risco", "descricao": "Identificar riscos", "xp": 45},
            {"nome": "🔄 Kanban/Scrum", "descricao": "Aplicar metodologia ágil", "xp": 50}
        ]
    },
    "Inteligência Emocional": {
        "descricao": "Capacidade de reconhecer e gerenciar emoções.",
        "atividades": [
            {"nome": "😌 Gerenciar Estresse", "descricao": "Aplicar técnica de respiração", "xp": 20},
            {"nome": "👂 Escuta Ativa", "descricao": "Ouvir sem interromper", "xp": 25},
            {"nome": "📝 Diário de Emoções", "descricao": "Registrar gatilhos", "xp": 15},
            {"nome": "💬 Feedback Construtivo", "descricao": "Dar feedback com técnica SBI", "xp": 35},
            {"nome": "🙏 Reconhecer Erro", "descricao": "Admitir erro", "xp": 30}
        ]
    }
}

# =========================
# CONTEÚDO DAS CERTIFICAÇÕES
# =========================
CONTEUDO_CERTIFICACOES = {
    "AZ-900": {
        "titulo": "Microsoft Azure Fundamentals",
        "descricao": "Certificação de entrada para Azure. Valida conhecimentos básicos de cloud computing.",
        "dominios": [
            {"nome": "Conceitos de nuvem (25-30%)", "topicos": [
                "Benefícios da nuvem", "Modelos de serviço (IaaS, PaaS, SaaS)",
                "Modelos de implantação", "CAPEX vs OPEX"
            ]},
            {"nome": "Serviços principais (20-25%)", "topicos": [
                "Computação (VMs, Containers)", "Redes (VNet, VPN)",
                "Armazenamento (Blob, File)", "Banco de dados"
            ]},
            {"nome": "Soluções de segurança (15-20%)", "topicos": [
                "Segurança de rede", "Identidade (Azure AD)",
                "Proteção de dados", "Conformidade"
            ]},
            {"nome": "Gerenciamento e governança (10-15%)", "topicos": [
                "Cost Management", "Resource Groups",
                "Azure Monitor", "Azure Advisor"
            ]]
        ],
        "recursos": ["Microsoft Learn", "YouTube - John Savill", "GitHub"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "Udemy"],
        "semanas": 3, "horas": 30, "custo": "$99", "voucher": True
    },
    "SC-900": {
        "titulo": "Microsoft Security, Compliance and Identity",
        "descricao": "Certificação sobre segurança, compliance e identidade.",
        "dominios": [
            {"nome": "Conceitos de segurança (25-30%)", "topicos": [
                "Zero Trust", "Defesa em profundidade", "Responsabilidade compartilhada", "Criptografia"
            ]},
            {"nome": "Capacidades de identidade (35-40%)", "topicos": [
                "Azure AD", "MFA e Conditional Access", "Identity Protection", "Privileged Identity Management"
            ]},
            {"nome": "Capacidades de segurança (20-25%)", "topicos": [
                "Microsoft Defender", "Microsoft Sentinel", "Defender para endpoint", "Defender Office 365"
            ]},
            {"nome": "Capacidades de compliance (10-15%)", "topicos": [
                "Service Trust Portal", "Compliance Manager", "Azure Policy", "LGPD e GDPR"
            ]}
        ],
        "recursos": ["Microsoft Learn", "YouTube - John Savill", "Microsoft Docs"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "Whizlabs"],
        "semanas": 2, "horas": 25, "custo": "$99", "voucher": True
    },
    "AWS Cloud Practitioner": {
        "titulo": "AWS Cloud Practitioner",
        "descricao": "Certificação fundamental da AWS.",
        "dominios": [
            {"nome": "Conceitos de Nuvem (20%)", "topicos": [
                "Benefícios da AWS", "Modelos de implantação",
                "Modelos de serviço", "Infraestrutura global AWS"
            ]},
            {"nome": "Serviços Principais (30%)", "topicos": [
                "Computação (EC2, Lambda)", "Armazenamento (S3, EBS)",
                "Banco de dados (RDS, DynamoDB)", "Redes (VPC, CloudFront)"
            ]},
            {"nome": "Segurança (25%)", "topicos": [
                "Responsabilidade compartilhada", "IAM",
                "AWS Shield, WAF", "Conformidade"
            ]},
            {"nome": "Preços e Suporte (15%)", "topicos": [
                "Modelos de precificação", "AWS Pricing Calculator",
                "Planos de suporte", "AWS Organizations"
            ]},
            {"nome": "Tecnologias (10%)", "topicos": [
                "Machine Learning", "IoT", "Serverless", "DevOps"
            ]}
        ],
        "recursos": ["AWS Skill Builder", "YouTube - Stephane Maarek", "AWS Free Tier"],
        "simulados": ["AWS Official Practice", "TutorialsDojo", "Udemy"],
        "semanas": 4, "horas": 30, "custo": "$100", "voucher": True
    },
    "Security+": {
        "titulo": "CompTIA Security+ (SY0-701)",
        "descricao": "Certificação fundamental de cibersegurança.",
        "dominios": [
            {"nome": "Ameaças e Ataques (24%)", "topicos": [
                "Malware", "Ataques de rede", "Ataques de aplicação", "OWASP Top 10"
            ]},
            {"nome": "Tecnologias de Segurança (26%)", "topicos": [
                "Firewalls", "IDS/IPS", "SIEM", "Criptografia", "PKI", "MFA"
            ]},
            {"nome": "Arquitetura e Design (21%)", "topicos": [
                "Zero Trust", "Defesa em profundidade", "Segurança em nuvem", "Hardening"
            ]},
            {"nome": "Gestão de Acesso (16%)", "topicos": [
                "IAM", "SSO", "RBAC", "Kerberos", "PAM"
            ]},
            {"nome": "Riscos e Compliance (13%)", "topicos": [
                "Análise de risco", "BCP/DRP", "Resposta a incidentes", "LGPD/GDPR"
            ]}
        ],
        "recursos": ["YouTube - Professor Messer", "CompTIA Objectives", "GitHub"],
        "simulados": ["ExamCompass", "Professor Messer", "Jason Dion", "MeasureUp"],
        "semanas": 10, "horas": 80, "custo": "$392", "voucher": False
    },
    "Scrum Fundamentals": {
        "titulo": "Scrum Fundamentals Certified",
        "descricao": "Certificação básica de Scrum.",
        "dominios": [
            {"nome": "Fundamentos (30%)", "topicos": [
                "Manifesto Ágil", "Princípios ágeis", "Scrum vs Waterfall"
            ]},
            {"nome": "Papéis (25%)", "topicos": [
                "Product Owner", "Scrum Master", "Development Team"
            ]},
            {"nome": "Eventos (25%)", "topicos": [
                "Sprint Planning", "Daily Scrum", "Review", "Retrospective"
            ]},
            {"nome": "Artefatos (20%)", "topicos": [
                "Product Backlog", "Sprint Backlog", "Increment", "Definition of Done"
            ]}
        ],
        "recursos": ["Scrum Guide", "YouTube - Scrum Framework", "Scrum.org"],
        "simulados": ["Scrum.org Assessment", "ScrumStudy", "Udemy"],
        "semanas": 1, "horas": 16, "custo": "R$ 500", "voucher": False
    },
    "CySA+": {
        "titulo": "CompTIA CySA+ (CS0-003)",
        "descricao": "Certificação de análise de segurança.",
        "dominios": [
            {"nome": "Segurança de Software (22%)", "topicos": [
                "SSDLC", "SAST/DAST/IAST", "DevSecOps"
            ]},
            {"nome": "Operações de Segurança (25%)", "topicos": [
                "SIEM", "SOAR", "Log management", "Threat hunting"
            ]},
            {"nome": "Inteligência de Ameaças (20%)", "topicos": [
                "Threat Intelligence", "MITRE ATT&CK", "Indicadores de comprometimento"
            ]},
            {"nome": "Resposta a Incidentes (18%)", "topicos": [
                "Ciclo de vida NIST", "Playbooks", "Forensics"
            ]},
            {"nome": "Gestão de Vulnerabilidades (15%)", "topicos": [
                "Scanning", "Vulnerability management", "Patch management"
            ]}
        ],
        "recursos": ["YouTube - Certify Breakfast", "CompTIA Objectives", "TryHackMe"],
        "simulados": ["Jason Dion", "Sybex", "ExamCompass"],
        "semanas": 8, "horas": 60, "custo": "$392", "voucher": False
    },
    "Power BI": {
        "titulo": "Microsoft Power BI Data Analyst",
        "descricao": "Certificação para análise de dados com Power BI.",
        "dominios": [
            {"nome": "Preparação de Dados (20%)", "topicos": [
                "Power Query", "Limpeza de dados", "Combinação de tabelas"
            ]},
            {"nome": "Modelagem de Dados (25%)", "topicos": [
                "Modelos star", "Relacionamentos", "DAX"
            ]},
            {"nome": "Visualização (30%)", "topicos": [
                "Gráficos", "Dashboards", "Drill-through"
            ]},
            {"nome": "Análise de Dados (15%)", "topicos": [
                "Funções DAX", "Inteligência de tempo", "Segmentação"
            ]},
            {"nome": "Implantação (10%)", "topicos": [
                "Publicação", "Gateways", "RLS"
            ]}
        ],
        "recursos": ["Hashtag Treinamentos", "Microsoft Learn", "YouTube - SQLBI"],
        "simulados": ["Microsoft Assessment", "ExamTopics", "MeasureUp"],
        "semanas": 6, "horas": 50, "custo": "$99", "voucher": False
    },
    "Python": {
        "titulo": "Python para Análise de Dados",
        "descricao": "Linguagem Python para automação e análise.",
        "dominios": [
            {"nome": "Fundamentos (25%)", "topicos": [
                "Sintaxe", "Estruturas de controle", "Funções", "Listas/Dicionários"
            ]},
            {"nome": "Manipulação de Dados (30%)", "topicos": [
                "Pandas", "Leitura de arquivos", "Filtros", "Tratamento de nulos"
            ]},
            {"nome": "Visualização (20%)", "topicos": [
                "Matplotlib", "Seaborn", "Plotly"
            ]},
            {"nome": "Automação (25%)", "topicos": [
                "Automação de planilhas", "E-mails", "Web scraping", "APIs"
            ]}
        ],
        "recursos": ["Hashtag Treinamentos", "Curso em Vídeo", "DataCamp"],
        "simulados": ["HackerRank", "LeetCode", "Python Institute"],
        "semanas": 8, "horas": 60, "custo": "R$ 650", "voucher": False
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Linguagem SQL para consultas.",
        "dominios": [
            {"nome": "Consultas Básicas (30%)", "topicos": [
                "SELECT/WHERE", "ORDER BY", "Operadores", "Agregações"
            ]},
            {"nome": "Joins (30%)", "topicos": [
                "INNER/LEFT/RIGHT JOIN", "Self JOIN", "Subconsultas", "CTEs"
            ]},
            {"nome": "Manipulação (20%)", "topicos": [
                "INSERT/UPDATE/DELETE", "CREATE/ALTER/DROP", "Índices", "Transações"
            ]},
            {"nome": "Funções Avançadas (20%)", "topicos": [
                "Window Functions", "GROUP BY", "Funções string/date", "Stored Procedures"
            ]}
        ],
        "recursos": ["Hashtag Treinamentos", "SQLZoo", "Mode Analytics"],
        "simulados": ["HackerRank", "LeetCode", "StrataScratch"],
        "semanas": 6, "horas": 45, "custo": "R$ 650", "voucher": False
    },
    "CISSP": {
        "titulo": "Certified Information Systems Security Professional",
        "descricao": "Certificação mais reconhecida em cibersegurança.",
        "dominios": [
            {"nome": "Security and Risk Management (15%)", "topicos": ["CIA Triade", "Governança", "Gestão de riscos", "LGPD/GDPR"]},
            {"nome": "Asset Security (10%)", "topicos": ["Classificação de dados", "Retenção", "Handling"]},
            {"nome": "Security Architecture (13%)", "topicos": ["Arquitetura", "Criptografia", "Modelos de segurança"]},
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
        "titulo": "Global Industrial Cyber Security Professional",
        "descricao": "Certificação especializada em segurança industrial (OT/ICS).",
        "dominios": [
            {"nome": "OT/ICS Fundamentals (25%)", "topicos": ["Arquitetura ICS", "Protocolos industriais", "Ataques industriais", "TI vs OT"]},
            {"nome": "Riscos em OT (20%)", "topicos": ["Análise de risco", "Vulnerabilidades ICS", "MITRE ATT&CK ICS"]},
            {"nome": "Segurança de Rede Industrial (20%)", "topicos": ["Segmentação", "Firewalls industriais", "Network monitoring", "IEC 62443"]},
            {"nome": "Controles de Segurança (20%)", "topicos": ["Hardening de PLCs", "Controle de acesso", "Patch management", "Backup"]},
            {"nome": "Resposta a Incidentes OT (15%)", "topicos": ["Planos de resposta OT", "Forensics industrial", "Recuperação"]}
        ],
        "recursos": ["GIAC Official Course", "SANS ICS Security", "CISA ICS Training"],
        "simulados": ["GIAC Practice Tests", "CyberSecurity Training"],
        "semanas": 12, "horas": 120, "custo": "$949", "voucher": False
    }
}

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026},
    "AWS Cloud Practitioner": {"emblema": "☁️📘", "cor": "#FF9900", "titulo": "AWS Cloud", "xp": 100, "ano": 2027},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027},
    "Scrum Fundamentals": {"emblema": "🔄📋", "cor": "#0A5C4A", "titulo": "Scrum", "xp": 60, "ano": 2026},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo"}
}

# =========================
# EMENTA PUC MINAS
# =========================
EMENTA_PUC = {
    "Arquitetura de Cibersegurança e Zero Trust": {
        "ementa": "Fundamentos de arquitetura de segurança. Zero Trust. Defesa em profundidade.",
        "certificacoes": ["Security+", "CCNA"],
        "topicos": ["Zero Trust", "Defesa em profundidade", "Segurança em nuvem", "Firewalls", "IDS/IPS"],
        "horas": 60
    },
    "Gestão de Riscos Cibernéticos": {
        "ementa": "Fundamentos de riscos. ISO 27005. NIST CSF.",
        "certificacoes": ["CISSP", "Security+"],
        "topicos": ["ISO 27005", "NIST CSF", "Análise de riscos", "Tratamento de riscos"],
        "horas": 45
    },
    "Resposta a Incidentes": {
        "ementa": "Gestão de incidentes. NIST 800-61. SIEM, SOAR.",
        "certificacoes": ["CySA+", "CISSP"],
        "topicos": ["NIST 800-61", "SIEM", "SOAR", "Playbooks", "SOC"],
        "horas": 50
    },
    "Segurança e Gestão da Identidade": {
        "ementa": "IAM. RBAC. Autenticação. Zero Trust.",
        "certificacoes": ["SC-900", "Security+"],
        "topicos": ["IAM", "RBAC", "MFA/SSO", "Zero Trust", "Azure AD"],
        "horas": 45
    }
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
if "soft_skills_concluidas" not in st.session_state:
    st.session_state.soft_skills_concluidas = {}
if "cert_topicos_concluidos" not in st.session_state:
    st.session_state.cert_topicos_concluidos = {}

# =========================
# FUNÇÕES DE BACKUP
# =========================
ARQUIVO_BACKUP = "backup_diario.json"

def salvar_backup():
    dados = {"db": st.session_state.db, "xp": st.session_state.xp,
             "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status,
             "soft_skills_concluidas": st.session_state.soft_skills_concluidas,
             "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos}
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
# FUNÇÕES PRINCIPAIS
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
            data_atv = datetime.fromisoformat(a['data']).date() if isinstance(a['data'], str) else a['data'].date()
            if data_atv == hoje:
                resultado.append(a)
        except:
            pass
    return resultado

def get_xp_semana():
    hoje = datetime.now()
    inicio = hoje - timedelta(days=hoje.weekday())
    total = 0
    for a in st.session_state.db:
        try:
            data_atv = datetime.fromisoformat(a['data']) if isinstance(a['data'], str) else a['data']
            if data_atv.date() >= inicio.date():
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
# CARREGAR DADOS
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
# ABAS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "📚 Certificações", "💪 Soft Skills", "🎓 Pós PUC", "🎖️ Progresso", "🗺️ Roadmap"])

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
        st.markdown(f'<div class="kpi-card"><div style="font-size:36px;">🎯</div><div style="font-size:28px;">{xp_hoje}/50</div><div>Meta</div></div>', unsafe_allow_html=True)
        st.progress(min(xp_hoje / 50, 1.0))
    
    for atv in get_atividades_hoje():
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        st.markdown(f'<div class="atividade-card">{emblema} **{atv["area"][:30]}** | {atv["atividade"]} | ⭐ +{atv["xp"]}<br><small>📝 {atv["obs"][:50] if atv["obs"] else "-"}</small></div>', unsafe_allow_html=True)
    if not get_atividades_hoje():
        st.info("✨ Nenhuma atividade hoje. Comece agora!")

# =========================
# TAB 2 - CERTIFICAÇÕES
# =========================
with tab2:
    st.markdown("## 📚 PLANO DE ESTUDOS")
    cert_selecionada = st.selectbox("Selecione a certificação", list(CONTEUDO_CERTIFICACOES.keys()))
    if cert_selecionada in CONTEUDO_CERTIFICACOES:
        info = CONTEUDO_CERTIFICACOES[cert_selecionada]
        st.markdown(f'<div class="cert-card"><h2>{EMBLEMAS[cert_selecionada]["emblema"]} {cert_selecionada}</h2><h3>{info["titulo"]}</h3><p>{info["descricao"]}</p><p><strong>Duração:</strong> {info["semanas"]} semanas ({info["horas"]} horas)</p></div>', unsafe_allow_html=True)
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
                st.markdown(f"- {r}")
        with sub3:
            for s in info['simulados']:
                st.markdown(f"- {s}")

# =========================
# TAB 3 - SOFT SKILLS
# =========================
with tab3:
    st.markdown("## 💪 SOFT SKILLS")
    for categoria, info in SOFT_SKILLS_ATIVIDADES.items():
        with st.expander(f"📌 {categoria}"):
            st.markdown(f"*{info['descricao']}*")
            cols = st.columns(2)
            for i, atv in enumerate(info['atividades']):
                with cols[i % 2]:
                    key = f"soft_{categoria}_{atv['nome']}"
                    if st.button(f"✅ {atv['nome']} (+{atv['xp']} XP)", key=key):
                        if adicionar_soft_skill(categoria, atv['nome'], atv['xp']):
                            st.success(f"+{atv['xp']} XP!")
                            st.rerun()

# =========================
# TAB 4 - PÓS PUC
# =========================
with tab4:
    st.markdown("## 🎓 PÓS-GRADUAÇÃO PUC MINAS")
    for disciplina, info in EMENTA_PUC.items():
        with st.expander(f"📖 {disciplina}"):
            st.markdown(f"*{info['ementa']}*")
            st.markdown(f"**Certificações:** {', '.join(info['certificacoes'])}")
            for topico in info['topicos']:
                st.markdown(f"- {topico}")

# =========================
# TAB 5 - PROGRESSO
# =========================
with tab5:
    st.markdown("## 🎖️ PROGRESSO")
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
                    st.markdown(f'<div class="cert-card {"atrasado" if atrasado else ""}"><div style="text-align:center; font-size:32px;">{info["emblema"]}</div><div style="font-weight:bold;">{cert[:15]}</div><div style="font-size:24px;">{get_badge(status)}</div><div>{xp}/{info["xp"]} XP</div></div>', unsafe_allow_html=True)
                    st.progress(min(xp/info["xp"], 1.0))
                    novo = st.selectbox("", ["Não iniciada", "Em andamento", "Concluída"], index=["Não iniciada", "Em andamento", "Concluída"].index(status), key=f"status_{cert}", label_visibility="collapsed")
                    if novo != status:
                        st.session_state.cert_status[cert] = novo
                        salvar_backup()
                        st.rerun()

# =========================
# TAB 6 - ROADMAP
# =========================
with tab6:
    st.markdown("## 🗺️ ROADMAP")
    for ano in [2026, 2027, 2028, 2029]:
        titulo = {2026: "🌱 2026 - Fundação", 2027: "⚡ 2027 - Especialização", 2028: "🎯 2028 - Maestria", 2029: "👑 2029 - Liderança"}[ano]
        with st.expander(titulo):
            certs_ano = [c for c, d in EMBLEMAS.items() if d.get("ano") == ano]
            if certs_ano:
                cols = st.columns(min(4, len(certs_ano)))
                for i, cert in enumerate(certs_ano):
                    info = EMBLEMAS[cert]
                    st.markdown(f'<div style="text-align:center;"><div style="font-size:32px;">{info["emblema"]}</div><div>{cert}</div><div>{get_badge(st.session_state.cert_status[cert])}</div><div>{st.session_state.cert_xp[cert]}/{info["xp"]} XP</div></div>', unsafe_allow_html=True)

st.caption("🚀 Continue sua jornada, o universo te espera!")
