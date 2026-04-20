import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# =========================
# CONFIGURAÇÃO DE PERSISTÊNCIA
# =========================
def get_data_path():
    render_disk = Path("/opt/render/project/src/dados")
    if render_disk.exists() or os.getenv("RENDER"):
        render_disk.mkdir(exist_ok=True)
        return render_disk
    return Path(".")

DATA_FILE = get_data_path() / "progresso_juan.json"

def carregar_dados():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="🚀 Missão Carreira - Juan Felipe da Silva", layout="wide")

# =========================
# CREDENCIAIS
# =========================
USUARIO_VALIDO = "Juan"
SENHA_VALIDA = "Ju@n1990"

# =========================
# SOFT SKILLS
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
# CONTEÚDO DAS CERTIFICAÇÕES (VERSÃO RESUMIDA PARA CABER)
# =========================
CONTEUDO_CERTIFICACOES = {
    "AZ-900": {
        "titulo": "Microsoft Azure Fundamentals",
        "descricao": "Certificação de entrada para Azure.",
        "dominios": [{"nome": "Conceitos de nuvem", "topicos": ["Benefícios da nuvem", "Modelos de serviço", "Modelos de implantação"]}],
        "recursos": ["Microsoft Learn", "YouTube - John Savill"],
        "simulados": ["Microsoft Learn Assessment", "ExamTopics"],
        "semanas": 3, "horas": 30
    },
    "SC-900": {
        "titulo": "Microsoft Security, Compliance, and Identity",
        "descricao": "Conceitos de segurança na Microsoft.",
        "dominios": [{"nome": "Segurança", "topicos": ["Zero Trust", "Defesa em profundidade"]}],
        "recursos": ["Microsoft Learn", "YouTube - John Savill"],
        "simulados": ["Microsoft Learn Assessment"],
        "semanas": 2, "horas": 25
    },
    "Security+": {
        "titulo": "CompTIA Security+",
        "descricao": "Certificação fundamental de cibersegurança.",
        "dominios": [{"nome": "Ameaças", "topicos": ["Malware", "Ataques de rede", "Ataques de aplicação"]}],
        "recursos": ["Professor Messer", "CompTIA Official"],
        "simulados": ["ExamCompass", "Jason Dion"],
        "semanas": 10, "horas": 80
    },
    "CCNA": {
        "titulo": "Cisco Certified Network Associate",
        "descricao": "Fundamentos de redes Cisco.",
        "dominios": [{"nome": "Redes", "topicos": ["Modelo OSI", "Switching", "Roteamento"]}],
        "recursos": ["Jeremy's IT Lab", "Cisco Packet Tracer"],
        "simulados": ["Boson ExSim"],
        "semanas": 12, "horas": 120
    },
    "Python": {
        "titulo": "Python para Análise de Dados",
        "descricao": "Linguagem Python aplicada a dados.",
        "dominios": [{"nome": "Python", "topicos": ["Sintaxe", "Pandas", "Automação"]}],
        "recursos": ["Hashtag Treinamentos", "Curso em Vídeo"],
        "simulados": ["HackerRank"],
        "semanas": 8, "horas": 60
    },
    "Power BI": {
        "titulo": "Power BI Data Analyst",
        "descricao": "Análise e visualização de dados.",
        "dominios": [{"nome": "Power BI", "topicos": ["Power Query", "DAX", "Dashboards"]}],
        "recursos": ["Hashtag Treinamentos", "Microsoft Learn"],
        "simulados": ["Microsoft Learn Assessment"],
        "semanas": 6, "horas": 50
    },
    "SQL": {
        "titulo": "SQL para Análise de Dados",
        "descricao": "Consultas e manipulação de bancos de dados.",
        "dominios": [{"nome": "SQL", "topicos": ["SELECT", "JOINs", "Subconsultas"]}],
        "recursos": ["SQLZoo", "Mode Analytics"],
        "simulados": ["HackerRank"],
        "semanas": 6, "horas": 45
    },
    "AWS Cloud Practitioner": {
        "titulo": "AWS Cloud Practitioner",
        "descricao": "Fundamentos da AWS Cloud.",
        "dominios": [{"nome": "AWS", "topicos": ["Conceitos de nuvem", "Serviços principais"]}],
        "recursos": ["AWS Skill Builder", "YouTube - Stephane Maarek"],
        "simulados": ["AWS Official Practice"],
        "semanas": 4, "horas": 30
    },
    "Scrum Fundamentals": {
        "titulo": "Scrum Fundamentals",
        "descricao": "Metodologia ágil para gestão de projetos.",
        "dominios": [{"nome": "Scrum", "topicos": ["Papéis", "Eventos", "Artefatos"]}],
        "recursos": ["Scrum Guide", "Scrum.org"],
        "simulados": ["Scrum.org Open Assessment"],
        "semanas": 1, "horas": 16
    }
}

# =========================
# EMBLEMAS
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️", "cor": "#00A4EF", "xp": 120, "ano": 2026},
    "SC-900": {"emblema": "🔐", "cor": "#0078D4", "xp": 100, "ano": 2026},
    "Security+": {"emblema": "🛡️", "cor": "#FF0000", "xp": 120, "ano": 2027},
    "CCNA": {"emblema": "🌐", "cor": "#1BA0D7", "xp": 150, "ano": 2026},
    "Python": {"emblema": "🐍", "cor": "#3776AB", "xp": 150, "ano": 2026},
    "Power BI": {"emblema": "📊", "cor": "#F2C811", "xp": 120, "ano": 2026},
    "SQL": {"emblema": "🗄️", "cor": "#F29111", "xp": 120, "ano": 2026},
    "AWS Cloud Practitioner": {"emblema": "☁️📘", "cor": "#FF9900", "xp": 100, "ano": 2027},
    "Scrum Fundamentals": {"emblema": "🔄", "cor": "#0A5C4A", "xp": 60, "ano": 2026},
    "CISSP": {"emblema": "👑", "cor": "#C0C0C0", "xp": 200, "ano": 2029},
    "GICSP": {"emblema": "🏭", "cor": "#606060", "xp": 180, "ano": 2028}
}

# =========================
# CSS
# =========================
st.markdown("""
<style>
html, body { background: linear-gradient(135deg, #0a0e27, #1a1f3a); color: #4d9fff; }
h1, h2, h3 { background: linear-gradient(135deg, #4d9fff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
.red-text { color: #ff4444 !important; font-weight: bold; }
.green-text { color: #00ff88 !important; }
.stButton button { background: linear-gradient(135deg, #4d9fff, #7b2ff7) !important; color: white !important; border-radius: 10px; }
.cert-card { background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 12px; padding: 10px; margin: 5px; border: 1px solid rgba(77,159,255,0.3); }
.atividade-card { background: linear-gradient(135deg, rgba(77,159,255,0.08), rgba(123,47,247,0.03)); border-radius: 10px; padding: 10px; margin: 5px 0; border-left: 3px solid #4d9fff; }
.kpi-card { background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08)); border-radius: 12px; padding: 15px; text-align: center; }
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
# FUNÇÕES
# =========================
def calc_xp(atividade):
    tabela = {"📚 Estudo": 10, "🔬 Laboratório": 20, "🏗️ Projeto": 30, "🔄 Revisão": 15, "📝 Simulado": 15, "🎓 Aula Pós": 25, "🌎 Inglês": 15, "🏅 Certificação": 50}
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
    salvar_dados({"db": st.session_state.db, "xp": st.session_state.xp, "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status, "soft_skills_concluidas": st.session_state.soft_skills_concluidas, "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos})

def adicionar_soft_skill(categoria, atividade, xp):
    key = f"{categoria}_{atividade}"
    if key not in st.session_state.soft_skills_concluidas:
        st.session_state.soft_skills_concluidas[key] = True
        st.session_state.xp += xp
        salvar_dados({"db": st.session_state.db, "xp": st.session_state.xp, "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status, "soft_skills_concluidas": st.session_state.soft_skills_concluidas, "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos})
        return True
    return False

def marcar_topico_certificacao(cert, dominio, topico, concluido):
    key = f"{cert}_{dominio}_{topico}"
    if concluido and key not in st.session_state.cert_topicos_concluidos:
        st.session_state.cert_topicos_concluidos[key] = True
        st.session_state.xp += 3
        salvar_dados({"db": st.session_state.db, "xp": st.session_state.xp, "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status, "soft_skills_concluidas": st.session_state.soft_skills_concluidas, "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos})
    elif not concluido and key in st.session_state.cert_topicos_concluidos:
        del st.session_state.cert_topicos_concluidos[key]
        st.session_state.xp -= 3
        salvar_dados({"db": st.session_state.db, "xp": st.session_state.xp, "cert_xp": st.session_state.cert_xp, "cert_status": st.session_state.cert_status, "soft_skills_concluidas": st.session_state.soft_skills_concluidas, "cert_topicos_concluidos": st.session_state.cert_topicos_concluidos})

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

# =========================
# CARREGAR DADOS
# =========================
dados = carregar_dados()
if dados:
    st.session_state.db = dados.get("db", [])
    st.session_state.xp = dados.get("xp", 0)
    st.session_state.cert_xp = dados.get("cert_xp", st.session_state.cert_xp)
    st.session_state.cert_status = dados.get("cert_status", st.session_state.cert_status)
    st.session_state.soft_skills_concluidas = dados.get("soft_skills_concluidas", {})
    st.session_state.cert_topicos_concluidos = dados.get("cert_topicos_concluidos", {})

# =========================
# LOGIN
# =========================
if not st.session_state.autenticado:
    st.markdown('<div style="max-width: 400px; margin: 100px auto; padding: 40px; background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05)); border-radius: 20px; text-align: center;"><h1>🚀 MISSÃO CARREIRA</h1><h3>Acesso Autorizado</h3></div>', unsafe_allow_html=True)
    usuario = st.text_input("👨‍🚀 Usuário")
    senha = st.text_input("🔒 Senha", type="password")
    if st.button("🚀 Entrar", use_container_width=True):
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos!")
    st.stop()

# =========================
# HEADER
# =========================
hoje = datetime.now()
st.markdown(f'<div style="background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.08)); border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px;"><div style="font-size: 28px; font-weight: bold;">{hoje.strftime("%d/%m/%Y")}</div><div>{hoje.strftime("%A")}</div></div>', unsafe_allow_html=True)
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
    total_certs = len(EMBLEMAS)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
    st.progress(concluidas / total_certs if total_certs > 0 else 0)
    st.caption(f"{concluidas}/{total_certs} certificações")
    st.markdown("---")
    atv_hoje = get_atividades_hoje()
    st.markdown(f"**📅 Hoje:** {len(atv_hoje)} atv | +{sum(a['xp'] for a in atv_hoje)} XP")
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# =========================
# ABAS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Dashboard", "📚 Certificações", "💪 Soft Skills", "🎖️ Progresso"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    st.markdown("## ⚡ ATIVIDADES DE HOJE")
    col1, col2 = st.columns([3, 1])
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
        st.markdown(f'<div class="kpi-card"><div style="font-size: 36px;">⭐</div><div style="font-size: 28px;">+{sum(a["xp"] for a in get_atividades_hoje())}</div><div>XP hoje</div></div>', unsafe_allow_html=True)
    
    if get_atividades_hoje():
        for atv in get_atividades_hoje():
            emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
            st.markdown(f'<div class="atividade-card">{emblema} **{atv["area"][:30]}** | {atv["atividade"]} | ⭐ +{atv["xp"]}<br><small>📝 {atv["obs"][:50] if atv["obs"] else "-"}</small></div>', unsafe_allow_html=True)
    else:
        st.info("✨ Nenhuma atividade hoje. Comece agora!")
    
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎮 Missões", len(st.session_state.db))
    c2.metric("⭐ XP", st.session_state.xp)
    c3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
    c4.metric("✅ Certificações", f"{concluidas}/{total_certs}")

# =========================
# TAB 2 - CERTIFICAÇÕES
# =========================
with tab2:
    st.markdown("## 📚 CERTIFICAÇÕES")
    cert_selecionada = st.selectbox("Selecione", list(CONTEUDO_CERTIFICACOES.keys()))
    if cert_selecionada in CONTEUDO_CERTIFICACOES:
        info = CONTEUDO_CERTIFICACOES[cert_selecionada]
        st.markdown(f"### {EMBLEMAS[cert_selecionada]['emblema']} {cert_selecionada}")
        st.markdown(f"**{info['titulo']}**")
        st.markdown(f"{info['descricao']}")
        st.markdown(f"⏱️ {info['semanas']} semanas ({info['horas']} horas)")
        
        for dominio in info['dominios']:
            st.markdown(f"#### 📌 {dominio['nome']}")
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
        
        st.markdown("### 🎓 Recursos")
        for r in info['recursos']:
            st.markdown(f"- {r}")

# =========================
# TAB 3 - SOFT SKILLS
# =========================
with tab3:
    st.markdown("## 💪 SOFT SKILLS")
    for categoria, info in SOFT_SKILLS_ATIVIDADES.items():
        with st.expander(f"📌 {categoria}", expanded=False):
            st.markdown(f"*{info['descricao']}*")
            cols = st.columns(2)
            for i, atv in enumerate(info['atividades']):
                with cols[i % 2]:
                    if st.button(f"✅ {atv['nome']} (+{atv['xp']} XP)", key=f"soft_{categoria}_{atv['nome']}", use_container_width=True):
                        if adicionar_soft_skill(categoria, atv['nome'], atv['xp']):
                            st.success(f"+{atv['xp']} XP!")
                            st.rerun()
                        else:
                            st.info("Já concluída!")

# =========================
# TAB 4 - PROGRESSO
# =========================
with tab4:
    st.markdown("## 🎖️ PROGRESSO")
    for cert, info in EMBLEMAS.items():
        xp_atual = st.session_state.cert_xp.get(cert, 0)
        xp_max = info["xp"]
        percentual = min(xp_atual / xp_max, 1.0)
        status = st.session_state.cert_status[cert]
        st.markdown(f"**{info['emblema']} {cert}** - {xp_atual}/{xp_max} XP - {get_badge(status)}")
        st.progress(percentual)

st.caption("🚀 Continue sua jornada, o universo te espera!")
