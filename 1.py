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
    "ISO 27001 Implementer": {
        "titulo": "ISO/IEC 27001 Lead Implementer",
        "descricao": "Certificação para implementar e gerenciar um Sistema de Gestão de Segurança da Informação (SGSI) conforme a norma ISO 27001:2022.",
        "dominios": [
            {"nome": "Fundamentos e Contexto (15%)", "topicos": [
                "Princípios da ISO 27001:2022",
                "Contexto da organização",
                "Partes interessadas e requisitos",
                "Escopo do SGSI"
            ]},
            {"nome": "Planejamento e Liderança (20%)", "topicos": [
                "Política de segurança da informação",
                "Papéis e responsabilidades",
                "Análise de riscos (ISO 31000)",
                "Declaração de Aplicabilidade (SoA)"
            ]},
            {"nome": "Implementação dos Controles (30%)", "topicos": [
                "Controles do Anexo A (93 controles)",
                "Gestão de ativos",
                "Controle de acesso",
                "Criptografia e segurança física",
                "Gestão de incidentes"
            ]},
            {"nome": "Operação e Monitoramento (20%)", "topicos": [
                "Programa de conscientização",
                "Gestão de fornecedores",
                "Monitoramento e métricas",
                "Auditoria interna"
            ]},
            {"nome": "Melhoria Contínua (15%)", "topicos": [
                "Não conformidades e ações corretivas",
                "Análise crítica pela direção",
                "Melhoria contínua do SGSI"
            ]}
        ],
        "recursos": [
            "ISO 27001:2022 (norma oficial)",
            "ISO 27002:2022 (controles)",
            "PECB / BSI Lead Implementer Course",
            "YouTube - ISACA Training"
        ],
        "simulados": [
            "PECB Practice Exams",
            "Udemy - ISO 27001 Lead Implementer"
        ],
        "semanas": 8,
        "horas": 60
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Linguagem SQL para consultas, manipulação e análise de bancos de dados relacionais.",
        "dominios": [
            {"nome": "Consultas Básicas (30%)", "topicos": [
                "SELECT, FROM, WHERE",
                "ORDER BY, LIMIT, DISTINCT",
                "Operadores (LIKE, IN, BETWEEN)",
                "Funções de agregação (COUNT, SUM, AVG, MAX, MIN)"
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
                "Índices e chaves primárias/estrangeiras",
                "Transações (COMMIT, ROLLBACK)"
            ]},
            {"nome": "Funções Avançadas (20%)", "topicos": [
                "Window Functions (ROW_NUMBER, RANK, LAG, LEAD)",
                "GROUP BY e HAVING",
                "Funções de string e data",
                "Views e Stored Procedures"
            ]}
        ],
        "recursos": [
            "SQLZoo (interativo e grátis)",
            "Mode Analytics SQL Tutorial",
            "Hashtag Treinamentos - SQL Impressionador",
            "W3Schools SQL (referência rápida)"
        ],
        "simulados": [
            "HackerRank - SQL (gratuito)",
            "LeetCode - Database",
            "StrataScratch"
        ],
        "semanas": 6,
        "horas": 45
    },
    "Security+": {
        "titulo": "CompTIA Security+ (SY0-701)",
        "descricao": "Certificação fundamental de cibersegurança, reconhecida mundialmente. Base para toda a trilha de segurança.",
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
                "Contas privilegiadas (PAM)"
            ]},
            {"nome": "Gestão de Riscos e Compliance (13%)", "topicos": [
                "Análise de risco (qualitativa/quantitativa)",
                "BCP e DRP (RTO, RPO, MTD)",
                "Planos de resposta a incidentes",
                "LGPD, GDPR, HIPAA, PCI-DSS",
                "Tipos de controles (preventivo, detetivo, corretivo)"
            ]}
        ],
        "recursos": [
            "Professor Messer - Security+ SY0-701 (grátis no YouTube)",
            "CompTIA Security+ SY0-701 Objectives (PDF oficial)",
            "TryHackMe - Security+ Path",
            "GitHub - Security+ Study Guide"
        ],
        "simulados": [
            "ExamCompass (gratuito)",
            "Professor Messer Practice Exams",
            "Jason Dion (Udemy)",
            "MeasureUp"
        ],
        "semanas": 10,
        "horas": 80
    },
    "Ingles": {
        "titulo": "Inglês para Cibersegurança",
        "descricao": "Desenvolvimento contínuo do inglês com foco em leitura técnica, comunicação profissional e certificações internacionais.",
        "dominios": [
            {"nome": "Leitura Técnica (30%)", "topicos": [
                "Leitura de documentação oficial (RFCs, CVEs, advisories)",
                "Artigos e whitepapers de segurança",
                "Relatórios de threat intelligence",
                "Normas e frameworks em inglês (NIST, ISO)"
            ]},
            {"nome": "Comunicação Profissional (30%)", "topicos": [
                "E-mails e relatórios técnicos",
                "Apresentações em inglês",
                "Reuniões com times internacionais",
                "LinkedIn e networking global"
            ]},
            {"nome": "Certificações e Provas (25%)", "topicos": [
                "Vocabulário técnico de segurança",
                "Interpretação de questões de prova",
                "Listening para webinars e cursos",
                "Leitura de questões em inglês"
            ]},
            {"nome": "Imersão e Prática (15%)", "topicos": [
                "Podcasts de cibersegurança em inglês",
                "YouTube técnico em inglês",
                "Comunidades internacionais (Reddit, Discord)",
                "CTF Writeups em inglês"
            ]}
        ],
        "recursos": [
            "Duolingo (prática diária)",
            "Anki - Flashcards de vocabulário técnico",
            "YouTube - Professor Messer (inglês técnico)",
            "Podcasts: Darknet Diaries, Security Now"
        ],
        "simulados": [
            "Cambridge English (B2/C1)",
            "TOEIC (para mercado corporativo)"
        ],
        "semanas": 52,
        "horas": 300
    },
    "CySA+": {
        "titulo": "CompTIA CySA+ (CS0-003)",
        "descricao": "Certificação de análise de segurança e resposta a incidentes. Pré-requisito recomendado: Security+.",
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
            "TryHackMe (SOC Level 1)",
            "Blue Team Labs Online"
        ],
        "simulados": [
            "Jason Dion (Udemy)",
            "Sybex Practice Tests",
            "ExamCompass"
        ],
        "semanas": 8,
        "horas": 60
    },
    "Pos-graduacao": {
        "titulo": "Pós-graduação PUC Minas — Cibersegurança e Governança de Dados",
        "descricao": "Pós-graduação lato sensu com foco em cibersegurança, governança de dados e proteção da informação.",
        "dominios": [
            {"nome": "Segurança Técnica", "topicos": [
                "Arquitetura de Cibersegurança e Zero Trust",
                "Criptografia e Segurança de Dados",
                "Ethical Hacking e Gestão de Vulnerabilidades",
                "DevSecOps: Segurança Integrada e Scanning",
                "Computação Forense e Perícia Digital",
                "Resposta a Incidentes e Gestão de Crises"
            ]},
            {"nome": "Governança e Compliance", "topicos": [
                "Governança e Compliance em Cibersegurança",
                "Gestão de Riscos Cibernéticos",
                "Governança de Dados e Compliance",
                "Governança de Privacidade e Proteção de Dados",
                "Aspectos Jurídicos de Conformidade Digital"
            ]},
            {"nome": "Tecnologia e Inovação", "topicos": [
                "Segurança e Gestão da Identidade Digital",
                "Monitoramento e Observabilidade",
                "Resiliência Cibernética e Continuidade de Negócios",
                "Projeto em Cibersegurança e Governança com IA"
            ]}
        ],
        "recursos": [
            "Material didático PUC Minas",
            "Biblioteca Virtual PUC",
            "ABNT NBR ISO/IEC 27001:2022",
            "NIST Cybersecurity Framework"
        ],
        "simulados": [
            "Provas e trabalhos das disciplinas",
            "TCC / Projeto Final"
        ],
        "semanas": 80,
        "horas": 600
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
    "Pos-graduacao":         {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação PUC Minas", "xp": 12000, "ano": 2026},
    "ISO 27001 Implementer": {"emblema": "🔒🛠️", "cor": "#FFA000", "titulo": "ISO 27001 Implementer",  "xp": 1200,  "ano": 2026},
    "SQL":                   {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL para Dados",          "xp": 900,   "ano": 2026},
    "Security+":             {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "CompTIA Security+",       "xp": 1600,  "ano": 2026},
    "Ingles":                {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês",                 "xp": 6000,  "ano": "Contínuo"},
    "CySA+":                 {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CompTIA CySA+",           "xp": 1200,  "ano": 2027},
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
if "soft_skills_historico" not in st.session_state:
    st.session_state.soft_skills_historico = []

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
        "soft_skills_historico": st.session_state.soft_skills_historico,
        "data_backup": datetime.now().isoformat()
    }
    return salvar_no_supabase(dados)

def carregar_backup():
    dados = carregar_do_supabase()
    if dados:
        st.session_state.db = dados.get("db", [])
        st.session_state.xp = dados.get("xp", 0)

        # Filtrar apenas as certs do novo plano
        certs_validas = set(EMBLEMAS.keys())

        cert_xp_salvo = dados.get("cert_xp", {})
        st.session_state.cert_xp = {c: cert_xp_salvo.get(c, 0) for c in certs_validas}

        cert_status_salvo = dados.get("cert_status", {})
        st.session_state.cert_status = {c: cert_status_salvo.get(c, "Não iniciada") for c in certs_validas}

        st.session_state.disciplinas_progresso = dados.get("disciplinas_progresso", st.session_state.disciplinas_progresso)
        st.session_state.topicos_concluidos = dados.get("topicos_concluidos", {})
        st.session_state.cert_topicos_concluidos = dados.get("cert_topicos_concluidos", {})
        st.session_state.soft_skills_concluidas = dados.get("soft_skills_concluidas", {})
        st.session_state.soft_skills_historico = dados.get("soft_skills_historico", [])
        return True
    return False

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

# Horas por certificação (1h = 20 XP)
HORAS_CERT = {
    "Pos-graduacao":         600,
    "ISO 27001 Implementer": 60,
    "SQL":                   45,
    "Security+":             80,
    "Ingles":                300,
    "CySA+":                 60,
}

# Peso de cada tipo de atividade
PESO_ATIVIDADE = {
    "📚 Estudo":      1.0,
    "🔬 Laboratório": 1.5,
    "🏗️ Projeto":    2.0,
    "🔄 Revisão":     0.5,
    "📝 Simulado":    1.2,
    "🎓 Aula Pós":    1.0,
    "🌎 Inglês":      1.0,
    "🏅 Certificação": 5.0
}

def calc_xp(atividade, area):
    """XP proporcional às horas da cert × peso da atividade"""
    horas = HORAS_CERT.get(area, 40)
    xp_por_hora = EMBLEMAS[area]["xp"] / horas
    peso = PESO_ATIVIDADE.get(atividade, 1.0)
    xp = int(xp_por_hora * peso)
    return max(xp, 20)

def calc_streak():
    """Dias consecutivos de estudo"""
    if not st.session_state.db:
        return 0
    datas = set()
    for a in st.session_state.db:
        try:
            if isinstance(a['data'], str):
                d = datetime.fromisoformat(a['data']).date()
            else:
                d = a['data'].date()
            datas.add(d)
        except:
            pass
    hoje = datetime.now().date()
    streak = 0
    dia = hoje
    while dia in datas:
        streak += 1
        dia -= timedelta(days=1)
    return streak

def multiplicador_streak(streak):
    """Bônus de streak: +10% a cada 3 dias consecutivos, máximo +50%"""
    bonus = min((streak // 3) * 0.10, 0.50)
    return 1.0 + bonus

def calc_meta_diaria():
    """Meta diária baseada nas certs ativas"""
    certs_ativas = [c for c, s in st.session_state.cert_status.items() if s in ["Em andamento", "Não iniciada"]]
    if not certs_ativas:
        return 500
    media_xp = sum(EMBLEMAS[c]["xp"] for c in certs_ativas) / len(certs_ativas)
    return max(int(media_xp / 30), 200)

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
    streak = calc_streak()
    mult = multiplicador_streak(streak)
    xp_final = int(xp * mult)
    st.session_state.db.append({
        "data": datetime.now().isoformat(),
        "area": area,
        "atividade": atividade,
        "xp": xp_final,
        "obs": obs,
        "streak": streak,
        "multiplicador": mult
    })
    st.session_state.xp += xp_final
    st.session_state.cert_xp[area] += xp_final
    if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
        st.session_state.cert_status[area] = "Concluída"
    elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
        st.session_state.cert_status[area] = "Em andamento"
    salvar_backup()
    return xp_final, streak, mult

def adicionar_xp_disciplina(disciplina, xp):
    st.session_state.disciplinas_progresso[disciplina] += xp
    st.session_state.xp += xp
    salvar_backup()

def adicionar_soft_skill(categoria, atividade_nome, xp, descricao_livre=""):
    """Registra soft skill com histórico completo — permite repetir em dias diferentes"""
    if "soft_skills_historico" not in st.session_state:
        st.session_state.soft_skills_historico = []
    hoje = datetime.now().date().isoformat()
    chave_hoje = f"{categoria}_{atividade_nome}_{hoje}"
    if chave_hoje in st.session_state.soft_skills_concluidas:
        return False, "já_feita"
    st.session_state.soft_skills_concluidas[chave_hoje] = True
    st.session_state.soft_skills_historico.append({
        "data": datetime.now().isoformat(),
        "categoria": categoria,
        "atividade": atividade_nome,
        "descricao": descricao_livre,
        "xp": xp
    })
    st.session_state.xp += xp
    salvar_backup()
    return True, xp

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
    # Garantir que cert_xp e cert_status só tenham as certs do novo plano
    certs_validas = set(EMBLEMAS.keys())
    st.session_state.cert_xp = {c: st.session_state.cert_xp.get(c, 0) for c in certs_validas}
    st.session_state.cert_status = {c: st.session_state.cert_status.get(c, "Não iniciada") for c in certs_validas}
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
    st.markdown(f"🎖️ **Nível:** {st.session_state.xp // 1000 + 1}")
    st.markdown(f"📅 **Missões:** {len(st.session_state.db)}")
    streak_atual = calc_streak()
    mult_atual = multiplicador_streak(streak_atual)
    if streak_atual > 0:
        st.markdown(f"🔥 **Streak:** {streak_atual} dias")
        if mult_atual > 1.0:
            st.markdown(f"⚡ **Bônus:** +{int((mult_atual-1)*100)}% XP")
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
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
    if st.button("🔄 Resetar Certificações", use_container_width=True):
        certs_validas = set(EMBLEMAS.keys())
        st.session_state.cert_xp = {c: 0 for c in certs_validas}
        st.session_state.cert_status = {c: "Não iniciada" for c in certs_validas}
        salvar_backup()
        st.success("✅ Certificações resetadas!")
        st.rerun()

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🎮 Dashboard", "📚 Certificações", "💪 Soft Skills", "🎓 Pós PUC", "🎖️ Progresso", "🗺️ Roadmap", "📊 Relatórios", "📅 Calendário"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    st.markdown("## ⚡ ATIVIDADES DE HOJE")
    streak_atual = calc_streak()
    mult_atual = multiplicador_streak(streak_atual)
    meta = calc_meta_diaria()

    # Banner de streak
    if streak_atual >= 3:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(255,140,0,0.2),rgba(255,69,0,0.1));
                    border-left:4px solid #ff8c00; border-radius:8px; padding:10px 16px; margin-bottom:10px;">
            🔥 <strong>Streak de {streak_atual} dias!</strong> Bônus de <strong>+{int((mult_atual-1)*100)}% XP</strong> ativo em todas as atividades!
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("#### ➕ Nova Atividade")
        with st.form("nova_atividade", clear_on_submit=True):
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
            atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"])
            obs = st.text_area("O que foi feito?")
            xp_preview = int(calc_xp(atividade, area) * mult_atual)
            st.caption(f"💡 Esta atividade vai render **{xp_preview} XP** (base: {calc_xp(atividade, area)} × {mult_atual:.1f}x streak)")
            if st.form_submit_button("🚀 Lançar", use_container_width=True):
                xp_base = calc_xp(atividade, area)
                xp_final, streak, mult = adicionar_atividade(area, atividade, xp_base, obs)
                if mult > 1.0:
                    st.success(f"🔥 +{xp_final} XP com bônus de streak {streak} dias!", icon="🎉")
                else:
                    st.success(f"+{xp_final} XP!", icon="🎉")
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
        progresso_meta = min(xp_hoje / meta, 1.0)
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 36px;">🎯</div>
            <div style="font-size: 22px;">{xp_hoje}/{meta}</div>
            <div>Meta do dia</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progresso_meta)
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
    c2.metric("⭐ XP Total", f"{st.session_state.xp:,}")
    c3.metric("🏆 Nível", st.session_state.xp // 1000 + 1)
    c4.metric("✅ Certificações", f"{concluidas}/{len(EMBLEMAS)}")
    c5.metric("🔥 Streak", f"{calc_streak()} dias")

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
    st.markdown("Registre suas atividades comportamentais e acompanhe sua evolução.")
    st.markdown("---")

    # Sub-abas internas
    ss_tab1, ss_tab2, ss_tab3 = st.tabs(["➕ Registrar Atividade", "📊 Meu Progresso", "📋 Histórico"])

    # -------------------------
    # SUB-ABA 1 — REGISTRAR
    # -------------------------
    with ss_tab1:
        st.markdown("### ➕ Nova Atividade de Soft Skill")

        with st.form("form_soft_skill", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                categoria_sel = st.selectbox("📌 Categoria", list(SOFT_SKILLS_ATIVIDADES.keys()))
            with col_b:
                atividades_cat = [a['nome'] for a in SOFT_SKILLS_ATIVIDADES[categoria_sel]['atividades']]
                atividade_sel = st.selectbox("🎯 Atividade", atividades_cat)

            descricao_livre = st.text_area("📝 O que você fez? (descreva com detalhes)", height=100,
                                           placeholder="Ex: Apresentei o relatório mensal para a equipe de TI, recebi feedback positivo sobre a clareza da apresentação...")

            # Mostrar XP da atividade selecionada
            xp_ativ = next((a['xp'] for a in SOFT_SKILLS_ATIVIDADES[categoria_sel]['atividades'] if a['nome'] == atividade_sel), 20)
            st.info(f"⭐ Esta atividade vale **{xp_ativ} XP**")

            submitted = st.form_submit_button("✅ Registrar Atividade", use_container_width=True)
            if submitted:
                if not descricao_livre.strip():
                    st.error("❌ Descreva o que você fez antes de registrar!")
                else:
                    ok, resultado = adicionar_soft_skill(categoria_sel, atividade_sel, xp_ativ, descricao_livre)
                    if ok:
                        st.success(f"🎉 +{xp_ativ} XP! Atividade registrada com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.warning("⚠️ Você já registrou esta atividade hoje! Tente amanhã ou escolha outra.")

        # Cards das atividades disponíveis
        st.markdown("---")
        st.markdown("### 📚 Atividades Disponíveis")
        for categoria, info in SOFT_SKILLS_ATIVIDADES.items():
            with st.expander(f"📌 {categoria} — {info['descricao']}", expanded=False):
                cols = st.columns(2)
                for i, atv in enumerate(info['atividades']):
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div style="background:rgba(77,159,255,0.08); border-radius:10px; padding:10px; margin:5px 0; border-left:3px solid #ff8800;">
                            <strong>{atv['nome']}</strong> — ⭐ {atv['xp']} XP<br>
                            <small style="color:#aaa;">{atv['descricao']}</small>
                        </div>
                        """, unsafe_allow_html=True)

    # -------------------------
    # SUB-ABA 2 — PROGRESSO
    # -------------------------
    with ss_tab2:
        st.markdown("### 📊 Meu Progresso em Soft Skills")

        historico = st.session_state.get("soft_skills_historico", [])

        if not historico:
            st.info("📭 Nenhuma atividade registrada ainda. Vá para 'Registrar Atividade' e comece!")
        else:
            # KPIs
            total_atividades = len(historico)
            total_xp_soft = sum(a['xp'] for a in historico)
            categorias_feitas = len(set(a['categoria'] for a in historico))
            k1, k2, k3 = st.columns(3)
            k1.metric("✅ Atividades", total_atividades)
            k2.metric("⭐ XP de Soft Skills", total_xp_soft)
            k3.metric("📌 Categorias", f"{categorias_feitas}/4")

            st.markdown("---")

            # Gráfico de barras por categoria (HTML puro)
            st.markdown("### 🏆 Atividades por Categoria")
            contagem = {}
            xp_por_cat = {}
            for a in historico:
                cat = a['categoria']
                contagem[cat] = contagem.get(cat, 0) + 1
                xp_por_cat[cat] = xp_por_cat.get(cat, 0) + a['xp']

            cores_soft = {
                "Comunicação e Apresentação": "#4d9fff",
                "Liderança de Equipes":        "#7b2ff7",
                "Gestão de Projetos":           "#00ff88",
                "Inteligência Emocional":       "#ff8800"
            }

            max_count = max(contagem.values()) if contagem else 1
            altura = 180
            barras = ""
            for cat, qtd in sorted(contagem.items(), key=lambda x: -x[1]):
                pct = (qtd / max_count)
                cor = cores_soft.get(cat, "#4d9fff")
                h = int(pct * altura)
                barras += f"""
                <div style="display:flex; flex-direction:column; align-items:center; flex:1; min-width:80px;">
                    <div style="font-size:12px; color:{cor}; font-weight:bold; margin-bottom:4px;">{qtd}x</div>
                    <div style="width:60%; height:{h}px; background:{cor}; border-radius:8px 8px 0 0;
                                display:flex; align-items:center; justify-content:center; color:white; font-size:11px; font-weight:bold;">
                        {xp_por_cat.get(cat,0)} XP
                    </div>
                    <div style="font-size:10px; color:#aaa; margin-top:6px; text-align:center; max-width:100px;">{cat}</div>
                </div>"""

            grafico_soft = f"""
            <!DOCTYPE html><html>
            <body style="margin:0;padding:16px;background:#0e1117;font-family:sans-serif;">
            <div style="display:flex; align-items:flex-end; gap:12px; height:{altura+60}px; padding:10px;">
                {barras}
            </div>
            </body></html>"""

            import streamlit.components.v1 as components
            components.html(grafico_soft, height=altura + 100, scrolling=False)

            st.markdown("---")

            # Gráfico de atividades por data
            st.markdown("### 📅 Atividades ao Longo do Tempo")
            from collections import defaultdict
            por_data = defaultdict(int)
            for a in historico:
                try:
                    d = datetime.fromisoformat(a['data']).strftime('%d/%m')
                    por_data[d] += a['xp']
                except:
                    pass

            if por_data:
                datas_ord = sorted(por_data.keys(), key=lambda x: datetime.strptime(x, '%d/%m'))
                max_xp_d = max(por_data.values())
                barras_data = ""
                for d in datas_ord:
                    xp_d = por_data[d]
                    h = int((xp_d / max_xp_d) * 140)
                    barras_data += f"""
                    <div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:50px;">
                        <div style="font-size:10px;color:#00ff88;font-weight:bold;margin-bottom:3px;">{xp_d}</div>
                        <div style="width:70%;height:{h}px;background:linear-gradient(180deg,#00ff88,#4d9fff);
                                    border-radius:6px 6px 0 0;"></div>
                        <div style="font-size:10px;color:#aaa;margin-top:5px;">{d}</div>
                    </div>"""

                grafico_tempo = f"""
                <!DOCTYPE html><html>
                <body style="margin:0;padding:16px;background:#0e1117;font-family:sans-serif;">
                <div style="display:flex;align-items:flex-end;gap:8px;height:200px;overflow-x:auto;">
                    {barras_data}
                </div>
                </body></html>"""
                components.html(grafico_tempo, height=220, scrolling=False)

    # -------------------------
    # SUB-ABA 3 — HISTÓRICO
    # -------------------------
    with ss_tab3:
        st.markdown("### 📋 Histórico Completo de Soft Skills")

        historico = st.session_state.get("soft_skills_historico", [])

        if not historico:
            st.info("📭 Nenhuma atividade registrada ainda.")
        else:
            # Filtro por categoria
            cats_disponiveis = ["Todas"] + list(set(a['categoria'] for a in historico))
            filtro_cat = st.selectbox("🔍 Filtrar por categoria", cats_disponiveis)

            for atv in reversed(historico):
                if filtro_cat != "Todas" and atv['categoria'] != filtro_cat:
                    continue
                try:
                    data_fmt = datetime.fromisoformat(atv['data']).strftime('%d/%m/%Y %H:%M')
                except:
                    data_fmt = atv['data']
                cor = cores_soft.get(atv['categoria'], '#4d9fff') if 'cores_soft' in dir() else '#4d9fff'
                st.markdown(f"""
                <div style="background:rgba(77,159,255,0.07); border-radius:10px; padding:12px 16px;
                            margin:8px 0; border-left:4px solid {cor};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:13px; font-weight:bold;">{atv['atividade']}</span>
                        <span style="color:#ffd700; font-weight:bold;">⭐ +{atv['xp']} XP</span>
                    </div>
                    <div style="font-size:11px; color:#888; margin:2px 0;">
                        📌 {atv['categoria']} &nbsp;|&nbsp; 📅 {data_fmt}
                    </div>
                    <div style="font-size:12px; color:#ccc; margin-top:6px;">
                        📝 {atv.get('descricao', '-')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

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
    st.markdown("Sua trilha focada e objetiva para 2026-2027.")
    st.markdown("---")

    for ano, titulo, desc in [
        (2026, "🌱 2026 — Fundação e Especialização",
         "Pós-graduação em andamento, ISO 27001 Implementer, SQL e Security+ concluídos, Inglês em progresso contínuo."),
        (2027, "⚡ 2027 — Consolidação",
         "Continuar a Pós-graduação, conquistar o CySA+ e avançar no Inglês.")
    ]:
        st.markdown(f"### {titulo}")
        st.caption(desc)
        certs_ano = [c for c, d in EMBLEMAS.items() if d.get("ano") == ano or (ano == 2026 and d.get("ano") == "Contínuo")]
        if certs_ano:
            cols = st.columns(len(certs_ano))
            for i, cert in enumerate(certs_ano):
                info = EMBLEMAS[cert]
                status = st.session_state.cert_status.get(cert, "Não iniciada")
                xp_atual = st.session_state.cert_xp.get(cert, 0)
                percent = min((xp_atual / info["xp"]) * 100, 100)
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align:center; padding:16px; background:rgba(77,159,255,0.1);
                                border-radius:12px; border:1px solid rgba(77,159,255,0.2);">
                        <div style="font-size:36px;">{info['emblema']}</div>
                        <div style="font-size:12px; font-weight:bold; color:#4d9fff; margin:6px 0;">{cert}</div>
                        <div style="font-size:11px; color:#aaa;">{info['titulo']}</div>
                        <div style="font-size:20px; margin:6px 0;">{get_badge(status)}</div>
                        <div style="font-size:11px; color:#ffd700;">{xp_atual:,}/{info['xp']:,} XP</div>
                        <div style="font-size:11px; color:#aaa;">{percent:.0f}% concluído</div>
                        <div style="background:#333; border-radius:5px; height:6px; margin-top:8px;">
                            <div style="background:{info['cor']}; width:{percent}%; height:6px; border-radius:5px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("---")

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

# =========================
# TAB 8 - CALENDÁRIO
# =========================
with tab8:
    import calendar as _cal

    # ── Paleta de cores por frente ──
    COR_POS    = "#7b2ff7"
    COR_SEC    = "#185FA5"
    COR_ISO    = "#0C447C"
    COR_ING    = "#1E90FF"
    COR_FUNDO  = "rgba(77,159,255,0.07)"

    # ── Disciplinas da pós com datas exatas ──
    DISCIPLINAS_POS = [
        {"num": 1,  "nome": "Governança de Privacidade e Proteção de Dados",         "inicio": "Mai 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos e bases legais", ["Taxonomia e classificação de dados pessoais", "Princípios norteadores e bases legais para tratamento", "Direitos dos titulares e procedimentos de atendimento"]),
             ("Sem 2", "Gestão e riscos de privacidade", ["Agentes de tratamento e responsabilidades", "Análise de risco e elaboração do RIPDP", "Gestão de consentimentos · resposta a incidentes"]),
             ("Sem 3", "Programa e projeto prático", ["DPO, anonimização e pseudonimização", "Programa PGPPD · IA aplicada à privacidade", "Projeto prático + revisão e entrega final"]),
         ]},
        {"num": 2,  "nome": "Aspectos Jurídicos de Conformidade Digital",            "inicio": "Jun 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Direito digital e LGPD", ["Proteção de dados como direito fundamental", "Panorama internacional de legislações", "LGPD e Marco Civil da Internet"]),
             ("Sem 2", "Responsabilidades e crimes digitais", ["Código de Defesa do Consumidor digital", "Direito penal cibernético e crimes digitais", "Convenção de Budapeste e cooperação internacional"]),
             ("Sem 3", "Contratos, auditorias e projeto", ["Responsabilidade civil e criminal no ciberespaço", "Contratos e acordos de processamento de dados", "Aspectos jurídicos da perícia forense + projeto"]),
         ]},
        {"num": 3,  "nome": "Ethical Hacking e Gestão de Vulnerabilidades",          "inicio": "Jul 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos e ameaças", ["Cenário da cibercriminalidade e ameaças digitais", "Principais tipos de ataques e técnicas ofensivas", "Fundamentos de ethical hacking e offensive security"]),
             ("Sem 2", "Pentest e Red Team", ["Abordagens Pentest e Red Team", "Threat Intelligence e simulação de adversários", "MITRE ATT&CK: táticas, técnicas e procedimentos"]),
             ("Sem 3", "Ferramentas e metodologias", ["Frameworks de análise de vulnerabilidade", "IA para detecção automatizada de vulnerabilidades", "Processo de identificação e gestão de vulnerabilidades"]),
             ("Sem 4", "Projeto prático", ["Execução de pentest guiado em laboratório", "Elaboração de relatório de vulnerabilidades", "Revisão, ajustes e entrega final"]),
         ]},
        {"num": 4,  "nome": "Criptografia e Segurança de Dados",                     "inicio": "Ago 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos criptográficos", ["Sistemas simétricos e assimétricos · cifras de bloco e fluxo", "Principais algoritmos: AES, RSA, ECC, DH", "Criptoanálise · hashing · assinatura digital"]),
             ("Sem 2", "Criptografia em camadas", ["IPSec (rede) · TLS (transporte) · ALE (aplicação)", "mTLS e autenticação mútua · certificados digitais e ICP", "Gerenciamento e ciclo de vida de chaves criptográficas"]),
             ("Sem 3", "Criptografia avançada", ["Blockchain · criptografia pós-quântica", "Criptografia com preservação de formato (FPE)", "Criptografia homomórfica · segurança de dados em trânsito/repouso/uso"]),
             ("Sem 4", "Aplicações e projeto prático", ["IA aplicada em segurança criptográfica", "Laboratório prático de criptografia", "Revisão e entrega final"]),
         ]},
        {"num": 5,  "nome": "DevSecOps: Segurança Integrada e Scanning",             "inicio": "Set 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos DevSecOps", ["Security by Design · SDLC seguro · práticas ágeis", "Segurança end-to-end em pipelines CI/CD", "Visão geral das ferramentas de verificação"]),
             ("Sem 2", "Ferramentas de scanning", ["SAST, DAST, IAST e RASP na prática", "Security Observability: métricas, logs, tracing", "Implementação em pipelines CI/CD"]),
             ("Sem 3", "Cloud-native DevSecOps", ["Melhores práticas em ambientes cloud-native", "IA para análise de vulnerabilidades e threat intelligence", "Threat intelligence integrado ao pipeline"]),
             ("Sem 4", "Projeto prático", ["Construção de pipeline DevSecOps completo", "Integração das ferramentas de segurança", "Revisão, testes e entrega"]),
         ]},
        {"num": 6,  "nome": "Segurança e Gestão da Identidade Digital",              "inicio": "Out 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos IAM", ["Identidade digital e IAM · ciclo de vida de identidades", "Modelos de controle: RBAC, ABAC, PBAC, DAC, MAC", "Autenticação e autorização inteligente"]),
             ("Sem 2", "Tecnologias de identidade", ["Biometria e verificação de identidade", "Segurança da identidade e Zero Trust", "Políticas de Gestão de Acesso (IAM)"]),
             ("Sem 3", "IA em IAM + projeto prático", ["IA aplicada em IAM", "Processos de gerência de identidades e controle de acesso", "Projeto prático + revisão final"]),
         ]},
        {"num": 7,  "nome": "Resposta a Incidentes e Gestão de Crises Cibernéticas", "inicio": "Nov 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos e ciclo de vida", ["Fundamentos de incidentes cibernéticos", "Processo e plano de resposta a incidentes", "Ciclo de vida: NIST SP 800-61 · ISO/IEC 27035"]),
             ("Sem 2", "Tecnologias de apoio", ["SIEM, SOAR e EDR na prática", "Playbooks e runbooks · estrutura e exemplos", "SOC — Centros de Operação de Segurança"]),
             ("Sem 3", "Gestão e simulação", ["Gestão de equipes e comunicação de crise", "Tabletop exercises e simulações de incidentes", "Atividades pós-incidente · lições aprendidas"]),
             ("Sem 4", "IA, aspectos legais e projeto", ["IA aplicada em resposta a incidentes", "Aspectos legais e regulatórios · estudos de caso", "Projeto prático + revisão e entrega"]),
         ]},
        {"num": 8,  "nome": "Computação Forense e Perícia Digital",                  "inicio": "Dez 2026", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos forenses", ["Fundamentos de computação forense", "Evidências digitais e vestígios computacionais", "Metodologias e processos forenses"]),
             ("Sem 2", "Ferramentas e técnicas", ["Ferramentas e tecnologias forenses", "Perícia especializada por ambiente", "Processo de perícia digital"]),
             ("Sem 3", "Aspectos jurídicos e IA", ["Aspectos jurídicos e documentação pericial", "Padrões e normas periciais · IA na perícia digital", "Técnicas anti-forense e contramedidas"]),
             ("Sem 4", "Projeto prático", ["Estudos de casos práticos de forense", "Laboratório forense guiado", "Revisão e entrega final"]),
         ]},
        {"num": 9,  "nome": "Governança de Dados e Compliance",                      "inicio": "Jan 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos da Governança de Dados", ["Contexto organizacional e estratégico dos dados", "Framework DMBoK · Data Stewardship · Data Owners", "Dados Mestres, Referência, Metadados e Catálogo"]),
             ("Sem 2", "Compliance e Governança 2.0", ["Compliance em IA e data-driven: LGPD e GDPR", "Risk Assessment e mitigação de riscos", "Governança 2.0: ética, agilidade, mudança organizacional"]),
             ("Sem 3", "IA e projeto prático", ["IA para análise/geração de políticas e frameworks", "Automação de catalogação e documentação técnica", "Estudo de casos + projeto prático"]),
         ]},
        {"num": 10, "nome": "Arquitetura de Cibersegurança e Zero Trust",            "inicio": "Fev 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos e Zero Trust", ["Fundamentos de arquitetura de segurança", "Paradigma e arquitetura Zero Trust", "Segurança em camadas e defesa em profundidade"]),
             ("Sem 2", "Arquitetura em nuvem e ferramentas", ["CAF e WAF · NGFW · NIDPS · WAF", "CSPM, CNAPP, CWPP, CASB, SASE", "Compliance e Governança em Ambientes Cloud"]),
             ("Sem 3", "IA e projeto prático", ["IA para análise de vulnerabilidades e threat intelligence", "Otimização de arquitetura com IA", "Projeto: implementação de arquitetura Zero Trust"]),
         ]},
        {"num": 11, "nome": "Resiliência Cibernética e Continuidade de Negócios",   "inicio": "Mar 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos de resiliência", ["Fundamentos e estratégias de ciber-resiliência", "NIST 800-34 e ISO 22301", "BIA (Business Impact Analysis)"]),
             ("Sem 2", "Continuidade e recuperação", ["Protocolos e tecnologias para resiliência cibernética", "Plano de recuperação de desastres (DRP) e BCP", "Continuidade em nuvem · DRaaS"]),
             ("Sem 3", "IA e projeto prático", ["IA aplicada à resiliência · governança de equipes", "Projeto prático de resiliência", "Revisão e entrega final"]),
         ]},
        {"num": 12, "nome": "Monitoramento e Observabilidade",                       "inicio": "Abr 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos de observabilidade", ["Monitoramento vs observabilidade · pilares e benefícios", "Design for observability · shift-left observability", "Observabilidade em cloud-native e microsserviços"]),
             ("Sem 2", "Instrumentação e plataformas", ["OpenTelemetry · SLO e Error Budgeting", "Observability Stacks · AIOps e Machine Learning", "SRE e Engenharia de Confiabilidade"]),
             ("Sem 3", "Dashboards e segurança", ["Dashboards, alertas e relatórios de performance", "Logs, métricas e tracing na prática", "Observabilidade de segurança e de escala"]),
             ("Sem 4", "IA e projeto prático", ["IA para predição de falhas e análise de anomalias", "Resposta autônoma com IA", "Projeto: arquitetura observável com IA e SRE"]),
         ]},
        {"num": 13, "nome": "Gestão de Riscos Cibernéticos",                        "inicio": "Mai 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos e frameworks", ["Fundamentos de riscos de segurança da informação", "ISO/IEC 27005 · NIST Cybersecurity Framework", "Programa de gestão de riscos cibernéticos"]),
             ("Sem 2", "Processo de gestão de riscos", ["Escopo, contexto, critério, identificação", "Análise, avaliação e tratamento de riscos", "Comunicação e monitoramento contínuo"]),
             ("Sem 3", "TPRM, IA e casos", ["Gestão de Riscos de Terceiros (TPRM)", "IA aplicada à gestão de riscos", "Cenários e estudos de caso práticos"]),
             ("Sem 4", "Projeto prático", ["Elaboração de relatório de risco", "Projeto de programa de gestão", "Revisão e entrega final"]),
         ]},
        {"num": 14, "nome": "Governança e Compliance em Cibersegurança",             "inicio": "Jun 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "Fundamentos de governança", ["Fundamentos da governança de cibersegurança", "Modelos e frameworks de governança", "Normas: ISO/IEC 27000 e 27003"]),
             ("Sem 2", "Políticas e SGSI", ["Políticas e procedimentos de segurança", "SGSI — Sistema de Gestão da Segurança da Informação", "Programa de cultura e conscientização"]),
             ("Sem 3", "Maturidade e financeiro", ["Avaliação de maturidade em segurança", "PDSI — Plano Diretor de Segurança", "Princípios financeiros e gestão de orçamentos"]),
             ("Sem 4", "GRC, IA e projeto", ["GRC contextualizado em cibersegurança", "IA para compliance, monitoramento e relatórios", "Projeto prático integrado de GRC"]),
             ("Sem 5", "Revisão e entrega final", ["Revisão geral de governança e compliance", "Ajustes finais do projeto", "Entrega e apresentação"]),
         ]},
        {"num": 15, "nome": "Projeto em Cibersegurança e Governança de Dados com IA","inicio": "Jul 2027", "horas": 24,
         "semanas": [
             ("Sem 1", "IA aplicada — fundamentos", ["IA para segurança em cenários reais", "Detecção e resposta a ameaças com IA", "IA Generativa em Cibersegurança: aplicações e riscos"]),
             ("Sem 2", "IA adversarial e LLMs", ["IA Adversarial: ataques, defesas e robustez de modelos", "Engenharia de prompt e proteção contra abusos", "Riscos emergentes em LLMs · análise e mitigação"]),
             ("Sem 3", "Automação e governança de IA", ["Automação de SOC: orquestração, triagem e resposta", "Detecção de anomalias e profiling inteligente", "Governança de IA em ambientes corporativos"]),
             ("Sem 4", "Desenvolvimento e entrega do projeto", ["Desenvolvimento do projeto aplicado com IA", "Integração com cenários de cibersegurança e governança", "Entrega e apresentação final"]),
         ]},
        {"num": 16, "nome": "Humanidades",                                           "inicio": "Jul 2027", "horas": 24,
         "semanas": [
             ("Sem 1–4", "Conteúdo de Humanidades", ["Conteúdo conforme grade curricular da PUC Minas", "Paralelo à Disciplina 15 — Projeto com IA", "Entrega: ago/2027"]),
         ]},
        {"num": 17, "nome": "Trabalho de Conclusão de Curso (TCC)",                  "inicio": "Opcional", "horas": 0,
         "semanas": [
             ("Fase 1", "Escolha e planejamento", ["Definição do tema e orientador", "Revisão bibliográfica e metodologia"]),
             ("Fase 2", "Desenvolvimento", ["Redação, pesquisa e análise", "Orientação e feedbacks"]),
             ("Fase 3", "Entrega e defesa", ["Revisão final e formatação", "Defesa perante banca examinadora"]),
         ]},
    ]
    # ── Cronograma das certificações por mês ──
    CERT_POR_MES = {
        "Mai 2026": {
            "cert": "🛡️ CompTIA Security+", "fase": "FASE 1 — Módulos 1 e 2",
            "semanas": [
                ("Sem 1", "Módulo 1 — Conceitos de Segurança", ["CIA Triad · tipos de controles · regulamentações", "Terminologia: asset, threat, vulnerability, risk, control"]),
                ("Sem 2", "Módulo 2 — Ameaças (Parte 1)", ["Malware: vírus, worm, ransomware, spyware, trojan, rootkit", "Engenharia social: phishing, spear phishing, vishing, smishing"]),
                ("Sem 3", "Módulo 2 — Mitigações (Parte 2)", ["Hardening · patch management · threat hunting", "IoC/IoA · MITRE ATT&CK TTPs"]),
                ("Sem 4", "Revisão + Simulado Parcial", ["Revisão módulos 1–2 · quiz em inglês (Anki)", "Simulado parcial TestOut (30–40 questões)"]),
            ]
        },
        "Jun 2026": {
            "cert": "🛡️ CompTIA Security+", "fase": "FASE 2 — Módulos 3 e 4",
            "semanas": [
                ("Sem 5", "Módulo 3 — Criptografia Parte 1", ["Simétrica: AES, DES · assimétrica: RSA, ECC, DH", "Hashing: SHA-256, HMAC · PKI · certificados X.509"]),
                ("Sem 6", "Módulo 3 — Criptografia Parte 2", ["TLS 1.2/1.3 · handshake · PFS", "Protocolos seguros: HTTPS, SSH, SFTP · criptografia pós-quântica"]),
                ("Sem 7", "Módulo 4 — IAM", ["MFA: TOTP, FIDO2, biometria · RBAC, ABAC, MAC, DAC", "SSO: SAML 2.0, OAuth 2.0, OIDC · PAM"]),
                ("Sem 8", "Revisão + Labs Práticos", ["Lab: TLS e certificados · Lab: MFA e RBAC", "Simulado parcial módulos 3–4 (40 questões)"]),
            ]
        },
        "Jul 2026": {
            "cert": "🛡️ CompTIA Security+", "fase": "FASE 3 — Módulos 5, 6 e 7",
            "semanas": [
                ("Sem 9",  "Módulo 5 — Arquitetura de Rede Parte 1", ["VLANs · segmentação · firewalls · DMZ · IDS/IPS · VPN"]),
                ("Sem 10", "Módulo 5 — Arquitetura de Rede Parte 2", ["ZTNA · SD-WAN · SASE · WPA3 · NAC · 802.1X · DNSSEC"]),
                ("Sem 11", "Módulo 6 — Resiliência", ["HA · backup 3-2-1 · RTO/RPO · BCP/DRP · RAID"]),
                ("Sem 12", "Módulo 7 — Gestão de Vulnerabilidades", ["Nessus/OpenVAS · CVSS v3.1 · CVE · NVD · patch management"]),
                ("Sem 13", "Revisão + Simulado Acumulado", ["Simulado 90 questões módulos 1–7 · análise por domínio"]),
            ]
        },
        "Ago 2026": {
            "cert": "🛡️ CompTIA Security+", "fase": "FASE 4 — Módulos 8, 9 e 10",
            "semanas": [
                ("Sem 14", "Módulo 8 — Endpoint e Rede", ["EDR/XDR · hardening Windows/Linux/mobile · DLP · UEBA"]),
                ("Sem 15", "Módulo 9 — Resposta a Incidentes", ["NIST SP 800-61 · forense básica · chain of custody · tabletop"]),
                ("Sem 16", "Módulo 10 — Protocolos, Apps e Nuvem", ["APIs: OAuth, JWT, OWASP · Shared Responsibility · CASB, CSPM", "Container security: Docker, Kubernetes · serverless"]),
                ("Sem 17", "Revisão Intensiva + Labs", ["Lab resposta a incidentes · lab cloud security", "Simulado completo 90 questões (módulos 1–10)"]),
            ]
        },
        "Set 2026": {
            "cert": "🛡️ CompTIA Security+", "fase": "FASE 5 — Módulos 11, 12 e 13",
            "semanas": [
                ("Sem 18", "Módulo 11 — Governança", ["NIST CSF 2.0 · ISO 27001 · CIS Controls v8", "Classificação de dados · gestão de ativos · papéis e responsabilidades"]),
                ("Sem 19", "Módulo 12 — Gestão de Riscos", ["SLE, ARO, ALE, ROSI · BIA · estratégias de tratamento"]),
                ("Sem 20", "Módulo 13 — Proteção de Dados e Compliance", ["GDPR, HIPAA, PCI-DSS v4, SOX · Privacy by Design · e-discovery"]),
                ("Sem 21", "Revisão GRC + Simulado", ["Simulado GRC 60 questões · comparativo de frameworks"]),
            ]
        },
        "Out 2026": {
            "cert": "🛡️ CompTIA Security+", "fase": "FASE 6 — SIMULADOS INTENSIVOS ★",
            "semanas": [
                ("Sem 22", "Revisão Geral e Pontos Fracos", ["Revisão dos 13 módulos · foco nos domínios mais fracos", "Flashcards, mapas mentais e labs complementares"]),
                ("Sem 23", "Simulado Oficial 1 — Apêndice A", ["90 questões CompTIA SY0-701 · 90 minutos cronometrados", "Análise item a item · estratégia PBQ"]),
                ("Sem 24", "Simulado Oficial 2 — Apêndice B", ["TestOut Security Pro completo · registro de tempo por questão"]),
                ("Sem 25", "Preparação Final", ["Revisão leve · logística Pearson VUE · descanso"]),
                ("★ Sem 26", "PROVA CompTIA Security+ SY0-701", ["Pearson VUE · 90min · 90 questões · Score 750/900 🎉"]),
            ]
        },
        "Nov 2026": {
            "cert": "🔒 ISO 27001 Lead Implementer", "fase": "FASE 1 — Cláusulas 4, 5 e 6",
            "semanas": [
                ("Sem 1", "Visão Geral ISO 27001:2022", ["Histórico 2005/2013/2022 · 93 controles em 4 temas", "Processo de certificação PECB · relação com ISO 27002/27005"]),
                ("Sem 2", "Cláusula 4 — Contexto Organizacional", ["4.1 contexto · 4.2 partes interessadas · 4.3 escopo do SGSI"]),
                ("Sem 3", "Cláusulas 5 e 6 — Liderança e Planejamento", ["Política de SI · papéis · objetivos · ações para tratar riscos"]),
                ("Sem 4", "Revisão + Estudo de Caso", ["Elaborar escopo e política de SI · quiz ISO 27001"]),
            ]
        },
        "Dez 2026": {
            "cert": "🔒 ISO 27001 Lead Implementer", "fase": "FASE 2 — Riscos, SoA e Suporte",
            "semanas": [
                ("Sem 5", "Avaliação e Tratamento de Riscos (ISO 27005)", ["Identificação de ativos, ameaças e vulnerabilidades", "Análise qualitativa (5×5) e quantitativa (ALE=SLE×ARO)", "Plano de Tratamento de Riscos (RTP)"]),
                ("Sem 6", "Declaração de Aplicabilidade (SoA)", ["4 temas e 93 controles do Anexo A versão 2022", "Como selecionar, justificar e documentar controles"]),
                ("Sem 7", "Cláusula 7 — Suporte", ["7.1 Recursos · 7.2 Competências · 7.3 Conscientização", "7.4 Comunicação · 7.5 Informação documentada"]),
                ("Sem 8", "Revisão + Simulado PECB Parcial", ["SoA + matriz de riscos · simulado 50 questões PECB"]),
            ]
        },
        "Jan 2027": {
            "cert": "🔒 ISO 27001 Lead Implementer", "fase": "FASE 3 — Cláusula 8 + Anexo A",
            "semanas": [
                ("Sem 9",  "Cláusula 8 — Operação", ["Controle operacional · avaliação e tratamento de riscos em campo"]),
                ("Sem 10", "Anexo A — Controles Organizacionais (37)", ["Políticas, organização, ativos, acesso, fornecedores (5.1–5.37)"]),
                ("Sem 11", "Anexo A — Pessoas e Físico (22)", ["Triagem, NDA, trabalho remoto (6.1–6.8) · físico (7.1–7.14)"]),
                ("Sem 12", "Anexo A — Tecnológico (34)", ["Endpoint, logging, criptografia, SDLC seguro, DLP (8.1–8.34)"]),
                ("Sem 13", "Revisão Anexo A + Caso Prático", ["Mapa mental 93 controles · simulado 80 questões PECB"]),
            ]
        },
        "Fev 2027": {
            "cert": "🔒 ISO 27001 Lead Implementer", "fase": "FASE 4 — Cláusulas 9 e 10",
            "semanas": [
                ("Sem 14", "Cláusula 9 — Avaliação de Desempenho", ["Monitoramento, medição, auditoria interna, análise crítica pela direção"]),
                ("Sem 15", "Cláusula 10 — Melhoria Contínua", ["NC e RCA · ciclo PDCA · lições aprendidas"]),
                ("Sem 16", "Processo de Certificação", ["Estágio 1 documental · estágio 2 campo · tipos de achados"]),
                ("Sem 17", "Simulado PECB + Revisão", ["120 questões formato real · questões dissertativas"]),
            ]
        },
        "Mar 2027": {
            "cert": "🔒 ISO 27001 Lead Implementer", "fase": "FASE 5 — Implementação Prática",
            "semanas": [
                ("Sem 18", "Projeto de Implementação do SGSI", ["Gap analysis AS-IS vs TO-BE · roadmap 12–18 meses"]),
                ("Sem 19", "Documentação do SGSI", ["12 documentos + 12 registros obrigatórios · controle de versão"]),
                ("Sem 20", "Gestão de Riscos Avançada + Terceiros", ["ISO 27005 aprofundado · due diligence · contratos de SI"]),
                ("Sem 21", "Conscientização + Métricas", ["Programa de conscientização · KPIs · dashboard executivo"]),
            ]
        },
        "Abr 2027": {
            "cert": "🔒 ISO 27001 Lead Implementer", "fase": "FASE 6 — Simulados PECB ★",
            "semanas": [
                ("Sem 22", "Revisão Completa", ["Cláusulas 4–10 + 93 controles · spaced repetition"]),
                ("Sem 23", "Simulado 1 — Formato Real", ["150 questões · 3 horas cronometradas · estudo de caso"]),
                ("Sem 24", "Simulado 2 + Redação", ["Foco em cenários · redação dissertativa · vocabulário PECB"]),
                ("Sem 25", "Preparação Final", ["Revisão leve · logística PECB · descanso"]),
                ("★ Sem 26", "PROVA ISO 27001 Lead Implementer", ["Parte 1: múltipla escolha (2h) · Parte 2: estudo de caso (1h)", "Aprovação: 70% + caso · Atualizar LinkedIn e Credly 🎉"]),
            ]
        },
        "Mai 2027": {"cert": None, "fase": "", "semanas": []},
        "Jun 2027": {"cert": None, "fase": "", "semanas": []},
        "Jul 2027": {"cert": None, "fase": "", "semanas": []},
        "Ago 2027": {"cert": None, "fase": "", "semanas": []},
    }

    INGLES_POR_MES = {
        "Mai 2026": ("B1",  "Deck Anki CompTIA SY0-701 em inglês\nProfessor Messer no YouTube (inglês)\nQuestões de simulado sem tradução\nFoco: ler perguntas sem dicionário"),
        "Jun 2026": ("B1",  "Vocabulário IAM e criptografia\nRisky Business Podcast (inglês)\nFlashcards de algoritmos e protocolos\nNível B1 consolidado"),
        "Jul 2026": ("B1+", "NIST SP 800-61 em inglês\nDarknet Diaries com transcrição\nLeitura de advisories CISA em inglês\nFluência sem parar para traduzir"),
        "Ago 2026": ("B1+", "NIST SP 800-53 em inglês\nSmashing Security Podcast\nNível B1+ → B2 em evolução\nLeitura de CVEs e security advisories"),
        "Set 2026": ("B2",  "CIS Controls v8 em inglês\nCISO Talks Podcast\nQuestões CompTIA sem dicionário\nPreparação final: prova em inglês"),
        "Out 2026": ("B2",  "B2 consolidado · prova em inglês\nAnki de manutenção\nInício do vocabulário ISO/auditoria\nCISO Series Podcast"),
        "Nov 2026": ("B2",  "ISO 27001:2022 texto normativo em inglês\nTerminologia PECB: implement, conform, clause\nSecurity Conversations Podcast\nAnki vocabulário de auditoria"),
        "Dez 2026": ("B2",  "ISO 27002:2022 guidance em inglês\nSecurity Conversations Podcast\nB2 sólido · redação técnica simples\nGlossário ISO português + inglês"),
        "Jan 2027": ("B2",  "Study guides PECB em inglês\nDark Reading · SANS NewsBites\nPrática de redação de respostas curtas\nTerminologia de implementação ISO"),
        "Fev 2027": ("B2+", "ISO 27002 e 27005 em inglês\nCISO Series Podcast\nRedação de respostas PECB em inglês\nB2+ em vocabulário de auditoria"),
        "Mar 2027": ("B2+", "Verizon DBIR em inglês\nIBM X-Force Threat Intelligence Index\nRFC 8446 (TLS 1.3) em inglês\nDark Reading e SANS NewsBites"),
        "Abr 2027": ("B2+", "Manutenção B2+ · Anki de revisão\nLeitura técnica livre\nVocabulário avançado de governança\nPreparação redação PECB"),
        "Mai 2027": ("B2+", "B2+ consolidado · leitura livre\nRFCs e vendor blogs em inglês\nManutenção com podcasts avançados"),
        "Jun 2027": ("B2+", "Leitura técnica livre avançada\nCISO Series e Risky Business\nManutenção B2+ sem esforço extra"),
        "Jul 2027": ("B2+", "B2+ celebração! 🎉\nLeitura livre em inglês\nVocabulário de negócios e liderança"),
        "Ago 2027": ("B2+", "Manutenção B2+ contínua\nPodcasts avançados de segurança\nLeitura de threat reports e white papers"),
    }

    # Mapa fixo: cada mês → quais números de disciplina estão ativos
    DISC_POR_MES = {
        "Mai 2026": [1],        # Disc. 1 — Governança de Privacidade
        "Jun 2026": [2],        # Disc. 2 — Aspectos Jurídicos
        "Jul 2026": [3],        # Disc. 3 — Ethical Hacking
        "Ago 2026": [4],        # Disc. 4 — Criptografia
        "Set 2026": [5],        # Disc. 5 — DevSecOps
        "Out 2026": [6],        # Disc. 6 — Segurança e Gestão da Identidade Digital
        "Nov 2026": [7],        # Disc. 7 — Resposta a Incidentes
        "Dez 2026": [8],        # Disc. 8 — Computação Forense
        "Jan 2027": [9],        # Disc. 9 — Governança de Dados e Compliance
        "Fev 2027": [10],       # Disc. 10 — Arquitetura e Zero Trust
        "Mar 2027": [11],       # Disc. 11 — Resiliência Cibernética
        "Abr 2027": [12],       # Disc. 12 — Monitoramento e Observabilidade
        "Mai 2027": [13],       # Disc. 13 — Gestão de Riscos
        "Jun 2027": [14],       # Disc. 14 — Governança e Compliance
        "Jul 2027": [15, 16],   # Disc. 15 + 16 — Projeto IA + Humanidades
        "Ago 2027": [17],       # Disc. 17 — TCC (opcional)
    }

    def disc_ativa_no_mes(mes_str):
        nums = DISC_POR_MES.get(mes_str, [])
        return [d for d in DISCIPLINAS_POS if d["num"] in nums]

    # ────────────────────────────────────────────
    # HEADER
    # ────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(77,159,255,0.15),rgba(123,47,247,0.08));
                border-radius:14px;padding:18px;text-align:center;margin-bottom:18px;">
        <div style="font-size:24px;font-weight:bold;color:#4d9fff;">📅 CALENDÁRIO COMPLETO — MAI/2026 → AGO/2027</div>
        <div style="font-size:13px;color:#aaa;margin-top:6px;">
            🎓 Pós-Graduação PUC Minas — 17 disciplinas (Disc. 1 inicia em Mai/2026)  &nbsp;|&nbsp;
            🛡️ CompTIA Security+ SY0-701 (Mai–Out/2026)  &nbsp;|&nbsp;
            🔒 ISO 27001 Lead Implementer (Nov/2026–Abr/2027)  &nbsp;|&nbsp;
            🇬🇧 Inglês 20min/dia
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtro
    opcoes = ["Todos os meses"] + MESES_ORDEM
    col_f1, col_f2 = st.columns([1,3])
    with col_f1:
        mes_filtro = st.selectbox("🗓️ Mês:", opcoes, key="cal_filtro")
    meses_render = MESES_ORDEM if mes_filtro == "Todos os meses" else [mes_filtro]

    # ────────────────────────────────────────────
    # RENDER MÊS A MÊS
    # ────────────────────────────────────────────
    for mes in meses_render:
        discs = disc_ativa_no_mes(mes)
        cert_info = CERT_POR_MES.get(mes, {"cert": None, "fase": "", "semanas": []})
        ing_nivel, ing_texto = INGLES_POR_MES.get(mes, ("B1",""))

        # ── Cabeçalho do mês ──
        st.markdown(f"""
        <div style="background:linear-gradient(90deg,rgba(77,159,255,0.18),rgba(123,47,247,0.08));
                    border-left:5px solid #4d9fff;border-radius:10px;
                    padding:12px 18px;margin:22px 0 10px 0;">
            <span style="font-size:20px;font-weight:bold;color:#4d9fff;">📆 {mes}</span>
        </div>
        """, unsafe_allow_html=True)

        col_pos, col_cert, col_ing = st.columns([1.1, 1.1, 0.8])

        # ── PÓS-GRADUAÇÃO ──
        with col_pos:
            st.markdown(f"<div style='font-size:13px;font-weight:bold;color:{COR_POS};margin-bottom:6px;'>🎓 PÓS-GRADUAÇÃO</div>", unsafe_allow_html=True)
            if mes == "Mai 2027":
                st.markdown("""
                <div style="border-left:3px solid #ffd700;padding:8px 12px;border-radius:0 8px 8px 0;
                            background:rgba(255,215,0,0.08);">
                    <span style="font-size:14px;font-weight:bold;color:#ffd700;">🎓 CONCLUSÃO DA PÓS-GRADUAÇÃO!</span><br>
                    <span style="font-size:12px;color:#aaa;">Todas as 16 disciplinas concluídas · TCC entregue (se optante)</span>
                </div>
                """, unsafe_allow_html=True)
            elif discs:
                for d in discs:
                    cor_d = CORES_DISC[(d["num"]-1) % len(CORES_DISC)]
                    st.markdown(f"""
                    <div style="border-left:3px solid {cor_d};padding:6px 10px;
                                margin-bottom:6px;border-radius:0 8px 8px 0;
                                background:rgba(77,159,255,0.05);">
                        <span style="font-size:12px;font-weight:bold;color:{cor_d};">
                            Disc. {d['num']} — {d['nome']}
                        </span><br>
                        <span style="font-size:11px;color:#aaa;">📅 Início: {d['inicio']} · ⏱️ {d['horas']}h</span>
                    </div>
                    """, unsafe_allow_html=True)
                    for sem_label, sem_titulo, sem_subs in d["semanas"]:
                        with st.expander(f"📌 {sem_label} — {sem_titulo}", expanded=False):
                            for sub in sem_subs:
                                st.markdown(f"<div style='font-size:12px;padding:3px 0 3px 10px;border-left:2px solid {cor_d};margin:3px 0;color:#ddd;'>• {sub}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size:12px;color:#666;'>Sem disciplina ativa.</div>", unsafe_allow_html=True)

        # ── CERTIFICAÇÃO ──
        with col_cert:
            if cert_info["cert"]:
                cor_c = COR_SEC if "Security" in cert_info["cert"] else COR_ISO
                emoji_c = "🛡️" if "Security" in cert_info["cert"] else "🔒"
                label_c = cert_info["cert"].replace("🛡️ ","").replace("🔒 ","")
                st.markdown(f"<div style='font-size:13px;font-weight:bold;color:{cor_c};margin-bottom:6px;'>{emoji_c} {label_c}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:11px;color:#aaa;margin-bottom:8px;'>{cert_info['fase']}</div>", unsafe_allow_html=True)
                for sem_label, sem_titulo, sem_subs in cert_info["semanas"]:
                    lbl = sem_titulo[:38] + "…" if len(sem_titulo) > 38 else sem_titulo
                    with st.expander(f"📌 {sem_label} — {lbl}", expanded=False):
                        for sub in sem_subs:
                            st.markdown(f"<div style='font-size:12px;padding:3px 0 3px 10px;border-left:2px solid {cor_c};margin:3px 0;color:#ddd;'>• {sub}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='font-size:13px;font-weight:bold;color:#555;margin-bottom:6px;'>⏳ Certificação</div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:12px;color:#555;'>CompTIA Security+ inicia em Mai/2026</div>", unsafe_allow_html=True)

        # ── INGLÊS ──
        with col_ing:
            st.markdown(f"<div style='font-size:13px;font-weight:bold;color:{COR_ING};margin-bottom:4px;'>🇬🇧 Inglês · Meta: <span style='color:#ffd700;'>{ing_nivel}</span></div>", unsafe_allow_html=True)
            for linha in ing_texto.strip().split("\n"):
                st.markdown(f"<div style='font-size:11px;padding:3px 0 3px 8px;border-left:2px solid {COR_ING};margin:3px 0;color:#ccc;'>• {linha.strip()}</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11px;color:#555;margin-top:6px;'>📌 20min/dia · todos os dias</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(77,159,255,0.15);margin:12px 0;'>", unsafe_allow_html=True)

    # ── Legenda ──
    st.markdown("""
    <div style="background:rgba(77,159,255,0.07);border-radius:10px;padding:12px 16px;margin-top:8px;font-size:12px;color:#aaa;">
    <b style="color:#4d9fff;">📌 Legenda:</b>&nbsp;
    🎓 Pós PUC Minas — 17 disciplinas na sequência exata &nbsp;|&nbsp;
    🛡️ CompTIA Security+ (Mai–Out/2026) &nbsp;|&nbsp;
    🔒 ISO 27001 Lead Implementer (Nov/2026–Mai/2027) &nbsp;|&nbsp;
    🇬🇧 Inglês 20min/dia &nbsp;|&nbsp;
    ★ = Prova &nbsp;|&nbsp;
    Ritmo: 1h30 seg–sex · 2h sáb–dom · ~15h/semana
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 📅 CALENDÁRIO — MAI/2026 ATÉ MAI/2027")
    st.markdown("Cronograma completo das 3 frentes integradas: Pós-Graduação, CompTIA Security+ e ISO 27001 Lead Implementer.")

    # ── Dados do calendário ──
    CALENDARIO = [
        {
            "mes": "Mai 2026",
            "pos": "Disc. 4 — Criptografia e Seg. de Dados (até 03/mai)\nDisc. 5 — DevSecOps: Segurança Integrada e Scanning\n(27 abr → 24 mai)",
            "pos_semanas": [
                ("Sem 1", "DevSecOps Fundamentos", ["Security by Design e SDLC seguro", "CI/CD e pipelines seguros", "Visão geral de integração contínua"]),
                ("Sem 2", "Ferramentas de Scanning", ["SAST, DAST, IAST, RASP", "Implementação em pipelines", "Security Observability: métricas, logs, tracing"]),
                ("Sem 3", "Cloud-native DevSecOps", ["Melhores práticas cloud-native", "IA para análise de vulnerabilidades", "Threat intelligence em pipeline"]),
                ("Sem 4", "Projeto Prático", ["Construção de pipeline DevSecOps completo", "Integração das ferramentas de segurança", "Revisão e entrega"]),
            ],
            "cert": "🛡️ INÍCIO CompTIA Security+\nFase 1 — Módulos 1 e 2",
            "cert_semanas": [
                ("Sem 1", "Módulo 1 — Conceitos de Segurança", ["CIA Triad: Confidencialidade, Integridade, Disponibilidade", "Tipos de controles: preventivo, detectivo, corretivo", "Regulamentações: HIPAA, PCI-DSS, GDPR, NIST CSF", "Terminologia: asset, threat, vulnerability, risk, control"]),
                ("Sem 2", "Módulo 2 — Ameaças (Parte 1)", ["Malware: vírus, worm, ransomware, spyware, trojan, rootkit", "Engenharia social: phishing, spear phishing, vishing, smishing", "Ataques de aplicação: SQL injection, XSS, buffer overflow", "APT e ameaças internas (insider threats)"]),
                ("Sem 3", "Módulo 2 — Mitigações (Parte 2)", ["Hardening de sistemas e patch management", "Threat hunting e IoC/IoA", "MITRE ATT&CK: TTPs e grupos de ameaça", "CIS Benchmarks e baseline de segurança"]),
                ("Sem 4", "Revisão + Simulado Parcial", ["Revisão completa dos módulos 1 e 2", "Quiz de vocabulário técnico em inglês (Anki)", "Simulado parcial no TestOut (30–40 questões)", "Análise e anotação dos pontos fracos"]),
            ],
            "ingles": "Anki — deck CompTIA SY0-701 (inglês)\nProfessor Messer em inglês (YouTube)\nQuestões de simulado sem tradução\nFoco: ler questões sem dicionário",
            "cor": "#185FA5",
            "emoji": "🔵",
        },
        {
            "mes": "Jun 2026",
            "pos": "Disc. 6 — Segurança e Gestão da Identidade Digital\n(18 mai → 07 jun)",
            "pos_semanas": [
                ("Sem 1", "Fundamentos IAM", ["Identidade digital e IAM: conceitos e ciclo de vida", "Modelos de controle: RBAC, ABAC, PBAC, DAC, MAC", "Autenticação e autorização inteligente"]),
                ("Sem 2", "Tecnologias de Identidade", ["Biometria e verificação de identidade", "Segurança da identidade e Zero Trust", "Políticas de Gestão de Acesso (IAM)"]),
                ("Sem 3", "IA em IAM + Projeto", ["IA aplicada em IAM", "Processos de gerência de identidades", "Projeto prático + revisão final"]),
            ],
            "cert": "🛡️ CompTIA Security+ — Fase 2\nMódulos 3 e 4: Criptografia + IAM",
            "cert_semanas": [
                ("Sem 5", "Módulo 3 — Criptografia (Parte 1)", ["Simétrica: AES-128/256, DES, 3DES, ChaCha20", "Assimétrica: RSA, ECC, Diffie-Hellman, DSA", "Hashing: SHA-256, SHA-3, MD5, HMAC", "PKI: CA, RA, CRL, OCSP, certificados X.509"]),
                ("Sem 6", "Módulo 3 — Criptografia (Parte 2)", ["TLS 1.2 vs TLS 1.3: handshake e PFS", "Protocolos seguros: HTTPS, SFTP, SSH, LDAPS", "Assinatura digital e não-repúdio", "Criptografia pós-quântica: CRYSTALS-Kyber (NIST)"]),
                ("Sem 7", "Módulo 4 — IAM", ["IAM: provisionamento e ciclo de vida de identidades", "MFA: TOTP, FIDO2/WebAuthn, biometria, hardware tokens", "SSO e federação: SAML 2.0, OAuth 2.0, OpenID Connect", "PAM: just-in-time access, session recording"]),
                ("Sem 8", "Revisão + Labs Práticos", ["Lab: configurar TLS num servidor web", "Lab: configurar MFA, RBAC e políticas de senha", "Simulado parcial módulos 3 e 4 (40 questões)", "Flashcards de algoritmos criptográficos"]),
            ],
            "ingles": "Anki — vocabulário de IAM e criptografia\nRisky Business Podcast (inglês)\nFlashcards de algoritmos e protocolos\nNível B1 consolidado",
            "cor": "#534AB7",
            "emoji": "🟣",
        },
        {
            "mes": "Jul 2026",
            "pos": "Disc. 7 — Resposta a Incidentes e Gestão de Crises\n(08 jun → 05 jul)\nDisc. 8 — Computação Forense e Perícia Digital\n(06 jul → 02 ago)",
            "pos_semanas": [
                ("Sem 1", "Resposta a Incidentes — Fundamentos", ["Fundamentos de incidentes, processo e plano de resposta", "Ciclo de vida: NIST SP 800-61 e ISO/IEC 27035"]),
                ("Sem 2", "Tecnologias de Resposta", ["SIEM, SOAR, EDR · Playbooks e runbooks · SOC"]),
                ("Sem 3", "Gestão e Simulação", ["Gestão de equipes · Tabletop exercises · Atividades pós-incidente"]),
                ("Sem 4", "IA + Projeto Resposta a Inc.", ["IA em resposta, aspectos legais, projeto prático"]),
                ("Sem 5", "Forense — Fundamentos", ["Fundamentos forenses · Evidências digitais · Metodologias"]),
                ("Sem 6", "Ferramentas Forenses", ["Ferramentas e técnicas · Perícia especializada por ambiente"]),
            ],
            "cert": "🛡️ CompTIA Security+ — Fase 3\nMódulos 5, 6 e 7: Redes, Resiliência, Vulnerabilidades",
            "cert_semanas": [
                ("Sem 9", "Módulo 5 — Arquitetura de Rede (Parte 1)", ["Segmentação: VLANs, subnetting, microsegmentação", "Firewalls: packet filter, stateful, NGFW, WAF · DMZ", "IDS/IPS network-based e host-based", "VPN: SSL/TLS VPN, IPSec tunnel e transport mode"]),
                ("Sem 10", "Módulo 5 — Arquitetura de Rede (Parte 2)", ["Zero Trust Network Access (ZTNA) vs VPN", "SD-WAN, SASE e SSE (Security Service Edge)", "Wireless: WPA3, EAP-TLS, NAC e 802.1X", "Segurança de DNS: DNSSEC, DNS filtering, sinkholes"]),
                ("Sem 11", "Módulo 6 — Resiliência e Segurança", ["Alta disponibilidade: clustering, failover, load balancing", "Backup: full/incremental/diferencial · Regra 3-2-1-1-0", "RTO e RPO · BCP e DRP: tipos de testes", "RAID, replicação síncrona e assíncrona"]),
                ("Sem 12", "Módulo 7 — Gestão de Vulnerabilidades", ["Ciclo de vida: discovery → patch → verify → report", "Ferramentas: Nessus, OpenVAS, Qualys", "CVSS v3.1: base, temporal, ambiental · CVE, NVD", "Patch management: janelas, rollback, ambientes de teste"]),
                ("Sem 13", "Revisão + Simulado Acumulado", ["Simulado acumulado: 90 questões (módulos 1–7)", "Labs: scan de vulnerabilidades, análise de logs de rede", "Análise de performance por domínio", "Replanejamento para módulos com menor acerto"]),
            ],
            "ingles": "NIST SP 800-61 em inglês\nDarknet Diaries Podcast (com transcrição)\nFluência em leitura sem tradução\nNível B1+",
            "cor": "#993C1D",
            "emoji": "🔴",
        },
        {
            "mes": "Ago 2026",
            "pos": "Disc. 8 cont. — Computação Forense e Perícia Digital\nDisc. 9 — Governança de Dados e Compliance\n(03 ago → 23 ago)",
            "pos_semanas": [
                ("Sem 7", "Forense — Aspectos Jurídicos e IA", ["Aspectos jurídicos · documentação pericial · normas", "IA aplicada na perícia digital"]),
                ("Sem 8", "Anti-Forense + Projeto Forense", ["Técnicas anti-forense e contramedidas · projeto prático"]),
                ("Sem 9", "Governança de Dados — Fundamentos", ["Framework DMBoK · Data Stewardship · Metadados · Catálogo"]),
                ("Sem 10", "Compliance e Governança 2.0", ["Compliance LGPD/GDPR · Risk Assessment · Ética em dados"]),
                ("Sem 11", "IA + Projeto Governança", ["IA para políticas e catalogação · projeto prático"]),
            ],
            "cert": "🛡️ CompTIA Security+ — Fase 4\nMódulos 8, 9 e 10: Endpoint, Resposta, Nuvem",
            "cert_semanas": [
                ("Sem 14", "Módulo 8 — Segurança de Rede e Endpoint", ["EDR/XDR e antivírus de nova geração (ML, sandbox)", "Hardening: Windows (Group Policy), Linux (SELinux), mobile (MDM)", "DLP: network, endpoint, cloud · UEBA e log management"]),
                ("Sem 15", "Módulo 9 — Resposta a Incidentes", ["Ciclo de vida NIST SP 800-61: Preparação → Recuperação", "Forense básica: coleta de evidências, chain of custody", "Tabletop exercises e comunicação de crise"]),
                ("Sem 16", "Módulo 10 — Protocolos, Apps e Nuvem", ["Protocolos seguros: HTTPS, SFTP, SSH, SNMPv3, LDAPS", "APIs: OAuth, JWT, OWASP API Top 10, rate limiting", "Shared Responsibility Model · CASB, CSPM, CWPP, CNAPP", "Container security (Docker, Kubernetes)"]),
                ("Sem 17", "Revisão Intensiva + Labs", ["Lab de resposta a incidentes no TestOut", "Lab de cloud security e CASB", "Simulado completo 90 questões (módulos 1–10)", "Identificação de lacunas por domínio"]),
            ],
            "ingles": "NIST SP 800-53 em inglês\nSmashing Security Podcast\nNível B1+ → B2\nLeitura de advisories sem pausa",
            "cor": "#3B6D11",
            "emoji": "🟢",
        },
        {
            "mes": "Set 2026",
            "pos": "Disc. 10 — Arquitetura de Cibersegurança e Zero Trust\n(24 ago → 13 set)\nDisc. 11 — Resiliência Cibernética e Continuidade de Negócios\n(14 set → 04 out)",
            "pos_semanas": [
                ("Sem 1", "Zero Trust — Fundamentos", ["Paradigma Zero Trust · segurança em camadas · defesa em profundidade"]),
                ("Sem 2", "Arquitetura em Nuvem", ["CAF/WAF · NGFW · NIDPS · CSPM · CNAPP · CASB · SASE · endpoint"]),
                ("Sem 3", "IA + Projeto Zero Trust", ["IA na arquitetura · implementação de arquitetura Zero Trust"]),
                ("Sem 4", "Resiliência — Fundamentos", ["Ciber-resiliência · NIST 800-34 · ISO 22301 · BIA"]),
                ("Sem 5", "Continuidade e Recuperação", ["DRP · continuidade em nuvem · DRaaS · protocolos de resiliência"]),
            ],
            "cert": "🛡️ CompTIA Security+ — Fase 5\nMódulos 11, 12 e 13: Governança, Riscos, Compliance",
            "cert_semanas": [
                ("Sem 18", "Módulo 11 — Governança de Segurança", ["Frameworks: NIST CSF 2.0, ISO 27001, CIS Controls v8", "Políticas, procedimentos, padrões e diretrizes — hierarquia", "Classificação de dados: público, interno, confidencial, restrito", "Gestão de ativos: inventário, ciclo de vida, disposal seguro"]),
                ("Sem 19", "Módulo 12 — Gestão de Riscos", ["Qualitativa: probabilidade × impacto, apetite vs tolerância", "Quantitativa: SLE, ARO, ALE, ROSI", "Estratégias: evitar, mitigar, transferir (seguro), aceitar", "BIA: MTD, MTTF, MTTR, MTBF"]),
                ("Sem 20", "Módulo 13 — Proteção de Dados e Compliance", ["GDPR, HIPAA, PCI-DSS v4, SOX, CCPA — obrigações-chave", "Privacy by Design (7 princípios) e Privacy by Default", "E-discovery e retenção legal de dados", "Auditorias: SOC 1, SOC 2, ISO 27001 — diferenças"]),
                ("Sem 21", "Revisão GRC + Simulado", ["Simulado GRC: 60 questões (módulos 11–13)", "Comparativo de frameworks: NIST CSF × ISO 27001 × CIS", "Vocabulário jurídico em inglês: annex, clause, nonconformity", "Análise de performance acumulada"]),
            ],
            "ingles": "CIS Controls v8 em inglês\nCISO Talks Podcast\nNível B2 — questões sem dicionário\nPreparação final para prova CompTIA",
            "cor": "#0F6E56",
            "emoji": "🟤",
        },
        {
            "mes": "Out 2026",
            "pos": "Disc. 11 cont. — Resiliência Cibernética\nDisc. 12 — Monitoramento e Observabilidade\n(05 out → 08 nov)",
            "pos_semanas": [
                ("Sem 6", "Resiliência — IA + Projeto", ["IA aplicada à resiliência · gestão de equipes · projeto prático"]),
                ("Sem 7", "Observabilidade — Fundamentos", ["Monitoramento vs observabilidade · shift-left · pilares"]),
                ("Sem 8", "OpenTelemetry e SLO", ["OpenTelemetry · SLO · Error Budgeting · arquitetura cloud-native"]),
                ("Sem 9", "Plataformas e AIOps", ["Observability Stacks · AIOps e ML · Observability Pipelines"]),
                ("Sem 10", "SRE e Dashboards", ["SRE · dashboards · alertas · logs, métricas e tracing"]),
            ],
            "cert": "🛡️ CompTIA Security+ — FASE 6\n★ SIMULADOS INTENSIVOS → PROVA",
            "cert_semanas": [
                ("Sem 22", "Revisão Geral e Pontos Fracos", ["Revisão completa dos 13 módulos — visão consolidada", "Foco nos domínios com pior desempenho", "Flashcards, mapas mentais e anotações", "Labs complementares nas áreas de maior dificuldade"]),
                ("Sem 23", "Simulado Oficial 1 — Apêndice A", ["CompTIA SY0-701 completo: 90 questões cronometradas", "Análise questão a questão dos erros", "Ajuste de estratégia: eliminação, gestão de tempo", "Atenção especial às questões PBQ (Performance-Based)"]),
                ("Sem 24", "Simulado Oficial 2 — Apêndice B", ["TestOut Security Pro completo — cronometrado", "Registro de tempo por questão", "Revisão focada nas categorias mais fracas", "Técnica de eliminação para questões de cenário complexo"]),
                ("Sem 25", "Preparação Final", ["Revisão leve: máximo 1h/dia, só flashcards", "Sem simulados longos — preservar energia", "Logística: Pearson VUE, documentos, horário", "Sono, alimentação e bem-estar"]),
                ("★ Sem 26", "PROVA CompTIA Security+ SY0-701", ["Pearson VUE — presencial ou online proctored", "90 minutos · 90 questões · Score: 750/900", "Tipos: múltipla escolha + PBQ (Performance-Based)", "Pós-prova: documentação do aprendizado 🎉"]),
            ],
            "ingles": "Smashing Security + CISO Talks\nB2 consolidado — prova em inglês\nAnki de manutenção + vocabulário ISO\nInício do vocabulário de auditoria",
            "cor": "#BA7517",
            "emoji": "🟠",
        },
        {
            "mes": "Nov 2026",
            "pos": "Disc. 12 cont. — Monitoramento e Observabilidade\nDisc. 13 — Gestão de Riscos Cibernéticos\n(09 nov → 06 dez)",
            "pos_semanas": [
                ("Sem 11", "Observabilidade — IA + Projeto", ["IA para predição de falhas e anomalias · projeto SRE"]),
                ("Sem 12", "Gestão de Riscos — Fundamentos", ["ISO/IEC 27005 · NIST CSF · fundamentos de risco"]),
                ("Sem 13", "Processo de Gestão de Riscos", ["Escopo, análise, avaliação e tratamento · comunicação"]),
                ("Sem 14", "TPRM + IA + Projeto", ["Gestão de riscos de terceiros · IA aplicada · projeto prático"]),
            ],
            "cert": "🔒 INÍCIO ISO 27001 Lead Implementer\nFase 1 — Cláusulas 4, 5 e 6",
            "cert_semanas": [
                ("Sem 1", "Visão Geral ISO 27001:2022", ["Histórico: 2005, 2013, 2022 — mudanças principais", "Estrutura HLS — integração com outros sistemas de gestão", "93 controles em 4 temas (era 114 em 14 domínios)", "Processo de certificação PECB: requisitos e exame"]),
                ("Sem 2", "Cláusula 4 — Contexto Organizacional", ["4.1: Contexto interno e externo da organização", "4.2: Partes interessadas e requisitos de SI", "4.3: Determinação do escopo do SGSI", "Ferramentas: SWOT, PESTLE, análise de stakeholders"]),
                ("Sem 3", "Cláusulas 5 e 6 — Liderança e Planejamento", ["5.1: Liderança e comprometimento da alta direção", "5.2: Política de segurança da informação", "5.3: Papéis, responsabilidades e autoridades", "6.1/6.2: Ações para tratar riscos e objetivos de SI"]),
                ("Sem 4", "Revisão + Estudo de Caso Prático", ["Elaborar escopo de SGSI para empresa fictícia", "Rascunho de política de segurança completa", "Quiz de fundamentos ISO 27001 (30 questões)", "Leitura de trechos do texto normativo em inglês"]),
            ],
            "ingles": "Vocabulário ISO 27001 e auditoria\nLeitura do texto normativo em inglês\nCISO Series Podcast\nTerminologia PECB: implement, conform, clause",
            "cor": "#0C447C",
            "emoji": "🔵",
        },
        {
            "mes": "Dez 2026",
            "pos": "Disc. 13 cont. — Gestão de Riscos Cibernéticos\nDisc. 14 — Governança e Compliance em Cibersegurança\n(07 dez → 10 jan)",
            "pos_semanas": [
                ("Sem 15", "Gestão de Riscos — Projeto Prático", ["Programa de gestão de riscos · relatório de risco · entrega"]),
                ("Sem 16", "Governança — Fundamentos", ["Frameworks de governança · ISO/IEC 27000/27003"]),
                ("Sem 17", "Políticas e SGSI", ["Políticas de segurança · SGSI · programa de conscientização"]),
                ("Sem 18", "Maturidade e PDSI", ["Avaliação de maturidade · Plano Diretor · orçamentos"]),
            ],
            "cert": "🔒 ISO 27001 Lead Implementer — Fase 2\nCláusula 6 (Riscos) + SoA + Cláusula 7",
            "cert_semanas": [
                ("Sem 5", "Cláusula 6 — Avaliação e Tratamento de Riscos", ["Identificação de ativos, ameaças, vulnerabilidades e impactos", "Análise qualitativa (5×5) e quantitativa (ALE = SLE × ARO)", "Plano de Tratamento de Riscos (RTP): opções e responsáveis"]),
                ("Sem 6", "Declaração de Aplicabilidade (SoA)", ["4 temas do Anexo A versão 2022: Organizacional, Pessoas, Físico, Tecnológico", "11 atributos dos controles · como selecionar e justificar", "Exercício: elaborar SoA simplificada para empresa fictícia"]),
                ("Sem 7", "Cláusula 7 — Suporte", ["7.1: Recursos · 7.2: Competências · 7.3: Conscientização", "7.4: Comunicação interna e externa sobre o SGSI", "7.5: Informação documentada: criação, controle, retenção"]),
                ("Sem 8", "Revisão e Exercício Prático", ["SoA completa + matriz de riscos tratada (exercício guiado)", "Simulado parcial estilo PECB: 50 questões", "Glossário pessoal ISO 27001 em português e inglês"]),
            ],
            "ingles": "Leitura ISO 27001:2022 em inglês\nSecurity Conversations Podcast\nB2 consolidado\nTerminologia de auditoria e conformidade",
            "cor": "#534AB7",
            "emoji": "🟣",
        },
        {
            "mes": "Jan 2027",
            "pos": "Disc. 14 cont. — Governança e Compliance em Cibersegurança\nDisc. 15 & 16 — Projeto com IA + Humanidades\n(11 jan → 08 fev)",
            "pos_semanas": [
                ("Sem 19", "GRC + IA", ["GRC contextualizado em cibersegurança · IA para compliance"]),
                ("Sem 20", "Projeto Prático GRC", ["Projeto integrado de GRC · revisão e entrega final"]),
                ("Sem 21", "Projeto com IA — Fundamentos", ["IA aplicada · IA Generativa em cybersec · IA Adversarial"]),
                ("Sem 22", "Projeto com IA — Desenvolvimento", ["Engenharia de prompt · privacidade em IA · riscos em LLMs"]),
            ],
            "cert": "🔒 ISO 27001 Lead Implementer — Fase 3\nCláusula 8 + Anexo A completo (93 controles)",
            "cert_semanas": [
                ("Sem 9", "Cláusula 8 — Operação", ["8.1: Planejamento e controle operacional do SGSI", "8.2: Avaliação de riscos em intervalos planejados ou por mudança", "8.3: Executar o RTP — evidências e monitoramento"]),
                ("Sem 10", "Anexo A — Controles Organizacionais (37 controles)", ["Políticas, organização, papéis, segregação de funções (5.1–5.8)", "Gestão de ativos: inventário, classificação, uso aceitável (5.9–5.14)", "Controles de acesso, identidade, autenticação, privilégios (5.15–5.18)", "Segurança de fornecedores, supply chain, conformidade (5.19–5.37)"]),
                ("Sem 11", "Anexo A — Controles de Pessoas e Físicos (22 controles)", ["Pessoas (6.1–6.8): triagem, NDA, conscientização, trabalho remoto", "Físico (7.1–7.14): perímetro, acesso, clear desk, descarte seguro"]),
                ("Sem 12", "Anexo A — Controles Tecnológicos (34 controles)", ["Endpoint, hardening, antimalware, gestão de vulnerabilidades (8.1–8.9)", "Logging, monitoramento, criptografia, gestão de chaves (8.15, 8.24)", "Desenvolvimento seguro, SDLC, testes (8.25–8.29)", "DLP, backup, redundância, segurança de redes (8.11–8.23)"]),
                ("Sem 13", "Revisão Anexo A + Caso Prático", ["Mapa mental: 93 controles por tema", "Exercício: mapear controles ao estudo de caso", "Simulado: 80 questões estilo PECB com cenários"]),
            ],
            "ingles": "Study guides PECB em inglês\nDark Reading e SANS NewsBites\nPrática de redação em inglês (prep. PECB)\nB2 — vocabulário de auditoria ISO",
            "cor": "#0F6E56",
            "emoji": "🟢",
        },
        {
            "mes": "Fev 2027",
            "pos": "Disc. 15 & 16 cont. — Entrega final\nTCC (opcional) — início",
            "pos_semanas": [
                ("Sem 23", "Projeto com IA — Automação de SOC", ["Automação de SOC · detecção de anomalias · governança de IA"]),
                ("Sem 24", "Entrega Final + Início TCC", ["Entrega do projeto aplicado · início do TCC (se optante)"]),
            ],
            "cert": "🔒 ISO 27001 Lead Implementer — Fase 4\nCláusulas 9 e 10: Avaliação + Melhoria",
            "cert_semanas": [
                ("Sem 14", "Cláusula 9 — Avaliação de Desempenho", ["9.1: Monitoramento, medição, análise e avaliação — o que, como, quando", "9.2: Auditoria interna: programa, execução e relatório de achados", "9.3: Análise crítica pela direção — entradas e saídas obrigatórias", "KPIs e métricas: incidentes, MTTD, MTTR, cobertura de controles"]),
                ("Sem 15", "Cláusula 10 — Melhoria Contínua", ["10.1: Melhoria contínua do SGSI", "10.2: Não-conformidade e RCA (Root Cause Analysis)", "Ciclo PDCA aplicado ao SGSI: Plan → Do → Check → Act", "Lições aprendidas: captura, registro e integração"]),
                ("Sem 16", "Processo de Certificação ISO 27001", ["Estágio 1 (documental): o que o auditor verifica", "Estágio 2 (campo): entrevistas, observação, evidências", "Achados: conformidade, OFI, NC menor, NC maior", "Manutenção: vigilância anual e recertificação trienal"]),
                ("Sem 17", "Simulado PECB + Revisão", ["Simulado 120 questões — formato real PECB", "Questões de estudo de caso: respostas dissertativas", "Mapeamento: peso por domínio no exame PECB", "Identificação de lacunas finais"]),
            ],
            "ingles": "ISO 27002:2022 guidance em inglês\nB2+ em vocabulário de auditoria\nPrática de redação de respostas curtas\nCISO Series Podcast (manutenção)",
            "cor": "#993C1D",
            "emoji": "🔴",
        },
        {
            "mes": "Mar 2027",
            "pos": "TCC — Desenvolvimento e orientação",
            "pos_semanas": [
                ("TCC", "Desenvolvimento do TCC", ["Pesquisa, revisão bibliográfica e redação", "Orientação e feedback do professor"]),
            ],
            "cert": "🔒 ISO 27001 Lead Implementer — Fase 5\nImplementação prática: projeto SGSI",
            "cert_semanas": [
                ("Sem 18", "Projeto de Implementação do SGSI", ["Gap analysis: AS-IS vs TO-BE (requisitos ISO 27001)", "Roadmap de implementação: 12–18 meses, fases e marcos", "Gestão de stakeholders, patrocínio executivo, quick wins"]),
                ("Sem 19", "Documentação do SGSI", ["12 documentos + 12 registros obrigatórios pela norma", "Política de SI: estrutura, aprovação, divulgação, revisão", "Controle de documentos: versão, aprovação, distribuição"]),
                ("Sem 20", "Gestão de Riscos Avançada + Terceiros", ["ISO 27005:2022: processo detalhado de GR", "Due diligence de fornecedores: questionários, certificações exigidas", "Contratos com cláusulas de segurança · monitoramento contínuo"]),
                ("Sem 21", "Programa de Conscientização + Métricas", ["Design de programa de conscientização: canais, frequência, mensuração", "Dashboard de SI para reporte executivo: métricas e tendências", "Estudos de casos reais de implementação ISO 27001"]),
            ],
            "ingles": "White papers de segurança em inglês\nVerizon DBIR (leitura em inglês)\nDark Reading, SANS NewsBites\nB2+ — leitura técnica avançada",
            "cor": "#BA7517",
            "emoji": "🟠",
        },
        {
            "mes": "Abr 2027",
            "pos": "TCC — Revisão final e banca",
            "pos_semanas": [
                ("TCC", "Revisão Final + Banca", ["Revisão, formatação e defesa perante banca"]),
            ],
            "cert": "🔒 ISO 27001 Lead Implementer — Fase 6\nSimulados PECB intensivos",
            "cert_semanas": [
                ("Sem 22", "Revisão Completa — Cláusulas + Anexo A", ["Revisão cláusulas 4–10 com foco em questões de exame", "Mapa mental dos 93 controles por tema", "Técnicas: spaced repetition (Anki), associações, esquemas visuais"]),
                ("Sem 23", "Simulado Completo 1 — Formato Real", ["150 questões múltipla escolha — 3 horas cronometradas", "Questões de estudo de caso: prática de redação dissertativa", "Revisão detalhada dos erros"]),
                ("Sem 24", "Simulado Completo 2 + Redação", ["Simulado 2: foco em cenários de implementação e auditoria", "Preparação e ensaio do estudo de caso escrito do exame", "Revisão terminologia ISO/PECB em inglês"]),
                ("Sem 25", "Preparação Final", ["Revisão leve: máximo 1h/dia, só pontos-chave", "Logística: plataforma PECB, horário, documentos", "Descanso e cuidados com bem-estar"]),
            ],
            "ingles": "Manutenção B2+ — Anki de revisão\nRFC 8446 (TLS 1.3) em inglês\nIBM X-Force Threat Intelligence Index\nVocabulário avançado de governança",
            "cor": "#0C447C",
            "emoji": "🔵",
        },
        {
            "mes": "Mai 2027",
            "pos": "Conclusão da Pós-Graduação 🎓",
            "pos_semanas": [
                ("🎓", "Conclusão!", ["Entrega final e colação de grau 🎓"]),
            ],
            "cert": "🔒 ★ PROVA ISO 27001 Lead Implementer\nExame PECB — Mai/2027 🏆",
            "cert_semanas": [
                ("★ Sem 26", "EXAME ISO/IEC 27001 LEAD IMPLEMENTER (PECB)", ["Parte 1: questões de múltipla escolha (2h)", "Parte 2: estudo de caso dissertativo (1h)", "Pontuação: 70% + aprovação no caso", "Pós-exame: atualizar LinkedIn, currículo e Credly 🎉"]),
            ],
            "ingles": "Manutenção B2+ livre\nRFCs, threat reports, vendor blogs\nLeitura técnica sem restrição\nCelebração da jornada! 🎉",
            "cor": "#0F6E56",
            "emoji": "🏆",
        },
    ]

    # ── Filtro de mês ──
    meses_disponiveis = [m["mes"] for m in CALENDARIO]
    mes_selecionado = st.selectbox("🗓️ Selecionar mês:", ["Todos"] + meses_disponiveis)

    dados_filtrados = CALENDARIO if mes_selecionado == "Todos" else [m for m in CALENDARIO if m["mes"] == mes_selecionado]

    # ── Render ──
    for mes_data in dados_filtrados:
        cor = mes_data["cor"]
        emoji = mes_data["emoji"]

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{cor}22,{cor}11);border-left:4px solid {cor};
                    border-radius:12px;padding:14px 18px;margin:18px 0 8px 0;">
            <span style="font-size:22px;font-weight:bold;color:{cor};">{emoji} {mes_data['mes']}</span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])

        # ── COLUNA PÓS ──
        with col1:
            st.markdown(f"<div style='font-size:13px;font-weight:bold;color:#7b2ff7;'>🎓 PÓS-GRADUAÇÃO</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:12px;color:#ccc;white-space:pre-line;margin-bottom:8px;'>{mes_data['pos']}</div>", unsafe_allow_html=True)
            for sem_label, sem_titulo, sem_subs in mes_data["pos_semanas"]:
                with st.expander(f"📌 {sem_label} — {sem_titulo}"):
                    for sub in sem_subs:
                        st.markdown(f"<div style='font-size:12px;padding:3px 0 3px 10px;border-left:2px solid #7b2ff7;margin:3px 0;color:#ddd;'>• {sub}</div>", unsafe_allow_html=True)

        # ── COLUNA CERTIFICAÇÃO ──
        with col2:
            st.markdown(f"<div style='font-size:13px;font-weight:bold;color:{cor};'>{'🛡️ COMPTIA SECURITY+' if '🛡️' in mes_data['cert'] else '🔒 ISO 27001'}</div>", unsafe_allow_html=True)
            cert_clean = mes_data['cert'].replace('🛡️ ','').replace('🔒 ','')
            st.markdown(f"<div style='font-size:12px;color:#ccc;white-space:pre-line;margin-bottom:8px;'>{cert_clean}</div>", unsafe_allow_html=True)
            for sem_label, sem_titulo, sem_subs in mes_data["cert_semanas"]:
                lbl = sem_titulo[:35] + "…" if len(sem_titulo) > 35 else sem_titulo
                with st.expander(f"📌 {sem_label} — {lbl}"):
                    for sub in sem_subs:
                        st.markdown(f"<div style='font-size:12px;padding:3px 0 3px 10px;border-left:2px solid {cor};margin:3px 0;color:#ddd;'>• {sub}</div>", unsafe_allow_html=True)

        # ── COLUNA INGLÊS ──
        with col3:
            st.markdown("<div style='font-size:13px;font-weight:bold;color:#1E90FF;'>🇬🇧 INGLÊS (20min/dia)</div>", unsafe_allow_html=True)
            for linha in mes_data["ingles"].split("\n"):
                st.markdown(f"<div style='font-size:12px;padding:4px 0 4px 10px;border-left:2px solid #1E90FF;margin:3px 0;color:#ddd;'>• {linha}</div>", unsafe_allow_html=True)

        st.markdown("---")

    # ── Legenda final ──
    st.markdown("""
    <div style="background:rgba(77,159,255,0.08);border-radius:10px;padding:12px 16px;margin-top:10px;font-size:12px;color:#aaa;">
    <b style="color:#4d9fff;">📌 Legenda:</b>&nbsp;
    🛡️ CompTIA Security+ (Mai–Nov 2026) &nbsp;|&nbsp;
    🔒 ISO 27001 Lead Implementer (Nov 2026–Mai 2027) &nbsp;|&nbsp;
    🇬🇧 Inglês técnico 20min/dia todos os dias &nbsp;|&nbsp;
    ★ = Data alvo do exame &nbsp;|&nbsp;
    Ritmo: 1h30 seg–sex · 2h sáb–dom
    </div>
    """, unsafe_allow_html=True)

st.caption("🚀 Continue sua jornada, o universo te espera!")
