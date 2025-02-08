from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import Color
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

styles = getSampleStyleSheet()
TITLE_STYLE = ParagraphStyle(
    'title_style',
    parent=styles['Title'],
    fontName='Helvetica-Bold',
    fontSize=16,
    spaceAfter=12,
)
SUBTITLE_STYLE = ParagraphStyle(
    'subtitle_style',
    parent=styles['Title'],
    fontName='Helvetica-Bold',
    fontSize=12,
    spaceAfter=8,
)

NORMAL_STYLE = ParagraphStyle(
    'normal_style',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=8,
    spaceAfter=8,
    alignment=TA_CENTER
)

NORMAL_STYLE_INFO = ParagraphStyle(
    'normal_style',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=10,
    spaceAfter=8
)

HEADER_STYLE = ParagraphStyle(
    'header_style',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    textColor=colors.whitesmoke,
    alignment=TA_CENTER
)

TABLE_STYLE = (TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
BRANDING_STYLE = ParagraphStyle(
    "BrandingStyle",
    parent=TITLE_STYLE,
    fontSize=14,  # Slightly larger than normal text
    textColor=colors.red,  # Red color to highlight it
    alignment=1,  # Center alignment
    spaceBefore=10,  # Some space before the text
    spaceAfter=10,  # Some space after the text
)
