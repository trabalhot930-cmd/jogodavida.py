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
        "descricao": "Capacidade de transmitir ideias claramente, fazer apresentações impactantes e se comunicar com diferentes níveis hierárquicos.",
        "atividades": [
            {"nome": "🎤 Apresentação Técnica", "descricao": "Apresentar um projeto para sua equipe ou gestão", "xp": 30},
            {"nome": "📝 Escrever Documentação", "descricao": "Documentar um procedimento ou projeto", "xp": 20},
            {"nome": "🎯 Pitch de Ideia", "descricao": "Apresentar uma melhoria para a liderança", "xp": 40},
            {"nome": "📊 Dashboard para Gestão", "descricao": "Criar relatório visual para tomada de decisão", "xp": 35},
            {"nome": "🗣️ Reunião em Inglês", "descricao": "Participar de reunião ou call em inglês", "xp": 50},
            {"nome": "📹 Gravar Tutorial", "descricao": "Gravar vídeo explicando um conceito técnico", "xp": 45},
            {"nome": "✍️ Resumo Executivo", "descricao": "Escrever resumo de 1 página para direção", "xp": 25}
        ]
    },
    "Liderança de Equipes": {
        "descricao": "Capacidade de motivar, orientar e coordenar pessoas para alcançar objetivos comuns.",
        "atividades": [
            {"nome": "👥 Mentorar Colega", "descricao": "Ensinar um processo ou tecnologia a um colega", "xp": 35},
            {"nome": "📋 Liderar Reunião", "descricao": "Conduzir uma reunião de equipe", "xp": 30},
            {"nome": "🎯 Definir Metas", "descricao": "Estabelecer objetivos claros para sua equipe", "xp": 40},
            {"nome": "🔄 Delegar Tarefas", "descricao": "Distribuir atividades entre a equipe", "xp": 25},
            {"nome": "🏆 Reconhecer Time", "descricao": "Dar feedback positivo público para colega", "xp": 20},
            {"nome": "🚦 Resolver Conflito", "descricao": "Mediar situação de conflito na equipe", "xp": 50},
            {"nome": "📈 Avaliar Performance", "descricao": "Fazer avaliação de desempenho de um colega", "xp": 45}
        ]
    },
    "Gestão de Projetos": {
        "descricao": "Planejar, executar e monitorar projetos dentro de prazo, orçamento e qualidade.",
        "atividades": [
            {"nome": "📅 Planejar Projeto", "descricao": "Criar cronograma com marcos e entregas", "xp": 40},
            {"nome": "💰 Controlar Orçamento", "descricao": "Monitorar gastos e fazer ajustes", "xp": 35},
            {"nome": "📊 Relatório de Status", "descricao": "Produzir relatório de progresso do projeto", "xp": 30},
            {"nome": "⚠️ Gestão de Risco", "descricao": "Identificar e mitigar riscos do projeto", "xp": 45},
            {"nome": "🔄 Kanban/Scrum", "descricao": "Aplicar metodologia ágil no dia a dia", "xp": 50},
            {"nome": "🎉 Encerrar Projeto", "descricao": "Documentar lições aprendidas", "xp": 60},
            {"nome": "🤝 Gestão de Stakeholders", "descricao": "Gerenciar expectativas e comunicação", "xp": 55}
        ]
    },
    "Negociação e Influência": {
        "descricao": "Capacidade de persuadir, negociar recursos e influenciar decisões.",
        "atividades": [
            {"nome": "💰 Negociar Recurso", "descricao": "Conseguir orçamento ou equipamento", "xp": 50},
            {"nome": "🤝 Alinhar Expectativas", "descricao": "Negociar prazos com stakeholders", "xp": 40},
            {"nome": "📢 Defender Ideia", "descricao": "Apresentar argumentos para aprovação", "xp": 45},
            {"nome": "🔄 Gerenciar Mudança", "descricao": "Convencer equipe a adotar novo processo", "xp": 60},
            {"nome": "🎯 Influenciar Decisão", "descricao": "Levar sua proposta para aprovação", "xp": 55}
        ]
    },
    "Inteligência Emocional": {
        "descricao": "Capacidade de reconhecer e gerenciar emoções próprias e alheias.",
        "atividades": [
            {"nome": "😌 Gerenciar Estresse", "descricao": "Aplicar técnica de respiração/pausa", "xp": 20},
            {"nome": "👂 Escuta Ativa", "descricao": "Praticar ouvir sem interromper", "xp": 25},
            {"nome": "📝 Diário de Emoções", "descricao": "Registrar gatilhos emocionais", "xp": 15},
            {"nome": "💬 Feedback Construtivo", "descricao": "Dar feedback usando técnica SBI", "xp": 35},
            {"nome": "🙏 Reconhecer Erro", "descricao": "Admitir erro e pedir desculpas", "xp": 30},
            {"nome": "🎯 Definir Limites", "descricao": "Dizer não de forma assertiva", "xp": 40}
        ]
    },
    "Pensamento Crítico e Resolução de Problemas": {
        "descricao": "Capacidade de analisar problemas complexos e encontrar soluções criativas.",
        "atividades": [
            {"nome": "🔍 Análise de Causa Raiz", "descricao": "Aplicar técnica 5 Porquês", "xp": 35},
            {"nome": "🧠 Brainstorming", "descricao": "Gerar soluções com a equipe", "xp": 25},
            {"nome": "📊 Análise de Dados", "descricao": "Usar dados para tomar decisão", "xp": 40},
            {"nome": "🎯 Matriz de Decisão", "descricao": "Avaliar opções com critérios", "xp": 30},
            {"nome": "⚡ Solução Criativa", "descricao": "Implementar solução não óbvia", "xp": 50},
            {"nome": "📚 Estudar Caso", "descricao": "Analisar case de sucesso/fracasso", "xp": 25}
        ]
    }
}

# =========================
# CONTEÚDO DAS CERTIFICAÇÕES (COMPLETO)
# =========================
CONTEUDO_CERTIFICACOES = {
    "AZ-900": {
        "titulo": "Microsoft Azure Fundamentals",
        "descricao": "Certificação de entrada para Azure. Valida conhecimentos básicos de cloud computing e serviços Azure.",
        "dominios": [
            {"nome": "Descrever conceitos de nuvem (25-30%)", "topicos": [
                "Benefícios da nuvem (alta disponibilidade, escalabilidade, elasticidade)",
                "Modelos de serviço (IaaS, PaaS, SaaS)",
                "Modelos de implantação (pública, privada, híbrida)",
                "CAPEX vs OPEX"
            ]},
            {"nome": "Descrever serviços principais do Azure (20-25%)", "topicos": [
                "Computação (VMs, Containers, Functions)",
                "Redes (VNet, VPN, Load Balancer)",
                "Armazenamento (Blob, File, Queue, Table)",
                "Banco de dados (Cosmos DB, SQL Database)"
            ]},
            {"nome": "Descrever soluções de segurança (15-20%)", "topicos": [
                "Segurança de rede (NSG, Firewall)",
                "Identidade (Azure AD, MFA)",
                "Proteção de dados (encryption, Key Vault)",
                "Conformidade (Policy, Blueprints)"
            ]},
            {"nome": "Descrever gerenciamento e governança (10-15%)", "topicos": [
                "Cost Management",
                "Resource Groups e Tags",
                "Azure Monitor",
                "Azure Advisor"
            ]}
        ],
        "recursos": ["Microsoft Learn - AZ-900 Learning Path", "YouTube - John Savill", "GitHub - Microsoft Learning"],
        "simulados": ["Microsoft Learn - Assessment", "ExamTopics", "Udemy - Simulados"],
        "semanas": 3, "horas": 30, "custo": "$99 (~R$ 515)", "voucher": True
    },
    "SC-900": {
        "titulo": "Microsoft Security, Compliance, and Identity Fundamentals",
        "descricao": "Certificação sobre conceitos de segurança, compliance e identidade na Microsoft.",
        "dominios": [
            {"nome": "Descrever conceitos de segurança (25-30%)", "topicos": [
                "Zero Trust", "Defesa em profundidade", "Responsabilidade compartilhada", "Criptografia e hashing"
            ]},
            {"nome": "Descrever capacidades de identidade (35-40%)", "topicos": [
                "Azure AD e identidades híbridas", "MFA e Conditional Access", "Identity Protection", "Privileged Identity Management (PIM)"
            ]},
            {"nome": "Descrever capacidades de segurança (20-25%)", "topicos": [
                "Microsoft Defender para nuvem", "Microsoft Sentinel", "Defender para endpoint", "Defender para Office 365"
            ]},
            {"nome": "Descrever capacidades de compliance (10-15%)", "topicos": [
                "Service Trust Portal", "Compliance Manager", "Azure Policy", "LGPD e GDPR"
            ]}
        ],
        "recursos": ["Microsoft Learn - SC-900 Learning Path", "YouTube - John Savill", "Microsoft Security Documentation"],
        "simulados": ["Microsoft Learn - Assessment", "ExamTopics", "Whizlabs"],
        "semanas": 2, "horas": 25, "custo": "$99 (~R$ 515)", "voucher": True
    },
    "AWS Cloud Practitioner": {
        "titulo": "AWS Cloud Practitioner",
        "descricao": "Certificação fundamental da AWS, valida conhecimentos básicos de cloud computing na maior plataforma do mundo.",
        "dominios": [
            {"nome": "Conceitos de Nuvem (20%)", "topicos": [
                "Benefícios da AWS (escalabilidade, elasticidade, pay-as-you-go)",
                "Modelos de implantação (nuvem, híbrida, on-premise)",
                "Modelos de serviço (IaaS, PaaS, SaaS)",
                "AWS Global Infrastructure (Regiões, Zonas de Disponibilidade)"
            ]},
            {"nome": "Serviços Principais da AWS (30%)", "topicos": [
                "Computação (EC2, Lambda, Elastic Beanstalk)",
                "Armazenamento (S3, EBS, EFS, Glacier)",
                "Banco de dados (RDS, DynamoDB, Redshift)",
                "Redes (VPC, CloudFront, Route 53)"
            ]},
            {"nome": "Segurança e Conformidade (25%)", "topicos": [
                "Modelo de responsabilidade compartilhada",
                "IAM (Identity and Access Management)",
                "AWS Shield, WAF, KMS",
                "Conformidade (Artifacts, Config, CloudTrail)"
            ]},
            {"nome": "Preços e Suporte (15%)", "topicos": [
                "Modelos de precificação (On-Demand, Reserved, Spot)",
                "AWS Pricing Calculator",
                "Planos de suporte (Basic, Developer, Business, Enterprise)",
                "AWS Organizations e Consolidated Billing"
            ]},
            {"nome": "Tecnologias Principais (10%)", "topicos": [
                "Machine Learning (Rekognition, Comprehend)",
                "IoT Core", "Serverless (API Gateway, Step Functions)", "DevOps (CodePipeline, CodeBuild)"
            ]}
        ],
        "recursos": ["AWS Skill Builder (gratuito)", "YouTube - Stephane Maarek", "AWS Free Tier", "ExamPro"],
        "simulados": ["AWS Official Practice Exam", "TutorialsDojo", "Udemy - Practice Exams"],
        "semanas": 4, "horas": 30, "custo": "$100 (~R$ 520)", "voucher": True
    },
    "Security+": {
        "titulo": "CompTIA Security+ (SY0-701)",
        "descricao": "Certificação fundamental de cibersegurança, reconhecida mundialmente.",
        "dominios": [
            {"nome": "Ameaças, Ataques e Vulnerabilidades (24%)", "topicos": [
                "Tipos de malware (vírus, worm, ransomware, trojan)",
                "Ataques de rede (DoS, DDoS, MITM, DNS poisoning)",
                "Ataques de aplicação (SQL Injection, XSS, CSRF)",
                "Ameaças internas e externas", "Vulnerabilidades comuns (OWASP Top 10)"
            ]},
            {"nome": "Tecnologias e Ferramentas de Segurança (26%)", "topicos": [
                "Firewalls (NGFW, WAF)", "IDS/IPS (Signature, Anomaly)", "SIEM", "Criptografia simétrica e assimétrica",
                "PKI e certificados digitais", "MFA e autenticação forte", "EDR, DLP, UTM"
            ]},
            {"nome": "Arquitetura e Design de Segurança (21%)", "topicos": [
                "Zero Trust Architecture", "Defesa em profundidade", "Segurança em nuvem (IaaS, PaaS, SaaS)",
                "Segurança de redes (segmentação, VLAN)", "Segurança de endpoints (hardening)", "Redundância e alta disponibilidade"
            ]},
            {"nome": "Gestão de Identidade e Acesso (16%)", "topicos": [
                "IAM fundamentals", "SSO e federação", "RBAC, ABAC, DAC, MAC",
                "Kerberos, RADIUS, LDAP", "Contas privilegiadas (PAM)", "JIT e JEA"
            ]},
            {"nome": "Gestão de Riscos e Compliance (13%)", "topicos": [
                "Análise de risco (qualitativa/quantitativa)", "BCP e DRP (RTO, RPO, MTD)",
                "Planos de resposta a incidentes", "LGPD, GDPR, HIPAA, PCI-DSS", "Forensics e cadeia de custódia", "Tipos de controles"
            ]}
        ],
        "recursos": ["YouTube - Professor Messer", "CompTIA Security+ SY0-701 Objectives", "GitHub - Security+ Study Guide"],
        "simulados": ["ExamCompass", "Professor Messer Practice Exams", "Jason Dion (Udemy)", "MeasureUp"],
        "semanas": 10, "horas": 80, "custo": "$392 (~R$ 2.040)", "voucher": False
    },
    "Scrum Fundamentals": {
        "titulo": "Scrum Fundamentals Certified (SFC)",
        "descricao": "Certificação básica de Scrum, metodologia ágil para gestão de projetos.",
        "dominios": [
            {"nome": "Fundamentos do Scrum (30%)", "topicos": [
                "Manifesto Ágil e seus 4 valores", "Os 12 princípios ágeis", "Scrum vs Waterfall", "Benefícios da metodologia ágil"
            ]},
            {"nome": "Papéis do Scrum (25%)", "topicos": [
                "Product Owner (responsabilidades)", "Scrum Master (facilitador)",
                "Development Team (auto-organização)", "Características de times de alta performance"
            ]},
            {"nome": "Eventos Scrum (25%)", "topicos": [
                "Sprint Planning (planejamento)", "Daily Scrum (15 minutos)",
                "Sprint Review (demonstração)", "Sprint Retrospective (melhoria contínua)"
            ]},
            {"nome": "Artefatos Scrum (20%)", "topicos": [
                "Product Backlog (priorização)", "Sprint Backlog (compromisso da sprint)",
                "Increment (entregável)", "Definição de Pronto (DoD) e Definição de Feito"
            ]]
        ],
        "recursos": ["Scrum Guide (gratuito)", "YouTube - Scrum Framework", "Scrum.org - Open Assessments"],
        "simulados": ["Scrum.org Open Assessment", "ScrumStudy.com Practice Tests", "Udemy - Mock Exams"],
        "semanas": 1, "horas": 16, "custo": "R$ 500-800", "voucher": False
    },
    "Power BI": {
        "titulo": "Microsoft Power BI Data Analyst (PL-900)",
        "descricao": "Certificação para análise e visualização de dados com Power BI.",
        "dominios": [
            {"nome": "Preparação de Dados (20%)", "topicos": [
                "Power Query (ETL)", "Limpeza e transformação de dados", "Tratamento de erros e nulos", "Combinação de tabelas"
            ]},
            {"nome": "Modelagem de Dados (25%)", "topicos": [
                "Modelos star e snowflake", "Relacionamentos entre tabelas", "Medidas e colunas calculadas (DAX)", "Hierarquias e roles"
            ]},
            {"nome": "Visualização de Dados (30%)", "topicos": [
                "Gráficos e visuais básicos", "Dashboards interativos", "Drill-through e drill-down", "Bookmarks e botões"
            ]},
            {"nome": "Análise de Dados (15%)", "topicos": [
                "Funções DAX (CALCULATE, FILTER)", "Inteligência de tempo (YTD, MTD)", "Segmentação de dados", "Quick measures"
            ]},
            {"nome": "Implantação e Manutenção (10%)", "topicos": [
                "Publicação no Service", "Gateways e atualização de dados", "Row-Level Security (RLS)", "Workspaces e apps"
            ]}
        ],
        "recursos": ["Hashtag Treinamentos", "Microsoft Learn - PL-900 Path", "YouTube - SQLBI"],
        "simulados": ["Microsoft Learn Assessment", "ExamTopics", "MeasureUp"],
        "semanas": 6, "horas": 50, "custo": "$99 (~R$ 515)", "voucher": False
    },
    "Python": {
        "titulo": "Python para Análise de Dados",
        "descricao": "Linguagem Python aplicada à automação e análise de dados.",
        "dominios": [
            {"nome": "Fundamentos de Python (25%)", "topicos": [
                "Sintaxe básica", "Estruturas de controle", "Funções e módulos", "Listas, tuplas, dicionários, sets"
            ]},
            {"nome": "Manipulação de Dados (30%)", "topicos": [
                "Pandas (DataFrame, Series)", "Leitura de arquivos", "Filtros, agregações e merges", "Tratamento de dados nulos"
            ]},
            {"nome": "Visualização de Dados (20%)", "topicos": [
                "Matplotlib", "Seaborn", "Plotly"
            ]},
            {"nome": "Automação (25%)", "topicos": [
                "Automação de planilhas", "Envio de e-mails", "Web scraping", "APIs"
            ]}
        ],
        "recursos": ["Hashtag Treinamentos", "Curso em Vídeo (Guanabara)", "DataCamp"],
        "simulados": ["HackerRank", "LeetCode", "Python Institute"],
        "semanas": 8, "horas": 60, "custo": "R$ 650 (Hashtag anual)", "voucher": False
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Linguagem SQL para consultas e manipulação de bancos de dados.",
        "dominios": [
            {"nome": "Consultas Básicas (30%)", "topicos": [
                "SELECT, FROM, WHERE", "ORDER BY, LIMIT, DISTINCT", "Operadores (LIKE, IN, BETWEEN)", "Funções de agregação"
            ]},
            {"nome": "Joins e Subconsultas (30%)", "topicos": [
                "INNER, LEFT, RIGHT, FULL JOIN", "Self JOIN e CROSS JOIN", "Subconsultas correlacionadas", "CTEs"
            ]},
            {"nome": "Manipulação de Dados (20%)", "topicos": [
                "INSERT, UPDATE, DELETE", "CREATE, ALTER, DROP", "Índices e chaves", "Transações"
            ]},
            {"nome": "Funções Avançadas (20%)", "topicos": [
                "Window Functions", "GROUP BY e HAVING", "Funções de string e data", "Stored Procedures e Views"
            ]}
        ],
        "recursos": ["Hashtag Treinamentos", "SQLZoo", "Mode Analytics SQL Tutorial"],
        "simulados": ["HackerRank - SQL", "LeetCode - Database", "StrataScratch"],
        "semanas": 6, "horas": 45, "custo": "R$ 650 (Hashtag anual)", "voucher": False
    }
}

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES (COMPLETO)
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026},
    "AWS Cloud Practitioner": {"emblema": "☁️📘", "cor": "#FF9900", "titulo": "AWS Cloud Practitioner", "xp": 100, "ano": 2027},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027},
    "Scrum Fundamentals": {"emblema": "🔄📋", "cor": "#0A5C4A", "titulo": "Scrum Fundamentals", "xp": 60, "ano": 2026},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026},
    "ISO 27001 Fundamentals": {"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation", "xp": 100, "ano": 2026},
    "CCNA": {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA", "xp": 150, "ano": 2027},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027},
    "AWS Solutions Architect": {"emblema": "☁️🏗️", "cor": "#FF9900", "titulo": "AWS Solutions Architect", "xp": 180, "ano": 2028},
    "PSM I": {"emblema": "🔄🎓", "cor": "#0A5C4A", "titulo": "Professional Scrum Master", "xp": 100, "ano": 2027},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo"}
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
if "soft_skills_concluidas" not in st.session_state:
    st.session_state.soft_skills_concluidas = {}
if "cert_topicos_concluidos" not in st.session_state:
    st.session_state.cert_topicos_concluidos = {}

# =========================
# FUNÇÕES DE BACKUP
# =========================
ARQUIVO_BACKUP = "backup_diario.json"

def salvar_backup():
    dados = {
        "db": st.session_state.db, "xp": st.session_state.xp,
        "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status,
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
# FUNÇÃO DE LOGIN
# =========================
def fazer_login():
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 40px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 20px; text-align: center;">
        <h1>🚀 MISSÃO CARREIRA</h1>
        <h3>Acesso Autorizado</h3>
    </div>
    """, unsafe_allow_html=True)
    usuario = st.text_input("👨‍🚀 Usuário")
    senha = st.text_input("🔒 Senha", type="password")
    if st.button("🚀 Entrar", use_container_width=True):
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos!")

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

st.title("🚀 MISSÃO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Cibersegurança | Pós-graduação PUC Minas")
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
    atividades_hoje = get_atividades_hoje()
    xp_hoje = sum(a['xp'] for a in atividades_hoje)
    st.markdown(f"**📅 Hoje:** {len(atividades_hoje)} atv | +{xp_hoje} XP")
    st.markdown(f"**📆 Semana:** +{get_xp_semana()} XP")
    st.markdown(f"**📅 Mês:** +{get_xp_mes()} XP")
    st.markdown("---")
    
    if st.button("📥 Backup Manual", use_container_width=True):
        salvar_backup()
        st.success("Backup salvo!")
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎮 Dashboard", "📚 Certificações", "💪 Soft Skills", "🎖️ Progresso", "🗺️ Roadmap"])

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
        st.info("✨ Nenhuma atividade hoje. Comece agora!")
    
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
    c1.metric("🎮 Missões", len(st.session_state.db))
    c2.metric("⭐ XP", st.session_state.xp)
    c3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
    c4.metric("✅ Certificações", f"{concluidas}/{len(EMBLEMAS)}")
    c5.metric("📊 Progresso", f"{(concluidas/len(EMBLEMAS)*100):.0f}%")

# =========================
# TAB 2 - CERTIFICAÇÕES (CONTEÚDO DETALHADO)
# =========================
with tab2:
    st.markdown("## 📚 PLANO DE ESTUDOS POR CERTIFICAÇÃO")
    cert_selecionada = st.selectbox("🎯 Selecione a certificação", list(CONTEUDO_CERTIFICACOES.keys()))
    
    if cert_selecionada in CONTEUDO_CERTIFICACOES:
        info = CONTEUDO_CERTIFICACOES[cert_selecionada]
        emblema = EMBLEMAS.get(cert_selecionada, {}).get('emblema', '📌')
        
        st.markdown(f"""
        <div class="cert-card">
            <h2>{emblema} {cert_selecionada}</h2>
            <h3>{info['titulo']}</h3>
            <p>{info['descricao']}</p>
            <p><strong>⏱️ Duração estimada:</strong> {info['semanas']} semanas ({info['horas']} horas)</p>
            <p><strong>💰 Custo da prova:</strong> {info['custo']}</p>
            <p><strong>🎟️ Voucher grátis:</strong> {'✅ Sim' if info.get('voucher', False) else '❌ Não'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📖 Domínios e Tópicos", "🎓 Recursos", "📝 Simulados"])
        
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
            st.markdown("### 🎓 Recursos Gratuitos")
            for recurso in info['recursos']:
                st.markdown(f"- 📹 {recurso}")
        
        with sub_tab3:
            st.markdown("### 📝 Simulados Recomendados")
            for simulado in info['simulados']:
                st.markdown(f"- ✅ {simulado}")
            st.markdown("---")
            st.markdown("### 🎯 Dicas para a Prova")
            st.markdown("1. Faça simulados até atingir 85%+ de acertos")
            st.markdown("2. Revise os tópicos que você errou")
            st.markdown("3. Marque a prova com 2-3 semanas de antecedência")

# =========================
# TAB 3 - SOFT SKILLS
# =========================
with tab3:
    st.markdown("## 💪 DESENVOLVIMENTO DE SOFT SKILLS")
    st.markdown("Atividades práticas para desenvolver habilidades comportamentais essenciais para liderança.")
    
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
                            st.success(f"+{atividade['xp']} XP - {atividade['nome']} concluída!")
                            st.rerun()
                        else:
                            st.info("Você já concluiu esta atividade hoje!")
                    st.caption(f"📝 {atividade['descricao']}")

# =========================
# TAB 4 - PROGRESSO DAS CERTIFICAÇÕES
# =========================
with tab4:
    st.markdown("## 🎖️ PROGRESSO DAS CERTIFICAÇÕES")
    filtro = st.selectbox("🔍 Filtrar por status", ["Todas", "Em andamento", "Concluída", "Não iniciada"])
    
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
                progresso = min(xp / info["xp"], 1.0)
                classe = "cert-card atrasado" if atrasado else "cert-card"
                with cols[j]:
                    st.markdown(f'<div class="{classe}"><div style="text-align:center; font-size:32px;">{info["emblema"]}</div><div style="font-weight:bold; text-align:center; font-size:11px;">{cert[:20]}</div><div style="text-align:center; font-size:24px;">{get_badge(status)}</div><div style="text-align:center; font-size:10px;">{xp}/{info["xp"]} XP</div></div>', unsafe_allow_html=True)
                    st.progress(progresso)
                    opcoes = ["Não iniciada", "Em andamento", "Concluída"]
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
    st.markdown("## 🗺️ ROADMAP ESTRATÉGICO 2026-2029")
    
    roadmap = {
        2026: {"titulo": "🌱 FUNDAÇÃO", "certs": ["AZ-900", "SC-900", "Scrum Fundamentals", "Power BI", "Python", "SQL", "ISO 27001 Fundamentals", "Pos-graduacao"]},
        2027: {"titulo": "⚡ ESPECIALIZAÇÃO", "certs": ["AWS Cloud Practitioner", "Security+", "CCNA", "CySA+", "PSM I"]},
        2028: {"titulo": "🎯 MAESTRIA TÉCNICA", "certs": ["AWS Solutions Architect", "GICSP"]},
        2029: {"titulo": "👑 LIDERANÇA", "certs": ["CISSP", "Ingles"]}
    }
    
    for ano, info in roadmap.items():
        with st.expander(f"{info['titulo']} - {ano}", expanded=(ano == 2026)):
            cols = st.columns(4)
            for i, cert in enumerate(info['certs']):
                if cert in EMBLEMAS:
                    emblema = EMBLEMAS[cert]
                    status = st.session_state.cert_status.get(cert, "Não iniciada")
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
    
    st.markdown("---")
    st.markdown("### 📊 PROJEÇÃO SALARIAL")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hoje (2026)", "R$ 7.500", "Técnico Sênior")
    col2.metric("Dez/2026", "R$ 10-11k", "+ Security+")
    col3.metric("2027", "R$ 13-18k", "+ CySA+ + AWS")
    col4.metric("2028/2029", "R$ 20-30k", "+ GICSP + CISSP")

st.caption("🚀 Continue sua jornada, o universo te espera!")
