# ─────────────────────────────────────────────
# DADOS ATUALIZADOS DO PLANEJAMENTO (2026-2029)
# ─────────────────────────────────────────────

FASES = {
    "2026: BASE + INÍCIO DA PÓS": {
        "range": (1, 12), "cor": "#1a6abf", "emoji": "🚀",
        "metas": [
            ("AZ",  "#0078d4", "Azure Fundamentals (AZ-900)", "Abr/2026"),
            ("ISO", "#e53935", "ISO/IEC 27001 Fundamentals", "Mai/2026"),
            ("PÓS", "#7b1fa2", "Pós-graduação (Início)",      "Jun/2026"),
            ("CCNA","#00b4ad", "Cisco CCNA",                  "Jul/2026"),
            ("SC",  "#3267d3", "Microsoft (SC-900)",          "Out/2026"),
            ("EN",  "#00695c", "Inglês (30-40 min/dia)",      "Diário"),
        ]
    },
    "2027: SEGURANÇA + OT + GOVERNANÇA": {
        "range": (13, 28), "cor": "#2e7d32", "emoji": "🛡️",
        "metas": [
            ("S+",  "#cc6600", "CompTIA Security+",           "Fev/2027"),
            ("LI",  "#1565c0", "ISO 27001 Lead Implementer",  "Mai/2027"),
            ("624", "#f57c00", "ISA/IEC 62443 Fundamentals",  "Ago/2027"),
            ("MT",  "#4a148c", "MITRE ATT&CK for ICS",        "Out/2027"),
            ("Cy",  "#d32f2f", "CompTIA CySA+",               "Dez/2027"),
        ]
    },
    "2028: ESPECIALIZAÇÃO + FINAL PÓS": {
        "range": (29, 42), "cor": "#e65100", "emoji": "⚙️",
        "metas": [
            ("GI",  "#2e7d32", "Global ICS Prof. (GICSP)",    "Mar/2028"),
            ("LA",  "#bf360c", "ISO 27001 Lead Auditor",      "Ago/2028"),
            ("🎓",  "#6a1c77", "Conclusão Pós-graduação",     "Dez/2028"),
        ]
    },
    "2029: CONSOLIDAÇÃO": {
        "range": (43, 50), "cor": "#6a1c77", "emoji": "👑",
        "metas": [
            ("CIS", "#b71c1c", "CISSP (Meta Final)",          "Jun/2029"),
            ("EN+", "#01579b", "Inglês: Fluência Funcional",  "2029"),
        ]
    }
}

# Mapeia as casas específicas do tabuleiro para mostrar os troféus
CERT_MAP = {
    4:  ("AZ",  "#0078d4", "AZ-900"),
    8:  ("ISO", "#e53935", "ISO 27001"),
    12: ("CCNA","#00b4ad", "CCNA"),
    16: ("SC",  "#3267d3", "SC-900"),
    20: ("S+",  "#cc6600", "Security+"),
    24: ("624", "#f57c00", "ISA 62443"),
    30: ("Cy",  "#d32f2f", "CySA+"),
    36: ("GI",  "#2e7d32", "GICSP"),
    45: ("LA",  "#bf360c", "Lead Auditor"),
    50: ("🏆",  "#8a30c0", "CISSP"),
}
