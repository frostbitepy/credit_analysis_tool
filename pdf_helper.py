from fpdf import FPDF
from io import BytesIO

def generate_detailed_pdf(nombre, profesion, ingresos, fecha_nacimiento, empresa, perfil_comercial, producto, monto_solicitado, plazo, cuota, garantia, scoring, deuda_financiera, deuda_comercial, ratio_deuda_ingresos, puntaje, dictamen):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Dictamen de Crédito", 0, 1, 'C')
    
    # Datos del solicitante
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Datos del solicitante:", 0, 1, 'L')
    pdf.set_font("Arial", 'U', 12)
    pdf.cell(0, 0, "", 0, 1, 'L')
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Nombre: {nombre}", 0, 0, 'L')
    pdf.cell(0, 10, f"Fecha de Nacimiento: {fecha_nacimiento}", 0, 1, 'L')
    pdf.cell(100, 10, f"Profesión: {profesion}", 0, 0, 'L')
    pdf.cell(0, 10, f"Empresa: {empresa}", 0, 1, 'L')
    pdf.cell(100, 10, f"Ingresos: {ingresos}", 0, 0, 'L')
    pdf.cell(0, 10, f"Perfil Comercial: {perfil_comercial}", 0, 1, 'L')
    
    # Datos de la Operación
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Datos de la Operación:", 0, 1, 'L')
    pdf.set_font("Arial", 'U', 12)
    pdf.cell(0, 0, "", 0, 1, 'L')
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Producto: {producto}", 0, 1, 'L')
    pdf.cell(100, 10, f"Monto solicitado: {monto_solicitado}", 0, 1, 'L')
    pdf.cell(100, 10, f"Plazo: {plazo}", 0, 1, 'L')
    pdf.cell(100, 10, f"Cuota: {cuota}", 0, 1, 'L')
    pdf.cell(100, 10, f"Garantía: {garantia}", 0, 1, 'L')
    
    # Informe financiero
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Informe financiero:", 0, 1, 'L')
    pdf.set_font("Arial", 'U', 12)
    pdf.cell(0, 0, "", 0, 1, 'L')
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Scoring: {scoring}", 0, 1, 'L')
    pdf.cell(100, 10, f"Deuda financiera: {deuda_financiera}", 0, 1, 'L')
    pdf.cell(100, 10, f"Deuda comercial: {deuda_comercial}", 0, 1, 'L')
    pdf.cell(100, 10, f"Ratio deuda/ingresos: {ratio_deuda_ingresos}", 0, 1, 'L')
    
    # Calificación final
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Calificación Final:", 0, 1, 'L')
    pdf.set_font("Arial", 'U', 12)
    pdf.cell(0, 0, "", 0, 1, 'L')
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Puntaje: {puntaje}", 0, 1, 'L')
    pdf.cell(100, 10, f"Dictamen: {dictamen}", 0, 1, 'L')
    
    pdf_buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')  # Get PDF content as string
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)
    return pdf_buffer