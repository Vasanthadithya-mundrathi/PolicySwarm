"""
PolicySwarm PDF Generator
Generates official-looking policy documents in Indian Government Gazette format
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.colors import HexColor, black, grey
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

# Indian Government Gazette Specifications
# A4: 21.2cm x 29.7cm, Matter: 17cm x 24cm
# Margins: Top/Bottom 3cm, Left/Right 2cm

def create_policy_pdf(
    policy_title: str,
    original_policy: str,
    revised_policy: str,
    citizen_feedback_summary: str,
    senate_analysis: str,
    eligibility_criteria: list,
    benefits_summary: list,
    citizen_score: float,
    senate_score: float,
    iteration_count: int
) -> BytesIO:
    """Generate a professional government-style PDF policy document"""
    
    buffer = BytesIO()
    
    # Document setup with gazette margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=3*cm
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles matching government documents
    govt_header = ParagraphStyle(
        'GovtHeader',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=HexColor('#1a365d')
    )
    
    gazette_title = ParagraphStyle(
        'GazetteTitle',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=12,
        spaceBefore=6
    )
    
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=12,
        textColor=HexColor('#2c5282')
    )
    
    subsection = ParagraphStyle(
        'Subsection',
        parent=styles['Heading3'],
        fontName='Times-Bold',
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=4,
        spaceBefore=8
    )
    
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14
    )
    
    quote_text = ParagraphStyle(
        'QuoteText',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        alignment=TA_LEFT,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=6,
        textColor=HexColor('#4a5568')
    )
    
    footer_text = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        alignment=TA_CENTER,
        textColor=grey
    )
    
    # Build document content
    story = []
    
    # === HEADER SECTION ===
    story.append(Paragraph("GOVERNMENT OF INDIA", govt_header))
    story.append(Paragraph("MINISTRY OF POLICY & PROGRAMME IMPLEMENTATION", 
                          ParagraphStyle('SubHeader', parent=govt_header, fontSize=10)))
    story.append(Spacer(1, 0.3*cm))
    
    # Horizontal line
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#1a365d')))
    story.append(Spacer(1, 0.3*cm))
    
    # Document metadata
    today = datetime.now().strftime("%d %B %Y")
    doc_no = f"F.No. PS/{datetime.now().strftime('%Y')}/POL/{iteration_count:03d}"
    
    metadata = f"""
    <b>Document No.:</b> {doc_no}<br/>
    <b>Date:</b> {today}<br/>
    <b>Subject:</b> {policy_title}
    """
    story.append(Paragraph(metadata, body_text))
    story.append(Spacer(1, 0.5*cm))
    
    # === TITLE SECTION ===
    story.append(Paragraph(f"POLICY DOCUMENT", gazette_title))
    story.append(Paragraph(f"<b>{policy_title.upper()}</b>", gazette_title))
    story.append(HRFlowable(width="100%", thickness=0.5, color=grey))
    story.append(Spacer(1, 0.5*cm))
    
    # === CONSENSUS STATUS ===
    story.append(Paragraph("PART I: CONSENSUS STATUS", section_header))
    
    status_data = [
        ['Metric', 'Score', 'Target', 'Status'],
        ['Citizen Satisfaction', f'{citizen_score:.1f}%', '≥75%', '✓ PASSED' if citizen_score >= 75 else '✗ NEEDS REVISION'],
        ['Government Viability', f'{senate_score:.1f}%', '≥80%', '✓ PASSED' if senate_score >= 80 else '✗ NEEDS REVISION'],
        ['Iterations Completed', str(iteration_count), '≤3', '✓ WITHIN LIMIT' if iteration_count <= 3 else '✗ EXCEEDED'],
    ]
    
    status_table = Table(status_data, colWidths=[5*cm, 3*cm, 3*cm, 4*cm])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(status_table)
    story.append(Spacer(1, 0.5*cm))
    
    # === ELIGIBILITY CRITERIA ===
    story.append(Paragraph("PART II: ELIGIBILITY CRITERIA", section_header))
    story.append(Paragraph(
        "The following eligibility criteria have been determined based on citizen feedback and government analysis:",
        body_text
    ))
    
    for i, criteria in enumerate(eligibility_criteria, 1):
        story.append(Paragraph(f"<b>{i}.</b> {criteria}", body_text))
    story.append(Spacer(1, 0.3*cm))
    
    # === BENEFITS SUMMARY ===
    story.append(Paragraph("PART III: BENEFITS SUMMARY", section_header))
    story.append(Paragraph(
        "Citizens meeting the above criteria shall be entitled to the following benefits:",
        body_text
    ))
    
    for i, benefit in enumerate(benefits_summary, 1):
        story.append(Paragraph(f"<b>{i}.</b> {benefit}", body_text))
    story.append(Spacer(1, 0.3*cm))
    
    # === POLICY INTERPRETATION ===
    story.append(Paragraph("PART IV: POLICY INTERPRETATION", section_header))
    story.append(Paragraph("<b>Original Policy Statement:</b>", subsection))
    story.append(Paragraph(f'"{original_policy}"', quote_text))
    
    story.append(Paragraph("<b>Simplified Interpretation:</b>", subsection))
    story.append(Paragraph(revised_policy, body_text))
    story.append(Spacer(1, 0.3*cm))
    
    # === CITIZEN ADVOCACY ===
    story.append(Paragraph("PART V: CITIZEN ADVOCACY SUMMARY", section_header))
    story.append(Paragraph(
        "The following concerns were raised by citizen representatives during the consultation process:",
        body_text
    ))
    story.append(Paragraph(citizen_feedback_summary, quote_text))
    story.append(Spacer(1, 0.3*cm))
    
    # === GOVERNMENT RESPONSE ===
    story.append(Paragraph("PART VI: GOVERNMENT RESPONSE", section_header))
    story.append(Paragraph(
        "The following analysis was provided by the Senate Advisory Committee:",
        body_text
    ))
    story.append(Paragraph(senate_analysis, quote_text))
    story.append(Spacer(1, 0.5*cm))
    
    # === AUTHENTICATION ===
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#1a365d')))
    story.append(Spacer(1, 0.3*cm))
    
    auth_text = f"""
    <b>AUTHENTICATED</b><br/>
    This document has been generated by PolicySwarm Consensus Engine<br/>
    Iteration: {iteration_count} | Citizen Score: {citizen_score:.1f}% | Senate Score: {senate_score:.1f}%<br/>
    Generated on: {datetime.now().strftime("%d-%m-%Y %H:%M:%S IST")}
    """
    story.append(Paragraph(auth_text, footer_text))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_test_pdf():
    """Generate a test PDF with sample data"""
    
    pdf = create_policy_pdf(
        policy_title="Agricultural Market Reform Act, 2024",
        original_policy="Allow farmers to sell produce directly to private corporations outside government mandis. Remove essential commodity limits. Enable contract farming with pre-agreed prices.",
        revised_policy="""
This policy aims to provide farmers with greater market access while maintaining essential protections. 
Key provisions include:
1. Farmers may sell directly to registered buyers outside mandis, with mandatory digital price disclosure
2. Essential commodity limits apply to hoarding quantities exceeding 1000 quintals
3. Contract farming agreements must include minimum support price (MSP) guarantees
4. A dispute resolution mechanism with 30-day timeline is established
5. Small farmers (under 2 hectares) receive priority access to government procurement
        """,
        citizen_feedback_summary="""
Key concerns raised by citizen representatives:
- Small farmers fear exploitation by large corporations without MSP protection
- Auto drivers and daily wage workers worry about food price volatility
- Business owners support deregulation but want stable supply chains
- Retired persons on fixed income need price stability assurances
- College students concerned about long-term environmental impact
        """,
        senate_analysis="""
Economic Analysis: Potential GDP growth of 1.2% if implemented with safeguards.
Constitutional Review: Article 19(1)(g) compliance achieved with dispute mechanism.
Social Impact: Requires MSP floor to prevent farmer exploitation.
Recommendation: Proceed with phased implementation starting with pilot states.
        """,
        eligibility_criteria=[
            "All agricultural landholders with valid land records",
            "Registered farmer cooperatives and farmer producer organizations (FPOs)",
            "Licensed agricultural traders with APMC registration",
            "Contract farming companies registered under the Companies Act, 2013",
            "Small and marginal farmers (land holding ≤ 2 hectares) receive priority benefits"
        ],
        benefits_summary=[
            "Direct market access to pan-India buyers without mandi intermediaries",
            "Zero tax on first ₹10 lakh of direct sales annually",
            "Government-backed crop insurance at subsidized premiums",
            "Access to cold storage facilities at concessional rates",
            "Digital platform for price discovery and buyer matching",
            "Dispute resolution within 30 days through designated authorities"
        ],
        citizen_score=68.5,
        senate_score=72.0,
        iteration_count=2
    )
    
    # Save test PDF
    with open("test_policy_document.pdf", "wb") as f:
        f.write(pdf.read())
    
    print("✅ Test PDF generated: test_policy_document.pdf")
    return "test_policy_document.pdf"


if __name__ == "__main__":
    generate_test_pdf()
