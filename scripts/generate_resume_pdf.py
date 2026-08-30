"""Generate the public one-page resume PDF."""

from pathlib import Path
import shutil

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "hadi-budhy-resume.pdf"
PUBLIC = ROOT / "public" / "hadi-budhy-resume.pdf"

INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#536079")
ACCENT = colors.HexColor("#087E8B")
RULE = colors.HexColor("#D7DEE8")


def build_resume() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.4, textColor=MUTED, spaceAfter=2.5)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=8, firstLineIndent=-5, bulletIndent=0, spaceAfter=1.8)
    role = ParagraphStyle("Role", parent=body, fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=INK, spaceAfter=0)
    date = ParagraphStyle("Date", parent=body, fontSize=8.4, leading=11, textColor=ACCENT, alignment=TA_RIGHT)
    heading = ParagraphStyle("Heading", parent=body, fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=ACCENT, spaceBefore=6, spaceAfter=3.5, uppercase=True)
    small = ParagraphStyle("Small", parent=body, fontSize=8, leading=10, textColor=MUTED)

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm,
        topMargin=12 * mm, bottomMargin=11 * mm, title="Hadi Budhy - Senior Data Analyst Resume",
        author="Hadi Budhy", subject="Public resume",
    )

    story = [
        Paragraph("HADI BUDHY", ParagraphStyle("Name", parent=body, fontName="Helvetica-Bold", fontSize=20, leading=22, textColor=INK, spaceAfter=1)),
        Paragraph("SENIOR DATA ANALYST - GROWTH &amp; DECISION ANALYTICS", ParagraphStyle("Target", parent=body, fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=ACCENT, spaceAfter=3)),
        Paragraph(
            'Jakarta, Indonesia  |  <link href="mailto:hadi.budhy@gmail.com" color="#087E8B">hadi.budhy@gmail.com</link>  |  '
            '<link href="https://linkedin.com/in/hadibudhy" color="#087E8B">LinkedIn</link>  |  '
            '<link href="https://github.com/hadibudhy" color="#087E8B">GitHub</link>  |  '
            '<link href="https://hadibudhy.github.io" color="#087E8B">Portfolio</link>', small),
        Spacer(1, 3),
        Paragraph("PROFILE", heading),
        Paragraph("Data analyst with 5+ years across business intelligence, customer analytics, and data automation. Turns messy business data into decision-ready analysis, reliable reporting, and practical tests. Public work demonstrates experimental design, causal restraint, marketplace measurement, and auditable AI workflows.", body),
        Paragraph("EXPERIENCE", heading),
    ]

    roles = [
        ("Data Analyst | Consumer commerce platform", "Oct 2024 - present", [
            "Own event-driven alerting and warehouse pipelines for customer-activity monitoring.",
            "Maintain live dashboards used by support and product teams to detect and respond to change.",
        ]),
        ("Data & Automation Consultant | Independent consulting", "Mar 2023 - Oct 2024", [
            "Turn complex survey and campaign data into reusable analytical models.",
            "Automate warehouse workflows and translate results into leadership-ready reporting.",
        ]),
        ("Senior Business Intelligence Analyst | E-commerce platform", "Jul 2022 - Mar 2023", [
            "Connected churn, segmentation, and cohort analysis into a consistent customer view.",
            "Governed KPI definitions used by retention and marketing teams.",
        ]),
        ("Business Intelligence Analyst | E-commerce platform", "Apr 2021 - Jun 2022", [
            "Built product, customer, and commercial reporting for recurring decision support.",
            "Surfaced engagement patterns used in roadmap discussions.",
        ]),
    ]
    for title, period, bullets in roles:
        header = Table([[Paragraph(title, role), Paragraph(period, date)]], colWidths=[132 * mm, 30 * mm])
        header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        story.append(KeepTogether([header, *[Paragraph(text, bullet, bulletText="-") for text in bullets], Spacer(1, 2)]))

    story.extend([
        Paragraph("SELECTED PUBLIC EVIDENCE", heading),
        Paragraph('<b>Campaign Incrementality</b> - Randomized benchmark analysis separates additional conversions from customers who would have converted anyway. <link href="https://hadibudhy.github.io/projects/campaign-incrementality" color="#087E8B">Case study</link>', body),
        Paragraph('<b>Marketplace Supply &amp; Demand</b> - Limited-data diagnosis separates recorded trips from the requests and driver hours required to measure imbalance. <link href="https://hadibudhy.github.io/projects/marketplace-supply-demand" color="#087E8B">Case study</link>', body),
        Paragraph('<b>ComplaintFlow</b> - Reference implementation combines transparent routing, approved-playbook retrieval, uncertainty escalation, PII redaction, and an auditable decision log. <link href="https://hadibudhy.github.io/projects/2026-08-23-complaintflow-ai-triage" color="#087E8B">Case study</link>', body),
        Paragraph("SKILLS &amp; EDUCATION", heading),
        Paragraph("SQL  |  Python  |  BigQuery  |  dbt  |  Airflow  |  A/B testing  |  Cohort analysis  |  FastAPI  |  LLM evaluation  |  Git", body),
        Paragraph("Bachelor of Public Health (Biostatistics), Universitas Indonesia", body),
        Spacer(1, 3),
        Table([[Paragraph("Public version omits employer/client names and unverified outcome metrics.", small)]], colWidths=[162 * mm], style=TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.6, RULE), ("TOPPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)])),
    ])

    doc.build(story)
    shutil.copy2(OUTPUT, PUBLIC)


if __name__ == "__main__":
    build_resume()
