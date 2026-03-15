"""
PDF Export Module for Theory2Practice AI Bridge
Generates formatted PDF documents from generated use cases
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import datetime


def create_pdf_export(content: dict) -> BytesIO:
    """
    Generate a professional PDF handout from the generated content
    
    Args:
        content: Dictionary containing use cases and metadata
        
    Returns:
        BytesIO buffer containing the PDF
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=1*inch, bottomMargin=0.75*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor('#ff7f0e'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName='Helvetica'
    )
    
    # Header
    elements.append(Paragraph(f"Theory2Practice: {content['topic']}", title_style))
    
    subtitle_text = f"{content['field']} • {content['difficulty_level']} Level • {content['generated_at']}"
    elements.append(Paragraph(subtitle_text, subtitle_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Separator line
    elements.append(Table([['_'*100]], colWidths=[7*inch]))
    elements.append(Spacer(1, 0.3*inch))
    
    # Introduction
    intro_text = "This document presents real-world industry applications of the above topic. Each use case demonstrates how theoretical concepts translate into practical solutions that drive business value and innovation."
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Use Cases
    elements.append(Paragraph("Real-World Use Cases", heading_style))
    
    for i, use_case in enumerate(content['use_cases'], 1):
        # Use case title
        elements.append(Paragraph(f"{i}. {use_case['title']}", subheading_style))
        
        # Industry badge
        industry_data = [['Industry:', use_case['industry']]]
        industry_table = Table(industry_data, colWidths=[1.2*inch, 5.8*inch])
        industry_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('BACKGROUND', (1, 0), (1, 0), HexColor('#e6f2ff')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(industry_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Problem Statement
        elements.append(Paragraph("<b>Problem Statement:</b>", body_style))
        elements.append(Paragraph(use_case['problem'], body_style))
        
        # Theory Application
        elements.append(Paragraph("<b>How Theory Applies:</b>", body_style))
        elements.append(Paragraph(use_case['theory_application'], body_style))
        
        # Impact
        elements.append(Paragraph("<b>Impact:</b>", body_style))
        elements.append(Paragraph(use_case['impact'], body_style))
        
        # Job Roles and Companies in a table
        details_data = [
            ['Relevant Job Roles:', ', '.join(use_case['job_roles'])],
            ['Example Companies:', ', '.join(use_case['companies'])]
        ]
        details_table = Table(details_data, colWidths=[1.5*inch, 5.5*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f2f6')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Key Insights Section
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Key Insights for Students", heading_style))
    
    # Key Takeaway
    elements.append(Paragraph("<b>💡 Main Takeaway:</b>", subheading_style))
    elements.append(Paragraph(content['key_takeaway'], body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Related Skills
    elements.append(Paragraph("<b>📖 Related Skills to Master:</b>", subheading_style))
    for skill in content['related_skills']:
        elements.append(Paragraph(f"• {skill}", body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Learning Path
    elements.append(Paragraph("<b>🛤️ Suggested Learning Path:</b>", subheading_style))
    elements.append(Paragraph(content['learning_path'], body_style))
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Table([['_'*100]], colWidths=[7*inch]))
    footer_text = "Generated by Theory2Practice AI Bridge • Built with ❤️ for Educators"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    buffer.seek(0)
    return buffer


def get_pdf_filename(topic: str) -> str:
    """Generate a clean filename for the PDF export"""
    clean_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_topic = clean_topic.replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"Theory2Practice_{clean_topic}_{timestamp}.pdf"
