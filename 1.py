import streamlit as st
import pandas as pd
from datetime import date

# =========================
# OPENAI (OPCIONAL)
# =========================
from openai import OpenAI
import os

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# SESSION STATE
# =========================
if "db" not in st.session_state:
    st.session_state.db = []

if "progress" not in st.session_state:
    st.session_state.progress = {
        "AZ-900": 20,
        "ISO 27001": 10,
        "CCNA": 15,
        "Security+": 5
    }

# =========================
# SCORE DE DISCIPLINA
# =========================
def disciplina_score():
    df = pd.DataFrame(st.session_state.db)

    base = len(df) * 5

    progresso_bonus = sum(st.session_state.progress.values()) * 0.2

    return base + progresso_bonus

# =========================
# IA PLANNER SEMANAL
# =========================
def gerar_plano():

    df = pd.DataFrame(st.session_state.db)

    contexto = f"""
Progresso atual:
{st.session_state.progress}

Atividades recentes:
{df.tail(5).to_string() if not df.empty else "Nenhuma atividade ainda"}

Crie um plano semanal de estudos para certificações de segurança e redes.
Inclua:
- segunda a domingo
- foco prático
- equilíbrio estudo/lab/descanso
"""

    # SE NÃO TIVER OPENAI
    if client is None:
        return """
📅 PLANO SEMANAL (BÁSICO)

Segunda: Estudo teórico (1h)
Terça: Laboratório prático
Quarta: Estudo + revisão
Quinta: Lab de redes
Sexta: Projeto prático
Sábado: Revisão geral
Domingo: descanso leve / leitura
"""

    # OPENAI REAL
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um coach de carreira em segurança da informação."},
            {"role": "user", "content": contexto}
        ]
    )

    return response.choices[0].message.content

# =========================
# UI
# =========================
st.title("🤖 IA Planejador + Ranking de Disciplina")

# =========================
# PLANO SEMANAL
# =========================
st.subheader("📅 Plano da Semana (IA)")

if st.button("Gerar plano semanal"):
    st.info(gerar_plano())

# =========================
# RANKING DE DISCIPLINA
# =========================
st.subheader("🏆 Ranking de Disciplina (MVP)")

# simulação de usuários (MVP local)
ranking = pd.DataFrame([
    {"usuario": "Você", "score": disciplina_score()},
    {"usuario": "Aluno A", "score": 120},
    {"usuario": "Aluno B", "score": 90},
    {"usuario": "Aluno C", "score": 60},
])

ranking = ranking.sort_values("score", ascending=False)

st.dataframe(ranking, use_container_width=True)

st.bar_chart(ranking.set_index("usuario"))
