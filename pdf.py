import fitz, os

def splitPdf(pdf_path, matcher):
    if os.path.exists(pdf_path):
        files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f)) and f.endswith('.pdf')]
        if not os.path.exists(os.path.join(pdf_path, 'output')):
            os.mkdir(os.path.join(pdf_path, 'output'))
        for file in files:
            site = file.replace('.pdf','')[-6:]
            pdf_document = fitz.open(os.path.join(pdf_path, file))
            for key in matcher:
                doc = fitz.open()
                for i in range(pdf_document.page_count):
                    content = pdf_document.load_page(i).get_text().split('\n')
                    if  [s for s in content if any(xs in s for xs in matcher[key])]:
                        teks = key + ' ' + site + file + ': page ' + str(i+1) 
                        print(teks)
                        doc.insert_pdf(pdf_document, from_page= i, to_page= i, start_at= -1)
                        saveFile = key + ' ' + site + '.pdf'
                        doc.save(os.path.join(pdf_path, 'output', saveFile))
                doc.close()
