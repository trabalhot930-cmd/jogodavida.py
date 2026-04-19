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
# SOFT SKILLS - ATIVIDADES PRÁTICAS (NOVO)
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
# CONTEÚDO DAS CERTIFICAÇÕES (ADICIONADO AWS e Scrum)
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
        "recursos": [
            "Microsoft Learn - AZ-900 Learning Path (grátis)",
            "YouTube - John Savill (AZ-900 Playlist)",
            "GitHub - Microsoft Learning"
        ],
        "simulados": [
            "Microsoft Learn - Assessment gratuito",
            "ExamTopics - Questões gratuitas",
            "Udemy - Simulados (promoção)"
        ],
        "semanas": 3, "horas": 30, "custo": "$99", "voucher": True
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
        "recursos": [
            "Microsoft Learn - SC-900 Learning Path",
            "YouTube - John Savill",
            "Microsoft Security Documentation"
        ],
        "simulados": [
            "Microsoft Learn - Assessment",
            "ExamTopics",
            "Whizlabs"
        ],
        "semanas": 2, "horas": 25, "custo": "$99", "voucher": True
    },
    "AWS Cloud Practitioner": {
        "titulo": "AWS Cloud Practitioner",
        "descricao": "Certificação fundamental da AWS, valida conhecimentos básicos de cloud computing.",
        "dominios": [
            {"nome": "Conceitos de Nuvem (20%)", "topicos": [
                "Benefícios da AWS", "Modelos de implantação",
                "Modelos de serviço", "Infraestrutura global AWS"
            ]},
            {"nome": "Serviços Principais da AWS (30%)", "topicos": [
                "Computação (EC2, Lambda)", "Armazenamento (S3, EBS)",
                "Banco de dados (RDS, DynamoDB)", "Redes (VPC, CloudFront)"
            ]},
            {"nome": "Segurança e Conformidade (25%)", "topicos": [
                "Modelo de responsabilidade compartilhada", "IAM",
                "AWS Shield, WAF", "Conformidade"
            ]},
            {"nome": "Preços e Suporte (15%)", "topicos": [
                "Modelos de precificação", "AWS Pricing Calculator",
                "Planos de suporte", "AWS Organizations"
            ]},
            {"nome": "Tecnologias Principais (10%)", "topicos": [
                "Machine Learning", "IoT", "Serverless", "DevOps"
            ]}
        ],
        "recursos": [
            "AWS Skill Builder (gratuito)",
            "YouTube - Stephane Maarek",
            "AWS Free Tier"
        ],
        "simulados": [
            "AWS Official Practice Exam",
            "TutorialsDojo",
            "Udemy"
        ],
        "semanas": 4, "horas": 30, "custo": "$100", "voucher": True
    },
    "Security+": {
        "titulo": "CompTIA Security+ (SY0-701)",
        "descricao": "Certificação fundamental de cibersegurança, reconhecida mundialmente.",
        "dominios": [
            {"nome": "Ameaças, Ataques e Vulnerabilidades (24%)", "topicos": [
                "Tipos de malware (vírus, worm, ransomware, trojan)",
                "Ataques de rede (DoS, DDoS, MITM, DNS poisoning)",
                "Ataques de aplicação (SQL Injection, XSS, CSRF)",
                "Ameaças internas e externas",
                "Vulnerabilidades comuns (OWASP Top 10)"
            ]},
            {"nome": "Tecnologias e Ferramentas de Segurança (26%)", "topicos": [
                "Firewalls (NGFW, WAF)", "IDS/IPS (Signature, Anomaly)", "SIEM (Security Information and Event Management)",
                "Criptografia simétrica e assimétrica", "PKI e certificados digitais", "MFA e autenticação forte",
                "EDR, DLP, UTM"
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
        "recursos": [
            "YouTube - Professor Messer (playlist completa - grátis)",
            "CompTIA Security+ SY0-701 Objectives (PDF oficial)",
            "GitHub - Security+ Study Guide"
        ],
        "simulados": [
            "ExamCompass (gratuito)",
            "Professor Messer Practice Exams",
            "Jason Dion (Udemy)",
            "MeasureUp (pago)"
        ],
        "semanas": 10, "horas": 80, "custo": "$392", "voucher": False
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
            ]}
        ],
        "recursos": [
            "Scrum Guide (gratuito)",
            "YouTube - Scrum Framework",
            "Scrum.org - Open Assessments"
        ],
        "simulados": [
            "Scrum.org Open Assessment (gratuito)",
            "ScrumStudy.com Practice Tests",
            "Udemy - Mock Exams"
        ],
        "semanas": 1, "horas": 16, "custo": "R$ 500", "voucher": False
    },
    "CySA+": {
        "titulo": "CompTIA CySA+ (CS0-003)",
        "descricao": "Certificação de análise de segurança e resposta a incidentes.",
        "dominios": [
            {"nome": "Segurança de Software e Sistemas (22%)", "topicos": [
                "Secure Software Development Lifecycle (SSDLC)", "SAST, DAST, IAST",
                "DevSecOps e CI/CD security", "Análise de vulnerabilidades"
            ]},
            {"nome": "Operações de Segurança e Monitoramento (25%)", "topicos": [
                "SIEM (configuração, correlação, análise)", "SOAR (automação e orquestração)",
                "Log management e análise", "Threat hunting"
            ]},
            {"nome": "Inteligência de Ameaças (20%)", "topicos": [
                "Threat Intelligence (TIP, STIX, TAXII)", "MITRE ATT&CK Framework",
                "Indicadores de comprometimento (IoC)", "Threat modeling"
            ]},
            {"nome": "Resposta a Incidentes (18%)", "topicos": [
                "Ciclo de vida da resposta a incidentes (NIST)", "Playbooks e runbooks",
                "Forensics e análise de malware", "Comunicação e relatórios"
            ]},
            {"nome": "Gestão de Vulnerabilidades (15%)", "topicos": [
                "Scanning e assessment", "Vulnerability management lifecycle",
                "Patch management", "Relatórios e priorização"
            ]}
        ],
        "recursos": [
            "YouTube - Certify Breakfast",
            "CompTIA CySA+ Objectives PDF",
            "TryHackMe (SOC Level 1)"
        ],
        "simulados": [
            "Jason Dion (Udemy)",
            "Sybex Practice Tests",
            "ExamCompass"
        ],
        "semanas": 8, "horas": 60, "custo": "$392", "voucher": False
    },
    "Power BI": {
        "titulo": "Microsoft Power BI Data Analyst (PL-900)",
        "descricao": "Certificação para análise e visualização de dados com Power BI.",
        "dominios": [
            {"nome": "Preparação de Dados (20%)", "topicos": [
                "Power Query (ETL)", "Limpeza e transformação de dados",
                "Tratamento de erros e nulos", "Combinação de tabelas (Merge/Append)"
            ]},
            {"nome": "Modelagem de Dados (25%)", "topicos": [
                "Modelos star e snowflake", "Relacionamentos entre tabelas",
                "Medidas e colunas calculadas (DAX)", "Hierarquias e roles"
            ]},
            {"nome": "Visualização de Dados (30%)", "topicos": [
                "Gráficos e visuais básicos", "Dashboards interativos",
                "Drill-through e drill-down", "Bookmarks e botões"
            ]},
            {"nome": "Análise de Dados (15%)", "topicos": [
                "Funções DAX (CALCULATE, FILTER)", "Inteligência de tempo (YTD, MTD)",
                "Segmentação de dados", "Quick measures"
            ]},
            {"nome": "Implantação e Manutenção (10%)", "topicos": [
                "Publicação no Service", "Gateways e atualização de dados",
                "Row-Level Security (RLS)", "Workspaces e apps"
            ]}
        ],
        "recursos": [
            "Hashtag Treinamentos (curso completo)",
            "Microsoft Learn - PL-900 Path",
            "YouTube - SQLBI (DAX avançado)"
        ],
        "simulados": [
            "Microsoft Learn Assessment",
            "ExamTopics",
            "MeasureUp"
        ],
        "semanas": 6, "horas": 50, "custo": "$99", "voucher": False
    },
    "Python": {
        "titulo": "Python para Análise de Dados",
        "descricao": "Linguagem Python aplicada à automação e análise de dados.",
        "dominios": [
            {"nome": "Fundamentos de Python (25%)", "topicos": [
                "Sintaxe básica (variáveis, tipos, operadores)", "Estruturas de controle (if, for, while)",
                "Funções e módulos", "Listas, tuplas, dicionários, sets"
            ]},
            {"nome": "Manipulação de Dados (30%)", "topicos": [
                "Biblioteca Pandas (DataFrame, Series)", "Leitura de arquivos (CSV, Excel, JSON)",
                "Filtros, agregações e merges", "Tratamento de dados nulos"
            ]},
            {"nome": "Visualização de Dados (20%)", "topicos": [
                "Matplotlib (gráficos básicos)", "Seaborn (gráficos estatísticos)", "Plotly (gráficos interativos)"
            ]},
            {"nome": "Automação (25%)", "topicos": [
                "Automação de planilhas", "Envio de e-mails automáticos",
                "Web scraping (BeautifulSoup)", "APIs (requests)"
            ]}
        ],
        "recursos": [
            "Hashtag Treinamentos - Python Impressionador",
            "Curso em Vídeo (Guanabara - grátis)",
            "DataCamp - Python for Data Science"
        ],
        "simulados": [
            "HackerRank - Python Challenges",
            "LeetCode - Python",
            "Python Institute (PCAP)"
        ],
        "semanas": 8, "horas": 60, "custo": "R$ 650", "voucher": False
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Linguagem SQL para consultas e manipulação de bancos de dados.",
        "dominios": [
            {"nome": "Consultas Básicas (30%)", "topicos": [
                "SELECT, FROM, WHERE", "ORDER BY, LIMIT, DISTINCT",
                "Operadores (LIKE, IN, BETWEEN)", "Funções de agregação (COUNT, SUM, AVG)"
            ]},
            {"nome": "Joins e Subconsultas (30%)", "topicos": [
                "INNER, LEFT, RIGHT, FULL JOIN", "Self JOIN e CROSS JOIN",
                "Subconsultas correlacionadas", "CTEs (Common Table Expressions)"
            ]},
            {"nome": "Manipulação de Dados (20%)", "topicos": [
                "INSERT, UPDATE, DELETE", "CREATE, ALTER, DROP",
                "Índices e chaves", "Transações (COMMIT, ROLLBACK)"
            ]},
            {"nome": "Funções Avançadas (20%)", "topicos": [
                "Window Functions (ROW_NUMBER, RANK)", "GROUP BY e HAVING",
                "Funções de string e data", "Stored Procedures e Views"
            ]}
        ],
        "recursos": [
            "Hashtag Treinamentos - SQL Impressionador",
            "SQLZoo (interativo e grátis)",
            "Mode Analytics SQL Tutorial"
        ],
        "simulados": [
            "HackerRank - SQL",
            "LeetCode - Database",
            "StrataScratch"
        ],
        "semanas": 6, "horas": 45, "custo": "R$ 650", "voucher": False
    },
    "CISSP": {
        "titulo": "Certified Information Systems Security Professional",
        "descricao": "Certificação mais reconhecida globalmente em cibersegurança.",
        "dominios": [
            {"nome": "Security and Risk Management (15%)", "topicos": [
                "Confidencialidade, Integridade, Disponibilidade", "Governança e compliance",
                "Gestão de riscos", "LGPD, GDPR, HIPAA"
            ]},
            {"nome": "Asset Security (10%)", "topicos": [
                "Classificação de dados", "Retenção e destruição", "Handling de dados sensíveis"
            ]},
            {"nome": "Security Architecture and Engineering (13%)", "topicos": [
                "Arquitetura de segurança", "Criptografia e PKI", "Modelos de segurança"
            ]},
            {"nome": "Communication and Network Security (13%)", "topicos": [
                "Segurança de redes", "Protocolos seguros (TLS, IPsec)", "Segurança sem fio"
            ]},
            {"nome": "Identity and Access Management (13%)", "topicos": [
                "IAM, SSO, MFA", "Federacão de identidades", "Privileged Access Management"
            ]},
            {"nome": "Security Assessment and Testing (12%)", "topicos": [
                "Testes de penetração", "Análise de vulnerabilidades", "Auditoria de segurança"
            ]},
            {"nome": "Security Operations (13%)", "topicos": [
                "Resposta a incidentes", "BCP e DRP", "Forensics e investigação"
            ]},
            {"nome": "Software Development Security (11%)", "topicos": [
                "DevSecOps", "Segurança em SDLC", "OWASP Top 10"
            ]}
        ],
        "recursos": [
            "ISC2 Official Study Guide",
            "YouTube - Destination Certification",
            "LinkedIn Learning - CISSP Prep"
        ],
        "simulados": [
            "ISC2 Official Practice Tests",
            "Boson",
            "Pocket Prep"
        ],
        "semanas": 16, "horas": 200, "custo": "$749", "voucher": False
    },
    "GICSP": {
        "titulo": "Global Industrial Cyber Security Professional",
        "descricao": "Certificação especializada em segurança de sistemas industriais (OT/ICS).",
        "dominios": [
            {"nome": "OT/ICS Fundamentals (25%)", "topicos": [
                "Arquitetura ICS (PLC, SCADA, DCS, HMI, RTU)", "Protocolos industriais (Modbus, DNP3, OPC, PROFINET)",
                "Histórico e evolução de ataques industriais (Stuxnet, Triton)", "Diferenças entre TI e OT"
            ]},
            {"nome": "Riscos e Vulnerabilidades em OT (20%)", "topicos": [
                "Análise de risco em ambientes industriais", "Vulnerabilidades comuns em ICS",
                "Threat modeling para OT", "MITRE ATT&CK for ICS"
            ]},
            {"nome": "Segurança de Rede Industrial (20%)", "topicos": [
                "Segmentação de redes (DMZ industrial)", "Firewalls industriais e unidirecionais",
                "Network monitoring para OT", "Zona e conduits (IEC 62443)"
            ]},
            {"nome": "Controles de Segurança para OT (20%)", "topicos": [
                "Hardening de PLCs e RTUs", "Controle de acesso em sistemas industriais",
                "Patch management em OT", "Backup e recuperação industrial"
            ]},
            {"nome": "Resposta a Incidentes em OT (15%)", "topicos": [
                "Planos de resposta específicos para OT", "Forensics industrial",
                "Recuperação de sistemas críticos", "Exercícios de simulação"
            ]}
        ],
        "recursos": [
            "GIAC GICSP Official Course",
            "SANS ICS Security",
            "CISA ICS Training (gratuito)"
        ],
        "simulados": [
            "GIAC Practice Tests",
            "CyberSecurity Training (OT específico)"
        ],
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
        "ementa": "Fundamentos de arquitetura de segurança. Paradigma Zero Trust. Segurança em camadas.",
        "certificacoes": ["Security+", "CCNA"],
        "topicos": ["Zero Trust", "Defesa em profundidade", "Segurança em nuvem", "Firewalls", "IDS/IPS"],
        "horas": 60
    },
    "Gestão de Riscos Cibernéticos": {
        "ementa": "Fundamentos de riscos. ISO 27005. NIST Cybersecurity Framework.",
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
# STYLE (MANTIDO O MESMO DA REFERÊNCIA)
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
