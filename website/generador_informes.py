from fpdf import FPDF


def generar_informe(datos_monedas):
    first_row = ("Nº", "Valor", "Anverso", "Reverso", "Ceca", "Peso", "Mod", "P.C.", "Ref", "Registro")
    datos_monedas.insert(0, first_row)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=8)
    line_height = pdf.font_size * 10
    print(pdf.epw)
    col_width = (pdf.epw - 107) / 2  # distribute content evenly
    print(col_width)
    for row in datos_monedas:
        pdf.multi_cell(8, line_height, str(row[0]), border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(14, line_height, row[1], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(col_width, line_height, row[2], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(col_width, line_height, row[3], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(16, line_height, str(row[4]), border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(10, line_height, row[5], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(10, line_height, row[6], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(8, line_height, row[7], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(25, line_height, row[8], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.multi_cell(20, line_height, row[9], border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, align="C")
        pdf.ln(line_height)
    pdf.output(f"informes/documento.pdf")
