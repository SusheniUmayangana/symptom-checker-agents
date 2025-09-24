from datetime import datetime
from fpdf import FPDF
import re
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "[Health] Symptom Checker Assistant", ln=True, align="C")
        self.ln(5)

        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, text)
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C")

def clean_text(text: str) -> str:
    # Replace emojis with readable tags
    emoji_map = {
        "🩺": "[Health]",
        "🦠": "[Virus]",
        "✅": "[Success]",
        "🔍": "[Search]",
        "⬇️": "[Download]",
        "📄": "[Report]",
    }
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)

    # Remove any remaining non-latin characters
    return re.sub(r'[^\x00-\xFF]+', '', text)

def strip_markdown(text: str) -> str:
    # Remove bold, italic, and headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # italic
    text = re.sub(r'_([^_]+)_', r'\1', text)      # underscore italic
    text = re.sub(r'^#+\s*(.*)', r'\1', text, flags=re.MULTILINE)  # headers
    return text


def generate_pdf(report_text: str, filename: str = "health_report.pdf") -> str:
    folder = "reports"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    pdf = PDFReport()
    pdf.add_page()

    # ✅ Clean the report text
    report_text = clean_text(report_text)
    report_text = strip_markdown(report_text)
    
    # ✅ Add this debug line
    print("[PDF Content Preview]", report_text)

    # Split report into sections
    sections = {
        "Identified Symptoms": "",
        "Matched Conditions": "",
        "Advice": ""
    }

    current_section = None
    for line in report_text.split("\n"):
        line = line.strip().rstrip(":")  # ✅ Strip colon
        if line in sections:
            current_section = line
        elif current_section:
            sections[current_section] += line + "\n"

    # Render each section
    for title, body in sections.items():
        pdf.section_title(title)
        pdf.section_body(body.strip())

    pdf.output(filepath)
    return filepath