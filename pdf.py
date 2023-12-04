import fitz, os, datetime
from fpdf import FPDF
from re import finditer

def splitPdf(pdf_path, matcher):
    if os.path.exists(pdf_path):
        files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f)) and f.endswith('.pdf')]
        if not os.path.exists(os.path.join(pdf_path, 'output')):
            os.mkdir(os.path.join(pdf_path, 'output'))
        for file in files:
            print(getDate(), '| Split pdf on : ', file)
            site = file.replace('.pdf','')[-6:]
            pdf_document = fitz.open(os.path.join(pdf_path, file))
            for key in matcher:
                doc = fitz.open()
                for i in range(pdf_document.page_count):
                    content = pdf_document.load_page(i).get_text().split('\n')
                    if  [s for s in content if any(xs in s for xs in matcher[key])]:
                        teks = key + ' ' + site + file + ': page ' + str(i+1) 
                        print(getDate(), '| ', teks)
                        doc.insert_pdf(pdf_document, from_page= i, to_page= i, start_at= -1)
                        saveFile = key + ' ' + site + '.pdf'
                        doc.save(os.path.join(pdf_path, 'output', saveFile))
                        print(getDate(), '| save pdf at: ', os.path.join(pdf_path, 'output', saveFile))
                doc.close()

def writeToPdf(text, path, filename, doctype):
    if doctype == 1:
        paper = 'A4'
    else:
        paper = 'A3'
    pdf = FPDF('P','mm', paper)
    pdf.set_auto_page_break(auto=True, margin = 15)
    pdf.add_page()
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 5, ('\n').join(text))
    pdf.ln()
    if not os.path.exists(os.path.join(path, 'output')):
        os.mkdir(os.path.join(path, 'output'))
    pdf.output(os.path.join(path, 'output', filename))
    print(getDate(), '| ', text.length(), ' lines printed on ', os.path.join(path, 'output', filename))
    pdf.close()

def parseText(path, matcher):
    print(getDate(), '| Parse text on : ', file)
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and (f.endswith('.csv') or f.endswith('.txt'))]
    site = ''
    for ind, file in enumerate(files):
        print(getDate(), 'Open file : ', file)
        with open(os.path.join(path, file), mode = 'r') as f:
            data = {}
            lines = f.readlines()
            grabFlag = False
            doctype = 0
            site = ''
            for line in lines:
                if line.strip().startswith('LST '):
                    header = line.strip()[4:-2]
                    grabFlag = True
                    doctype = 1
                    data[header] = []
                elif line.strip().startswith('\"Start Time\",\"Period(min)\"'):
                    header = 'Data' + str(len(line))
                    grabFlag = True
                    doctype = 2
                    data[header] = []
                elif line.strip().startswith('---    END') and grabFlag:
                    grabFlag = False
                    data[header].append(line)
                    data[header].append('')
                    data[header].append('')
                elif doctype == 2 and grabFlag and site == '':
                    i = [m.start() for m in finditer(r',', line)]
                    site = line[i[1]+2: i[2]-2]
                    if site[1:2] == '_':
                        site = site[2:8]
                    print(getDate(), site)
                elif line.strip().startswith('+++    ') and grabFlag:
                    site = line.replace('+++    ','').strip()[:-19]
                    if site[1:2] == '_':
                        site = site[2:8]
                    print(getDate(), site)
                if grabFlag:
                    data[header].append(line.strip())
            print(getDate(), '| Parse ', data.length, ' lines')
            for key in matcher:
                pdf = []
                filename = key + ' ' + site + '.pdf'
                for i in data:
                    if  [s for s in data[i] if any(xs in s for xs in matcher[key])]:
                        pdf.extend(data[i])
                        print(getDate(), key, " => ", ('\n').join(data[i]))
                if pdf != []:
                    writeToPdf(pdf, path, filename, doctype)
                    print(getDate(), '| saved on ', os.path.join(path, filename))

def getDate(self):
    t = datetime.datetime.now()
    dt = str(t.year).rjust(2, '0') + str(t.month).rjust(2, '0') + str(t.day).rjust(2, '0') + str(t.hour).rjust(2, '0') + str(t.minute).rjust(2, '0') + str(t.second).rjust(2, '0') + str(t.microsecond).rjust(2, '0')
    return dt 
    
