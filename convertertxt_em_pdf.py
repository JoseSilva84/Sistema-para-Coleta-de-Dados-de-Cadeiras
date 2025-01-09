from fpdf import FPDF
import time

def conversao_txtpdf(arquivo_txt, arquivo_pdf):
    time.sleep(1)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=5)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    with open(arquivo_txt, "r", encoding="utf-8") as file_txt:
        for linha in file_txt:
            pdf.multi_cell(0, 5, linha.strip())
        
        pdf.output(arquivo_pdf)
        print(f"Arquivo pdf foi criado com sucesso: {arquivo_txt}")

# arquivo_txt = "ENROLADOR Wallison impressao.txt"
# arquivo_pdf = "ENROLADOR Wallison impressao.pdf"
# conversao_txtpdf(arquivo_txt, arquivo_pdf)