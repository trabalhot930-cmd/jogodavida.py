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
            {"nome": "🗣️ Reunião em Inglês", "descricao": "Participar de reunião ou call em inglês", "xp": 50}
        ]
    },
    "Liderança de Equipes": {
        "descricao": "Capacidade de motivar, orientar e coordenar pessoas para alcançar objetivos comuns.",
        "atividades": [
            {"nome": "👥 Mentorar Colega", "descricao": "Ensinar um processo ou tecnologia a um colega", "xp": 35},
            {"nome": "📋 Liderar Reunião", "descricao": "Conduzir uma reunião de equipe", "xp": 30},
            {"nome": "🎯 Definir Metas", "descricao": "Estabelecer objetivos claros para sua equipe", "xp": 40},
            {"nome": "🔄 Delegar Tarefas", "descricao": "Distribuir atividades entre a equipe", "xp": 25},
            {"nome": "🏆 Reconhecer Time", "descricao": "Dar feedback positivo público para colega", "xp": 20}
        ]
    },
    "Gestão de Projetos": {
        "descricao": "Planejar, executar e monitorar projetos dentro de prazo, orçamento e qualidade.",
        "atividades": [
            {"nome": "📅 Planejar Projeto", "descricao": "Criar cronograma com marcos e entregas", "xp": 40},
            {"nome": "💰 Controlar Orçamento", "descricao": "Monitorar gastos e fazer ajustes", "xp": 35},
            {"nome": "📊 Relatório de Status", "descricao": "Produzir relatório de progresso do projeto", "xp": 30},
            {"nome": "⚠️ Gestão de Risco", "descricao": "Identificar e mitigar riscos do projeto", "xp": 45},
            {"nome": "🔄 Kanban/Scrum", "descricao": "Aplicar metodologia ágil no dia a dia", "xp": 50}
        ]
    },
    "Inteligência Emocional": {
        "descricao": "Capacidade de reconhecer e gerenciar emoções próprias e alheias.",
        "atividades": [
            {"nome": "😌 Gerenciar Estresse", "descricao": "Aplicar técnica de respiração/pausa", "xp": 20},
            {"nome": "👂 Escuta Ativa", "descricao": "Praticar ouvir sem interromper", "xp": 25},
            {"nome": "📝 Diário de Emoções", "descricao": "Registrar gatilhos emocionais", "xp": 15},
            {"nome": "💬 Feedback Construtivo", "descricao": "Dar feedback usando técnica SBI", "xp": 35},
            {"nome": "🙏 Reconhecer Erro", "descricao": "Admitir erro e pedir desculpas", "xp": 30}
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
        "recursos": [
            "AWS Skill Builder (gratuito)",
            "YouTube - Stephane Maarek",
            "AWS Free Tier (laboratórios práticos)",
            "ExamPro - Practice Exams"
        ],
        "simulados": [
            "AWS Official Practice Exam",
            "TutorialsDojo",
            "Udemy - Practice Exams"
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
            "YouTube - Scrum Framework em 12 minutos",
            "Scrum.org - Open Assessments",
            "LinkedIn Learning - Scrum Basics"
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
            "CISA ICS Training (gratuito)",
            "Dragos ICS Cyber Security"
        ],
        "simulados": [
            "GIAC Practice Tests",
            "CyberSecurity Training (OT específico)"
        ],
        "semanas": 12, "horas": 120, "custo": "$949", "voucher": False
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
            "Fundamentos de arquitetura de segurança", "Zero Trust - conceitos e implementação", "Defesa em profundidade",
            "Arquitetura de segurança em nuvem (CAF/WAF)", "Next-Generation Firewall (NGFW)", "NIDPS (Network Intrusion Detection/Prevention)",
            "WAF (Web Application Firewall)", "CSPM, CNAPP e CWPP", "CASB (Cloud Access Security Broker)",
            "SASE (Secure Access Service Edge)", "Segurança de endpoint", "IA para análise de vulnerabilidades"
        ],
        "horas": 60, "semanas": 4
    },
    "Aspectos Jurídicos de Conformidade Digital": {
        "ementa": "Direito fundamental à proteção de dados pessoais. Panorama internacional das legislações de privacidade. Fundamentos da LGPD. Marco Civil da Internet. Código de Defesa do Consumidor digital. Direito penal cibernético. Convenção de Budapeste. Responsabilidade civil e criminal. Contratos e acordos de processamento de dados.",
        "certificacoes": ["ISO 27001", "CISSP"],
        "topicos": [
            "Direito à proteção de dados pessoais", "Legislações internacionais (GDPR, CCPA)", "LGPD - Lei Geral de Proteção de Dados",
            "Marco Civil da Internet", "Código de Defesa do Consumidor digital", "Crimes cibernéticos e legislação penal",
            "Convenção de Budapeste", "Contratos de processamento de dados", "Responsabilidade civil no ciberespaço"
        ],
        "horas": 40, "semanas": 3
    },
    "Computação Forense e Pericia Digital": {
        "ementa": "Fundamentos de computação forense. Evidências digitais. Metodologias forenses. Ferramentas e tecnologias. Perícia por ambiente. Aspectos jurídicos. Padrões e normas. IA aplicada na perícia digital. Técnicas anti-forense.",
        "certificacoes": ["CySA+", "Security+"],
        "topicos": [
            "Fundamentos de computação forense", "Evidências digitais e cadeia de custódia", "Metodologias forenses",
            "Ferramentas forenses (FTK, EnCase, Autopsy)", "Perícia em diferentes ambientes", "Documentação e laudos periciais",
            "IA aplicada à perícia digital", "Técnicas anti-forense e contramedidas"
        ],
        "horas": 50, "semanas": 4
    },
    "Criptografia e Segurança de Dados": {
        "ementa": "Fundamentos de criptografia. Sistemas simétricos e assimétricos. Algoritmos. Hashing. Assinatura digital. IPSec, TLS. Certificados digitais. PKI. Blockchain. Criptografia pós-quântica. IA aplicada.",
        "certificacoes": ["Security+", "CISSP", "AZ-500"],
        "topicos": [
            "Criptografia simétrica (AES, DES, 3DES)", "Criptografia assimétrica (RSA, ECC)", "Hashing criptográfico (MD5, SHA)",
            "Assinatura digital", "IPSec (camada de rede)", "TLS/SSL (camada de transporte)",
            "Certificados digitais e PKI", "Blockchain e criptomoedas", "Criptografia pós-quântica",
            "Criptografia homomórfica", "IA em segurança criptográfica"
        ],
        "horas": 55, "semanas": 4
    },
    "DevSecOps: Segurança Integrada e Scanning": {
        "ementa": "Fundamentos de DevSecOps. SDLC seguro. Segurança em pipelines CI/CD. Ferramentas IAST, SAST, DAST, RASP. Security Observability. IA para vulnerabilidades. Práticas cloud-native.",
        "certificacoes": ["DevSecOps", "AZ-500"],
        "topicos": [
            "Fundamentos de DevSecOps", "SDLC (Secure Development Lifecycle)", "Segurança em pipelines CI/CD",
            "SAST (Static Application Security Testing)", "DAST (Dynamic Application Security Testing)", "IAST (Interactive Application Security Testing)",
            "RASP (Runtime Application Self-Protection)", "Security Observability", "IA para análise de vulnerabilidades", "Cloud-native security"
        ],
        "horas": 45, "semanas": 3
    },
    "Ethical Hacking e Gestão de Vulnerabilidades": {
        "ementa": "Cenário da cibercriminalidade. Técnicas ofensivas. Ethical hacking. Pentest e Red Team. Threat Intelligence. Mitre Att&ck. IA para detecção de vulnerabilidades. Gestão de vulnerabilidades.",
        "certificacoes": ["Security+", "CySA+", "CEH"],
        "topicos": [
            "Cibercriminalidade e ameaças digitais", "Técnicas de ataque (recon, scan, exploit)", "Ethical hacking e pentest",
            "Red Team vs Blue Team", "Threat Intelligence", "MITRE ATT&CK Framework",
            "Ferramentas de pentest (Nmap, Metasploit, Burp)", "IA para detecção de vulnerabilidades", "Gestão do ciclo de vida de vulnerabilidades"
        ],
        "horas": 60, "semanas": 5
    },
    "Gestão de Riscos Cibernéticos": {
        "ementa": "Fundamentos de riscos. ISO/IEC 27005. NIST Cybersecurity Framework. Programa de gestão de riscos. Identificação, análise, avaliação. Gestão de riscos de terceiros. IA aplicada.",
        "certificacoes": ["ISO 27001", "CISSP", "Security+"],
        "topicos": [
            "Fundamentos de gestão de riscos", "ISO/IEC 27005", "NIST Cybersecurity Framework",
            "Identificação de riscos", "Análise de riscos (qualitativa/quantitativa)", "Avaliação e tratamento de riscos",
            "TPRM (Third Party Risk Management)", "IA para gestão de riscos", "Apettite e tolerância a risco"
        ],
        "horas": 45, "semanas": 3
    },
    "Governança de Dados e Compliance": {
        "ementa": "Governança de Dados e framework DMBoK. Políticas e padrões. Data Stewardship. Metadados. Compliance em IA. LGPD e GDPR. Governança 2.0. IA para governança.",
        "certificacoes": ["ISO 27001", "CISA"],
        "topicos": [
            "Fundamentos da Governança de Dados", "Framework DMBoK", "Data Stewardship e Data Owners",
            "Metadados e Catálogo de Dados", "Políticas e padrões de dados", "Compliance em ambientes IA",
            "LGPD e GDPR para dados", "Governança 2.0
