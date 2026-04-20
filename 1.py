import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# =========================
# CONFIGURAÇÃO DE PERSISTÊNCIA (RENDER)
# =========================
def get_data_path():
    """Retorna o caminho correto para salvar dados no Render ou localmente"""
    render_disk = Path("/opt/render/project/src/dados")
    if render_disk.exists() or os.getenv("RENDER"):
        render_disk.mkdir(exist_ok=True)
        return render_disk
    return Path(".")

DATA_FILE = get_data_path() / "progresso_juan.json"

def carregar_dados():
    """Carrega os dados do arquivo JSON"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    """Salva os dados no arquivo JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

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
            "Técnicas anti-forense
