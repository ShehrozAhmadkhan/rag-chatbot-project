import PyPDF2

def load_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        pdfinstring = ""
        for page in reader.pages:
            pdfinstring += page.extract_text()
    
    return pdfinstring

text = load_pdf("rag-chatbot-project/medicalbook.pdf")
print(text[:500])
