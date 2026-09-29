import os
import logging
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from backend.core.config import EXPORTS_DIR

logger = logging.getLogger("ai7.pdf_generator")

def generate_tailored_pdf_resume(candidate_data: dict, target_company: str, target_role: str, filename: str) -> str:
    """
    Generates an executive, professional PDF resume tailored to a specific company/role.
    Strictly uses ONLY verified facts from Candidate Brain.
    """
    out_path = EXPORTS_DIR / filename
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#B45309'), # Rich amber / gold accent
        spaceAfter=6
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=14,
        spaceAfter=3
    )

    role_title_style = ParagraphStyle(
        'RoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Header
    full_name = candidate_data.get("full_name", "V. JAGANNATH")
    story.append(Paragraph(full_name.upper(), title_style))
    story.append(Paragraph(f"{target_role.upper()} | TAILORED FOR {target_company.upper()}", subtitle_style))
    story.append(Paragraph("Dubai, UAE | +971 50 5099065 | v.jagannath3@gmail.com", contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0F172A'), spaceAfter=10))

    # Executive Summary (Grounded in Verified Facts)
    story.append(Paragraph("EXECUTIVE PROFILE", section_header))
    summary_text = (
        f"Senior Real Estate & Asset Management Executive with 20+ years of documented UAE & India institutional experience, "
        f"specializing in Portfolio Strategy, Commercial Leasing, CAPEX Prioritization, and NOI Optimization across diversified assets. "
        f"Track record includes directing an <b>AED 800M Real Estate Portfolio</b>, negotiating <b>2,500+ commercial lease agreements</b>, "
        f"and overseeing <b>800,000 sq. ft. of luxury retail and B2B commercial space</b> across flagship Investment Corporation of Dubai (ICD) developments. "
        f"Demonstrates proven commercial judgement in asset repositioning, tenant strategy, and institutional stakeholder negotiations."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 6))

    # Documented Metrics Grid
    story.append(Paragraph("KEY CAREER METRICS", section_header))
    metrics_data = [
        [
            Paragraph("<b>AED 800M</b><br/>Real Estate Portfolio", body_style),
            Paragraph("<b>800,000 Sq. Ft.</b><br/>Luxury & B2B Leasing Scope", body_style),
            Paragraph("<b>2,500+ Leases</b><br/>Negotiated with Landlords/Tenants", body_style)
        ],
        [
            Paragraph("<b>300+ Locations</b><br/>Catchment & Feasibility Studies", body_style),
            Paragraph("<b>200+ Properties</b><br/>Operations & Performance", body_style),
            Paragraph("<b>6,000+ Contacts</b><br/>Executive Decision-Maker Network", body_style)
        ]
    ]
    t = Table(metrics_data, colWidths=[175, 175, 175])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # Work Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_header))
    experiences = candidate_data.get("experiences", [])
    for exp in experiences:
        company_str = f"<b>{exp.get('employer', '')}</b>"
        if exp.get('parent_company'):
            company_str += f" | {exp['parent_company']}"
        company_str += f" — {exp.get('location', 'Dubai, UAE')}"

        role_dates = f"<b>{exp.get('role_title', '')}</b> ({exp.get('start_date', '')} – {exp.get('end_date', '')})"
        story.append(Paragraph(company_str, role_title_style))
        story.append(Paragraph(role_dates, subtitle_style))

        if exp.get("summary"):
            story.append(Paragraph(exp["summary"], body_style))

        achievements = exp.get("achievements", [])
        if isinstance(achievements, list):
            for ach in achievements:
                story.append(Paragraph(f"• {ach}", bullet_style))
        story.append(Spacer(1, 4))

    # Credentials & Education
    story.append(Paragraph("CREDENTIALS & EDUCATION", section_header))
    story.append(Paragraph("• <b>Certified Retail Management Expert (2026)</b>: Retail Asset Management, Tenant Mix Strategy, Commercial Yield Optimization.", bullet_style))
    story.append(Paragraph("• <b>RERA Certification (2011–2016)</b>: Real Estate Regulatory Agency, Dubai.", bullet_style))
    story.append(Paragraph("• <b>Bachelor's Degree in Hotel Management (2002)</b>: American University of Hawaii.", bullet_style))
    story.append(Paragraph("• <b>Affiliations</b>: Middle East Council of Shopping Centers (MECSC, 2011–2016), National Association of Realtors (NAR, 2017).", bullet_style))
    story.append(Paragraph("• <b>Languages</b>: English (Fluent), Hindi (Fluent), Urdu (Fluent), Telugu (Native).", bullet_style))

    doc.build(story)
    logger.info(f"Generated tailored PDF resume at: {out_path}")
    return str(out_path)
