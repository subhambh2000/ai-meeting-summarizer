from fpdf import FPDF


def pdf_generator(filename: str, transcript: str, summary: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="Meeting Transcript and Summary", ln=True, align='C')

    # Summary
    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, "Meeting Summary and action items", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)

    # Add appendix page
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, "Appendix", ln=True, align="C")

    # Transcript
    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, "Transcript", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, transcript)

    pdf.output(filename, 'F')
