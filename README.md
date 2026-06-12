---
Title: GPAI Code of Practice Self-Assessment Tool
ColorFrom: Blue
ColorTo: Indigo
Sdk: Streamlit
Sdk_version: 1.35.0
App_file: app.py
Pinned: True
License: MIT
Short_description: Check your GPAI model compliance with EU AI Act Articles 53 and 55
---

# GPAI Code of Practice Self-Assessment Tool

> A free, open-source self-assessment tool for providers of general-purpose AI (GPAI) models to check their compliance with the EU AI Act GPAI Code of Practice obligations under Articles 53 and 55.

**Built by:** [Suhana Sayyad](https://linkedin.com/in/suhana35) | MSc Cybersecurity, TUS Athlone

**GitHub:** [github.com/SuhanaSayyad](https://github.com/SuhanaSayyad)

---

## What this tool does

The GPAI Code of Practice was finalised on 10 July 2025. It sets out the concrete compliance measures that GPAI model providers must implement under Articles 53 and 55 of the EU AI Act. These obligations became applicable on 2 August 2025, with Commission enforcement powers beginning 2 August 2026.

This tool walks through 13 key measures across three chapters and generates a full compliance assessment with downloadable reports.

**Measures covered:**

- **Transparency (T1-T5)** - Technical documentation, training data summary, downstream provider information, instructions for use, and AI content marking. Applies to all GPAI providers.
- **Copyright (C1-C3)** - Copyright compliance policy, opt-out implementation, and training data documentation. Applies to all GPAI providers.
- **Systemic Risk (SR1-SR5)** - Adversarial testing, systemic risk assessment, risk mitigation, incident reporting, and cybersecurity protection. Applies only to models trained above 10^25 FLOPs or designated by the EU AI Office.

---

## Features

**Assessment**
- 13 measures mapped to specific EU AI Act articles
- Four compliance statuses per measure: Fully implemented / Partially implemented / Not implemented / Not applicable
- Implementation guidance for every measure explaining what is required
- Evidence checklist per measure listing the exact documents an auditor would ask for
- Notes field per measure to record your implementation evidence and references

**Results**
- Compliance score with a red/amber/green (RAG) colour-coded banner (green above 80%, amber above 50%, red below 50%)
- Radar chart showing compliance percentage across Transparency, Copyright, and Systemic Risk sections
- Colour-coded result card for every measure showing status and your notes
- Automatic skip of Systemic Risk section for models below the threshold

**Action plan**
- 90-day action plan automatically generated from your gaps
- Gaps categorised by implementation complexity: 30 days for quick wins, 60 days for medium effort, 90 days for complex implementation
- Priority categories based on actual effort required, not just article order

**Reports**
- Download as PDF: professional formatted report with score banner, all measure results, notes, and action plan
- Download as TXT: plain text version for import into compliance management systems
- Shareable URL: browser URL automatically updates with your answers so you can bookmark or share your exact assessment state

---

## Who this is for

- Providers of foundation models, large language models, and multimodal models placing systems on the EU market
- Compliance teams and DPOs at AI companies assessing GPAI obligations
- Legal and governance teams advising on EU AI Act implementation
- Researchers and practitioners studying the GPAI Code of Practice

---

## Legal basis

| Measure | ID | EU AI Act Reference |
|---|---|---|
| Technical documentation | T1 | Article 53(1)(a) + Annex XI |
| Training data summary | T2 | Article 53(1)(d) |
| Downstream provider info | T3 | Article 53(1)(b) |
| Instructions for use | T4 | Article 53(1)(b) |
| AI content marking | T5 | Article 50(5) |
| Copyright compliance policy | C1 | Article 53(1)(c) |
| Opt-out implementation | C2 | Article 53(1)(c) |
| Training data documentation | C3 | Article 53(1)(c) |
| Adversarial testing | SR1 | Article 55(1)(a) |
| Systemic risk assessment | SR2 | Article 55(1)(b) |
| Risk mitigation | SR3 | Article 55(1)(b) |
| Incident reporting | SR4 | Article 55(1)(c) |
| Cybersecurity | SR5 | Article 55(1)(d) |

---

## How to use

1. Click **Start Assessment**
2. Enter your model name and provider details
3. Confirm whether your model is a GPAI model and whether it has systemic risk designation (above 10^25 FLOPs)
4. Work through each section answering the compliance status for every measure
5. Add implementation notes and evidence references in the notes field under each measure
6. View your results including the radar chart and 90-day action plan
7. Download your PDF or TXT report

The assessment takes approximately 10 to 15 minutes to complete. Your answers are encoded in the URL as you go so you can bookmark or share at any point.

---

## Technical stack

| Component | Library |
|---|---|
| Web framework | Streamlit 1.35.0 |
| PDF generation | reportlab 4.1.0 |
| Radar chart | Plotly 5.22.0 |
| Language | Python 3.10+ |
| Hosting | Hugging Face Spaces |

---

## Running locally

```bash
git clone https://github.com/SuhanaSayyad/gpai-cop-self-assessment.git
cd gpai-cop-self-assessment
pip install -r requirements.txt
streamlit run app.py
```

---

## Disclaimer

This tool provides technical guidance only and does not constitute legal advice. It does not replace qualified legal counsel or formal conformity assessment. Always verify your obligations against the official EU AI Act text at [artificialintelligenceact.eu](https://artificialintelligenceact.eu).

Assessment content is based on analysis of the GPAI Code of Practice and EU AI Act text available as of June 2026.

---

## Related tools
 
| Tool | Description | Status |
|---|---|---|
| [EU AI Act / NIST AI RMF / ISO 42001 Crosswalk](https://suhanasayyad.github.io/eu-ai-act-crosswalk-tool) | Maps 30 EU AI Act obligations to NIST and ISO 42001 with strength indicators and gap analysis | Live |
| GPAI CoP Self-Assessment | This tool | Live |


Built by [Suhana Sayyad](https://linkedin.com/in/suhana35) | [GitHub](https://github.com/SuhanaSayyad) | MSc Cybersecurity, TUS Athlone, Ireland
