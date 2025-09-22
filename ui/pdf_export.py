from fpdf import FPDF

def generate_pdf(report_text, filename="health_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in report_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename