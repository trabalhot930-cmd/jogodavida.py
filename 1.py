import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide"
)

# =========================
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026, "trimestre": "Q1"},
    "AZ-104": {"emblema": "☁️⚙️", "cor": "#0078D4", "titulo": "Azure Administrator", "xp": 150, "ano": 2026, "trimestre": "Q2"},
    "AZ-500": {"emblema": "☁️🔐", "cor": "#005BA1", "titulo": "Azure Security", "xp": 150, "ano": 2026, "trimestre": "Q3"},
    "ISO 27001 Fundamentals": {"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation", "xp": 100, "ano": 2026, "trimestre": "Q2"},
    "ISO 27001 Auditor": {"emblema": "🔒🔍", "cor": "#FFC000", "titulo": "ISO Auditor", "xp": 150, "ano": 2027, "trimestre": "Q1"},
    "ISO 27001 Implementer": {"emblema": "🔒🛠️", "cor": "#FFA000", "titulo": "ISO Implementer", "xp": 150, "ano": 2027, "trimestre": "Q2"},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027, "trimestre": "Q3"},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027, "trimestre": "Q4"},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029, "trimestre": "Q2"},
    "IEC 62443": {"emblema": "🏭📏", "cor": "#808080", "titulo": "IEC 62443", "xp": 120, "ano": 2027, "trimestre": "Q2"},
    "MITRE ATT&CK ICS": {"emblema": "🎯🏭", "cor": "#A0A0A0", "titulo": "MITRE ICS", "xp": 120, "ano": 2028, "trimestre": "Q1"},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028, "trimestre": "Q3"},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026, "trimestre": "Q3"},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026, "trimestre": "Q4"},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026, "trimestre": "Q4"},
    "CCNA": {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA", "xp": 150, "ano": 2026, "trimestre": "Q2"},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026, "trimestre": "Q1"},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026, "trimestre": "Q2-Q4"},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo", "trimestre": "2026-2029"},
    "Cloud Security": {"emblema": "☁️🔒", "cor": "#00A4EF", "titulo": "Cloud Security", "xp": 150, "ano": 2028, "trimestre": "Q4"},
    "DevSecOps": {"emblema": "🔄🚀", "cor": "#6C3483", "titulo": "DevSecOps", "xp": 150, "ano": 2029, "trimestre": "Q1"}
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
.css-1d391kg, .css-12oz5g7 {
    background: linear-gradient(135deg, #0a0e27, #0d1133) !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #4d9fff, #7b2ff7) !important;
}
.save-indicator {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #00ff88;
    color: #0a0e27;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    z-index: 999;
    animation: fadeOut 3s ease-out forwards;
}
@keyframes fadeOut {
    0% { opacity: 1; }
    70% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÕES DE SALVAMENTO (localStorage via JavaScript)
# =========================
def inject_save_js():
    """Injeta código JavaScript para salvar no localStorage"""
    st.markdown("""
    <script>
    function salvarDadosLocalStorage(dados) {
        localStorage.setItem('diario_carreira_juan', JSON.stringify(dados));
        console.log('✅ Dados salvos no localStorage');
        
        // Mostrar indicador visual
        const indicator = document.createElement('div');
        indicator.className = 'save-indicator';
        indicator.innerHTML = '💾 Dados salvos!';
        document.body.appendChild(indicator);
        setTimeout(() => indicator.remove(), 3000);
    }
    
    function carregarDadosLocalStorage() {
        const dados = localStorage.getItem('diario_carreira_juan');
        if (dados) {
            console.log('✅ Dados carregados do localStorage');
            return JSON.parse(dados);
        }
        return null;
    }
    
    // Salvar dados quando a página for fechada
    window.addEventListener('beforeunload', function() {
        const dados = window.dadosParaSalvar;
        if (dados) {
            localStorage.setItem('diario_carreira_juan', JSON.stringify(dados));
        }
    });
    </script>
    """, unsafe_allow_html=True)

def salvar_dados_no_localstorage():
    """Salva os dados do session_state no localStorage via JavaScript"""
    dados = {
        "db": st.session_state.db,
        "xp": st.session_state.xp,
        "cert_xp": st.session_state.cert_xp,
        "cert_status": st.session_state.cert_status,
        "ultima_atualizacao": datetime.now().isoformat()
    }
    
    # Converter para JSON
    dados_json = json.dumps(dados, default=str)
    
    # Injetar JavaScript para salvar
    st.markdown(f"""
    <script>
    const dadosParaSalvar = {dados_json};
    localStorage.setItem('diario_carreira_juan', JSON.stringify(dadosParaSalvar));
    console.log('✅ Dados salvos no localStorage:', {len(st.session_state.db)} atividades);
    
    // Mostrar indicador visual
    const indicator = document.createElement('div');
    indicator.className = 'save-indicator';
    indicator.innerHTML = '💾 Diário salvo!';
    document.body.appendChild(indicator);
    setTimeout(() => indicator.remove(), 2000);
    </script>
    """, unsafe_allow_html=True)

def carregar_dados_do_localstorage():
    """Carrega dados do localStorage via JavaScript"""
    st.markdown("""
    <script>
    const dadosCarregados = localStorage.getItem('diario_carreira_juan');
    if (dadosCarregados) {
        const dados = JSON.parse(dadosCarregados);
        window.dadosCarregados = dados;
        console.log('✅ Dados carregados do localStorage:', dados.db?.length || 0, 'atividades');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Tentar recuperar dados via query param (método alternativo)
    import streamlit.components.v1 as components
    import uuid
    
    # Criar um componente HTML para comunicação
    components.html(f"""
    <div id="data-loader" style="display:none;"></div>
    <script>
    const dados = localStorage.getItem('diario_carreira_juan');
    if (dados) {{
        const dadosObj = JSON.parse(dados);
        // Salvar em um atributo global
        window.parent.document.body.setAttribute('data-dados-carregados', JSON.stringify(dadosObj));
    }}
    </script>
    """, height=0)

# =========================
# SESSION STATE
# =========================
if "db" not in st.session_state:
    st.session_state.db = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "cert_xp" not in st.session_state:
    st.session_state.cert_xp = {cert: 0 for cert in EMBLEMAS.keys()}
if "cert_status" not in st.session_state:
    st.session_state.cert_status = {cert: "Não iniciada" for cert in EMBLEMAS.keys()}
if "dados_carregados" not in st.session_state:
    st.session_state.dados_carregados = False

# =========================
# CARREGAR DADOS SALVOS
# =========================
inject_save_js()

# Tentar carregar dados salvos (via método de importação)
try:
    import streamlit.components.v1 as components
    
    # Criar um componente para ler localStorage
    components.html("""
    <script>
    const dados = localStorage.getItem('diario_carreira_juan');
    if (dados) {
        const dadosObj = JSON.parse(dados);
        // Salvar no sessionStorage para recuperar
        sessionStorage.setItem('dados_recuperados', dados);
    }
    </script>
    """, height=0)
    
    # Verificar se há dados para carregar
    if not st.session_state.dados_carregados and len(st.session_state.db) == 0:
        # Tentar recuperar de um arquivo de exemplo ou deixar vazio
        pass
except:
    pass

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

def delete_activity(index):
    atividade = st.session_state.db[index]
    st.session_state.xp -= atividade["xp"]
    st.session_state.cert_xp[atividade["area"]] -= atividade["xp"]
    st.session_state.db.pop(index)
    salvar_dados_no_localstorage()

def adicionar_atividade(area, atividade, xp, obs):
    st.session_state.db.append({
        "data": pd.Timestamp.now(),
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
    
    salvar_dados_no_localstorage()

def get_atividades_hoje():
    hoje = datetime.now().date()
    return [a for a in st.session_state.db if a['data'].date() == hoje]

def get_xp_semana():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    return sum(a['xp'] for a in st.session_state.db if a['data'].date() >= inicio_semana.date())

def get_xp_mes():
    hoje = datetime.now()
    return sum(a['xp'] for a in st.session_state.db if a['data'].month == hoje.month and a['data'].year == hoje.year)

def gerar_relatorio_html(data):
    atividades = [a for a in st.session_state.db if a['data'].date() == data]
    if not atividades:
        return None
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; margin: 40px; background: #0a0e27; color: #4d9fff; }}
            .container {{ max-width: 800px; margin: auto; background: rgba(77,159,255,0.1); border-radius: 20px; padding: 30px; }}
            h1 {{ text-align: center; }}
            .atividade {{ background: rgba(77,159,255,0.1); margin: 10px 0; padding: 15px; border-radius: 10px; }}
            .total {{ text-align: center; font-size: 24px; font-weight: bold; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 RELATÓRIO DE MISSÕES</h1>
            <h2>📅 {data.strftime('%d/%m/%Y')}</h2>
            <p>👨‍🚀 Juan Felipe da Silva</p>
            <hr>
    """
    total_xp = 0
    for atv in atividades:
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        total_xp += atv['xp']
        html += f'<div class="atividade">{emblema} <strong>{atv["area"]}</strong><br>⚔️ {atv["atividade"]}<br>⭐ +{atv["xp"]} XP<br>📝 {atv["obs"] if atv["obs"] else "-"}</div>'
    
    html += f"""
            <div class="total">🌟 TOTAL DO DIA: +{total_xp} XP 🌟</div>
            <hr>
            <p style="text-align: center; font-size: 12px;">Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
    </body>
    </html>"""
    return html

def exportar_dados_completos():
    dados = {
        "historico_atividades": st.session_state.db,
        "xp_total": st.session_state.xp,
        "certificacoes_xp": st.session_state.cert_xp,
        "certificacoes_status": st.session_state.cert_status,
        "data_exportacao": datetime.now().isoformat()
    }
    return json.dumps(dados, default=str, indent=2)

def importar_dados(dados_json):
    try:
        dados = json.loads(dados_json)
        st.session_state.db = dados.get("historico_atividades", [])
        st.session_state.xp = dados.get("xp_total", 0)
        st.session_state.cert_xp = dados.get("certificacoes_xp", {cert: 0 for cert in EMBLEMAS.keys()})
        st.session_state.cert_status = dados.get("certificacoes_status", {cert: "Não iniciada" for cert in EMBLEMAS.keys()})
        salvar_dados_no_localstorage()
        return True
    except:
        return False

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 NAVE ESTELAR")
    st.markdown(f"""
    <div style="text-align: center;">
        <div style="font-size: 48px;">👨‍🚀</div>
        <h3 style="margin: 0;">Juan Felipe</h3>
        <p style="margin: 0; opacity: 0.8;">Comandante</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"⭐ **XP Total:** {st.session_state.xp}")
    st.markdown(f"🎖️ **Nível:** {st.session_state.xp // 100 + 1}")
    st.markdown(f"📅 **Missões:** {len(st.session_state.db)}")
    
    xp_no_nivel = st.session_state.xp % 100
    st.progress(xp_no_nivel / 100 if xp_no_nivel > 0 else 0)
    st.caption(f"Próximo nível: {100 - xp_no_nivel} XP")
    
    st.markdown("---")
    
    atrasadas = [c for c, d in EMBLEMAS.items() if verificar_atraso(c, d.get("ano", 2030))]
    if atrasadas:
        st.markdown('<p class="red-text">⚠️ ATRASADAS:</p>', unsafe_allow_html=True)
        for c in atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[c]["emblema"]} {c[:15]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    atividades_hoje = get_atividades_hoje()
    xp_hoje = sum(a['xp'] for a in atividades_hoje)
    st.markdown(f"**📅 Hoje:** {len(atividades_hoje)} atv | +{xp_hoje} XP")
    st.markdown(f"**📆 Semana:** +{get_xp_semana()} XP")
    st.markdown(f"**📅 Mês:** +{get_xp_mes()} XP")
    
    st.markdown("---")
    st.markdown("### 💾 Backup")
    if st.button("📥 Exportar Dados", use_container_width=True):
        dados_json = exportar_dados_completos()
        st.download_button("Baixar JSON", dados_json, "backup_diario.json", "application/json")
    
    uploaded_file = st.file_uploader("📤 Importar Backup", type=["json"])
    if uploaded_file is not None:
        dados_json = uploaded_file.read().decode()
        if importar_dados(dados_json):
            st.success("✅ Dados importados com sucesso!")
            st.rerun()

# =========================
# HEADER
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Cibersegurança")
st.markdown('<p class="green-text">💾 Seu progresso é salvo automaticamente como um diário!</p>', unsafe_allow_html=True)
st.markdown("---")

# =========================
# ATIVIDADES DO DIA
# =========================
st.markdown("## ⚡ ATIVIDADES DE HOJE")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("#### ➕ Nova Atividade")
    with st.form("nova_atividade", clear_on_submit=True):
        area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
        atividade = st.selectbox("Tipo", ["📚 Estudo", "🔬 Laboratório", "🏗️ Projeto", "🔄 Revisão", "📝 Simulado", "🎓 Aula Pós", "🌎 Inglês", "🏅 Certificação"])
        obs = st.text_area("Observação", placeholder="Ex: Estudei módulo 3, fiz laboratório...")
        if st.form_submit_button("🚀 LANÇAR MISSÃO", use_container_width=True):
            xp_ganho = calc_xp(atividade)
            adicionar_atividade(area, atividade, xp_ganho, obs)
            st.success(f"+{xp_ganho} XP!", icon="🎉")
            st.rerun()

with col2:
    st.markdown("#### 📊 Hoje")
    xp_hoje = sum(a['xp'] for a in get_atividades_hoje())
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 36px;">⭐</div>
        <div style="font-size: 28px; font-weight: bold;">+{xp_hoje}</div>
        <div>XP hoje</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("#### 🎯 Meta Diária")
    meta = 50
    xp_hoje = sum(a['xp'] for a in get_atividades_hoje())
    progresso = min(xp_hoje / meta, 1.0)
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size: 36px;">🎯</div>
        <div style="font-size: 28px; font-weight: bold;">{xp_hoje}/{meta}</div>
        <div>XP meta</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progresso)

# Lista de atividades de hoje
atividades_hoje = get_atividades_hoje()
if atividades_hoje:
    st.markdown("#### 📝 Atividades Registradas Hoje")
    for atv in atividades_hoje:
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        st.markdown(f"""
        <div class="atividade-card">
            <table style="width: 100%;">
                <tr>
                    <td style="width: 40px; font-size: 24px;">{emblema}</td>
                    <td><strong>{atv['area'][:30]}</strong></td>
                    <td>{atv['atividade']}</td>
                    <td style="color: #00ff88;">⭐ +{atv['xp']}</td>
                </tr>
                <tr>
                    <td colspan="4" style="font-size: 12px; opacity: 0.7;">📝 {atv['obs'][:50] if atv['obs'] else '-'}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("✨ Nenhuma atividade hoje. Comece agora! Seu progresso será salvo automaticamente.")

st.markdown("---")

# =========================
# KPIS PRINCIPAIS
# =========================
c1, c2, c3, c4, c5 = st.columns(5)
concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
total_certs = len(EMBLEMAS)

c1.metric("🎮 Missões", len(st.session_state.db))
c2.metric("⭐ XP", st.session_state.xp)
c3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
c4.metric("✅ Concluídas", f"{concluidas}/{total_certs}")
c5.metric("📊 Progresso", f"{(concluidas/total_certs*100):.0f}%")

st.markdown("---")

# =========================
# CERTIFICAÇÕES EM GRID
# =========================
st.markdown("## 🎖️ JORNADA DAS CERTIFICAÇÕES")

# Filtro
col_filtro1, col_filtro2 = st.columns([3, 1])
with col_filtro2:
    filtro_status = st.selectbox("Filtrar", ["Todas", "Concluída", "Em andamento", "Não iniciada"])

certs_list = list(st.session_state.cert_xp.items())

for i in range(0, len(certs_list), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx < len(certs_list):
            cert, xp = certs_list[idx]
            info = EMBLEMAS[cert]
            status = st.session_state.cert_status[cert]
            
            if filtro_status != "Todas" and status != filtro_status:
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
                    salvar_dados_no_localstorage()
                    st.rerun()

st.markdown("---")

# =========================
# ROADMAP COMPLETO
# =========================
st.markdown("## 🗺️ ROADMAP ESTRATÉGICO 2026-2029")

anos = {
    2026: "🌱 ANO 1 - FUNDAÇÃO",
    2027: "⚡ ANO 2 - ESPECIALIZAÇÃO",
    2028: "🎯 ANO 3 - MAESTRIA TÉCNICA",
    2029: "👑 ANO 4 - LIDERANÇA"
}

for ano, titulo in anos.items():
    with st.expander(titulo, expanded=(ano == 2026)):
        certs_ano = [cert for cert, data in EMBLEMAS.items() if data.get("ano") == ano]
        
        if certs_ano:
            trimestres = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
            for cert in certs_ano:
                trimestre = EMBLEMAS[cert].get("trimestre", "Q1")
                if trimestre in trimestres:
                    trimestres[trimestre].append(cert)
            
            for trimestre, certs in trimestres.items():
                if certs:
                    st.markdown(f"#### {trimestre} - {ano}")
                    cols = st.columns(min(4, len(certs)))
                    for i, cert in enumerate(certs):
                        info = EMBLEMAS[cert]
                        status = st.session_state.cert_status[cert]
                        xp_atual = st.session_state.cert_xp[cert]
                        percent = (xp_atual / info["xp"]) * 100
                        
                        with cols[i % 4]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px; background: rgba(77,159,255,0.1); border-radius: 10px;">
                                <div style="font-size: 32px;">{info['emblema']}</div>
                                <div style="font-weight: bold; font-size: 11px;">{cert[:20]}</div>
                                <div style="font-size: 20px;">{get_badge(status)}</div>
                                <div style="font-size: 10px;">{xp_atual}/{info['xp']} XP</div>
                                <div style="background: #333; border-radius: 5px; height: 4px; margin-top: 5px;">
                                    <div style="background: {info['cor']}; width: {percent}%; height: 4px; border-radius: 5px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRÁFICOS
# =========================
if len(st.session_state.db) > 0:
    st.markdown("## 📈 ANÁLISE DE EVOLUÇÃO")
    
    df = pd.DataFrame(st.session_state.db)
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values('data')
    
    # Gráfico 1: Evolução Acumulada
    st.markdown("### 📊 Evolução do XP Acumulado")
    evolucao = df.groupby('data').agg({'xp': 'sum'}).reset_index()
    evolucao['xp_acumulado'] = evolucao['xp'].cumsum()
    
    if len(evolucao) > 0:
        chart1 = alt.Chart(evolucao).mark_line(
            point=alt.OverlayMarkDef(filled=True, fill='white', size=60),
            strokeWidth=3,
            color='#4d9fff'
        ).encode(
            x=alt.X('data:T', title='Data', axis=alt.Axis(labelAngle=-45, format='%d/%m/%Y')),
            y=alt.Y('xp_acumulado:Q', title='XP Total'),
            tooltip=['data:T', 'xp_acumulado:Q']
        ).properties(height=350)
        st.altair_chart(chart1, use_container_width=True)
    
    # Gráfico 2: XP por Certificação
    st.markdown("### 🎯 XP por Certificação")
    xp_por_cert = df.groupby('area').agg({'xp': 'sum'}).reset_index()
    xp_por_cert = xp_por_cert.sort_values('xp', ascending=False).head(10)
    
    chart2 = alt.Chart(xp_por_cert).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('area:N', title='Certificação', sort='-y', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('xp:Q', title='XP'),
        color=alt.Color('area:N', legend=None, scale=alt.Scale(scheme='turbo')),
        tooltip=['area', 'xp']
    ).properties(height=350)
    st.altair_chart(chart2, use_container_width=True)
    
    # Gráfico 3: Atividades por Tipo
    st.markdown("### 🍩 Distribuição por Tipo de Atividade")
    atividades_count = df['atividade'].value_counts().reset_index()
    atividades_count.columns = ['atividade', 'quantidade']
    
    chart3 = alt.Chart(atividades_count).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='quantidade', type='quantitative'),
        color=alt.Color(field='atividade', type='nominal', scale=alt.Scale(scheme='viridis')),
        tooltip=['atividade', 'quantidade']
    ).properties(height=350)
    st.altair_chart(chart3, use_container_width=True)

else:
    st.info("📊 Complete algumas missões para visualizar os gráficos de evolução!")

st.markdown("---")

# =========================
# RELATÓRIO E EXPORTAÇÃO
# =========================
st.markdown("## 📄 RELATÓRIO DIÁRIO")

col_r1,
