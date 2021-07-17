import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfplumber

pdf_file = PyPDF2.PdfFileReader("4714.pdf")
num_pages = pdf_file.getNumPages()
page_breaks = []
start_page = 0

with pdfplumber.open("4714.pdf") as pdf:
    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        if "11 745 ATHENS" in text:
            page_breaks.append((start_page, index-1))
            start_page = index

page_breaks = page_breaks[1:]
print(page_breaks)


# #START HERE
# writer = PdfFileWriter()
#
# for i in page_breaks:
#     x, y = i
#     for page in range(x,y):
#         with open("4714.pdf", 'rb') as infile:
#             reader = PdfFileReader(infile)
#             writer.addPage(reader.getPage(page))
#
#             with open("last.pdf", 'wb') as out:
#                 writer.write(out)

def pdf_split(fname, start, end=None):
    print('pdf_split', fname, start, end)
    # pdf_split ~/Downloads/4-27-files/Invoice Email-0.pdf 1 4

    #inputpdf = PdfFileReader(open("document.pdf", "rb"))
    inputpdf = PdfFileReader(open(fname, "rb"))
    output = PdfFileWriter()

    # turn 1,4 to 0,3
    num_pages = inputpdf.numPages
    if start:
        start-=1
    if not start:
        start=0
    if not end or end > num_pages:
        end=num_pages

    get_pages = list(range(start,end))
    #print('get_pages', get_pages, 'of', num_pages)
    # get_pages [0, 1, 2, 3]

    for i in range(start,end):
        if i < start:
            continue
        #output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))

    fname_no_pdf = fname
    if fname[:-4].lower() == '.pdf':
        fname_no_pdf = fname[:-4]
    out_filename = f"{fname_no_pdf}-{start+1}-{end}.pdf"
    with open(out_filename, "wb") as outputStream:
        output.write(outputStream)
    print('saved', out_filename)

#ADD MAIN

