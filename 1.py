import streamlit as st
import pandas as pd
import altair as alt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Planejamento de carreira Juan Felipe da Silva",
    layout="wide"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
html, body {
    background: linear-gradient(135deg, #061a3a, #0c2f6e);
    color: #e6f0ff;
}

.block-container {
    padding-top: 2rem;
}

.stButton button {
    background-color: #e53935 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
}

.delete-button {
    background-color: #dc3545 !important;
    color: white !important;
}

.edit-button {
    background-color: #ffc107 !important;
    color: black !important;
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
    st.session_state.cert_xp = {
        "AZ-900": 0,
        "ISO 27001": 0,
        "CCNA": 0,
        "SC-900": 0,
        "Python": 0,
        "SQL": 0,
        "Power BI": 0,
        "Security+": 0,
        "CySA+": 0,
        "GICSP": 0,
        "CISSP": 0,
        "Pós-graduação": 0,
        "Inglês": 0
    }

if "cert_status" not in st.session_state:
    st.session_state.cert_status = {
        "AZ-900": "Não iniciada",
        "ISO 27001": "Não iniciada",
        "CCNA": "Não iniciada",
        "SC-900": "Não iniciada",
        "Python": "Não iniciada",
        "SQL": "Não iniciada",
        "Power BI": "Não iniciada",
        "Security+": "Não iniciada",
        "CySA+": "Não iniciada",
        "GICSP": "Não iniciada",
        "CISSP": "Não iniciada",
        "Pós-graduação": "Não iniciada",
        "Inglês": "Não iniciada"
    }

# =========================
# XP SYSTEM
# =========================
def calc_xp(activity):
    return {
        "Estudo": 10,
        "Laboratório": 20,
        "Projeto": 30,
        "Revisão": 15,
        "Simulado": 15,
        "Aula Pós-graduação": 25,
        "Inglês": 15
    }.get(activity, 10)

def status_por_xp(xp):
    if xp >= 120:
        return "Concluída"
    elif xp >= 40:
        return "Em andamento"
    else:
        return "Não iniciada"

def badge(status):
    if status == "Concluída":
        return "🟢"
    elif status == "Em andamento":
        return "🟡"
    else:
        return "⬜"

# =========================
# FUNCTIONS
# =========================
def delete_activity(index):
    """Delete an activity and update XP totals"""
    activity = st.session_state.db[index]
    xp_to_remove = activity["xp"]
    
    # Remove from global XP
    st.session_state.xp -= xp_to_remove
    
    # Remove from certification XP
    area = activity["area"]
    st.session_state.cert_xp[area] -= xp_to_remove
    
    # Remove from database
    st.session_state.db.pop(index)
    
    # Update certification status based on new XP
    update_cert_status(area)

def update_cert_status(area):
    """Update certification status based on XP"""
    xp = st.session_state.cert_xp[area]
    new_status = status_por_xp(xp)
    st.session_state.cert_status[area] = new_status

def update_all_cert_statuses():
    """Update all certification statuses"""
    for area in st.session_state.cert_xp:
        update_cert_status(area)

# =========================
# HEADER
# =========================
st.title("📘 Planejamento de carreira Juan Felipe da Silva")
st.caption(f"⭐ XP Global: {st.session_state.xp} | Level: {st.session_state.xp // 100 + 1}")

# =========================
# ABAS
# =========================
tab1, tab2, tab3 = st.tabs(["🎓 Dashboard", "🛣️ Roadmap", "📆 Calendário"])

# =========================
# TAB 1
# =========================
with tab1:

    st.subheader("📌 Registrar atividade")

    col1, col2 = st.columns(2)

    with col1:
        area = st.selectbox(
            "Área",
            list(st.session_state.cert_xp.keys())
        )

        activity = st.selectbox(
            "Atividade",
            ["Estudo", "Laboratório", "Projeto", "Revisão", "Simulado", "Aula Pós-graduação", "Inglês"]
        )

    with col2:
        data = st.date_input("Data", value=pd.Timestamp.today())
        obs = st.text_area("Observação")

    if st.button("Salvar atividade"):

        xp_gain = calc_xp(activity)

        st.session_state.db.append({
            "data": pd.to_datetime(data),
            "area": area,
            "atividade": activity,
            "xp": xp_gain,
            "obs": obs,
            "index": len(st.session_state.db)  # Add index for reference
        })

        st.session_state.xp += xp_gain
        st.session_state.cert_xp[area] += xp_gain
        
        # Update status for this certification
        update_cert_status(area)

        st.success(f"+{xp_gain} XP!")

    df = pd.DataFrame(st.session_state.db)

    # =========================
    # KPIs
    # =========================
    st.subheader("📊 KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Registros", len(df))
    col2.metric("XP Global", st.session_state.xp)
    col3.metric("Level", st.session_state.xp // 100 + 1)

    # =========================
    # PROGRESSO GERAL COM STATUS EDITÁVEL
    # =========================
    st.subheader("🏆 Progresso Geral com Planejamento")

    planejamento = {
        "AZ-900": "Abril/2026",
        "ISO 27001": "Maio/2026",
        "CCNA": "Julho/2026",
        "SC-900": "Outubro/2026",
        "Python": "2026 contínuo",
        "SQL": "2026 contínuo",
        "Power BI": "2026 contínuo",
        "Security+": "Fevereiro/2027",
        "CySA+": "Dezembro/2027",
        "GICSP": "Março/2028",
        "CISSP": "Junho/2029",
        "Pós-graduação": "Junho/2026 → Dez/2028",
        "Inglês": "Abril/2026 → contínuo"
    }

    for item, xp in st.session_state.cert_xp.items():

        # Get current status (from XP or manual override)
        auto_status = status_por_xp(xp)
        current_status = st.session_state.cert_status.get(item, auto_status)
        
        icon = badge(current_status)
        data_planejada = planejamento.get(item, "Não definido")

        # Create expander for each certification
        with st.expander(f"{icon} {item} - {current_status}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
**📅 Planejado:** {data_planejada}  
**⭐ XP Acumulado:** {xp}  
**📊 Status Automático:** {auto_status}
                """)
            
            with col2:
                # Manual status override
                new_status = st.selectbox(
                    f"Alterar status - {item}",
                    ["Não iniciada", "Em andamento", "Concluída"],
                    index=["Não iniciada", "Em andamento", "Concluída"].index(current_status),
                    key=f"status_{item}"
                )
                
                if new_status != current_status:
                    st.session_state.cert_status[item] = new_status
                    st.rerun()
            
            # Progress bar based on XP
            progress = min(xp / 120, 1.0)
            st.progress(progress)
            st.caption(f"{xp}/120 XP para concluir")

        st.markdown("---")

    # =========================
    # HISTÓRICO COM BOTÃO DE EXCLUIR
    # =========================
    st.subheader("📚 Histórico de Atividades")

    if not df.empty:

        filtro = st.selectbox("Filtrar área", ["Todas"] + list(df["area"].unique()))
        
        if filtro != "Todas":
            df_f = df[df["area"] == filtro].copy()
        else:
            df_f = df.copy()

        # Add index column for reference
        df_f = df_f.reset_index(drop=True)
        
        # Display activities with delete buttons
        for idx, row in df_f.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 2, 0.8])
            
            with col1:
                st.write(f"📅 {row['data'].strftime('%d/%m/%Y')}")
            with col2:
                st.write(f"📚 {row['area']}")
            with col3:
                st.write(f"🎯 {row['atividade']}")
            with col4:
                st.write(f"⭐ +{row['xp']} XP")
            with col5:
                st.write(f"📝 {row['obs'] if pd.notna(row['obs']) else '-'}")
            with col6:
                # Find the actual index in the main database
                actual_idx = None
                for i, record in enumerate(st.session_state.db):
                    if (record['data'] == row['data'] and 
                        record['area'] == row['area'] and 
                        record['atividade'] == row['atividade'] and
                        record['xp'] == row['xp']):
                        actual_idx = i
                        break
                
                if actual_idx is not None:
                    if st.button("🗑️", key=f"delete_{actual_idx}_{idx}"):
                        delete_activity(actual_idx)
                        st.rerun()
            
            st.markdown("---")

        # Timeline chart
        if not df_f.empty:
            timeline = df_f.groupby("data").size().reset_index(name="atividades")
            st.altair_chart(
                alt.Chart(timeline).mark_line(point=True).encode(
                    x="data:T",
                    y="atividades:Q",
                    tooltip=["data", "atividades"]
                ),
                use_container_width=True
            )

    # =========================
    # EXPORTAÇÃO
    # =========================
    st.subheader("📤 Exportar Base de Dados")

    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Baixar CSV completo",
            csv,
            "carreira_juan_felipe.csv",
            "text/csv"
        )

    # =========================
    # GRÁFICO EM TORRE
    # =========================
    st.subheader("🏗️ Gráfico em Torre (Produtividade)")

    if not df.empty:

        torre = df.groupby("area").agg(
            xp_total=("xp", "sum"),
            atividades=("area", "count")
        ).reset_index()

        chart = alt.Chart(torre).mark_bar().encode(
            x=alt.X("area:N", sort="-y"),
            y="xp_total:Q",
            color="area:N",
            tooltip=["area", "xp_total", "atividades"]
        ).properties(height=400)

        st.altair_chart(chart, use_container_width=True)

# =========================
# TAB 2 - ROADMAP
# =========================
with tab2:

    st.title("🛣️ Roadmap Completo")

    st.markdown("""
## 📅 2026 — BASE + PÓS
- AZ-900  
- ISO 27001  
- CCNA  
- SC-900  
- Python / SQL / Power BI  
- Pós-graduação (Cibersegurança e Governança de Dados)  
- Inglês diário  

## 📅 2027
- Security+  
- CySA+  

## 📅 2028
- GICSP  
- ISO 27001 Lead Auditor  

## 📅 2029
- CISSP  
""")

# =========================
# TAB 3 - CALENDÁRIO
# =========================
with tab3:

    st.title("📆 Calendário")

    df = pd.DataFrame(st.session_state.db)

    if not df.empty:

        timeline = df.groupby("data").size().reset_index(name="atividades")

        st.altair_chart(
            alt.Chart(timeline).mark_bar().encode(
                x="data:T",
                y="atividades:Q",
                tooltip=["data", "atividades"]
            ),
            use_container_width=True
        )

        # Display activities with delete buttons in calendar tab as well
        st.subheader("Atividades Registradas")
        df_sorted = df.sort_values("data", ascending=False).reset_index(drop=True)
        
        for idx, row in df_sorted.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 2, 0.8])
            
            with col1:
                st.write(f"📅 {row['data'].strftime('%d/%m/%Y')}")
            with col2:
                st.write(f"📚 {row['area']}")
            with col3:
                st.write(f"🎯 {row['atividade']}")
            with col4:
                st.write(f"⭐ +{row['xp']} XP")
            with col5:
                st.write(f"📝 {row['obs'] if pd.notna(row['obs']) else '-'}")
            with col6:
                # Find the actual index in the main database
                actual_idx = None
                for i, record in enumerate(st.session_state.db):
                    if (record['data'] == row['data'] and 
                        record['area'] == row['area'] and 
                        record['atividade'] == row['atividade'] and
                        record['xp'] == row['xp']):
                        actual_idx = i
                        break
                
                if actual_idx is not None:
                    if st.button("🗑️", key=f"delete_calendar_{actual_idx}_{idx}"):
                        delete_activity(actual_idx)
                        st.rerun()
            
            st.markdown("---")

    else:
        st.info("Sem dados ainda.")
