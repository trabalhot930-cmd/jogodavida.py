import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import json
import os
import base64
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🚀 Missão Carreira - Juan Felipe da Silva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# EMOJIS E ÍCONES ÉPICOS
# =========================
EMBLEMAS = {
    "AZ-900": {
        "icone": "☁️",
        "cor": "#00A4EF",
        "emblema": "🌩️",
        "titulo": "Azure Fundamentals",
        "descricao": "Fundamentos do Cloud Computing",
        "nivel": "Foundation"
    },
    "ISO 27001": {
        "icone": "🔒",
        "cor": "#FFD700",
        "emblema": "🛡️",
        "titulo": "Security Management",
        "descricao": "Gestão de Segurança da Informação",
        "nivel": "Professional"
    },
    "CCNA": {
        "icone": "🌐",
        "cor": "#1BA0D7",
        "emblema": "🕸️",
        "titulo": "Networking Expert",
        "descricao": "Redes e Infraestrutura",
        "nivel": "Associate"
    },
    "SC-900": {
        "icone": "🔐",
        "cor": "#0078D4",
        "emblema": "🎯",
        "titulo": "Security Compliance",
        "descricao": "Segurança e Compliance",
        "nivel": "Foundation"
    },
    "Python": {
        "icone": "🐍",
        "cor": "#3776AB",
        "emblema": "⚡",
        "titulo": "Python Developer",
        "descricao": "Automação e Análise de Dados",
        "nivel": "Advanced"
    },
    "SQL": {
        "icone": "🗄️",
        "cor": "#F29111",
        "emblema": "📊",
        "titulo": "Database Expert",
        "descricao": "Consultas e Modelagem de Dados",
        "nivel": "Intermediate"
    },
    "Power BI": {
        "icone": "📈",
        "cor": "#F2C811",
        "emblema": "🎨",
        "titulo": "Data Visualization",
        "descricao": "Dashboards e Analytics",
        "nivel": "Intermediate"
    },
    "Security+": {
        "icone": "🛡️",
        "cor": "#FF0000",
        "emblema": "⚔️",
        "titulo": "Cybersecurity Core",
        "descricao": "Fundamentos de Cibersegurança",
        "nivel": "Professional"
    },
    "CySA+": {
        "icone": "🔍",
        "cor": "#FF4500",
        "emblema": "🕵️",
        "titulo": "Security Analyst",
        "descricao": "Análise de Vulnerabilidades",
        "nivel": "Advanced"
    },
    "GICSP": {
        "icone": "🏭",
        "cor": "#808080",
        "emblema": "⚙️",
        "titulo": "ICS Security",
        "descricao": "Segurança Industrial",
        "nivel": "Expert"
    },
    "CISSP": {
        "icone": "👑",
        "cor": "#C0C0C0",
        "emblema": "🏆",
        "titulo": "Security Architect",
        "descricao": "Arquitetura de Segurança",
        "nivel": "Master"
    },
    "Pós-graduação": {
        "icone": "🎓",
        "cor": "#800080",
        "emblema": "📜",
        "titulo": "Postgraduate",
        "descricao": "Especialização Acadêmica",
        "nivel": "Advanced"
    },
    "Inglês": {
        "icone": "🇬🇧",
        "cor": "#1E90FF",
        "emblema": "💬",
        "titulo": "English Fluency",
        "descricao": "Proficiência Internacional",
        "nivel": "Essential"
    }
}

# =========================
# STYLE ÉPICO
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1433 100%);
    color: #e6f0ff;
}

.block-container {
    padding-top: 2rem;
    background: radial-gradient(circle at 20% 50%, rgba(0,100,255,0.05) 0%, rgba(0,0,0,0) 50%);
}

/* Títulos galácticos */
h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, #00d4ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: bold !important;
}

/* Botões épicos */
.stButton button {
    background: linear-gradient(135deg, #00d4ff, #7b2ff7) !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,212,255,0.3);
}

/* Cards de certificação */
.cert-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.3s;
}

.cert-card:hover {
    transform: translateX(10px);
    box-shadow: 0 5px 25px rgba(0,212,255,0.2);
}

/* Badges de nível */
.level-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-left: 10px;
}

/* Animações */
@keyframes glow {
    0%, 100% { text-shadow: 0 0 5px rgba(0,212,255,0.5); }
    50% { text-shadow: 0 0 20px rgba(0,212,255,0.8); }
}

.glow-text {
    animation: glow 2s infinite;
}
</style>
""", unsafe_allow_html=True)

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

# =========================
# FUNÇÕES AUXILIARES
# =========================
def calc_xp(activity):
    xp_table = {
        "Estudo": 10,
        "Laboratório": 20,
        "Projeto": 30,
        "Revisão": 15,
        "Simulado": 15,
        "Aula Pós-graduação": 25,
        "Inglês": 15
    }
    return xp_table.get(activity, 10)

def status_por_xp(xp):
    if xp >= 120:
        return "Concluída"
    elif xp >= 40:
        return "Em andamento"
    else:
        return "Não iniciada"

def get_badge_icon(status):
    return {
        "Concluída": "🏆",
        "Em andamento": "⚡",
        "Não iniciada": "💤"
    }.get(status, "❓")

def get_nivel_icon(nivel):
    icons = {
        "Foundation": "🌱",
        "Essential": "📘",
        "Associate": "🥈",
        "Intermediate": "📊",
        "Professional": "💼",
        "Advanced": "🚀",
        "Expert": "🎯",
        "Master": "👑"
    }
    return icons.get(nivel, "⭐")

def delete_activity(index):
    activity = st.session_state.db[index]
    xp_to_remove = activity["xp"]
    
    st.session_state.xp -= xp_to_remove
    area = activity["area"]
    st.session_state.cert_xp[area] -= xp_to_remove
    st.session_state.db.pop(index)
    
    # Atualiza status
    new_status = status_por_xp(st.session_state.cert_xp[area])
    st.session_state.cert_status[area] = new_status

# =========================
# SIDEBAR ÉPICA
# =========================
with st.sidebar:
    st.markdown("## 🚀 **Nave Estelar**")
    st.markdown(f"""
    ### 👨‍🚀 **Comandante:** Juan Felipe
    ### ⭐ **XP Total:** {st.session_state.xp}
    ### 🎖️ **Nível:** {st.session_state.xp // 100 + 1}
    ### 📅 **Missões:** {len(st.session_state.db)}
    """)
    
    st.progress(min(st.session_state.xp % 100, 100) / 100)
    st.caption(f"Próximo nível: {100 - (st.session_state.xp % 100)} XP")
    
    st.markdown("---")
    st.markdown("### 🎯 **Ranking de Especialização**")
    
    # Ranking das certificações por XP
    ranking = sorted(st.session_state.cert_xp.items(), key=lambda x: x[1], reverse=True)
    for cert, xp in ranking[:5]:
        emblema = EMBLEMAS[cert]["emblema"]
        st.markdown(f"{emblema} **{cert}**: {xp} XP")

# =========================
# HEADER PRINCIPAL
# =========================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🚀 **MISSÃO CARREIRA**")
    st.markdown("### *Juan Felipe da Silva - O Caminho do Especialista*")
    st.markdown("---")

# =========================
# ABAS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 **Dashboard Épico**", "🗺️ **Mapa da Jornada**", "📅 **Cronograma Estelar**", "🏅 **Conquistas**"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    
    # Registro de Atividade
    with st.expander("✨ **NOVA MISSÃO**", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.selectbox("🎯 **Área de Especialização**", list(EMBLEMAS.keys()))
            activity = st.selectbox("⚔️ **Tipo de Missão**", 
                                   ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", 
                                    "Aula Pós-graduação", "Inglês"])
        
        with col2:
            data = st.date_input("📆 **Data**", value=pd.Timestamp.today())
            obs = st.text_area("📝 **Observações de Bordo**")
        
        if st.button("🚀 **LANÇAR MISSÃO**", use_container_width=True):
            xp_gain = calc_xp(activity)
            st.session_state.db.append({
                "data": pd.to_datetime(data),
                "area": area,
                "atividade": activity,
                "xp": xp_gain,
                "obs": obs
            })
            st.session_state.xp += xp_gain
            st.session_state.cert_xp[area] += xp_gain
            new_status = status_por_xp(st.session_state.cert_xp[area])
            st.session_state.cert_status[area] = new_status
            st.success(f"✅ Missão completa! +{xp_gain} XP conquistado!", icon="🎉")
            st.balloons()
            st.rerun()
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎮 **Total de Missões**", len(st.session_state.db), delta="+hoje")
    col2.metric("⭐ **XP Global**", st.session_state.xp, delta=f"+{st.session_state.xp % 100}/100")
    col3.metric("🏆 **Nível**", st.session_state.xp // 100 + 1, delta=f"Nível {st.session_state.xp // 100 + 1}")
    col4.metric("🎯 **Certificações Ativas**", sum(1 for xp in st.session_state.cert_xp.values() if xp > 0))
    
    st.markdown("---")
    
    # Certificações com emblemas
    st.markdown("## 🎖️ **JORNADA DAS CERTIFICAÇÕES**")
    
    for cert, xp in st.session_state.cert_xp.items():
        emblema_data = EMBLEMAS[cert]
        status = st.session_state.cert_status[cert]
        auto_status = status_por_xp(xp)
        badge_icon = get_badge_icon(status)
        nivel_icon = get_nivel_icon(emblema_data["nivel"])
        
        # Card personalizado
        st.markdown(f"""
        <div class="cert-card">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="margin: 0;">
                        {emblema_data['emblema']} {cert} 
                        <span style="font-size: 14px; color: {emblema_data['cor']};">{emblema_data['titulo']}</span>
                        <span class="level-badge" style="background: {emblema_data['cor']}20; color: {emblema_data['cor']};">
                            {nivel_icon} {emblema_data['nivel']}
                        </span>
                    </h3>
                    <p style="margin: 5px 0 0 0; opacity: 0.8;">{emblema_data['descricao']}</p>
                </div>
                <div style="font-size: 48px;">
                    {badge_icon}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progresso e controle
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            progress = min(xp / 120, 1.0)
            st.progress(progress)
            st.caption(f"📊 Progresso: {xp}/120 XP ({int(progress*100)}%)")
        
        with col2:
            st.markdown(f"**Status:** {badge_icon} {status}")
        
        with col3:
            new_status_manual = st.selectbox(
                "🔧",
                ["Não iniciada", "Em andamento", "Concluída"],
                index=["Não iniciada", "Em andamento", "Concluída"].index(status),
                key=f"status_{cert}",
                label_visibility="collapsed"
            )
            if new_status_manual != status:
                st.session_state.cert_status[cert] = new_status_manual
                st.rerun()
        
        st.markdown("---")
    
    # Histórico com deleção
    st.markdown("## 📜 **REGISTRO DE MISSÕES**")
    
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        filtro = st.selectbox("🎯 **Filtrar por Especialização**", ["Todas"] + list(df["area"].unique()))
        
        if filtro != "Todas":
            df_f = df[df["area"] == filtro].copy()
        else:
            df_f = df.copy()
        
        df_f = df_f.sort_values("data", ascending=False).reset_index(drop=True)
        
        for idx, row in df_f.iterrows():
            emblema_icon = EMBLEMAS[row['area']]['emblema']
            
            cols = st.columns([1, 1.5, 1, 0.8, 2, 0.5])
            with cols[0]:
                st.write(f"{emblema_icon} **{row['area']}**")
            with cols[1]:
                st.write(f"📅 {row['data'].strftime('%d/%m/%Y')}")
            with cols[2]:
                st.write(f"⚔️ {row['atividade']}")
            with cols[3]:
                st.write(f"⭐ +{row['xp']}")
            with cols[4]:
                st.write(f"📝 {row['obs'] if pd.notna(row['obs']) else '-'}")
            with cols[5]:
                actual_idx = st.session_state.db.index(next(
                    (r for r in st.session_state.db if r['data'] == row['data'] and 
                     r['area'] == row['area'] and r['atividade'] == row['atividade']),
                    None
                ))
                if st.button("🗑️", key=f"del_{idx}_{actual_idx}"):
                    delete_activity(actual_idx)
                    st.rerun()
            st.markdown("---")
        
        # Gráfico de evolução
        st.markdown("## 📈 **EVOLUÇÃO ESTELAR**")
        timeline = df_f.groupby("data").agg({"xp": "sum"}).reset_index()
        chart = alt.Chart(timeline).mark_line(point=True, color='#00d4ff').encode(
            x=alt.X("data:T", title="Data"),
            y=alt.Y("xp:Q", title="XP Acumulado"),
            tooltip=["data", "xp"]
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
        
        # Exportação
        st.markdown("## 💾 **BACKUP DA JORNADA**")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 **BAIXAR RELATÓRIO COMPLETO**", csv, "jornada_estelar.csv", "text/csv")

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:
    st.markdown("## 🗺️ **MAPA DA CONQUISTA**")
    
    anos = {
        "2026": ["AZ-900", "ISO 27001", "CCNA", "SC-900", "Python", "SQL", "Power BI", "Pós-graduação", "Inglês"],
        "2027": ["Security+", "CySA+"],
        "2028": ["GICSP"],
        "2029": ["CISSP"]
    }
    
    for ano, certs in anos.items():
        with st.expander(f"🌟 **ANO {ano}**", expanded=(ano == "2026")):
            cols = st.columns(len(certs))
            for i, cert in enumerate(certs):
                emblema = EMBLEMAS[cert]
                status = st.session_state.cert_status.get(cert, "Não iniciada")
                badge = get_badge_icon(status)
                
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, {emblema['cor']}20, {emblema['cor']}05); border-radius: 10px;">
                        <div style="font-size: 48px;">{emblema['emblema']}</div>
                        <div style="font-size: 20px; font-weight: bold;">{cert}</div>
                        <div style="font-size: 12px;">{emblema['titulo']}</div>
                        <div style="font-size: 24px; margin-top: 10px;">{badge}</div>
                        <div style="font-size: 12px;">{status}</div>
                    </div>
                    """, unsafe_allow_html=True)

# =========================
# TAB 3 - CALENDÁRIO
# =========================
with tab3:
    st.markdown("## 📅 **LINHA DO TEMPO ESTELAR**")
    
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        df['mes'] = df['data'].dt.to_period('M')
        
        # Heatmap mensal
        heatmap_data = df.groupby(['mes', 'area']).size().reset_index(name='atividades')
        heatmap_data['mes'] = heatmap_data['mes'].astype(str)
        
        chart = alt.Chart(heatmap_data).mark_rect().encode(
            x=alt.X('mes:N', title="Mês"),
            y=alt.Y('area:N', title="Certificação"),
            color=alt.Color('atividades:Q', scale=alt.Scale(scheme='turbo')),
            tooltip=['mes', 'area', 'atividades']
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Timeline detalhada
        st.markdown("## 📋 **TODAS AS MISSÕES**")
        df_sorted = df.sort_values("data", ascending=False)
        for _, row in df_sorted.iterrows():
            emblema = EMBLEMAS[row['area']]['emblema']
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, rgba(0,212,255,0.1), transparent); padding: 10px; margin: 5px 0; border-radius: 5px;">
                {emblema} **{row['area']}** - {row['atividade']} - ⭐+{row['xp']} - 📅 {row['data'].strftime('%d/%m/%Y')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🌌 Nenhuma missão registrada ainda. Inicie sua jornada!")

# =========================
# TAB 4 - CONQUISTAS
# =========================
with tab4:
    st.markdown("## 🏅 **HALL DA FAMA**")
    
    # Conquistas calculadas dinamicamente
    conquistas = []
    
    # Maratonista
    if len(st.session_state.db) >= 10:
        conquistas.append({"nome": "🏃 **Maratonista**", "desc": "Completou 10 ou mais missões", "icone": "🎯"})
    
    # Especialista
    for cert, xp in st.session_state.cert_xp.items():
        if xp >= 120:
            conquistas.append({"nome": f"🎖️ **Mestre em {cert}**", "desc": f"Concluiu a certificação {cert}", "icone": EMBLEMAS[cert]['emblema']})
            break
    
    # Dedicado
    dias_unicos = len(set([r['data'].date() for r in st.session_state.db])) if st.session_state.db else 0
    if dias_unicos >= 5:
        conquistas.append({"nome": "📆 **Dedicado**", "desc": "Estudou em 5 ou mais dias diferentes", "icone": "📅"})
    
    # Veterano
    if st.session_state.xp >= 500:
        conquistas.append({"nome": "⚡ **Veterano**", "desc": "Acumulou 500+ XP", "icone": "💪"})
    
    # Lendário
    if st.session_state.xp >= 1000:
        conquistas.append({"nome": "👑 **Lendário**", "desc": "Ultrapassou 1000 XP", "icone": "🏆"})
    
    if conquistas:
        cols = st.columns(3)
        for i, conquista in enumerate(conquistas):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, gold, orange); border-radius: 15px; margin: 10px;">
                    <div style="font-size: 48px;">{conquista['icone']}</div>
                    <div style="font-size: 20px; font-weight: bold;">{conquista['nome']}</div>
                    <div style="font-size: 12px;">{conquista['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🎮 Complete missões para desbloquear conquistas épicas!")
    
    # Próximos objetivos
    st.markdown("## 🎯 **PRÓXIMOS OBJETIVOS**")
    st.markdown("""
    - 🏃 Complete 10 missões para virar **Maratonista**
    - 🎖️ Conclua sua primeira certificação (120 XP)
    - 📅 Estude em 5 dias diferentes
    - 💪 Acumule 500 XP total
    """)

# Footer épico
st.markdown("---")
st.markdown("<p style='text-align: center; opacity: 0.6;'>🚀 *Continue sua jornada, o universo da tecnologia espera por você!* 🌟</p>", unsafe_allow_html=True)
