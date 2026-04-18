import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

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
    margin-top: 0;
    margin-bottom: 10px;
}
.red-text {
    color: #ff4444 !important;
    font-weight: bold;
}
.stButton button {
    background: linear-gradient(135deg, #4d9fff, #7b2ff7) !important;
    color: white !important;
    border-radius: 10px;
}
.cert-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 12px;
    padding: 12px;
    margin: 5px;
    border: 1px solid rgba(77,159,255,0.3);
    transition: all 0.2s;
}
.cert-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(77,159,255,0.2);
}
.cert-card.atrasado {
    border-left: 3px solid #ff4444;
}
.cert-titulo {
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 8px;
}
.cert-emblema {
    font-size: 28px;
    text-align: center;
}
.cert-progresso {
    font-size: 11px;
    margin-top: 5px;
}
.css-1d391kg, .css-12oz5g7 {
    background: linear-gradient(135deg, #0a0e27, #0d1133) !important;
}
.report-box {
    background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(123,47,247,0.1));
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid rgba(77,159,255,0.4);
}
.stProgress > div > div {
    background: linear-gradient(90deg, #4d9fff, #7b2ff7) !important;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(77,159,255,0.1), rgba(123,47,247,0.05));
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    border: 1px solid rgba(77,159,255,0.2);
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
# FUNÇÕES
# =========================
def calc_xp(activity):
    tabela = {"Estudo": 10, "Laboratório": 20, "Projeto": 30, "Revisão": 15, "Simulado": 15, "Aula Pós-graduação": 25, "Inglês": 15, "Certificação": 50}
    return tabela.get(activity, 10)

def get_badge(status):
    return {"Concluída": "🏆", "Em andamento": "⚡", "Não iniciada": "💤"}.get(status, "❓")

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

def gerar_relatorio_dia(data_selecionada):
    atividades_dia = [a for a in st.session_state.db if a['data'].date() == data_selecionada]
    if not atividades_dia:
        return None
    
    html = f"""
    <html>
    <head><style>
        body {{ font-family: Arial; margin: 40px; background: #0a0e27; color: #4d9fff; }}
        .container {{ max-width: 800px; margin: auto; background: rgba(77,159,255,0.1); border-radius: 20px; padding: 30px; }}
        h1 {{ color: #4d9fff; text-align: center; }}
        .atividade {{ background: rgba(77,159,255,0.1); margin: 10px 0; padding: 15px; border-radius: 10px; }}
        .total {{ text-align: center; font-size: 24px; font-weight: bold; margin-top: 30px; }}
    </style></head>
    <body>
        <div class="container">
            <h1>🚀 Relatório de Missões</h1>
            <h2>📅 {data_selecionada.strftime('%d/%m/%Y')}</h2>
    """
    total_xp = 0
    for atv in atividades_dia:
        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
        total_xp += atv['xp']
        html += f'<div class="atividade">{emblema} <strong>{atv["area"]}</strong><br>⚔️ {atv["atividade"]}<br>⭐ +{atv["xp"]} XP</div>'
    
    html += f'<div class="total">🌟 Total do Dia: +{total_xp} XP 🌟</div></div></body></html>'
    return html

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 Nave")
    st.markdown(f"👨‍🚀 **Juan**")
    st.markdown(f"⭐ **XP:** {st.session_state.xp}")
    st.markdown(f"🎖️ **Nível:** {st.session_state.xp // 100 + 1}")
    st.markdown(f"📅 **Missões:** {len(st.session_state.db)}")
    
    atrasadas = [c for c, d in EMBLEMAS.items() if verificar_atraso(c, d.get("ano", 2030))]
    if atrasadas:
        st.markdown('<p class="red-text">⚠️ Atrasadas:</p>', unsafe_allow_html=True)
        for c in atrasadas[:3]:
            st.markdown(f'<p class="red-text">• {EMBLEMAS[c]["emblema"]} {c[:15]}</p>', unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 MISSÃO CARREIRA")
st.caption("Juan Felipe da Silva - Especialista em Cibersegurança")
st.markdown("---")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Dashboard", "🗺️ Roadmap", "📅 Trilhas", "🏅 Conquistas"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:
    # Nova Missão (compacto)
    with st.expander("✨ Nova Missão", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            area = st.selectbox("Certificação", list(EMBLEMAS.keys()))
            atividade = st.selectbox("Atividade", ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", "Aula Pós-graduação", "Inglês", "Certificação"])
        with col2:
            data = st.date_input("Data", value=pd.Timestamp.today())
            obs = st.text_area("Obs")
        
        if st.button("🚀 Lançar", use_container_width=True):
            ganho = calc_xp(atividade)
            st.session_state.db.append({
                "data": pd.to_datetime(data), "area": area, "atividade": atividade, "xp": ganho, "obs": obs
            })
            st.session_state.xp += ganho
            st.session_state.cert_xp[area] += ganho
            if st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"]:
                st.session_state.cert_status[area] = "Concluída"
            elif st.session_state.cert_xp[area] >= EMBLEMAS[area]["xp"] * 0.3:
                st.session_state.cert_status[area] = "Em andamento"
            st.success(f"+{ganho} XP!", icon="🎉")
            st.rerun()
    
    # KPIs compactos
    c1, c2, c3, c4 = st.columns(4)
    concluidas = sum(1 for c, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[c]["xp"])
    c1.metric("🎮 Missões", len(st.session_state.db))
    c2.metric("⭐ XP", st.session_state.xp)
    c3.metric("🏆 Nível", st.session_state.xp // 100 + 1)
    c4.metric("✅ Certificações", f"{concluidas}/{len(EMBLEMAS)}")
    
    st.markdown("---")
    
    # Relatório do Dia (compacto)
    with st.expander("📄 Relatório do Dia", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            data_relatorio = st.date_input("Data", value=pd.Timestamp.today(), key="data_relatorio")
        with col2:
            st.write("")
            if st.button("📄 Gerar", use_container_width=True):
                relatorio_html = gerar_relatorio_dia(data_relatorio)
                if relatorio_html:
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    atividades_dia = [a for a in st.session_state.db if a['data'].date() == data_relatorio]
                    for atv in atividades_dia:
                        emblema = EMBLEMAS.get(atv['area'], {}).get('emblema', '📌')
                        st.markdown(f"- {emblema} **{atv['area']}** - {atv['atividade']} - ⭐+{atv['xp']}")
                    total_dia = sum(a['xp'] for a in atividades_dia)
                    st.markdown(f"**🌟 Total: +{total_dia} XP**")
                    st.download_button("📥 Baixar", relatorio_html, f"relatorio_{data_relatorio.strftime('%Y%m%d')}.html", "text/html")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Sem atividades nesta data")
    
    st.markdown("---")
    st.markdown("## 🎖️ Certificações")
    
    # Certificações em GRID (4 por linha)
    certs_list = list(st.session_state.cert_xp.items())
    
    # Dividir em linhas de 4
    for i in range(0, len(certs_list), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < len(certs_list):
                cert, xp = certs_list[idx]
                info = EMBLEMAS[cert]
                status = st.session_state.cert_status[cert]
                atrasado = verificar_atraso(cert, info.get("ano", 2030))
                progresso = min(xp / info["xp"], 1.0)
                
                with cols[j]:
                    classe = "cert-card atrasado" if atrasado else "cert-card"
                    st.markdown(f"""
                    <div class="{classe}">
                        <div class="cert-emblema">{info['emblema']}</div>
                        <div class="cert-titulo">{cert[:20]}</div>
                        <div style="font-size: 20px; text-align: center;">{get_badge(status)}</div>
                        <div class="cert-progresso">{xp}/{info['xp']} XP</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.progress(progresso)
                    
                    # Status selector compacto
                    novo_status = st.selectbox("", ["NI", "EA", "C"], 
                                               index=["Não iniciada", "Em andamento", "Concluída"].index(status),
                                               key=f"status_{cert}", label_visibility="collapsed")
                    status_map = {"NI": "Não iniciada", "EA": "Em andamento", "C": "Concluída"}
                    if novo_status != status_map.get(novo_status, status):
                        st.session_state.cert_status[cert] = status_map[novo_status]
                        st.rerun()
    
    st.markdown("---")
    
    # Histórico e Gráfico
    if st.session_state.db:
        st.markdown("## 📜 Histórico")
        df = pd.DataFrame(st.session_state.db)
        df = df.sort_values("data", ascending=False).reset_index(drop=True)
        
        # Mostrar últimos 5 registros apenas para não poluir
        for i, row in df.head(10).iterrows():
            cols = st.columns([1.2, 1.2, 1, 0.8, 2, 0.5])
            cols[0].write(f"{EMBLEMAS[row['area']]['emblema']} {row['area'][:15]}")
            cols[1].write(f"{row['data'].strftime('%d/%m')}")
            cols[2].write(f"{row['atividade'][:10]}")
            cols[3].write(f"+{row['xp']}")
            cols[4].write(row['obs'][:20] if pd.notna(row['obs']) else "-")
            if cols[5].button("🗑️", key=f"del_{i}"):
                for j, rec in enumerate(st.session_state.db):
                    if rec['data'] == row['data'] and rec['area'] == row['area']:
                        delete_activity(j)
                        st.rerun()
            st.markdown("---")
        
        # Gráfico de evolução
        st.markdown("## 📈 Evolução")
        evolucao = df.groupby('data').agg({'xp': 'sum'}).reset_index()
        evolucao = evolucao.sort_values('data')
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

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:
    st.markdown("## 🗺️ Roadmap")
    for ano in [2026, 2027, 2028, 2029]:
        titulo = {2026: "🌱 2026", 2027: "⚡ 2027", 2028: "🎯 2028", 2029: "👑 2029"}[ano]
        with st.expander(titulo):
            certs = [c for c, d in EMBLEMAS.items() if d.get("ano") == ano]
            if certs:
                cols = st.columns(min(4, len(certs)))
                for i, cert in enumerate(certs):
                    info = EMBLEMAS[cert]
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div style="text-align:center; padding:10px; background:rgba(77,159,255,0.1); border-radius:10px;">
                            <div style="font-size:32px;">{info['emblema']}</div>
                            <div style="font-size:12px;">{cert[:15]}</div>
                            <div>{get_badge(st.session_state.cert_status[cert])}</div>
                        </div>
                        """, unsafe_allow_html=True)

# =========================
# TAB 3 - TRILHAS
# =========================
with tab3:
    st.markdown("## 🎯 Trilhas")
    trilhas = {
        "Azure": ["AZ-900", "AZ-104", "AZ-500"],
        "ISO 27001": ["ISO 27001 Fundamentals", "ISO 27001 Auditor", "ISO 27001 Implementer"],
        "Segurança": ["Security+", "CySA+", "CISSP"],
        "OT": ["IEC 62443", "MITRE ATT&CK ICS", "GICSP"],
        "Dados": ["Python", "SQL", "Power BI"]
    }
    
    for nome, certs in trilhas.items():
        st.markdown(f"### {nome}")
        cols = st.columns(3)
        for i, cert in enumerate(certs):
            info = EMBLEMAS[cert]
            xp_atual = st.session_state.cert_xp[cert]
            percent = (xp_atual / info["xp"]) * 100
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; padding:10px; background:rgba(77,159,255,0.1); border-radius:10px;">
                    <div style="font-size:36px;">{info['emblema']}</div>
                    <div style="font-size:11px;">{cert[:15]}</div>
                    <div>{get_badge(st.session_state.cert_status[cert])}</div>
                    <div style="font-size:11px;">{percent:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
        
        total_xp = sum(st.session_state.cert_xp.get(c, 0) for c in certs)
        total_need = sum(EMBLEMAS[c]["xp"] for c in certs)
        st.progress(min(total_xp / total_need, 1.0))
        st.caption(f"{total_xp}/{total_need} XP")
        st.markdown("---")

# =========================
# TAB 4 - CONQUISTAS
# =========================
with tab4:
    st.markdown("## 🏅 Conquistas")
    conquistas = []
    
    if len(st.session_state.db) >= 10:
        conquistas.append(("🏃 Maratonista", "10+ missões", True))
    else:
        conquistas.append(("🏃 Maratonista", f"{10 - len(st.session_state.db)} restantes", False))
    
    concluidas = sum(1 for c, xp in st.session_state.cert_xp.items() if xp >= EMBLEMAS[c]["xp"])
    if concluidas >= 1:
        conquistas.append(("🏆 Especialista", "1ª certificação", True))
    else:
        conquistas.append(("🏆 Especialista", "Conclua 1ª", False))
    
    if st.session_state.xp >= 500:
        conquistas.append(("💪 Veterano", "500+ XP", True))
    else:
        conquistas.append(("💪 Veterano", f"{500 - st.session_state.xp} XP", False))
    
    if st.session_state.xp >= 1000:
        conquistas.append(("🌟 Lendário", "1000+ XP", True))
    else:
        conquistas.append(("🌟 Lendário", f"{1000 - st.session_state.xp} XP", False))
    
    cols = st.columns(2)
    for i, (nome, desc, desbloq) in enumerate(conquistas):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="text-align:center; padding:15px; background:rgba(77,159,255,0.1); border-radius:10px; margin:5px;">
                <div style="font-size:36px;">{nome[:2]}</div>
                <div><strong>{nome}</strong></div>
                <div style="font-size:11px;">{desc}</div>
                <div>{'✅' if desbloq else '🔒'}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("🚀 Continue sua jornada!")
