from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)
from xml.sax.saxutils import escape


THEMES = {
    "blue": colors.HexColor("#2563eb"),
    "green": colors.HexColor("#15803d"),
    "black": colors.HexColor("#222222")
}


def clean_text(value):
    return escape(str(value or "").strip()).replace("\n", "<br/>")


def generate_pdf(data):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm
    )

    accent = THEMES.get(
        data.get("template", "blue"),
        THEMES["blue"]
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "NameStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=29,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#172554"),
        spaceAfter=5
    )

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=accent,
        spaceAfter=8
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        textColor=accent,
        spaceBefore=12,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=4
    )

    story = []

    # Personal information
    story.append(
        Paragraph(clean_text(data.get("name")), name_style)
    )

    if data.get("title"):
        story.append(
            Paragraph(clean_text(data["title"]), title_style)
        )

    contact = [
        data.get("email"),
        data.get("phone"),
        data.get("location")
    ]

    contact = [clean_text(x) for x in contact if x]

    if contact:
        story.append(
            Paragraph(" | ".join(contact), body_style)
        )

    links = [
        data.get("linkedin"),
        data.get("github")
    ]

    links = [clean_text(x) for x in links if x]

    if links:
        story.append(
            Paragraph(" | ".join(links), body_style)
        )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=accent,
            spaceBefore=5,
            spaceAfter=8
        )
    )

    # Resume sections
    sections = [
        ("Professional Summary", "summary"),
        ("Education", "education"),
        ("Technical Skills", "skills"),
        ("Projects", "projects"),
        ("Experience & Internships", "experience"),
        ("Certifications & Achievements", "certifications")
    ]

    for heading, key in sections:
        content = data.get(key, "").strip()

        if content:
            story.append(
                Paragraph(heading.upper(), heading_style)
            )

            story.append(
                Paragraph(clean_text(content), body_style)
            )

    document.build(story)

    buffer.seek(0)

    return buffer
