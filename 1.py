import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import requests

# =========================
# CONFIGURAÇÃO SUPABASE
# =========================
SUPABASE_URL = "https://bhwqrfolkusuzvwavanc.supabase.co"
SUPABASE_KEY = "sb_publishable_J_z2LmOOVT0cmJuYhqW0qg_9iAEHt4u"
SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
REGISTRO_ID = "juan_felipe"

def carregar_do_supabase():
    try:
        url = f"{SUPABASE_URL}/rest/v1/progresso_juan?id=eq.{REGISTRO_ID}&select=dados"
        r = requests.get(url, headers=SUPABASE_HEADERS, timeout=10)
        if r.status_code == 200 and r.json():
            return r.json()[0]["dados"]
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar do Supabase: {e}")
    return None

def salvar_no_supabase(dados):
    try:
        url = f"{SUPABASE_URL}/rest/v1/progresso_juan"
        payload = {
            "id": REGISTRO_ID,
            "dados": dados,
            "atualizado_em": datetime.now().isoformat()
        }
        headers = {**SUPABASE_HEADERS, "Prefer": "resolution=merge-duplicates"}
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        return r.status_code in [200, 201]
    except Exception as e:
        st.warning(f"⚠️ Erro ao salvar no Supabase: {e}")
        return False

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
        "semanas": 3,
        "horas": 30
    },
    "SC-900": {
        "titulo": "Microsoft Security, Compliance, and Identity Fundamentals",
        "descricao": "Certificação sobre conceitos de segurança, compliance e identidade na Microsoft.",
        "dominios": [
            {"nome": "Descrever conceitos de segurança (25-30%)", "topicos": [
                "Zero Trust",
                "Defesa em profundidade",
                "Responsabilidade compartilhada",
                "Criptografia e hashing"
            ]},
            {"nome": "Descrever capacidades de identidade (35-40%)", "topicos": [
                "Azure AD e identidades híbridas",
                "MFA e Conditional Access",
                "Identity Protection",
                "Privileged Identity Management (PIM)"
            ]},
            {"nome": "Descrever capacidades de segurança (20-25%)", "topicos": [
                "Microsoft Defender para nuvem",
                "Microsoft Sentinel",
                "Defender para endpoint",
                "Defender para Office 365"
            ]},
            {"nome": "Descrever capacidades de compliance (10-15%)", "topicos": [
                "Service Trust Portal",
                "Compliance Manager",
                "Azure Policy",
                "LGPD e GDPR"
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
        "semanas": 2,
        "horas": 25
    },
    "AWS Cloud Practitioner": {
        "titulo": "AWS Cloud Practitioner",
        "descricao": "Certificação fundamental da AWS, valida conhecimentos básicos de cloud computing.",
        "dominios": [
            {"nome": "Conceitos de Nuvem (20%)", "topicos": [
                "Benefícios da AWS",
                "Modelos de implantação (nuvem, híbrida, on-premise)",
                "Modelos de serviço (IaaS, PaaS, SaaS)",
                "Infraestrutura global AWS"
            ]},
            {"nome": "Serviços Principais (30%)", "topicos": [
                "Computação (EC2, Lambda)",
                "Armazenamento (S3, EBS, EFS)",
                "Banco de dados (RDS, DynamoDB)",
                "Redes (VPC, CloudFront, Route 53)"
            ]},
            {"nome": "Segurança e Conformidade (25%)", "topicos": [
                "Modelo de responsabilidade compartilhada",
                "IAM (Identity and Access Management)",
                "AWS Shield, WAF, KMS",
                "Conformidade (Artifacts, Config, CloudTrail)"
            ]},
            {"nome": "Preços e Suporte (15%)", "topicos": [
                "Modelos de precificação",
                "AWS Pricing Calculator",
                "Planos de suporte",
                "AWS Organizations"
            ]},
            {"nome": "Tecnologias Principais (10%)", "topicos": [
                "Machine Learning",
                "IoT Core",
                "Serverless",
                "DevOps"
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
        "semanas": 4,
        "horas": 30
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
                "Firewalls (NGFW, WAF)",
                "IDS/IPS (Signature, Anomaly)",
                "SIEM (Security Information and Event Management)",
                "Criptografia simétrica e assimétrica",
                "PKI e certificados digitais",
                "MFA e autenticação forte",
                "EDR, DLP, UTM"
            ]},
            {"nome": "Arquitetura e Design de Segurança (21%)", "topicos": [
                "Zero Trust Architecture",
                "Defesa em profundidade",
                "Segurança em nuvem (IaaS, PaaS, SaaS)",
                "Segurança de redes (segmentação, VLAN)",
                "Segurança de endpoints (hardening)",
                "Redundância e alta disponibilidade"
            ]},
            {"nome": "Gestão de Identidade e Acesso (16%)", "topicos": [
                "IAM fundamentals",
                "SSO e federação",
                "RBAC, ABAC, DAC, MAC",
                "Kerberos, RADIUS, LDAP",
                "Contas privilegiadas (PAM)",
                "JIT e JEA"
            ]},
            {"nome": "Gestão de Riscos e Compliance (13%)", "topicos": [
                "Análise de risco (qualitativa/quantitativa)",
                "BCP e DRP (RTO, RPO, MTD)",
                "Planos de resposta a incidentes",
                "LGPD, GDPR, HIPAA, PCI-DSS",
                "Forensics e cadeia de custódia",
                "Tipos de controles (preventivo, detetivo, corretivo)"
            ]}
        ],
        "recursos": [
            "YouTube - Professor Messer (playlist completa - grátis)",
            "YouTube - Inside Cloud and Security",
            "CompTIA Security+ SY0-701 Objectives (PDF oficial)",
            "GitHub - Security+ Study Guide"
        ],
        "simulados": [
            "ExamCompass (gratuito)",
            "Professor Messer Practice Exams",
            "Jason Dion (Udemy)",
            "MeasureUp (pago)"
        ],
        "semanas": 10,
        "horas": 80
    },
    "Scrum Fundamentals": {
        "titulo": "Scrum Fundamentals Certified (SFC)",
        "descricao": "Certificação básica de Scrum, metodologia ágil para gestão de projetos.",
        "dominios": [
            {"nome": "Fundamentos do Scrum (30%)", "topicos": [
                "Manifesto Ágil e seus 4 valores",
                "Os 12 princípios ágeis",
                "Scrum vs Waterfall",
                "Benefícios da metodologia ágil"
            ]},
            {"nome": "Papéis do Scrum (25%)", "topicos": [
                "Product Owner (responsabilidades)",
                "Scrum Master (facilitador)",
                "Development Team (auto-organização)",
                "Características de times de alta performance"
            ]},
            {"nome": "Eventos Scrum (25%)", "topicos": [
                "Sprint Planning (planejamento)",
                "Daily Scrum (15 minutos)",
                "Sprint Review (demonstração)",
                "Sprint Retrospective (melhoria contínua)"
            ]},
            {"nome": "Artefatos Scrum (20%)", "topicos": [
                "Product Backlog (priorização)",
                "Sprint Backlog (compromisso da sprint)",
                "Increment (entregável)",
                "Definição de Pronto (DoD) e Definição de Feito"
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
        "semanas": 1,
        "horas": 16
    },
    "CySA+": {
        "titulo": "CompTIA CySA+ (CS0-003)",
        "descricao": "Certificação de análise de segurança e resposta a incidentes.",
        "dominios": [
            {"nome": "Segurança de Software e Sistemas (22%)", "topicos": [
                "Secure Software Development Lifecycle (SSDLC)",
                "SAST, DAST, IAST",
                "DevSecOps e CI/CD security",
                "Análise de vulnerabilidades"
            ]},
            {"nome": "Operações de Segurança e Monitoramento (25%)", "topicos": [
                "SIEM (configuração, correlação, análise)",
                "SOAR (automação e orquestração)",
                "Log management e análise",
                "Threat hunting"
            ]},
            {"nome": "Inteligência de Ameaças (20%)", "topicos": [
                "Threat Intelligence (TIP, STIX, TAXII)",
                "MITRE ATT&CK Framework",
                "Indicadores de comprometimento (IoC)",
                "Threat modeling"
            ]},
            {"nome": "Resposta a Incidentes (18%)", "topicos": [
                "Ciclo de vida da resposta a incidentes (NIST)",
                "Playbooks e runbooks",
                "Forensics e análise de malware",
                "Comunicação e relatórios"
            ]},
            {"nome": "Gestão de Vulnerabilidades (15%)", "topicos": [
                "Scanning e assessment",
                "Vulnerability management lifecycle",
                "Patch management",
                "Relatórios e priorização"
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
        "semanas": 8,
        "horas": 60
    },
    "ISO 27001 Fundamentals": {
        "titulo": "ISO 27001 Foundation",
        "descricao": "Fundamentos da norma de Sistema de Gestão de Segurança da Informação (SGSI).",
        "dominios": [
            {"nome": "Contexto da Organização (10%)", "topicos": [
                "Partes interessadas",
                "Escopo do SGSI",
                "Contexto interno e externo"
            ]},
            {"nome": "Liderança e Comprometimento (15%)", "topicos": [
                "Política de segurança da informação",
                "Responsabilidades da alta direção",
                "Papéis e responsabilidades"
            ]},
            {"nome": "Planejamento do SGSI (20%)", "topicos": [
                "Análise de riscos (ISO 31000)",
                "Avaliação e tratamento de riscos",
                "Declaração de Aplicabilidade (SoA)",
                "Plano de tratamento de riscos"
            ]},
            {"nome": "Suporte e Operação (25%)", "topicos": [
                "Recursos e competências",
                "Conscientização e treinamento",
                "Controles do Anexo A",
                "Gestão de incidentes"
            ]},
            {"nome": "Avaliação de Desempenho (15%)", "topicos": [
                "Monitoramento e medição",
                "Auditoria interna",
                "Análise crítica pela direção"
            ]},
            {"nome": "Melhoria Contínua (15%)", "topicos": [
                "Não conformidade e ação corretiva",
                "Melhoria contínua do SGSI"
            ]}
        ],
        "recursos": [
            "ISO 27001:2022 (norma oficial)",
            "ISO 27002 (controles)",
            "YouTube - ISACA Training",
            "NIST SP 800-53"
        ],
        "simulados": [
            "ExamTopics",
            "Udemy - Simulados ISO 27001"
        ],
        "semanas": 4,
        "horas": 40
    },
    "CCNA": {
        "titulo": "Cisco Certified Network Associate",
        "descricao": "Certificação fundamental de redes da Cisco.",
        "dominios": [
            {"nome": "Fundamentos de Rede (20%)", "topicos": [
                "Modelo OSI e TCP/IP",
                "Switching e VLANs",
                "IPv4 e IPv6 (sub-redes)",
                "Roteamento estático e dinâmico"
            ]},
            {"nome": "Acesso à Rede (20%)", "topicos": [
                "Spanning Tree Protocol (STP)",
                "EtherChannel",
                "Wireless LAN",
                "Cisco Discovery Protocol (CDP)"
            ]},
            {"nome": "Conectividade IP (25%)", "topicos": [
                "OSPF (Open Shortest Path First)",
                "Roteamento entre VLANs",
                "NAT (Network Address Translation)",
                "DHCP, DNS, NTP"
            ]},
            {"nome": "Serviços de IP (15%)", "topicos": [
                "ACLs (Access Control Lists)",
                "QoS (Quality of Service)",
                "Syslog, SNMP, NetFlow",
                "FHRP (HSRP, VRRP)"
            ]},
            {"nome": "Fundamentos de Segurança (15%)", "topicos": [
                "Segurança de dispositivos",
                "Port Security",
                "DHCP Snooping",
                "VPN e criptografia básica"
            ]},
            {"nome": "Automação e Programabilidade (5%)", "topicos": [
                "REST API e JSON",
                "Ansible, Puppet, Chef",
                "Modelos de dados (YANG)"
            ]}
        ],
        "recursos": [
            "YouTube - NetworkChuck",
            "YouTube - Jeremy's IT Lab",
            "Cisco Packet Tracer (gratuito)",
            "GNS3 (laboratórios)"
        ],
        "simulados": [
            "Boson ExSim (recomendado)",
            "AlphaPrep",
            "ExamTopics"
        ],
        "semanas": 12,
        "horas": 120
    },
    "Power BI": {
        "titulo": "Microsoft Power BI Data Analyst (PL-900)",
        "descricao": "Certificação para análise e visualização de dados com Power BI.",
        "dominios": [
            {"nome": "Preparação de Dados (20%)", "topicos": [
                "Power Query (ETL)",
                "Limpeza e transformação de dados",
                "Tratamento de erros e nulos",
                "Combinação de tabelas (Merge/Append)"
            ]},
            {"nome": "Modelagem de Dados (25%)", "topicos": [
                "Modelos star e snowflake",
                "Relacionamentos entre tabelas",
                "Medidas e colunas calculadas (DAX)",
                "Hierarquias e roles"
            ]},
            {"nome": "Visualização de Dados (30%)", "topicos": [
                "Gráficos e visuais básicos",
                "Dashboards interativos",
                "Drill-through e drill-down",
                "Bookmarks e botões"
            ]},
            {"nome": "Análise de Dados (15%)", "topicos": [
                "Funções DAX (CALCULATE, FILTER)",
                "Inteligência de tempo (YTD, MTD)",
                "Segmentação de dados",
                "Quick measures"
            ]},
            {"nome": "Implantação e Manutenção (10%)", "topicos": [
                "Publicação no Service",
                "Gateways e atualização de dados",
                "Row-Level Security (RLS)",
                "Workspaces e apps"
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
        "semanas": 6,
        "horas": 50
    },
    "Python": {
        "titulo": "Python para Análise de Dados",
        "descricao": "Linguagem Python aplicada à automação e análise de dados.",
        "dominios": [
            {"nome": "Fundamentos de Python (25%)", "topicos": [
                "Sintaxe básica (variáveis, tipos, operadores)",
                "Estruturas de controle (if, for, while)",
                "Funções e módulos",
                "Listas, tuplas, dicionários, sets"
            ]},
            {"nome": "Manipulação de Dados (30%)", "topicos": [
                "Biblioteca Pandas (DataFrame, Series)",
                "Leitura de arquivos (CSV, Excel, JSON)",
                "Filtros, agregações e merges",
                "Tratamento de dados nulos"
            ]},
            {"nome": "Visualização de Dados (20%)", "topicos": [
                "Matplotlib (gráficos básicos)",
                "Seaborn (gráficos estatísticos)",
                "Plotly (gráficos interativos)"
            ]},
            {"nome": "Automação (25%)", "topicos": [
                "Automação de planilhas",
                "Envio de e-mails automáticos",
                "Web scraping (BeautifulSoup)",
                "APIs (requests)"
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
        "semanas": 8,
        "horas": 60
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Linguagem SQL para consultas e manipulação de bancos de dados.",
        "dominios": [
            {"nome": "Consultas Básicas (30%)", "topicos": [
                "SELECT, FROM, WHERE",
                "ORDER BY, LIMIT, DISTINCT",
                "Operadores (LIKE, IN, BETWEEN)",
                "Funções de agregação (COUNT, SUM, AVG)"
            ]},
            {"nome": "Joins e Subconsultas (30%)", "topicos": [
                "INNER, LEFT, RIGHT, FULL JOIN",
                "Self JOIN e CROSS JOIN",
                "Subconsultas correlacionadas",
                "CTEs (Common Table Expressions)"
            ]},
            {"nome": "Manipulação de Dados (20%)", "topicos": [
                "INSERT, UPDATE, DELETE",
                "CREATE, ALTER, DROP",
                "Índices e chaves",
                "Transações (COMMIT, ROLLBACK)"
            ]},
            {"nome": "Funções Avançadas (20%)", "topicos": [
                "Window Functions (ROW_NUMBER, RANK)",
                "GROUP BY e HAVING",
                "Funções de string e data",
                "Stored Procedures e Views"
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
        "semanas": 6,
        "horas": 45
    },
    "CISSP": {
        "titulo": "Certified Information Systems Security Professional",
        "descricao": "Certificação mais reconhecida globalmente em cibersegurança.",
        "dominios": [
            {"nome": "Security and Risk Management (15%)", "topicos": [
                "Confidencialidade, Integridade, Disponibilidade",
                "Governança e compliance",
                "Gestão de riscos",
                "LGPD, GDPR, HIPAA"
            ]},
            {"nome": "Asset Security (10%)", "topicos": [
                "Classificação de dados",
                "Retenção e destruição",
                "Handling de dados sensíveis"
            ]},
            {"nome": "Security Architecture and Engineering (13%)", "topicos": [
                "Arquitetura de segurança",
                "Criptografia e PKI",
                "Modelos de segurança"
            ]},
            {"nome": "Communication and Network Security (13%)", "topicos": [
                "Segurança de redes",
                "Protocolos seguros (TLS, IPsec)",
                "Segurança sem fio"
            ]},
            {"nome": "Identity and Access Management (13%)", "topicos": [
                "IAM, SSO, MFA",
                "Federacão de identidades",
                "Privileged Access Management"
            ]},
            {"nome": "Security Assessment and Testing (12%)", "topicos": [
                "Testes de penetração",
                "Análise de vulnerabilidades",
                "Auditoria de segurança"
            ]},
            {"nome": "Security Operations (13%)", "topicos": [
                "Resposta a incidentes",
                "BCP e DRP",
                "Forensics e investigação"
            ]},
            {"nome": "Software Development Security (11%)", "topicos": [
                "DevSecOps",
                "Segurança em SDLC",
                "OWASP Top 10"
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
        "semanas": 16,
        "horas": 200
    },
    "GICSP": {
        "titulo": "Global Industrial Cyber Security Professional",
        "descricao": "Certificação especializada em segurança de sistemas industriais (OT/ICS).",
        "dominios": [
            {"nome": "OT/ICS Fundamentals (25%)", "topicos": [
                "Arquitetura ICS (PLC, SCADA, DCS, HMI, RTU)",
                "Protocolos industriais (Modbus, DNP3, OPC, PROFINET)",
                "Histórico e evolução de ataques industriais (Stuxnet, Triton)",
                "Diferenças entre TI e OT"
            ]},
            {"nome": "Riscos e Vulnerabilidades em OT (20%)", "topicos": [
                "Análise de risco em ambientes industriais",
                "Vulnerabilidades comuns em ICS",
                "Threat modeling para OT",
                "MITRE ATT&CK for ICS"
            ]},
            {"nome": "Segurança de Rede Industrial (20%)", "topicos": [
                "Segmentação de redes (DMZ industrial)",
                "Firewalls industriais e unidirecionais",
                "Network monitoring para OT",
                "Zona e conduits (IEC 62443)"
            ]},
            {"nome": "Controles de Segurança para OT (20%)", "topicos": [
                "Hardening de PLCs e RTUs",
                "Controle de acesso em sistemas industriais",
                "Patch management em OT",
                "Backup e recuperação industrial"
            ]},
            {"nome": "Resposta a Incidentes em OT (15%)", "topicos": [
                "Planos de resposta específicos para OT",
                "Forensics industrial",
                "Recuperação de sistemas críticos",
                "Exercícios de simulação"
            ]}
        ],
        "recursos": [
            "GIAC GICSP Official Course",
            "SANS ICS Security",
            "CISA ICS Training (gratuito)",
            "Dragos ICS Cyber Security"
        ],
        "simulados": [
            "GIAC Practice Tests",
            "CyberSecurity Training (OT específico)"
        ],
        "semanas": 12,
        "horas": 120
    }
}

# =========================
# EMENTA COMPLETA DA PUC MINAS
# =========================
EMENTA_PUC = {
    "Arquitetura de Cibersegurança e Zero Trust": {
        "ementa": "Fundamentos de arquitetura de segurança. Paradigma e arquitetura Zero Trust. Segurança em camadas. Defesa em profundidade. Arquitetura de segurança em nuvem: CAF e WAF. Next-Generation Firewall. NIDPS. WAF. CSPM, CNAPP e CWPP. CASB. SASE. Segurança de endpoint. Aplicação de IA para análise de vulnerabilidades.",
        "certificacoes": ["Security+", "AZ-500", "CCNA"],
        "topicos": [
            "Fundamentos de arquitetura de segurança",
            "Zero Trust - conceitos e implementação",
            "Defesa em profundidade",
            "Arquitetura de segurança em nuvem (CAF/WAF)",
            "Next-Generation Firewall (NGFW)",
            "NIDPS (Network Intrusion Detection/Prevention)",
            "WAF (Web Application Firewall)",
            "CSPM, CNAPP e CWPP",
            "CASB (Cloud Access Security Broker)",
            "SASE (Secure Access Service Edge)",
            "Segurança de endpoint",
            "IA para análise de vulnerabilidades"
        ],
        "horas": 60,
        "semanas": 4
    },
    "Aspectos Jurídicos de Conformidade Digital": {
        "ementa": "Direito fundamental à proteção de dados pessoais. Panorama internacional das legislações de privacidade. Fundamentos da LGPD. Marco Civil da Internet. Código de Defesa do Consumidor digital. Direito penal cibernético. Convenção de Budapeste. Responsabilidade civil e criminal. Contratos e acordos de processamento de dados.",
        "certificacoes": ["ISO 27001", "CISSP"],
        "topicos": [
            "Direito à proteção de dados pessoais",
            "Legislações internacionais (GDPR, CCPA)",
            "LGPD - Lei Geral de Proteção de Dados",
            "Marco Civil da Internet",
            "Código de Defesa do Consumidor digital",
            "Crimes cibernéticos e legislação penal",
            "Convenção de Budapeste",
            "Contratos de processamento de dados",
            "Responsabilidade civil no ciberespaço"
        ],
        "horas": 40,
        "semanas": 3
    },
    "Computação Forense e Pericia Digital": {
        "ementa": "Fundamentos de computação forense. Evidências digitais. Metodologias forenses. Ferramentas e tecnologias. Perícia por ambiente. Aspectos jurídicos. Padrões e normas. IA aplicada na perícia digital. Técnicas anti-forense.",
        "certificacoes": ["CySA+", "Security+"],
        "topicos": [
            "Fundamentos de computação forense",
            "Evidências digitais e cadeia de custódia",
            "Metodologias forenses",
            "Ferramentas forenses (FTK, EnCase, Autopsy)",
            "Perícia em diferentes ambientes",
            "Documentação e laudos periciais",
            "IA aplicada à perícia digital",
            "Técnicas anti-forense e contramedidas"
        ],
        "horas": 50,
        "semanas": 4
    },
    "Criptografia e Segurança de Dados": {
        "ementa": "Fundamentos de criptografia. Sistemas simétricos e assimétricos. Algoritmos. Hashing. Assinatura digital. IPSec, TLS. Certificados digitais. PKI. Blockchain. Criptografia pós-quântica. IA aplicada.",
        "certificacoes": ["Security+", "CISSP", "AZ-500"],
        "topicos": [
            "Criptografia simétrica (AES, DES, 3DES)",
            "Criptografia assimétrica (RSA, ECC)",
            "Hashing criptográfico (MD5, SHA)",
            "Assinatura digital",
            "IPSec (camada de rede)",
            "TLS/SSL (camada de transporte)",
            "Certificados digitais e PKI",
            "Blockchain e criptomoedas",
            "Criptografia pós-quântica",
            "Criptografia homomórfica",
            "IA em segurança criptográfica"
        ],
        "horas": 55,
        "semanas": 4
    },
    "DevSecOps: Segurança Integrada e Scanning": {
        "ementa": "Fundamentos de DevSecOps. SDLC seguro. Segurança em pipelines CI/CD. Ferramentas IAST, SAST, DAST, RASP. Security Observability. IA para vulnerabilidades. Práticas cloud-native.",
        "certificacoes": ["DevSecOps", "AZ-500"],
        "topicos": [
            "Fundamentos de DevSecOps",
            "SDLC (Secure Development Lifecycle)",
            "Segurança em pipelines CI/CD",
            "SAST (Static Application Security Testing)",
            "DAST (Dynamic Application Security Testing)",
            "IAST (Interactive Application Security Testing)",
            "RASP (Runtime Application Self-Protection)",
            "Security Observability",
            "IA para análise de vulnerabilidades",
            "Cloud-native security"
        ],
        "horas": 45,
        "semanas": 3
    },
    "Ethical Hacking e Gestão de Vulnerabilidades": {
        "ementa": "Cenário da cibercriminalidade. Técnicas ofensivas. Ethical hacking. Pentest e Red Team. Threat Intelligence. Mitre Att&ck. IA para detecção de vulnerabilidades. Gestão de vulnerabilidades.",
        "certificacoes": ["Security+", "CySA+", "CEH"],
        "topicos": [
            "Cibercriminalidade e ameaças digitais",
            "Técnicas de ataque (recon, scan, exploit)",
            "Ethical hacking e pentest",
            "Red Team vs Blue Team",
            "Threat Intelligence",
            "MITRE ATT&CK Framework",
            "Ferramentas de pentest (Nmap, Metasploit, Burp)",
            "IA para detecção de vulnerabilidades",
            "Gestão do ciclo de vida de vulnerabilidades"
        ],
        "horas": 60,
        "semanas": 5
    },
    "Gestão de Riscos Cibernéticos": {
        "ementa": "Fundamentos de riscos. ISO/IEC 27005. NIST Cybersecurity Framework. Programa de gestão de riscos. Identificação, análise, avaliação. Gestão de riscos de terceiros. IA aplicada.",
        "certificacoes": ["ISO 27001", "CISSP", "Security+"],
        "topicos": [
            "Fundamentos de gestão de riscos",
            "ISO/IEC 27005",
            "NIST Cybersecurity Framework",
            "Identificação de riscos",
            "Análise de riscos (qualitativa/quantitativa)",
            "Avaliação e tratamento de riscos",
            "TPRM (Third Party Risk Management)",
            "IA para gestão de riscos",
            "Apettite e tolerância a risco"
        ],
        "horas": 45,
        "semanas": 3
    },
    "Governança de Dados e Compliance": {
        "ementa": "Governança de Dados e framework DMBoK. Políticas e padrões. Data Stewardship. Metadados. Compliance em IA. LGPD e GDPR. Governança 2.0. IA para governança.",
        "certificacoes": ["ISO 27001", "CISA"],
        "topicos": [
            "Fundamentos da Governança de Dados",
            "Framework DMBoK",
            "Data Stewardship e Data Owners",
            "Metadados e Catálogo de Dados",
            "Políticas e padrões de dados",
            "Compliance em ambientes IA",
            "LGPD e GDPR para dados",
            "Governança 2.0 (ágil)",
            "IA para automação de governança"
        ],
        "horas": 40,
        "semanas": 3
    },
    "Governança de Privacidade e Proteção de Dados": {
        "ementa": "Classificação de dados. Princípios LGPD. Direitos dos titulares. RIPDP. Consentimento. Resposta a incidentes. DPO. Anonimização. IA para privacidade.",
        "certificacoes": ["ISO 27001", "CIPM", "CIPP"],
        "topicos": [
            "Taxonomia e classificação de dados",
            "Princípios da LGPD",
            "Direitos dos titulares",
            "RIPDP (Relatório de Impacto)",
            "Gestão de consentimentos",
            "Resposta a incidentes de dados",
            "DPO (Data Protection Officer)",
            "Anonimização e pseudonimização",
            "IA para avaliação de riscos de privacidade"
        ],
        "horas": 45,
        "semanas": 3
    },
    "Governança e Compliance em Cibersegurança": {
        "ementa": "Governança de cibersegurança. ISO/IEC 27001/27003. Políticas de segurança. SGSI. Plano Diretor. GRC. IA para compliance.",
        "certificacoes": ["ISO 27001", "CISSP", "CISM"],
        "topicos": [
            "Fundamentos da governança de cibersegurança",
            "ISO/IEC 27001 e 27003",
            "Políticas de segurança da informação",
            "SGSI (Sistema de Gestão)",
            "Programa de conscientização",
            "Plano Diretor de Segurança (PDSI)",
            "GRC em cibersegurança",
            "IA para automação de compliance"
        ],
        "horas": 40,
        "semanas": 3
    },
    "Monitoramento e Observabilidade": {
        "ementa": "Monitoramento vs Observabilidade. OpenTelemetry. SLO e Error Budgeting. AIOps. SRE. Dashboards. Logs, métricas e tracing. IA para predição.",
        "certificacoes": ["Security+", "CySA+"],
        "topicos": [
            "Diferença entre monitoramento e observabilidade",
            "Pilares da observabilidade",
            "OpenTelemetry",
            "SLO, SLI e Error Budget",
            "AIOps e Machine Learning",
            "SRE (Site Reliability Engineering)",
            "Dashboards e alertas",
            "Logs, métricas e tracing",
            "IA para predição de falhas"
        ],
        "horas": 35,
        "semanas": 3
    },
    "Projeto em Cibersegurança e Governança de Dados com IA": {
        "ementa": "IA para segurança. Detecção de ameaças. IA Generativa. IA Adversarial. Segurança em LLMs. Automação de SOC. Detecção de anomalias.",
        "certificacoes": ["CISSP", "Cloud Security"],
        "topicos": [
            "IA para detecção de ameaças",
            "IA Generativa em cibersegurança",
            "IA Adversarial (ataques a modelos)",
            "Segurança em LLMs e prompts",
            "Automação de SOC com IA",
            "Detecção de anomalias",
            "Governança de IA corporativa",
            "Projeto prático integrado"
        ],
        "horas": 80,
        "semanas": 6
    },
    "Resiliência Cibernética e Continuidade de Negócios": {
        "ementa": "Ciber-resiliência. NIST 800-34. ISO 22301. BIA. DRaaS. IA para resiliência. Plano de recuperação.",
        "certificacoes": ["CISSP", "GICSP", "Security+"],
        "topicos": [
            "Fundamentos de ciber-resiliência",
            "NIST SP 800-34",
            "ISO 22301 (Continuidade)",
            "BIA (Business Impact Analysis)",
            "Plano de recuperação de desastres (DRP)",
            "BCP (Business Continuity Plan)",
            "DRaaS (Disaster Recovery as a Service)",
            "IA para resiliência"
        ],
        "horas": 40,
        "semanas": 3
    },
    "Resposta a Incidentes e Gestão de Crises Cibernéticas": {
        "ementa": "Gestão de incidentes. NIST SP 800-61. ISO 27035. SIEM, SOAR, EDR. SOC. Playbooks. IA para resposta.",
        "certificacoes": ["CySA+", "CISSP", "Security+"],
        "topicos": [
            "Ciclo de vida de resposta a incidentes",
            "NIST SP 800-61",
            "ISO/IEC 27035",
            "SIEM (Security Information and Event Management)",
            "SOAR (Orchestration, Automation and Response)",
            "EDR (Endpoint Detection and Response)",
            "Playbooks e runbooks",
            "SOC (Security Operations Center)",
            "Table top exercises",
            "IA para resposta a incidentes"
        ],
        "horas": 50,
        "semanas": 4
    },
    "Segurança e Gestão da Identidade Digital": {
        "ementa": "IAM. Ciclo de vida de identidades. RBAC, ABAC. Autenticação. Biometria. Zero Trust. IA para IAM.",
        "certificacoes": ["SC-900", "AZ-500", "Security+"],
        "topicos": [
            "Fundamentos de IAM",
            "Ciclo de vida de identidades",
            "RBAC, ABAC, PBAC",
            "Autenticação (MFA, SSO)",
            "Autorização e privilégios",
            "Biometria e verificação de identidade",
            "Zero Trust e identidade",
            "IAM em nuvem (Azure AD)",
            "IA para IAM"
        ],
        "horas": 45,
        "semanas": 3
    }
}

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900":                {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals",      "xp": 3000,  "ano": 2026},
    "AZ-104":                {"emblema": "☁️⚙️",  "cor": "#0078D4", "titulo": "Azure Administrator",     "xp": 6000,  "ano": 2026},
    "AZ-500":                {"emblema": "☁️🔐", "cor": "#005BA1", "titulo": "Azure Security",           "xp": 6000,  "ano": 2026},
    "ISO 27001 Fundamentals":{"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation",           "xp": 4000,  "ano": 2026},
    "ISO 27001 Auditor":     {"emblema": "🔒🔍", "cor": "#FFC000", "titulo": "ISO Auditor",              "xp": 5000,  "ano": 2027},
    "ISO 27001 Implementer": {"emblema": "🔒🛠️", "cor": "#FFA000", "titulo": "ISO Implementer",         "xp": 6000,  "ano": 2027},
    "Security+":             {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus",           "xp": 8000,  "ano": 2027},
    "AWS Cloud Practitioner":{"emblema": "☁️📘", "cor": "#FF9900", "titulo": "AWS Cloud",               "xp": 3000,  "ano": 2027},
    "Scrum Fundamentals":    {"emblema": "🔄📋", "cor": "#0A5C4A", "titulo": "Scrum",                   "xp": 1600,  "ano": 2026},
    "CySA+":                 {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus",               "xp": 6000,  "ano": 2027},
    "CISSP":                 {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP",                    "xp": 20000, "ano": 2029},
    "IEC 62443":             {"emblema": "🏭📏", "cor": "#808080", "titulo": "IEC 62443",                "xp": 8000,  "ano": 2027},
    "MITRE ATT&CK ICS":      {"emblema": "🎯🏭", "cor": "#A0A0A0", "titulo": "MITRE ICS",               "xp": 4000,  "ano": 2028},
    "GICSP":                 {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP",                   "xp": 12000, "ano": 2028},
    "Python":                {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python",                   "xp": 6000,  "ano": 2026},
    "SQL":                   {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL",                     "xp": 4500,  "ano": 2026},
    "Power BI":              {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI",                 "xp": 5000,  "ano": 2026},
    "CCNA":                  {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA",                   "xp": 12000, "ano": 2026},
    "SC-900":                {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900",                   "xp": 2500,  "ano": 2026},
    "Pos-graduacao":         {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação",            "xp": 60000, "ano": 2026},
    "Ingles":                {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês",                 "xp": 30000, "ano": "Contínuo"},
    "Cloud Security":        {"emblema": "☁️🔒", "cor": "#00A4EF", "titulo": "Cloud Security",          "xp": 6000,  "ano": 2028},
    "DevSecOps":             {"emblema": "🔄🚀", "cor": "#6C3483", "titulo": "DevSecOps",               "xp": 6000,  "ano": 2029}
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
.disciplina-card, .cert-conteudo-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid rgba(77,159,255,0.2);
    transition: all 0.3s;
}
.disciplina-card:hover, .cert-conteudo-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(77,159,255,0.2);
}
.topico-item {
    background: rgba(77,159,255,0.05);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 5px 0;
    font-size: 13px;
}
.dominio-header {
    background: rgba(77,159,255,0.15);
    border-radius: 8px;
    padding: 10px;
    margin: 10px 0 5px 0;
    font-weight: bold;
}
.soft-card {
    background: linear-gradient(135deg, rgba(255,68,68,0.1), rgba(123,47,247,0.05));
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border-left: 3px solid #ff8800;
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
if "disciplinas_progresso" not in st.session_state:
    st.session_state.disciplinas_progresso = {disciplina: 0 for disciplina in EMENTA_PUC.keys()}
if "topicos_concluidos" not in st.session_state:
    st.session_state.topicos_concluidos = {}
if "cert_topicos_concluidos" not in st.session_state:
    st.session_state.cert_topicos_concluidos = {}
if "soft_skills_concluidas" not in st.session_state:
    st.session_state.soft_skills_concluidas = {}

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
            st.success("✅ Acesso concedido!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos!")

# =========================
# FUNÇÕES DE BACKUP (SUPABASE)
# =========================
def salvar_backup():
    dados = {
        "db": st.session_state.db,
        "xp": st.session_state.xp,
        "cert_xp": st.session_state.cert_xp,
        "cert_status": st.session_state.cert_status,
        "disciplinas_progresso": st.session_state.disciplinas_progresso,
        "topicos_concluidos": st.session_state.topicos_concluidos,
        "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos,
        "soft_skills_concluidas": st.session_state.soft_skills_concluidas,
        "data_backup": datetime.now().isoformat()
    }
    return salvar_no_supabase(dados)

def carregar_backup():
    dados = carregar_do_supabase()
    if dados:
        st.session_state.db = dados.get("db", [])
        st.session_state.xp = dados.get("xp", 0)
        st.session_state.cert_xp = dados.get("cert_xp", st.session_state.cert_xp)
        st.session_state.cert_status = dados.get("cert_status", st.session_state.cert_status)
        st.session_state.disciplinas_progresso = dados.get("disciplinas_progresso", st.session_state.disciplinas_progresso)
        st.session_state.topicos_concluidos = dados.get("topicos_concluidos", {})
        st.session_state.cert_topicos_concluidos = dados.get("cert_topicos_concluidos", {})
        st.session_state.soft_skills_concluidas = dados.get("soft_skills_concluidas", {})
        return True
    return False

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
        "data": datetime.now().isoformat(),
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
    salvar_backup()

def adicionar_xp_disciplina(disciplina, xp):
    st.session_state.disciplinas_progresso[disciplina] += xp
    st.session_state.xp += xp
    salvar_backup()

def adicionar_soft_skill(categoria, atividade, xp):
    key = f"{categoria}_{atividade}"
    if key not in st.session_state.soft_skills_concluidas:
        st.session_state.soft_skills_concluidas[key] = True
        st.session_state.xp += xp
        salvar_backup()
        return True
    return False

def marcar_topico_puc(disciplina, topico, concluido):
    if disciplina not in st.session_state.topicos_concluidos:
        st.session_state.topicos_concluidos[disciplina] = []
    if concluido and topico not in st.session_state.topicos_concluidos[disciplina]:
        st.session_state.topicos_concluidos[disciplina].append(topico)
        st.session_state.xp += 5
        salvar_backup()
    elif not concluido and topico in st.session_state.topicos_concluidos[disciplina]:
        st.session_state.topicos_concluidos[disciplina].remove(topico)
        st.session_state.xp -= 5
        salvar_backup()

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
# CARREGAR DADOS SALVOS (apenas uma vez por sessão)
# =========================
if "dados_carregados" not in st.session_state:
    carregar_backup()
    st.session_state.dados_carregados = True

# =========================
# VERIFICAR LOGIN
# =========================
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
    st.markdown("### 🎓 Pós PUC Minas")
    total_disciplinas = len(EMENTA_PUC)
    disciplinas_concluidas = sum(1 for p in st.session_state.disciplinas_progresso.values() if p >= 100)
    st.progress(disciplinas_concluidas / total_disciplinas if total_disciplinas > 0 else 0)
    st.caption(f"{disciplinas_concluidas}/{total_disciplinas} disciplinas")
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🎮 Dashboard", "📚 Certificações", "💪 Soft Skills", "🎓 Pós PUC", "🎖️ Progresso", "🗺️ Roadmap", "📊 Relatórios"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    st.markdown("## ⚡ ATIVIDADES DE HOJE")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("#### ➕ Nova Atividade")
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
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 36px;">⭐</div>
            <div style="font-size: 28px;">+{xp_hoje}</div>
            <div>XP hoje</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        meta = 50
        progresso = min(xp_hoje / meta, 1.0)
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 36px;">🎯</div>
            <div style="font-size: 28px;">{xp_hoje}/{meta}</div>
            <div>Meta</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progresso)
    atividades_hoje = get_atividades_hoje()
    if atividades_hoje:
        for atv in atividades_hoje:
            emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
            st.markdown(f"""
            <div class="atividade-card">
                {emblema} **{atv['area'][:30]}** | {atv['atividade']} | ⭐ +{atv['xp']}<br>
                <small>📝 {atv['obs'][:50] if atv['obs'] else '-'}</small>
            </div>
            """, unsafe_allow_html=True)
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
# TAB 2 - CONTEÚDO DAS CERTIFICAÇÕES
# =========================
with tab2:
    st.markdown("## 📚 PLANO DE ESTUDOS POR CERTIFICAÇÃO")
    st.markdown("Selecione uma certificação para ver o conteúdo detalhado")
    st.markdown("---")
    cert_selecionada = st.selectbox("🎯 Selecione a certificação", list(CONTEUDO_CERTIFICACOES.keys()))
    if cert_selecionada in CONTEUDO_CERTIFICACOES:
        info = CONTEUDO_CERTIFICACOES[cert_selecionada]
        st.markdown(f"""
        <div class="cert-conteudo-card">
            <h2>{EMBLEMAS[cert_selecionada]['emblema']} {cert_selecionada}</h2>
            <h3>{info['titulo']}</h3>
            <p>{info['descricao']}</p>
            <p><strong>⏱️ Duração estimada:</strong> {info['semanas']} semanas ({info['horas']} horas)</p>
        </div>
        """, unsafe_allow_html=True)
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["📖 Domínios e Tópicos", "✅ Checklist de Estudos", "🎓 Recursos Gratuitos", "📝 Simulados"])
        with sub_tab1:
            st.markdown("### 📋 Domínios da Prova")
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
            st.markdown("### ✅ Seu Progresso")
            total_topicos = sum(len(d['topicos']) for d in info['dominios'])
            topicos_feitos = len([k for k in st.session_state.cert_topicos_concluidos if k.startswith(cert_selecionada)])
            percentual = (topicos_feitos / total_topicos * 100) if total_topicos > 0 else 0
            st.progress(percentual / 100)
            st.caption(f"Progresso: {topicos_feitos}/{total_topicos} tópicos concluídos ({percentual:.0f}%)")
            st.markdown("---")
            st.markdown("### 📅 Cronograma Sugerido")
            st.markdown(f"**Duração recomendada:** {info['semanas']} semanas")
            st.markdown(f"**Carga horária semanal:** ~{info['horas'] // info['semanas']} horas/semana")
            st.markdown("#### Plano Semanal:")
            for semana in range(1, min(info['semanas'] + 1, 5)):
                st.markdown(f"- **Semana {semana}:** {info['dominios'][semana-1]['nome'][:50]}...")
            if info['semanas'] > 4:
                st.markdown(f"- **Semana {info['semanas']}:** Revisão geral e simulados")
        with sub_tab3:
            st.markdown("### 🎓 Recursos Gratuitos")
            for recurso in info['recursos']:
                st.markdown(f"- 📹 {recurso}")
            st.markdown("---")
            st.markdown("### 💻 Cursos Recomendados")
            st.markdown("- **Hashtag Treinamentos** (Python, SQL, Power BI)")
            st.markdown("- **Microsoft Learn** (AZ-900, SC-900)")
            st.markdown("- **Professor Messer** (Security+, CySA+)")
            st.markdown("- **Jeremy's IT Lab** (CCNA)")
        with sub_tab4:
            st.markdown("### 📝 Simulados Recomendados")
            for simulado in info['simulados']:
                st.markdown(f"- ✅ {simulado}")
            st.markdown("---")
            st.markdown("### 🎯 Dicas para a Prova")
            st.markdown("1. Faça simulados até atingir 85%+ de acertos")
            st.markdown("2. Revise os tópicos que você errou")
            st.markdown("3. Marque a prova com 2-3 semanas de antecedência")
            st.markdown("4. Descanse bem na véspera")

# =========================
# TAB 3 - SOFT SKILLS
# =========================
with tab3:
    st.markdown("## 💪 DESENVOLVIMENTO DE SOFT SKILLS")
    st.markdown("Atividades práticas para desenvolver habilidades comportamentais essenciais.")
    st.markdown("---")
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
# TAB 4 - PÓS PUC
# =========================
with tab4:
    st.markdown("## 🎓 PÓS-GRADUAÇÃO PUC MINAS")
    st.markdown("### Cibersegurança e Governança de Dados")
    st.markdown("---")
    filtro_cert = st.selectbox("🔍 Filtrar por certificação relacionada",
                               ["Todas", "Security+", "AZ-500", "CCNA", "ISO 27001", "CISSP", "CySA+", "SC-900", "DevSecOps"])
    for disciplina, info in EMENTA_PUC.items():
        if filtro_cert != "Todas" and filtro_cert not in info["certificacoes"]:
            continue
        progresso_disciplina = st.session_state.disciplinas_progresso.get(disciplina, 0)
        percentual = min(progresso_disciplina, 100)
        with st.expander(f"📖 {disciplina}", expanded=False):
            st.markdown(f"""
            <div class="disciplina-card">
                <p><strong>📝 Ementa:</strong> {info['ementa'][:200]}...</p>
                <p><strong>🏷️ Certificações relacionadas:</strong> {', '.join(info['certificacoes'])}</p>
                <p><strong>⏱️ Carga horária estimada:</strong> {info['horas']} horas | <strong>📅 Duração:</strong> {info['semanas']} semanas</p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(percentual / 100)
            st.caption(f"Progresso: {percentual}%")
            st.markdown("#### ✅ Tópicos de Estudo (+5 XP cada)")
            for topico in info["topicos"]:
                topico_key = f"puc_{disciplina}_{topico}"
                concluido = topico in st.session_state.topicos_concluidos.get(disciplina, [])
                if st.checkbox(topico, value=concluido, key=topico_key):
                    if not concluido:
                        marcar_topico_puc(disciplina, topico, True)
                        st.rerun()
                else:
                    if concluido:
                        marcar_topico_puc(disciplina, topico, False)
                        st.rerun()
            st.markdown("#### 🎯 Adicionar Progresso")
            col_a, col_b = st.columns([2, 1])
            with col_a:
                xp_adicional = st.number_input("Horas estudadas", min_value=0, max_value=10, key=f"horas_{disciplina}")
            with col_b:
                if st.button(f"Adicionar +{xp_adicional * 5} XP", key=f"add_xp_{disciplina}"):
                    ganho = xp_adicional * 5
                    adicionar_xp_disciplina(disciplina, ganho)
                    st.success(f"+{ganho} XP em {disciplina}!")
                    st.rerun()

# =========================
# TAB 5 - PROGRESSO DAS CERTIFICAÇÕES
# =========================
with tab5:
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
                        salvar_backup()
                        st.rerun()

# =========================
# TAB 6 - ROADMAP
# =========================
with tab6:
    st.markdown("## 🗺️ ROADMAP DAS CERTIFICAÇÕES")
    for ano in [2026, 2027, 2028, 2029]:
        titulo = {2026: "🌱 2026 - Fundação", 2027: "⚡ 2027 - Especialização", 2028: "🎯 2028 - Maestria", 2029: "👑 2029 - Liderança"}[ano]
        with st.expander(titulo):
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
                        <div style="text-align:center; padding:10px; background:rgba(77,159,255,0.1); border-radius:10px;">
                            <div style="font-size:32px;">{info['emblema']}</div>
                            <div style="font-size:11px;">{cert[:15]}</div>
                            <div>{get_badge(status)}</div>
                            <div style="font-size:10px;">{xp_atual}/{info['xp']} XP</div>
                            <div style="background:#333; border-radius:5px; height:4px;">
                                <div style="background:{info['cor']}; width:{percent}%; height:4px; border-radius:5px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# =========================
# TAB 7 - RELATÓRIOS
# =========================
with tab7:
    st.markdown("## 📊 RELATÓRIOS")

    if len(st.session_state.db) > 0:
        dados_df = []
        for a in st.session_state.db:
            try:
                if isinstance(a['data'], str):
                    data_atv = datetime.fromisoformat(a['data'])
                else:
                    data_atv = a['data']
                dados_df.append({
                    "data": data_atv,
                    "data_label": data_atv.strftime('%d/%m/%Y'),
                    "hora": data_atv.strftime('%H:%M'),
                    "area": a['area'],
                    "atividade": a['atividade'],
                    "obs": a.get('obs', ''),
                    "xp": a['xp']
                })
            except:
                pass

        if dados_df:
            df = pd.DataFrame(dados_df)
            df = df.sort_values('data', ascending=False)

            # -------------------------
            # TABELA DETALHADA
            # -------------------------
            st.markdown("### 📋 Histórico Detalhado de Atividades")
            df_exibir = df[['data_label', 'hora', 'area', 'atividade', 'obs', 'xp']].copy()
            df_exibir.columns = ['📅 Data', '🕐 Hora', '🎯 Certificação', '📚 Tipo', '📝 O que foi feito', '⭐ XP']
            df_exibir['📝 O que foi feito'] = df_exibir['📝 O que foi feito'].apply(lambda x: x[:60] + '...' if len(str(x)) > 60 else x)
            st.dataframe(df_exibir, use_container_width=True, height=300)

            st.markdown("---")

            # -------------------------
            # GRÁFICO DE BARRAS EMPILHADAS POR DATA (HTML puro, sem altair)
            # -------------------------
            st.markdown("### 📊 XP por Certificação — Gráfico por Data")

            # Agrupar XP por data e certificação
            df_grafico = df.groupby(['data_label', 'area'])['xp'].sum().reset_index()
            datas = sorted(df['data_label'].unique(), key=lambda d: datetime.strptime(d, '%d/%m/%Y'))
            certs_usadas = df['area'].unique().tolist()

            # Cores para cada certificação
            cores = [
                "#4d9fff","#7b2ff7","#ff6b6b","#00ff88","#ffd700",
                "#ff8800","#00cfff","#ff4ecb","#a8ff3e","#ff3e3e",
                "#3effd8","#ff9f43","#54a0ff","#5f27cd","#01aac1"
            ]
            cor_map = {cert: cores[i % len(cores)] for i, cert in enumerate(certs_usadas)}

            # Calcular max para escala
            xp_por_data = df.groupby('data_label')['xp'].sum()
            max_xp = int(xp_por_data.max()) if len(xp_por_data) > 0 else 100
            altura_barra = 220

            # Montar HTML do gráfico
            barras_html = ""
            for data in datas:
                df_data = df_grafico[df_grafico['data_label'] == data]
                total = int(df_data['xp'].sum())
                segmentos = ""
                for _, row in df_data.iterrows():
                    pct = (row['xp'] / max_xp) * 100
                    cor = cor_map.get(row['area'], '#4d9fff')
                    segmentos += f"""
                    <div title="{row['area']}: {int(row['xp'])} XP"
                         style="width:100%; height:{pct * altura_barra / 100:.1f}px;
                                background:{cor}; margin:0; padding:0;
                                display:flex; align-items:center; justify-content:center;
                                font-size:9px; color:white; overflow:hidden; font-weight:bold;">
                        {int(row['xp'])}
                    </div>"""
                barras_html += f"""
                <div style="display:flex; flex-direction:column; align-items:center; flex:1; min-width:60px; max-width:100px;">
                    <div style="font-size:10px; color:#4d9fff; margin-bottom:4px; font-weight:bold;">{total} XP</div>
                    <div style="width:80%; display:flex; flex-direction:column-reverse; height:{altura_barra}px;
                                background:rgba(255,255,255,0.05); border-radius:6px; overflow:hidden;">
                        {segmentos}
                    </div>
                    <div style="font-size:10px; color:#aaa; margin-top:6px; text-align:center;">{data}</div>
                </div>"""

            # Legenda
            legenda_html = ""
            for cert in certs_usadas:
                cor = cor_map.get(cert, '#4d9fff')
                legenda_html += f"""
                <div style="display:flex; align-items:center; gap:6px; margin:4px 8px;">
                    <div style="width:12px; height:12px; background:{cor}; border-radius:3px; flex-shrink:0;"></div>
                    <span style="font-size:11px; color:#ccc;">{cert[:20]}</span>
                </div>"""

            grafico_html = f"""
            <!DOCTYPE html>
            <html>
            <body style="margin:0; padding:0; background:#0e1117; font-family:sans-serif;">
            <div style="padding:16px; border-radius:12px; border:1px solid rgba(77,159,255,0.2);">
                <div style="display:flex; align-items:flex-end; gap:8px; overflow-x:auto; padding-bottom:10px; min-height:{altura_barra + 40}px;">
                    {barras_html}
                </div>
                <div style="margin-top:12px; border-top:1px solid rgba(77,159,255,0.2); padding-top:10px;">
                    <div style="font-size:11px; color:#888; margin-bottom:6px;">📌 Legenda:</div>
                    <div style="display:flex; flex-wrap:wrap;">
                        {legenda_html}
                    </div>
                </div>
            </div>
            </body>
            </html>"""

            import streamlit.components.v1 as components
            components.html(grafico_html, height=altura_barra + 200, scrolling=False)

            st.markdown("---")

            # -------------------------
            # XP POR CERTIFICAÇÃO
            # -------------------------
            st.markdown("### 🎯 XP Total por Certificação")
            xp_por_cert = df.groupby('area')['xp'].sum().reset_index().sort_values('xp', ascending=False).head(10)
            for _, row in xp_por_cert.iterrows():
                pct = min(row['xp'] / max(xp_por_cert['xp'].max(), 1), 1.0)
                cor = cor_map.get(row['area'], '#4d9fff')
                emblema = EMBLEMAS.get(row['area'], {}).get('emblema', '📌')
                st.markdown(f"""
                <div style="margin:8px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span style="font-size:13px;">{emblema} <strong>{row['area']}</strong></span>
                        <span style="font-size:13px; color:{cor}; font-weight:bold;">{int(row['xp'])} XP</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.1); border-radius:6px; height:8px;">
                        <div style="background:{cor}; width:{pct*100:.1f}%; height:8px; border-radius:6px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.info("📭 Nenhuma atividade registrada ainda. Comece lançando atividades no Dashboard!")

    st.markdown("---")
    st.markdown("### 📄 Exportar Dados")
    if st.button("📥 Exportar Progresso Completo", use_container_width=True):
        export_data = {
            "xp_total": st.session_state.xp,
            "certificacoes": st.session_state.cert_xp,
            "disciplinas_puc": st.session_state.disciplinas_progresso,
            "topicos_concluidos": st.session_state.topicos_concluidos,
            "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos,
            "soft_skills_concluidas": st.session_state.soft_skills_concluidas,
            "historico": st.session_state.db
        }
        export_json = json.dumps(export_data, default=str, indent=2)
        st.download_button("📥 Baixar JSON", export_json, "progresso_completo.json", "application/json")

st.caption("🚀 Continue sua jornada, o universo te espera!")
