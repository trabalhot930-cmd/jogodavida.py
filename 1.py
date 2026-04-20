import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from supabase import create_client, Client

# =========================
# CONFIGURAÇÃO SUPABASE
# =========================
SUPABASE_URL = "https://bhwqrfolkusuzvwavanc.supabase.co"
SUPABASE_KEY = "sb_publishable_J_z2LmOOVT0cmJuYhqW0qg_9iAEHt4u"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="🚀 Missão Carreira - Juan Felipe", layout="wide")

# =========================
# CREDENCIAIS
# =========================
USUARIO_VALIDO = "Juan"
SENHA_VALIDA = "Ju@n1990"

# =========================
# DADOS DAS CERTIFICAÇÕES
# =========================
CERTIFICACOES = {
    "AZ-900": {"emblema": "☁️", "xp_max": 120, "cor": "#00A4EF", "ano": 2026, "descricao": "Microsoft Azure Fundamentals - Conceitos básicos de nuvem"},
    "SC-900": {"emblema": "🔐", "xp_max": 100, "cor": "#0078D4", "ano": 2026, "descricao": "Security, Compliance and Identity Fundamentals"},
    "AWS Cloud Practitioner": {"emblema": "☁️📘", "xp_max": 100, "cor": "#FF9900", "ano": 2027, "descricao": "Fundamentos da AWS Cloud"},
    "Security+": {"emblema": "🛡️", "xp_max": 120, "cor": "#FF0000", "ano": 2027, "descricao": "CompTIA Security+ - Cibersegurança"},
    "CCNA": {"emblema": "🌐", "xp_max": 150, "cor": "#1BA0D7", "ano": 2026, "descricao": "Cisco Certified Network Associate"},
    "Python": {"emblema": "🐍", "xp_max": 150, "cor": "#3776AB", "ano": 2026, "descricao": "Python para Análise de Dados"},
    "Power BI": {"emblema": "📊", "xp_max": 120, "cor": "#F2C811", "ano": 2026, "descricao": "Microsoft Power BI Data Analyst"},
    "SQL": {"emblema": "🗄️", "xp_max": 120, "cor": "#F29111", "ano": 2026, "descricao": "SQL para Análise de Dados"},
    "ISO 27001": {"emblema": "🔒", "xp_max": 100, "cor": "#FFD700", "ano": 2026, "descricao": "ISO 27001 Fundamentals"},
    "CySA+": {"emblema": "🔍", "xp_max": 150, "cor": "#FF4500", "ano": 2027, "descricao": "CompTIA CySA+ - Análise de Segurança"},
    "Scrum": {"emblema": "🔄", "xp_max": 60, "cor": "#0A5C4A", "ano": 2026, "descricao": "Scrum Fundamentals Certified"},
    "CISSP": {"emblema": "👑", "xp_max": 200, "cor": "#C0C0C0", "ano": 2029, "descricao": "Certified Information Systems Security Professional"},
    "GICSP": {"emblema": "🏭", "xp_max": 180, "cor": "#606060", "ano": 2028, "descricao": "Global Industrial Cyber Security Professional"},
}

# =========================
# CONTEÚDO DETALHADO DAS CERTIFICAÇÕES
# =========================
CONTEUDO_CERT = {
    "AZ-900": {
        "topicos": ["Conceitos de nuvem", "Serviços principais do Azure", "Segurança e compliance", "Preços e suporte"],
        "recursos": ["Microsoft Learn", "YouTube - John Savill", "GitHub Learning Lab"]
    },
    "Security+": {
        "topicos": ["Ameaças e ataques", "Tecnologias de segurança", "Arquitetura e design", "Identidade e acesso", "Gestão de riscos"],
        "recursos": ["Professor Messer", "CompTIA Official", "ExamCompass"]
    },
    "CCNA": {
        "topicos": ["Fundamentos de rede", "Switching e VLANs", "Roteamento", "Serviços IP", "Segurança de rede"],
        "recursos": ["Jeremy's IT Lab", "Cisco Packet Tracer", "Boson ExSim"]
    },
    "Python": {
        "topicos": ["Sintaxe básica", "Estruturas de dados", "Pandas", "Visualização", "Automação"],
        "recursos": ["Hashtag Treinamentos", "Curso em Vídeo", "DataCamp"]
    },
    "Power BI": {
        "topicos": ["Power Query", "Modelagem de dados", "DAX", "Dashboards", "Publicação"],
        "recursos": ["Hashtag Treinamentos", "Microsoft Learn", "SQLBI"]
    },
    "SQL": {
        "topicos": ["Consultas básicas", "Joins", "Subconsultas", "Funções agregadas", "Manipulação de dados"],
        "recursos": ["SQLZoo", "Mode Analytics", "HackerRank"]
    }
}

# =========================
# FUNÇÕES DE PERSISTÊNCIA
# =========================
def carregar_dados():
    try:
        response = supabase.table("progresso").select("dados").eq("usuario", "Juan").execute()
        if response.data and len(response.data) > 0:
            return response.data[0]["dados"]
    except Exception as e:
        st.error(f"Erro ao carregar: {e}")
    return {}

def salvar_dados(dados):
    try:
        supabase.table("progresso").upsert({
            "usuario": "Juan",
            "dados": dados,
            "updated_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
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

# =========================
# INICIALIZAÇÃO
# =========================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "db" not in st.session_state:
    st.session_state.db = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "cert_xp" not in st.session_state:
    st.session_state.cert_xp = {cert: 0 for cert in CERTIFICACOES.keys()}
if "topicos_feitos" not in st.session_state:
    st.session_state.topicos_feitos = {}

dados_salvos = carregar_dados()
if dados_salvos:
    st.session_state.db = dados_salvos.get("db", [])
    st.session_state.xp = dados_salvos.get("xp", 0)
    st.session_state.cert_xp = dados_salvos.get("cert_xp", st.session_state.cert_xp)
    st.session_state.topicos_feitos = dados_salvos.get("topicos_feitos", {})

# =========================
# LOGIN
# =========================
if not st.session_state.autenticado:
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
    st.stop()

# =========================
# CABEÇALHO
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Cibersegurança | Pós-graduação PUC Minas")
st.markdown("---")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### 👨‍🚀 Juan Felipe")
    st.markdown(f"⭐ **XP Total:** {st.session_state.xp}")
    st.markdown(f"🎖️ **Nível:** {st.session_state.xp // 100 + 1}")
    st.markdown(f"📅 **Missões:** {len(st.session_state.db)}")
    st.markdown("---")
    
    total_certs = len(CERTIFICACOES)
    concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= CERTIFICACOES[cert]["xp_max"])
    st.markdown(f"📊 **Progresso Geral:** {concluidas}/{total_certs} certs")
    st.progress(concluidas / total_certs if total_certs > 0 else 0)
    
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# =========================
# ABAS PRINCIPAIS
# =========================
tab1, tab2, tab3 = st.tabs(["🎮 Dashboard", "📚 Certificações", "📜 Histórico"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⭐ XP Total", st.session_state.xp)
    col2.metric("🎮 Missões", len(st.session_state.db))
    col3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
    col4.metric("✅ Certificações", f"{concluidas}/{total_certs}")
    
    st.markdown("---")
    st.markdown("## ⚡ Adicionar Atividade")
    
    with st.form("nova_atividade", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            certificado = st.selectbox("Certificação", list(CERTIFICACOES.keys()))
            atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"])
        with col_b:
            obs = st.text_input("Observação")
        
        if st.form_submit_button("🚀 Adicionar", use_container_width=True):
            xp_ganho = calc_xp(atividade)
            
            st.session_state.db.append({
                "data": datetime.now().isoformat(),
                "certificacao": certificado,
                "atividade": atividade,
                "xp": xp_ganho,
                "obs": obs
            })
            st.session_state.xp += xp_ganho
            st.session_state.cert_xp[certificado] += xp_ganho
            
            salvar_dados({
                "db": st.session_state.db,
                "xp": st.session_state.xp,
                "cert_xp": st.session_state.cert_xp,
                "topicos_feitos": st.session_state.topicos_feitos
            })
            
            st.success(f"+{xp_ganho} XP em {certificado}!", icon="🎉")
            st.rerun()

# =========================
# TAB 2 - CERTIFICAÇÕES
# =========================
with tab2:
    st.markdown("## 📚 MINHAS CERTIFICAÇÕES")
    
    for cert, info in CERTIFICACOES.items():
        xp_atual = st.session_state.cert_xp.get(cert, 0)
        xp_max = info["xp_max"]
        percentual = min(xp_atual / xp_max, 1.0)
        
        with st.expander(f"{info['emblema']} {cert} - {xp_atual}/{xp_max} XP", expanded=False):
            st.markdown(f"**📝 Descrição:** {info['descricao']}")
            st.markdown(f"**📅 Ano alvo:** {info['ano']}")
            st.progress(percentual)
            
            if cert in CONTEUDO_CERT:
                st.markdown("### 📖 Tópicos de Estudo")
                for topico in CONTEUDO_CERT[cert]["topicos"]:
                    key = f"{cert}_{topico}"
                    concluido = st.session_state.topicos_feitos.get(key, False)
                    
                    if st.checkbox(f"✅ {topico}", value=concluido, key=key):
                        if not concluido:
                            st.session_state.topicos_feitos[key] = True
                            st.session_state.xp += 5
                            salvar_dados({
                                "db": st.session_state.db,
                                "xp": st.session_state.xp,
                                "cert_xp": st.session_state.cert_xp,
                                "topicos_feitos": st.session_state.topicos_feitos
                            })
                            st.rerun()
                    else:
                        if concluido:
                            st.session_state.topicos_feitos[key] = False
                            st.session_state.xp -= 5
                            salvar_dados({
                                "db": st.session_state.db,
                                "xp": st.session_state.xp,
                                "cert_xp": st.session_state.cert_xp,
                                "topicos_feitos": st.session_state.topicos_feitos
                            })
                            st.rerun()
                
                st.markdown("### 🎓 Recursos Recomendados")
                for recurso in CONTEUDO_CERT[cert]["recursos"]:
                    st.markdown(f"- 📹 {recurso}")

# =========================
# TAB 3 - HISTÓRICO
# =========================
with tab3:
    st.markdown("## 📜 HISTÓRICO DE ATIVIDADES")
    
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data", ascending=False)
        
        st.dataframe(df[["data", "certificacao", "atividade", "xp", "obs"]], use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 Resumo por Certificação")
        
        resumo = df.groupby("certificacao").agg({"xp": "sum"}).reset_index()
        resumo = resumo.sort_values("xp", ascending=False)
        
        for _, row in resumo.iterrows():
            st.markdown(f"- **{row['certificacao']}:** {row['xp']} XP")
    else:
        st.info("Nenhuma atividade registrada ainda. Comece agora!")

st.markdown("---")
st.caption("🚀 Continue sua jornada, o universo te espera!")
