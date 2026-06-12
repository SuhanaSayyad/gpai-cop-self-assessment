import streamlit as st
from datetime import datetime
import io

st.set_page_config(
    page_title="GPAI Code of Practice Self-Assessment",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header{background:linear-gradient(135deg,#003399 0%,#0044cc 50%,#0055ff 100%);padding:2.5rem 2rem;border-radius:12px;margin-bottom:1.5rem;color:white;text-align:center;}
    .main-header h1{font-size:2rem;margin-bottom:0.4rem;}
    .main-header p{opacity:0.85;font-size:0.95rem;}
    .section-card{background:white;border-radius:12px;padding:1.5rem;margin-bottom:1rem;border:1px solid #e5e7eb;box-shadow:0 2px 8px rgba(0,0,0,0.06);}
    .section-title{font-size:1.1rem;font-weight:700;color:#1a1f36;margin-bottom:0.3rem;}
    .section-subtitle{font-size:0.82rem;color:#6b7280;margin-bottom:1.2rem;}
    .result-met{background:#dcfce7;border-left:4px solid #16a34a;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;}
    .result-partial{background:#fef3c7;border-left:4px solid #d97706;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;}
    .result-not-met{background:#fee2e2;border-left:4px solid #dc2626;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;}
    .result-na{background:#f3f4f6;border-left:4px solid #9ca3af;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;color:#6b7280;}
    .score-banner{padding:1.5rem;border-radius:12px;text-align:center;margin-bottom:1.5rem;color:white;}
    .action-30{background:#dcfce7;border-left:4px solid #16a34a;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;}
    .action-60{background:#fef3c7;border-left:4px solid #d97706;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;}
    .action-90{background:#fee2e2;border-left:4px solid #dc2626;padding:0.75rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:0.88rem;}
    .disclaimer{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:0.75rem 1rem;font-size:0.82rem;color:#92400e;margin-top:1rem;}
    .share-box{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:1rem;margin-top:0.5rem;}
    div[data-testid="stSelectbox"] label{font-weight:600;}
    div[data-testid="stTextInput"] label{font-weight:600;}
    div[data-testid="stTextArea"] label{font-weight:600;font-size:0.82rem;color:#6b7280;}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "model_info" not in st.session_state:
    st.session_state.model_info = {}
if "notes" not in st.session_state:
    st.session_state.notes = {}
if "url_loaded" not in st.session_state:
    st.session_state.url_loaded = False

# ── MEASURES DATA ─────────────────────────────────────────────────────────────
MEASURES = {
    "T1": {
        "id": "T1", "article": "Article 53(1)(a) + Annex XI",
        "title": "Technical Documentation", "section": "transparency",
        "priority": 60,
        "question": "Have you drawn up technical documentation for your GPAI model in accordance with Annex XI of the EU AI Act, covering model architecture, training methodology, data used, evaluation results and intended capabilities?",
        "guidance": "Annex XI requires detailed technical documentation including model description, training details, testing and evaluation results, and information about intended use. This must be made available to the EU AI Office on request.",
        "evidence": ["Model card or system card published", "Architecture diagram", "Training data description document", "Evaluation and benchmarking results", "Annex XI compliant technical documentation template", "Version history and changelog"]
    },
    "T2": {
        "id": "T2", "article": "Article 53(1)(d)",
        "title": "Training Data Summary", "section": "transparency",
        "priority": 30,
        "question": "Have you published a sufficiently detailed publicly available summary of the content used for training your GPAI model?",
        "guidance": "This must be published and publicly accessible before or at the time of placing the model on the market. It should describe the general nature of the training data without requiring disclosure of trade secrets.",
        "evidence": ["Publicly accessible training data summary page or document", "URL to published summary", "Publication date recorded", "Summary reviewed and approved by legal/DPO"]
    },
    "T3": {
        "id": "T3", "article": "Article 53(1)(b)",
        "title": "Information to Downstream Providers", "section": "transparency",
        "priority": 60,
        "question": "Do you provide downstream providers (companies building on top of your GPAI model) with sufficient information about the model's capabilities, limitations, and how to use it safely and compliantly?",
        "guidance": "Downstream providers need information to assess their own obligations under the EU AI Act. This includes model cards, API documentation, safety evaluations, and known limitations.",
        "evidence": ["API documentation", "Model capabilities and limitations document", "Safety evaluation results shared with downstream providers", "Known failure modes and edge cases documented", "Downstream provider agreement or terms of service"]
    },
    "T4": {
        "id": "T4", "article": "Article 53(1)(b)",
        "title": "Instructions for Use", "section": "transparency",
        "priority": 30,
        "question": "Do you provide clear and up-to-date instructions for use, including intended purposes, prohibited uses, and technical requirements for safe deployment of your GPAI model?",
        "guidance": "Instructions must include at minimum: intended and prohibited uses, foreseeable misuses, technical requirements for deployment, known limitations, and update/maintenance policies.",
        "evidence": ["User manual or usage documentation", "Prohibited use cases policy (publicly available)", "Technical requirements and prerequisites document", "Update and maintenance policy", "Contact details for reporting issues"]
    },
    "T5": {
        "id": "T5", "article": "Article 50(5)",
        "title": "AI-Generated Content Marking", "section": "transparency",
        "priority": 60,
        "question": "If your GPAI model generates content, does it have the technical capability to mark outputs as AI-generated in a machine-readable format?",
        "guidance": "Article 50(5) requires GPAI model providers to ensure that outputs can be marked and detected as artificially generated. This includes watermarking or other detectable metadata.",
        "evidence": ["Watermarking or metadata marking implementation documentation", "Technical specification of marking method used", "Testing evidence demonstrating marking capability", "Detection tool or API for downstream providers"]
    },
    "C1": {
        "id": "C1", "article": "Article 53(1)(c)",
        "title": "Copyright Compliance Policy", "section": "copyright",
        "priority": 30,
        "question": "Do you have a documented policy for compliance with EU copyright law, including the Text and Data Mining (TDM) exceptions and opt-out obligations?",
        "guidance": "Providers must comply with EU copyright law including Directive 2019/790. This requires a clear internal policy covering how TDM opt-outs are respected, how copyrighted works are handled in training data, and how rights holders can assert their rights.",
        "evidence": ["Internal copyright compliance policy document", "Legal review sign-off on the policy", "Designated responsible person or team", "Publicly accessible copyright policy page", "Rights holder contact mechanism"]
    },
    "C2": {
        "id": "C2", "article": "Article 53(1)(c)",
        "title": "Opt-Out Implementation", "section": "copyright",
        "priority": 60,
        "question": "Do you implement state-of-the-art technical measures to identify and respect TDM opt-outs expressed by rights holders using recognised standards such as the Robots Exclusion Protocol or the Rights Reserved designation?",
        "guidance": "Rights holders can reserve their rights against TDM using machine-readable means. GPAI providers must implement technical measures to identify and respect these opt-outs.",
        "evidence": ["robots.txt compliance processing records", "Technical implementation documentation for opt-out detection", "Audit log showing opt-outs identified and processed", "Crawling and scraping configuration showing respect for opt-outs", "Third party verification or audit of opt-out compliance"]
    },
    "C3": {
        "id": "C3", "article": "Article 53(1)(c)",
        "title": "Training Data Documentation", "section": "copyright",
        "priority": 30,
        "question": "Do you maintain records of the data sources used for training your GPAI model, sufficient to demonstrate copyright compliance if requested by the EU AI Office or a court?",
        "guidance": "Documentation should cover what data was used, how it was obtained, what licences applied, how opt-outs were processed, and how data was filtered or excluded.",
        "evidence": ["Data source inventory spreadsheet or database", "Licensing records for proprietary datasets", "Data provenance and lineage documentation", "Filtering and exclusion logs", "Records of data provider agreements"]
    },
    "SR1": {
        "id": "SR1", "article": "Article 55(1)(a)",
        "title": "Adversarial Testing (Red-Teaming)", "section": "systemic_risk",
        "priority": 90, "systemic_only": True,
        "question": "Have you conducted model evaluations including adversarial testing (red-teaming) to identify systemic risks before releasing or updating your model?",
        "guidance": "Systemic risk providers must conduct thorough adversarial testing with internal and external red teams. This should cover misuse potential, capability elicitation, and emergent behaviours. Results must be documented and acted upon.",
        "evidence": ["Internal red-team exercise reports", "External evaluation reports from independent researchers", "Capability assessment results", "Adversarial prompt testing documentation", "Actions taken in response to findings", "Schedule for ongoing evaluation"]
    },
    "SR2": {
        "id": "SR2", "article": "Article 55(1)(b)",
        "title": "Systemic Risk Assessment", "section": "systemic_risk",
        "priority": 90, "systemic_only": True,
        "question": "Have you conducted a documented systemic risk assessment covering potential large-scale negative effects, including risks to public health, safety, security, fundamental rights, democratic processes, and economic stability?",
        "guidance": "The assessment must be proportionate to the risk level and cover foreseeable uses and misuses. It should be reviewed and updated with each significant model update.",
        "evidence": ["Systemic risk assessment document", "Board or senior leadership sign-off", "Review and update schedule", "Risk register with assigned owners", "Assessment methodology documentation"]
    },
    "SR3": {
        "id": "SR3", "article": "Article 55(1)(b)",
        "title": "Systemic Risk Mitigation", "section": "systemic_risk",
        "priority": 90, "systemic_only": True,
        "question": "Have you implemented measures to mitigate the identified systemic risks, including technical safeguards, use policies, and monitoring mechanisms?",
        "guidance": "Mitigation measures should be proportionate to identified risks and include a combination of technical measures, policy measures, and organisational measures.",
        "evidence": ["Technical safeguards implementation documentation", "Acceptable use policy and enforcement records", "Monitoring system configuration and logs", "Escalation procedures", "Effectiveness review records"]
    },
    "SR4": {
        "id": "SR4", "article": "Article 55(1)(c)",
        "title": "Incident Monitoring and Reporting", "section": "systemic_risk",
        "priority": 60, "systemic_only": True,
        "question": "Do you have a process for tracking, documenting, and reporting serious incidents and near-misses to the EU AI Office without undue delay?",
        "guidance": "Providers with systemic risk must report serious incidents to the EU AI Office. A serious incident is any event that leads to or could lead to death, serious harm, critical infrastructure disruption, or significant adverse effects at a large scale.",
        "evidence": ["Incident tracking system or register", "Incident reporting procedures document", "EU AI Office contact information and reporting template", "Staff training records on incident identification", "Incident response plan"]
    },
    "SR5": {
        "id": "SR5", "article": "Article 55(1)(d)",
        "title": "Cybersecurity Protection", "section": "systemic_risk",
        "priority": 90, "systemic_only": True,
        "question": "Have you implemented adequate cybersecurity measures to protect your GPAI model, its weights, and related infrastructure against adversarial attacks, model extraction, and unauthorised access?",
        "guidance": "Measures should include access controls for model weights, monitoring for extraction attempts, protection against adversarial prompt injection at scale, and security of fine-tuning APIs where applicable.",
        "evidence": ["Security assessment or penetration test report", "Access control policy for model weights", "Monitoring system for extraction attempts", "Security incident response plan", "Regular security review schedule"]
    }
}

ANSWER_OPTIONS = [
    "Yes - fully implemented",
    "Partially implemented",
    "No - not implemented",
    "Not applicable to my model"
]

# ── HELPERS ───────────────────────────────────────────────────────────────────
def answer_to_status(answer):
    return {"Yes - fully implemented": "Met", "Partially implemented": "Partial",
            "No - not implemented": "Not Met", "Not applicable to my model": "N/A"}.get(answer, "Not Met")

def get_status_html(status):
    icons = {"Met": "OK", "Partial": "~", "Not Met": "!", "N/A": "-"}
    classes = {"Met": "result-met", "Partial": "result-partial", "Not Met": "result-not-met", "N/A": "result-na"}
    return icons.get(status, "?"), classes.get(status, "result-na")

def compute_score(results):
    counted = [r for r in results if r["status"] != "N/A"]
    if not counted:
        return 0, 0
    score = sum(1 if r["status"] == "Met" else 0.5 if r["status"] == "Partial" else 0 for r in counted)
    return score, len(counted)

def get_section_scores(results):
    sections = {"transparency": [], "copyright": [], "systemic_risk": []}
    for r in results:
        if r["status"] != "N/A" and r["section"] in sections:
            sections[r["section"]].append(1 if r["status"] == "Met" else 0.5 if r["status"] == "Partial" else 0)
    scores = {}
    for k, vals in sections.items():
        scores[k] = int(sum(vals) / len(vals) * 100) if vals else None
    return scores

def load_from_url():
    if st.session_state.url_loaded:
        return
    try:
        params = st.query_params
        if not params:
            st.session_state.url_loaded = True
            return
        for mid in MEASURES:
            if mid in params:
                val = params[mid]
                if val in ANSWER_OPTIONS:
                    st.session_state.answers[mid] = val
        if "step" in params:
            try:
                st.session_state.step = min(int(params["step"]), 5)
            except Exception:
                pass
        if "systemic" in params:
            sr_val = "Yes - compute exceeded 10^25 FLOPs or the EU AI Office has designated it" if params["systemic"] == "yes" else "No - below the threshold and not designated"
            st.session_state.model_info["systemic_risk"] = sr_val
    except Exception:
        pass
    st.session_state.url_loaded = True

def update_url():
    try:
        params = {mid: ans for mid, ans in st.session_state.answers.items()}
        params["step"] = str(st.session_state.step)
        is_systemic = "Yes" in st.session_state.model_info.get("systemic_risk", "")
        params["systemic"] = "yes" if is_systemic else "no"
        st.query_params.update(params)
    except Exception:
        pass

def generate_text_report(model_info, results, is_systemic):
    lines = []
    lines.append("=" * 60)
    lines.append("GPAI CODE OF PRACTICE SELF-ASSESSMENT REPORT")
    lines.append("EU AI Act - Articles 53 and 55 Compliance Assessment")
    lines.append("=" * 60)
    lines.append("")
    lines.append("ASSESSMENT DETAILS")
    lines.append("-" * 40)
    lines.append(f"Model Name: {model_info.get('model_name', 'Not provided')}")
    lines.append(f"Provider Organisation: {model_info.get('provider', 'Not provided')}")
    lines.append(f"Assessment Date: {datetime.now().strftime('%d %B %Y')}")
    lines.append(f"Systemic Risk Model: {'Yes' if is_systemic else 'No'}")
    lines.append("")
    score, total = compute_score(results)
    pct = int(score / total * 100) if total > 0 else 0
    met = sum(1 for r in results if r["status"] == "Met")
    partial = sum(1 for r in results if r["status"] == "Partial")
    not_met = sum(1 for r in results if r["status"] == "Not Met")
    na = sum(1 for r in results if r["status"] == "N/A")
    lines.append("COMPLIANCE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Overall Score: {score:.1f} / {total} measures ({pct}%)")
    lines.append(f"Met: {met}  |  Partial: {partial}  |  Not Met: {not_met}  |  N/A: {na}")
    lines.append("")
    for section_title, section_key in [
        ("TRANSPARENCY MEASURES", "transparency"),
        ("COPYRIGHT MEASURES", "copyright"),
        ("SYSTEMIC RISK MEASURES", "systemic_risk")
    ]:
        sec = [r for r in results if r["section"] == section_key]
        if not sec:
            continue
        lines.append(section_title)
        lines.append("-" * 40)
        for r in sec:
            lines.append(f"{r['id']} - {r['title']}: {r['status']}")
            lines.append(f"   Article: {r['article']}")
            note = st.session_state.notes.get(r['id'], "").strip()
            if note:
                lines.append(f"   Notes: {note}")
            if r["status"] == "Not Met":
                lines.append(f"   Action: Implement this measure. See 90-day action plan below.")
            elif r["status"] == "Partial":
                lines.append(f"   Action: Complete implementation of this measure.")
            lines.append("")
    not_met_results = [r for r in results if r["status"] in ["Not Met", "Partial"]]
    if not_met_results:
        lines.append("90-DAY ACTION PLAN")
        lines.append("-" * 40)
        for priority, label in [(30, "30 DAYS - Quick Wins"), (60, "60 DAYS - Medium Effort"), (90, "90 DAYS - Complex Implementation")]:
            tasks = [r for r in not_met_results if MEASURES[r["id"]].get("priority", 90) == priority]
            if tasks:
                lines.append(label)
                for t in tasks:
                    lines.append(f"  - {t['id']} {t['title']} ({t['article']})")
                lines.append("")
    lines.append("DISCLAIMER")
    lines.append("-" * 40)
    lines.append("This report is for guidance only and does not constitute legal advice.")
    lines.append("Always verify obligations against the official EU AI Act text.")
    lines.append("Reference: artificialintelligenceact.eu")
    lines.append("")
    lines.append("Built by Suhana Sayyad | linkedin.com/in/suhana35")
    lines.append("github.com/SuhanaSayyad | IAPP Member | MSc Cybersecurity TUS Athlone")
    return "\n".join(lines)

def generate_pdf_report(model_info, results, is_systemic):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=15*mm, bottomMargin=15*mm, leftMargin=20*mm, rightMargin=20*mm)
        styles = getSampleStyleSheet()
        story = []

        header_style = ParagraphStyle("header", parent=styles["Normal"], fontSize=18, fontName="Helvetica-Bold",
                                       textColor=colors.HexColor("#003399"), spaceAfter=4, alignment=TA_CENTER)
        sub_style = ParagraphStyle("sub", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#6b7280"),
                                    spaceAfter=12, alignment=TA_CENTER)
        section_style = ParagraphStyle("section", parent=styles["Normal"], fontSize=12, fontName="Helvetica-Bold",
                                        textColor=colors.HexColor("#1a1f36"), spaceBefore=12, spaceAfter=4)
        body_style = ParagraphStyle("body", parent=styles["Normal"], fontSize=9, spaceAfter=3, leading=13)
        note_style = ParagraphStyle("note", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#6b7280"),
                                     spaceAfter=4, leftIndent=12)

        story.append(Paragraph("GPAI Code of Practice Self-Assessment Report", header_style))
        story.append(Paragraph("EU AI Act - Articles 53 and 55 | " + datetime.now().strftime("%d %B %Y"), sub_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#003399")))
        story.append(Spacer(1, 6))

        info_data = [
            ["Model Name", model_info.get("model_name", "Not provided")],
            ["Provider Organisation", model_info.get("provider", "Not provided")],
            ["Assessment Date", datetime.now().strftime("%d %B %Y")],
            ["Systemic Risk Model", "Yes" if is_systemic else "No"],
        ]
        info_table = Table(info_data, colWidths=[60*mm, 110*mm])
        info_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#374151")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#e5e7eb")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 10))

        score, total = compute_score(results)
        pct = int(score / total * 100) if total > 0 else 0
        met = sum(1 for r in results if r["status"] == "Met")
        partial = sum(1 for r in results if r["status"] == "Partial")
        not_met = sum(1 for r in results if r["status"] == "Not Met")
        na = sum(1 for r in results if r["status"] == "N/A")

        score_color = colors.HexColor("#16a34a") if pct >= 80 else colors.HexColor("#d97706") if pct >= 50 else colors.HexColor("#dc2626")
        score_label = "Strong compliance posture" if pct >= 80 else "Partial compliance - action needed" if pct >= 50 else "Significant gaps identified"

        score_data = [[
            Paragraph(f'<font size="20" color="white"><b>{score:.0f}/{total}</b></font>', ParagraphStyle("sc", alignment=TA_CENTER)),
            Paragraph(f'<font size="11" color="white"><b>{pct}% - {score_label}</b></font><br/><font size="9" color="white">Met: {met}  |  Partial: {partial}  |  Not Met: {not_met}  |  N/A: {na}</font>', ParagraphStyle("sl", alignment=TA_LEFT, leading=16))
        ]]
        score_table = Table(score_data, colWidths=[35*mm, 135*mm])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), score_color),
            ("PADDING", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [6]),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 12))

        status_colors = {"Met": colors.HexColor("#dcfce7"), "Partial": colors.HexColor("#fef3c7"),
                         "Not Met": colors.HexColor("#fee2e2"), "N/A": colors.HexColor("#f3f4f6")}
        status_text_colors = {"Met": colors.HexColor("#14532d"), "Partial": colors.HexColor("#78350f"),
                               "Not Met": colors.HexColor("#7f1d1d"), "N/A": colors.HexColor("#6b7280")}

        for section_title, section_key in [("Transparency Measures", "transparency"),
                                             ("Copyright Measures", "copyright"),
                                             ("Systemic Risk Measures", "systemic_risk")]:
            sec = [r for r in results if r["section"] == section_key]
            if not sec:
                continue
            story.append(Paragraph(section_title, section_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))
            story.append(Spacer(1, 4))
            for r in sec:
                bg = status_colors.get(r["status"], colors.white)
                tc = status_text_colors.get(r["status"], colors.black)
                row_data = [[
                    Paragraph(f'<b>{r["id"]} - {r["title"]}</b>', ParagraphStyle("rd", fontSize=9, fontName="Helvetica-Bold", textColor=tc)),
                    Paragraph(f'<b>{r["status"]}</b>', ParagraphStyle("rs", fontSize=9, fontName="Helvetica-Bold", textColor=tc, alignment=TA_CENTER)),
                    Paragraph(r["article"], ParagraphStyle("ra", fontSize=8, textColor=tc))
                ]]
                row_table = Table(row_data, colWidths=[90*mm, 28*mm, 52*mm])
                row_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), bg),
                    ("PADDING", (0, 0), (-1, -1), 5),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
                ]))
                story.append(row_table)
                note = st.session_state.notes.get(r["id"], "").strip()
                if note:
                    story.append(Paragraph(f"Notes: {note}", note_style))
            story.append(Spacer(1, 8))

        not_met_results = [r for r in results if r["status"] in ["Not Met", "Partial"]]
        if not_met_results:
            story.append(Paragraph("90-Day Action Plan", section_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))
            story.append(Spacer(1, 4))
            for priority, label, bg, tc in [
                (30, "0-30 Days: Quick Wins", colors.HexColor("#dcfce7"), colors.HexColor("#14532d")),
                (60, "31-60 Days: Medium Effort", colors.HexColor("#fef3c7"), colors.HexColor("#78350f")),
                (90, "61-90 Days: Complex Implementation", colors.HexColor("#fee2e2"), colors.HexColor("#7f1d1d"))
            ]:
                tasks = [r for r in not_met_results if MEASURES[r["id"]].get("priority", 90) == priority]
                if not tasks:
                    continue
                plan_data = [[Paragraph(f"<b>{label}</b>", ParagraphStyle("ph", fontSize=9, fontName="Helvetica-Bold", textColor=tc,
                                                                            spaceAfter=2))]]
                for t in tasks:
                    plan_data.append([Paragraph(f"  - {t['id']} {t['title']} ({t['article']})",
                                                ParagraphStyle("pt", fontSize=8, textColor=tc, leftIndent=8))])
                plan_table = Table(plan_data, colWidths=[170*mm])
                plan_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), bg),
                    ("PADDING", (0, 0), (-1, -1), 6),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
                ]))
                story.append(plan_table)
                story.append(Spacer(1, 4))

        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "This report is for guidance only and does not constitute legal advice. "
            "Built by Suhana Sayyad | linkedin.com/in/suhana35 | github.com/SuhanaSayyad | IAPP Member | MSc Cybersecurity TUS Athlone",
            ParagraphStyle("footer", fontSize=7, textColor=colors.HexColor("#9ca3af"), alignment=TA_CENTER)
        ))

        doc.build(story)
        return buf.getvalue()
    except Exception as e:
        return None

# ── MEASURE CARD HELPER ───────────────────────────────────────────────────────
def render_measure_card(measure_id):
    m = MEASURES[measure_id]
    st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{m["id"]} - {m["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Reference: {m["article"]}</div>', unsafe_allow_html=True)
    st.write(m["question"])

    col_a, col_b = st.columns([3, 1])
    with col_a:
        with st.expander("Implementation Guidance"):
            st.write(m["guidance"])
    with col_b:
        with st.expander("Evidence Checklist"):
            st.markdown("**Documents you need:**")
            for item in m["evidence"]:
                st.markdown(f"- {item}")

    current = st.session_state.answers.get(measure_id, ANSWER_OPTIONS[2])
    idx = ANSWER_OPTIONS.index(current) if current in ANSWER_OPTIONS else 2
    answer = st.selectbox("Your compliance status", ANSWER_OPTIONS, index=idx, key=f"select_{measure_id}")
    st.session_state.answers[measure_id] = answer

    note = st.text_area(
        "Implementation notes / evidence reference (optional)",
        value=st.session_state.notes.get(measure_id, ""),
        key=f"notes_{measure_id}",
        placeholder="e.g. Our model card is published at... / This is handled by policy document v2.3...",
        height=68
    )
    st.session_state.notes[measure_id] = note
    st.markdown('</div>', unsafe_allow_html=True)

# ── PROGRESS BAR ──────────────────────────────────────────────────────────────
def show_progress():
    if st.session_state.step > 0:
        steps = ["Info", "Transparency", "Copyright", "Systemic Risk", "Results"]
        current = min(st.session_state.step - 1, 4)
        cols = st.columns(5)
        for i, (col, label) in enumerate(zip(cols, steps)):
            with col:
                if i < current:
                    st.markdown(f"<div style='text-align:center;color:#16a34a;font-size:0.8rem;'>OK {label}</div>", unsafe_allow_html=True)
                elif i == current:
                    st.markdown(f"<div style='text-align:center;color:#003399;font-weight:700;font-size:0.8rem;'>* {label}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align:center;color:#9ca3af;font-size:0.8rem;'>{label}</div>", unsafe_allow_html=True)
        st.markdown("---")

# ── STEP 0: LANDING ───────────────────────────────────────────────────────────
def step_landing():
    st.markdown("""
    <div class="main-header">
        <h1>GPAI Code of Practice Self-Assessment Tool</h1>
        <p>EU AI Act Articles 53 and 55 | General-Purpose AI Models</p>
        <p>Check your compliance with the EU GPAI Code of Practice obligations</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="section-card">
        <div class="section-title">What is the GPAI CoP?</div>
        <div class="section-subtitle">Background and context</div>
        The GPAI Code of Practice is the official voluntary compliance framework for providers of general-purpose AI models under the EU AI Act. Finalised on 10 July 2025, it sets out concrete measures for transparency, copyright, and safety obligations under Articles 53 and 55.
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="section-card">
        <div class="section-title">Who must comply?</div>
        <div class="section-subtitle">Scope of application</div>
        Any provider that places a GPAI model on the EU market or makes it available to EU users. This includes providers of foundation models, large language models, multimodal models, and fine-tuned versions placed on the market under their own name.
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="section-card">
        <div class="section-title">What this tool covers</div>
        <div class="section-subtitle">Assessment scope</div>
        13 key measures across Transparency (T1-T5), Copyright (C1-C3), and Systemic Risk (SR1-SR5). Includes evidence checklists, notes per measure, downloadable PDF report, radar chart, 90-day action plan, and shareable URL.
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="disclaimer">
    This tool provides technical guidance only and does not constitute legal advice.
    Reference the official GPAI Code of Practice at <a href="https://artificialintelligenceact.eu" target="_blank">artificialintelligenceact.eu</a>
    </div>""", unsafe_allow_html=True)

    st.markdown("")
    if st.button("Start Assessment", type="primary", key="start_btn", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ── STEP 1: MODEL INFO ────────────────────────────────────────────────────────
def step_model_info():
    st.markdown("""<div class="main-header">
        <h1>Step 1 of 4 - Model Information</h1>
        <p>Basic details about the GPAI model being assessed</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">About Your Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">This information appears in your generated report only. Nothing is stored or transmitted.</div>', unsafe_allow_html=True)

    model_name = st.text_input("Model name or identifier", value=st.session_state.model_info.get("model_name", ""), placeholder="e.g. MyCompany-LLM-7B")
    provider = st.text_input("Provider organisation", value=st.session_state.model_info.get("provider", ""), placeholder="e.g. MyCompany AI Ltd")

    scope_options = ["Select an option", "Yes - it is trained on broad data and can perform a wide range of tasks",
                     "No - it is a narrow task-specific model", "Unsure"]
    gpai_scope = st.selectbox("Is this model a General-Purpose AI (GPAI) model under the EU AI Act?",
                               scope_options, index=scope_options.index(st.session_state.model_info.get("gpai_scope", "Select an option")))

    sr_options = ["Select an option", "Yes - compute exceeded 10^25 FLOPs or the EU AI Office has designated it",
                  "No - below the threshold and not designated", "Unsure"]
    systemic_risk = st.selectbox("Does your model have systemic risk designation?",
                                  sr_options, index=sr_options.index(st.session_state.model_info.get("systemic_risk", "Select an option")))

    with st.expander("What is the systemic risk threshold?"):
        st.write("Under Article 51 of the EU AI Act, a GPAI model is presumed to have systemic risk if it was trained using more than 10^25 FLOPs. The EU AI Office can also designate models as having systemic risk based on other criteria including number of users and scope of deployment.")

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col2:
        ready = gpai_scope != "Select an option" and systemic_risk != "Select an option"
        if st.button("Next: Transparency Measures", type="primary", key="next_info", disabled=not ready, use_container_width=True):
            st.session_state.model_info = {"model_name": model_name, "provider": provider,
                                            "gpai_scope": gpai_scope, "systemic_risk": systemic_risk}
            st.session_state.step = 5 if "No - it is a narrow task-specific model" in gpai_scope else 2
            st.rerun()
    with col1:
        if st.button("Back", key="back_info", use_container_width=True):
            st.session_state.step = 0
            st.rerun()

# ── STEP 2: TRANSPARENCY ──────────────────────────────────────────────────────
def step_transparency():
    st.markdown("""<div class="main-header">
        <h1>Step 2 of 4 - Transparency Measures</h1>
        <p>Article 53 obligations for all GPAI model providers</p>
    </div>""", unsafe_allow_html=True)

    for mid in ["T1", "T2", "T3", "T4", "T5"]:
        render_measure_card(mid)

    col1, col2 = st.columns([1, 3])
    with col2:
        if st.button("Next: Copyright Measures", type="primary", key="next_transparency", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    with col1:
        if st.button("Back", key="back_transparency", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# ── STEP 3: COPYRIGHT ─────────────────────────────────────────────────────────
def step_copyright():
    st.markdown("""<div class="main-header">
        <h1>Step 3 of 4 - Copyright Measures</h1>
        <p>Article 53(1)(c) obligations for all GPAI model providers</p>
    </div>""", unsafe_allow_html=True)

    for mid in ["C1", "C2", "C3"]:
        render_measure_card(mid)

    is_systemic = "Yes" in st.session_state.model_info.get("systemic_risk", "")
    col1, col2 = st.columns([1, 3])
    with col2:
        next_label = "Next: Systemic Risk Measures" if is_systemic else "See My Results"
        if st.button(next_label, type="primary", key="next_copyright", use_container_width=True):
            st.session_state.step = 4 if is_systemic else 5
            st.rerun()
    with col1:
        if st.button("Back", key="back_copyright", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# ── STEP 4: SYSTEMIC RISK ─────────────────────────────────────────────────────
def step_systemic():
    st.markdown("""<div class="main-header">
        <h1>Step 4 of 4 - Systemic Risk Measures</h1>
        <p>Article 55 obligations for GPAI models with systemic risk designation</p>
    </div>""", unsafe_allow_html=True)

    st.info("These measures apply only to GPAI models trained above 10^25 FLOPs or designated by the EU AI Office as having systemic risk.")

    for mid in ["SR1", "SR2", "SR3", "SR4", "SR5"]:
        render_measure_card(mid)

    col1, col2 = st.columns([1, 3])
    with col2:
        if st.button("See My Results", type="primary", key="next_systemic", use_container_width=True):
            st.session_state.step = 5
            st.rerun()
    with col1:
        if st.button("Back", key="back_systemic", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

# ── STEP 5: RESULTS ───────────────────────────────────────────────────────────
def step_results():
    st.markdown("""<div class="main-header">
        <h1>Your GPAI CoP Compliance Assessment</h1>
        <p>Based on your answers to the EU AI Act GPAI Code of Practice measures</p>
    </div>""", unsafe_allow_html=True)

    gpai_scope = st.session_state.model_info.get("gpai_scope", "")
    if "No - it is a narrow task-specific model" in gpai_scope:
        st.success("Based on your answers, your model does not appear to be a General-Purpose AI model and is likely outside the scope of GPAI CoP obligations under Articles 53 and 55.")
        if st.button("Start Again", key="restart_scope", use_container_width=True):
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.model_info = {}
            st.session_state.notes = {}
            st.rerun()
        return

    is_systemic = "Yes" in st.session_state.model_info.get("systemic_risk", "")
    all_ids = ["T1", "T2", "T3", "T4", "T5", "C1", "C2", "C3"] + (["SR1", "SR2", "SR3", "SR4", "SR5"] if is_systemic else [])

    results = []
    for mid in all_ids:
        if mid not in st.session_state.answers:
            continue
        m = MEASURES[mid]
        results.append({"id": mid, "title": m["title"], "article": m["article"],
                         "status": answer_to_status(st.session_state.answers[mid]), "section": m["section"]})

    if not results:
        st.warning("No answers found. Please complete the assessment from the beginning.")
        if st.button("Start Again", key="restart_empty", use_container_width=True):
            st.session_state.step = 0
            st.rerun()
        return

    update_url()

    score, total = compute_score(results)
    pct = int(score / total * 100) if total > 0 else 0
    met = sum(1 for r in results if r["status"] == "Met")
    partial = sum(1 for r in results if r["status"] == "Partial")
    not_met = sum(1 for r in results if r["status"] == "Not Met")

    color = "background:linear-gradient(135deg,#14532d,#16a34a)" if pct >= 80 else "background:linear-gradient(135deg,#78350f,#d97706)" if pct >= 50 else "background:linear-gradient(135deg,#7f1d1d,#dc2626)"
    label = "Strong compliance posture" if pct >= 80 else "Partial compliance - action needed" if pct >= 50 else "Significant compliance gaps identified"

    st.markdown(f"""
    <div class="score-banner" style="{color};color:white;">
        <div style="font-size:3rem;font-weight:700;line-height:1;">{score:.0f}/{total}</div>
        <div style="font-size:1.1rem;font-weight:600;margin-top:0.4rem;">{label}</div>
        <div style="opacity:0.8;font-size:0.85rem;margin-top:0.3rem;">Met: {met} &nbsp;|&nbsp; Partial: {partial} &nbsp;|&nbsp; Not Met: {not_met}</div>
    </div>""", unsafe_allow_html=True)

    # Radar chart + results side by side
    col_chart, col_results = st.columns([1, 2])

    with col_chart:
        st.markdown("#### Compliance by Section")
        try:
            import plotly.graph_objects as go
            section_scores = get_section_scores(results)
            categories = []
            values = []
            label_map = {"transparency": "Transparency", "copyright": "Copyright", "systemic_risk": "Systemic Risk"}
            for k, label_text in label_map.items():
                if section_scores.get(k) is not None:
                    categories.append(label_text)
                    values.append(section_scores[k])
            if len(categories) >= 2:
                fig = go.Figure(data=go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    fillcolor="rgba(0,51,153,0.15)",
                    line=dict(color="#003399", width=2),
                    marker=dict(color="#003399", size=6)
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                                               ticksuffix="%", tickfont=dict(size=9))),
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=300,
                    margin=dict(l=50, r=50, t=30, b=30)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                for k, label_text in label_map.items():
                    v = section_scores.get(k)
                    if v is not None:
                        st.metric(label_text, f"{v}%")
        except Exception:
            section_scores = get_section_scores(results)
            for k, label_text in [("transparency", "Transparency"), ("copyright", "Copyright"), ("systemic_risk", "Systemic Risk")]:
                v = section_scores.get(k)
                if v is not None:
                    st.metric(label_text, f"{v}%")

    with col_results:
        st.markdown("#### Results by Section")
        for section_title, section_key in [("Transparency (T1-T5)", "transparency"),
                                             ("Copyright (C1-C3)", "copyright"),
                                             ("Systemic Risk (SR1-SR5)", "systemic_risk")]:
            sec = [r for r in results if r["section"] == section_key]
            if not sec:
                continue
            st.markdown(f"**{section_title}**")
            for r in sec:
                icon, css = get_status_html(r["status"])
                note = st.session_state.notes.get(r["id"], "").strip()
                note_html = f' <span style="color:#6b7280;font-size:0.8em;">| {note[:50]}...</span>' if note and len(note) > 0 else ""
                st.markdown(f'<div class="{css}"><b>[{icon}] {r["id"]} - {r["title"]}</b> | {r["article"]} | <b>{r["status"]}</b>{note_html}</div>', unsafe_allow_html=True)

    # 90-Day Action Plan
    not_met_results = [r for r in results if r["status"] in ["Not Met", "Partial"]]
    if not_met_results:
        st.markdown("#### 90-Day Action Plan")
        plan_cols = st.columns(3)
        plan_data = [(30, "0-30 Days: Quick Wins", "action-30"), (60, "31-60 Days: Medium Effort", "action-60"), (90, "61-90 Days: Complex", "action-90")]
        for i, (priority, label_text, css_class) in enumerate(plan_data):
            tasks = [r for r in not_met_results if MEASURES[r["id"]].get("priority", 90) == priority]
            with plan_cols[i]:
                if tasks:
                    st.markdown(f'<div class="{css_class}"><b>{label_text}</b><br/>' + "".join(f'<br/>- {t["id"]} {t["title"]}' for t in tasks) + "</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-na"><b>{label_text}</b><br/>No gaps in this timeframe</div>', unsafe_allow_html=True)

    # Share URL
    st.markdown("#### Share This Assessment")
    st.markdown('<div class="share-box">', unsafe_allow_html=True)
    st.markdown("Your browser URL has been updated with your answers. Copy it from the address bar to share or bookmark this exact assessment.")
    st.markdown("Alternatively copy the parameters below to share via email:")
    share_params = "&".join([f"{mid}={ans.replace(' ', '+')}" for mid, ans in st.session_state.answers.items()])
    st.code(f"?{share_params}&step=5&systemic={'yes' if is_systemic else 'no'}", language=None)
    st.markdown('</div>', unsafe_allow_html=True)

    # Downloads
    st.markdown("#### Download Your Report")
    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        report_text = generate_text_report(st.session_state.model_info, results, is_systemic)
        st.download_button(
            label="Download Report (.txt)",
            data=report_text,
            file_name=f"gpai-cop-assessment-{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="dl_txt",
            use_container_width=True
        )

    with dl_col2:
        pdf_data = generate_pdf_report(st.session_state.model_info, results, is_systemic)
        if pdf_data:
            st.download_button(
                label="Download Report (.pdf)",
                data=pdf_data,
                file_name=f"gpai-cop-assessment-{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="dl_pdf",
                use_container_width=True
            )
        else:
            st.info("PDF generation requires reportlab. Use the .txt download instead.")

    with dl_col3:
        if st.button("Start Again", key="restart_results", use_container_width=True):
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.model_info = {}
            st.session_state.notes = {}
            try:
                st.query_params.clear()
            except Exception:
                pass
            st.rerun()

    # Reference links
    st.markdown("#### Reference Documents")
    st.markdown("""
- [EU AI Act full text](https://artificialintelligenceact.eu) - Articles 53 and 55
- [GPAI Code of Practice Final Version July 2025](https://artificialintelligenceact.eu)
- [EU AI Office](https://digital-strategy.ec.europa.eu/en/policies/ai-office)
- [EDPB Guidelines on AI](https://edpb.europa.eu)
""")

    st.markdown("""<div class="disclaimer">
    This assessment is for guidance only and does not constitute legal advice. It does not replace formal legal counsel or conformity assessment.
    Built by Suhana Sayyad - IAPP Member, MSc Cybersecurity TUS Athlone, Ireland.
    linkedin.com/in/suhana35 | github.com/SuhanaSayyad
    </div>""", unsafe_allow_html=True)

# ── ROUTER ────────────────────────────────────────────────────────────────────
load_from_url()
show_progress()

if st.session_state.step == 0:
    step_landing()
elif st.session_state.step == 1:
    step_model_info()
elif st.session_state.step == 2:
    step_transparency()
elif st.session_state.step == 3:
    step_copyright()
elif st.session_state.step == 4:
    step_systemic()
elif st.session_state.step == 5:
    step_results()
