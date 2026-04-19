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
# EMBLEMAS DAS CERTIFICAÇÕES
# =========================
EMBLEMAS = {
    "AZ-900": {"emblema": "☁️🌩️", "cor": "#00A4EF", "titulo": "Azure Fundamentals", "xp": 120, "ano": 2026},
    "AZ-104": {"emblema": "☁️⚙️", "cor": "#0078D4", "titulo": "Azure Administrator", "xp": 150, "ano": 2026},
    "AZ-500": {"emblema": "☁️🔐", "cor": "#005BA1", "titulo": "Azure Security", "xp": 150, "ano": 2026},
    "ISO 27001 Fundamentals": {"emblema": "🔒📘", "cor": "#FFD700", "titulo": "ISO Foundation", "xp": 100, "ano": 2026},
    "ISO 27001 Auditor": {"emblema": "🔒🔍", "cor": "#FFC000", "titulo": "ISO Auditor", "xp": 150, "ano": 2027},
    "ISO 27001 Implementer": {"emblema": "🔒🛠️", "cor": "#FFA000", "titulo": "ISO Implementer", "xp": 150, "ano": 2027},
    "Security+": {"emblema": "🛡️⚔️", "cor": "#FF0000", "titulo": "Security Plus", "xp": 120, "ano": 2027},
    "CySA+": {"emblema": "🔍🕵️", "cor": "#FF4500", "titulo": "CySA Plus", "xp": 150, "ano": 2027},
    "CISSP": {"emblema": "👑🏆", "cor": "#C0C0C0", "titulo": "CISSP", "xp": 200, "ano": 2029},
    "IEC 62443": {"emblema": "🏭📏", "cor": "#808080", "titulo": "IEC 62443", "xp": 120, "ano": 2027},
    "MITRE ATT&CK ICS": {"emblema": "🎯🏭", "cor": "#A0A0A0", "titulo": "MITRE ICS", "xp": 120, "ano": 2028},
    "GICSP": {"emblema": "🏭⚙️", "cor": "#606060", "titulo": "GICSP", "xp": 180, "ano": 2028},
    "Python": {"emblema": "🐍⚡", "cor": "#3776AB", "titulo": "Python", "xp": 150, "ano": 2026},
    "SQL": {"emblema": "🗄️📊", "cor": "#F29111", "titulo": "SQL", "xp": 120, "ano": 2026},
    "Power BI": {"emblema": "📈🎨", "cor": "#F2C811", "titulo": "Power BI", "xp": 120, "ano": 2026},
    "CCNA": {"emblema": "🌐🕸️", "cor": "#1BA0D7", "titulo": "CCNA", "xp": 150, "ano": 2026},
    "SC-900": {"emblema": "🔐🎯", "cor": "#0078D4", "titulo": "SC-900", "xp": 100, "ano": 2026},
    "Pos-graduacao": {"emblema": "🎓📜", "cor": "#800080", "titulo": "Pós-graduação", "xp": 300, "ano": 2026},
    "Ingles": {"emblema": "🇬🇧💬", "cor": "#1E90FF", "titulo": "Inglês", "xp": 250, "ano": "Contínuo"},
    "Cloud Security": {"emblema": "☁️🔒", "cor": "#00A4EF", "titulo": "Cloud Security", "xp": 150, "ano": 2028},
    "DevSecOps": {"emblema": "🔄🚀", "cor": "#6C3483", "titulo": "DevSecOps", "xp": 150, "ano": 2029}
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
.filtro-box {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 15px;
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
if "filtro_status" not in st.session_state:
    st.session_state.filtro_status = "Todas"

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
# FUNÇÕES DE BACKUP
# =========================
ARQUIVO_BACKUP = "backup_diario.json"

def salvar_backup():
    dados = {
        "db": st.session_state.db,
        "xp": st.session_state.xp,
        "cert_xp": st.session_state.cert_xp,
        "cert_status": st.session_state.cert_status,
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

def delete_activity(index):
    atividade = st.session_state.db[index]
    st.session_state.xp -= atividade["xp"]
    st.session_state.cert_xp[atividade["area"]] -= atividade["xp"]
    st.session_state.db.pop(index)
    salvar_backup()

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

def get_atividades_hoje():
    hoje = datetime.now().date()
    resultado = []
    for a in st.session_state.db:
        try:
            # Converter data para datetime se for string
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

def gerar_relatorio_html(data):
    atividades = []
    for a in st.session_state.db:
        try:
            if isinstance(a['data'], str):
                data_atv = datetime.fromisoformat(a['data']).date()
            else:
                data_atv = a['data'].date()
            if data_atv == data:
                atividades.append(a)
        except:
            pass
    
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
        html += f'<div class="atividade">{emblema} <strong>{atv["area"]}</strong><br>⚔️ {atv["atividade"]}<br>⭐ +{atv["xp"]} XP</div>'
    
    html += f'<div class="total">🌟 TOTAL DO DIA: +{total_xp} XP 🌟</div></div></body></html>'
    return html

# =========================
# CARREGAR DADOS SALVOS
# =========================
carregar_backup()

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
# ATIVIDADES DO DIA
# =========================
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

# =========================
# KPIS
# =========================
c1, c2, c3, c4, c5 = st.columns(5)
concluidas = sum(1 for cert, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[cert]["xp"])
c1.metric("🎮 Missões", len(st.session_state.db))
c2.metric("⭐ XP", st.session_state.xp)
c3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
c4.metric("✅ Concluídas", f"{concluidas}/{len(EMBLEMAS)}")
c5.metric("📊 Progresso", f"{(concluidas/len(EMBLEMAS)*100):.0f}%")

st.markdown("---")

# =========================
# CERTIFICAÇÕES COM FILTRO
# =========================
st.markdown("## 🎖️ CERTIFICAÇÕES")

# Filtro de status
col_f1, col_f2 = st.columns([1, 3])
with col_f1:
    filtro = st.selectbox("🔍 Filtrar por status", ["Todas", "Em andamento", "Concluída", "Não iniciada"])
    st.session_state.filtro_status = filtro

st.markdown('<div class="filtro-box">', unsafe_allow_html=True)
st.caption(f"📌 Mostrando certificações: {filtro}")
st.markdown('</div>', unsafe_allow_html=True)

certs_list = list(st.session_state.cert_xp.items())

# Aplicar filtro
certs_filtradas = []
for cert, xp in certs_list:
    status = st.session_state.cert_status[cert]
    if filtro == "Todas":
        certs_filtradas.append((cert, xp))
    elif filtro == "Em andamento" and status == "Em andamento":
        certs_filtradas.append((cert, xp))
    elif filtro == "Concluída" and status == "Concluída":
        certs_filtradas.append((cert, xp))
    elif filtro == "Não iniciada" and status == "Não iniciada":
        certs_filtradas.append((cert, xp))

# Mostrar certificações filtradas
for i in range(0, len(certs_filtradas), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx < len(certs_filtradas):
            cert, xp = certs_filtradas[idx]
            info = EMBLEMAS[cert]
            status = st.session_state.cert_status[cert]
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

st.markdown("---")

# =========================
# ROADMAP
# =========================
st.markdown("## 🗺️ ROADMAP")

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

st.markdown("---")

# =========================
# GRÁFICOS
# =========================
if len(st.session_state.db) > 0:
    st.markdown("## 📈 GRÁFICOS")
    
    # Converter dados para DataFrame
    dados_df = []
    for a in st.session_state.db:
        try:
            if isinstance(a['data'], str):
                data_atv = datetime.fromisoformat(a['data'])
            else:
                data_atv = a['data']
            dados_df.append({
                "data": data_atv,
                "area": a['area'],
                "atividade": a['atividade'],
                "xp": a['xp']
            })
        except:
            pass
    
    if dados_df:
        df = pd.DataFrame(dados_df)
        df = df.sort_values('data')
        
        # Gráfico de evolução
        evolucao = df.groupby('data').agg({'xp': 'sum'}).reset_index()
        evolucao['xp_acumulado'] = evolucao['xp'].cumsum()
        
        if len(evolucao) > 0:
            chart = alt.Chart(evolucao).mark_line(
                point=alt.OverlayMarkDef(filled=True, fill='white'),
                strokeWidth=2,
                color='#4d9fff'
            ).encode(
                x=alt.X('data:T', title='Data', axis=alt.Axis(labelAngle=-45, format='%d/%m')),
                y=alt.Y('xp_acumulado:Q', title='XP Total'),
                tooltip=['data:T', 'xp_acumulado:Q']
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        
        # Gráfico de barras
        xp_por_cert = df.groupby('area').agg({'xp': 'sum'}).reset_index()
        xp_por_cert = xp_por_cert.sort_values('xp', ascending=False).head(10)
        
        chart2 = alt.Chart(xp_por_cert).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('area:N', title='Certificação', sort='-y', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('xp:Q', title='XP'),
            color=alt.Color('area:N', legend=None),
            tooltip=['area', 'xp']
        ).properties(height=300)
        st.altair_chart(chart2, use_container_width=True)

st.markdown("---")

# =========================
# RELATÓRIO
# =========================
st.markdown("## 📄 RELATÓRIO")

col_r1, col_r2 = st.columns(2)

with col_r1:
    data_rel = st.date_input("Data", value=datetime.now().date())
    if st.button("📄 Gerar Relatório", use_container_width=True):
        relatorio = gerar_relatorio_html(data_rel)
        if relatorio:
            st.download_button("📥 Baixar HTML", relatorio, f"relatorio_{data_rel.strftime('%Y%m%d')}.html", "text/html")
        else:
            st.warning("Sem atividades nesta data")

with col_r2:
    if len(st.session_state.db) > 0:
        df_export = pd.DataFrame(dados_df) if dados_df else pd.DataFrame()
        if not df_export.empty:
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Baixar CSV", csv, f"historico_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

st.markdown("---")

# =========================
# HISTÓRICO
# =========================
if len(st.session_state.db) > 0 and dados_df:
    st.markdown("## 📜 HISTÓRICO")
    df_hist = pd.DataFrame(dados_df)
    df_hist = df_hist.sort_values('data', ascending=False).reset_index(drop=True)
    
    for i in range(min(15, len(df_hist))):
        row = df_hist.iloc[i]
        cols = st.columns([1.2, 1.2, 1.2, 0.8, 2, 0.5])
        emblema = EMBLEMAS.get(row['area'], {}).get('emblema', '📌')
        cols[0].write(f"{emblema} {row['area'][:15]}")
        cols[1].write(f"{row['data'].strftime('%d/%m/%Y')}")
        cols[2].write(f"{row['atividade'][:12]}")
        cols[3].write(f"+{row['xp']}")
        cols[4].write("-")
        if cols[5].button("🗑️", key=f"del_{i}"):
            for j, rec in enumerate(st.session_state.db):
                try:
                    if isinstance(rec['data'], str):
                        data_rec = datetime.fromisoformat(rec['data'])
                    else:
                        data_rec = rec['data']
                    if data_rec == row['data'] and rec['area'] == row['area']:
                        delete_activity(j)
                        st.rerun()
                except:
                    pass
        st.markdown("---")

st.caption("🚀 Continue sua jornada, o universo te espera!")
