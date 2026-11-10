from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import re

_BULLET_RE = re.compile(r"^\s*([-*•])\s+(.*)$")

def _escape_minimal(s: str) -> str:
    # ReportLab Paragraph supports a small HTML subset; escape the critical chars.
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )

def _inline_bold(s: str) -> str:
    # Minimal markdown-ish bold: **text** -> <b>text</b>
    def repl(m):
        return f"<b>{m.group(1)}</b>"
    return re.sub(r"\*\*(.+?)\*\*", repl, s)

def generate_pdf(text, path):
    styles = getSampleStyleSheet()

    base = ParagraphStyle(
        "Base",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=colors.black,
        spaceAfter=6,
    )
    title = ParagraphStyle(
        "Title",
        parent=base,
        fontSize=14,
        leading=18,
        spaceAfter=10,
    )

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="AI Text Assistant",
    )

    raw = (text or "").replace("\t", "    ").strip()
    if not raw:
        raw = "Aucun contenu."

    lines = raw.splitlines()
    story = []

    # If the first non-empty line is short, treat it like a title.
    first_non_empty_idx = next((i for i, l in enumerate(lines) if l.strip()), None)
    if first_non_empty_idx is not None:
        first = lines[first_non_empty_idx].strip()
        if len(first) <= 80 and first_non_empty_idx == 0:
            story.append(Paragraph(_inline_bold(_escape_minimal(first)), title))
            story.append(Spacer(1, 6))
            lines = lines[1:]

    bullets = []

    def flush_bullets():
        nonlocal bullets
        if not bullets:
            return
        items = [
            ListItem(Paragraph(_inline_bold(_escape_minimal(b)), base), leftIndent=0)
            for b in bullets
        ]
        story.append(
            ListFlowable(
                items,
                bulletType="bullet",
                leftIndent=14,
                bulletFontName="Helvetica",
                bulletFontSize=10,
                bulletOffsetY=1,
            )
        )
        story.append(Spacer(1, 4))
        bullets = []

    para_buf = []

    def flush_para():
        nonlocal para_buf
        if not para_buf:
            return
        paragraph_text = " ".join(s.strip() for s in para_buf if s.strip())
        if paragraph_text:
            story.append(Paragraph(_inline_bold(_escape_minimal(paragraph_text)), base))
        para_buf = []

    for line in lines:
        s = line.rstrip()
        if not s.strip():
            flush_bullets()
            flush_para()
            story.append(Spacer(1, 6))
            continue

        m = _BULLET_RE.match(s)
        if m:
            flush_para()
            bullets.append(m.group(2).strip())
            continue

        flush_bullets()
        para_buf.append(s.strip())

    flush_bullets()
    flush_para()

    doc.build(story)
