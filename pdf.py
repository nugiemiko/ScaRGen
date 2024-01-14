import fitz, os, datetime
from fpdf import FPDF
from re import finditer, findall

def splitPdf(pdf_path, matcher):
    if os.path.exists(pdf_path):
        files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f)) and f.endswith('.pdf')]
        if not os.path.exists(os.path.join(pdf_path, 'output')):
            os.mkdir(os.path.join(pdf_path, 'output'))
        for file in files:
            site = findall(r'([A-Z]{3}[0-9]{3})', file)[0]
            #site = file.replace('.pdf','')[-6:]
            pdf_document = fitz.open(os.path.join(pdf_path, file))
            print(getDates(), '| Split pdf on : ', os.path.join(pdf_path, file))
            for key in matcher:
                doc = fitz.open()
                for i in range(pdf_document.page_count):
                    content = pdf_document.load_page(i).get_text().split('\n')
                    if  [s for s in content if any(xs in s for xs in matcher[key])]:
                        teks = key + ' ' + site + file + ': page ' + str(i+1) 
                        print(getDates(), '|', teks)
                        doc.insert_pdf(pdf_document, from_page= i, to_page= i, start_at= -1)
                        saveFile = key + ' ' + site + '.pdf'
                        doc.save(os.path.join(pdf_path, 'output', saveFile))
                        print(getDates(), '| save pdf at: ', os.path.join(pdf_path, 'output', saveFile))
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
    if os.path.exists(os.path.join(path, 'output', filename)):
        filename1 = filename.replace('.', '1.')
        filename2 = filename.replace('.', '2.')
        os.rename(os.path.join(path, 'output', filename), os.path.join(path, 'output', filename1))
        pdf.output(os.path.join(path, 'output', filename2))
        result = fitz.open()
        for pdffile in [os.path.join(path, 'output', filename1), os.path.join(path, 'output', filename2)]:
            with fitz.open(pdffile) as mfile:
                result.insert_pdf(mfile)
            os.remove(pdffile)
        result.save(os.path.join(path, 'output', filename))
        result.close()
    else:
        pdf.output(os.path.join(path, 'output', filename))
    print(getDates(), '|', len(text), ' lines printed on ', os.path.join(path, 'output', filename))
    pdf.close()

def parseText(path, matcher):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and (f.endswith('.csv') or f.endswith('.txt'))]
    site = ''
    for ind, file in enumerate(files):
        print(getDates(), '| Parse text on : ', file)
        with open(os.path.join(path, file), mode = 'r') as f:
            data = {}
            lines = f.readlines()
            grabFlag = False
            doctype = 0
            site = ''
            header = ''
            for id, line in enumerate(lines):
                if line.strip().startswith('LST '):
                    #header = line.strip()[4:-2]
                    header = findall(r'([A-Z]{3}[0-9]{3})', lines[id+1])[0]
                    grabFlag = True
                    doctype = 1
                    data[header] = []
                elif line.strip().replace('\"', '').startswith('Start Time,'):
                    #header = 'Data' + str(len(line))
                    doctype = 2
                    headerD = line.strip()
                    #data[header] = []
                elif line.strip().startswith('---    END') and grabFlag:
                    grabFlag = False
                    data[header].append(line)
                    data[header].append('')
                    data[header].append('')
                elif doctype == 2:# and grabFlag and site == '':
                    try:
                        site = findall(r'([A-Z]{3}[0-9]{3})', line)[0]
                        header = site
                        grabFlag = True
                    except Exception as e:
                        i = [m.start() for m in finditer(r',', line)]
                        site = line.replace('\"', '')[i[1]+1: i[2]]
                        print(getDates(), '| Parse error 1 : ', e)
                        #if site[1:2] == '_':
                        #    site = site[2:8]
                    if not site in data:
                        data[header] = []
                        data[header].append(headerD)
                elif line.strip().startswith('+++    ') and grabFlag:
                    try:
                        site = findall(r'([A-Z]{3}[0-9]{3})', line)[0]
                    except Exception as e:
                        site = line.replace('+++    ','').strip()[:-19]
                        print(getDates(), '| Parse error 2 : ', e)
                        #if site[1:2] == '_':
                        #    site = site[2:8]
                if grabFlag:
                    data[header].append(line.strip())
            print(getDates(), '| Parse ', len(lines), ' lines')
            for key in matcher:
                for i in data:
                    pdf = []
                    #if doctype == 1:
                    #    filename = key + ' ' + site + '.pdf'
                    #else:
                    #    filename = key + ' ' + i + '.pdf'
                    filename = key + ' ' + i + '.pdf'
                    if  [s for s in data[i] if any(xs in s for xs in matcher[key])]:
                        pdf.extend(data[i])
                        print(getDates(), "|", key, " => ", len(data[i]), " lines")
                    if pdf != []:
                        writeToPdf(pdf, path, filename, doctype)
                        print(getDates(), '| saved on ', os.path.join(path, filename))

def getDates():
    t = datetime.datetime.now()
    dt = str(t.year).rjust(2, '0') + str(t.month).rjust(2, '0') + str(t.day).rjust(2, '0') + str(t.hour).rjust(2, '0') + str(t.minute).rjust(2, '0') + str(t.second).rjust(2, '0') + str(t.microsecond).rjust(8, '0')
    return dt 
    
