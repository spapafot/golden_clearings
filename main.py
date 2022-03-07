import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfplumber
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings

pdf_file = PyPDF2.PdfFileReader(settings.debit_name)
num_pages = pdf_file.getNumPages()
page_breaks = []
start_page = 0
file_list = []


with pdfplumber.open(settings.debit_name) as pdf:
    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        if f"{settings.identifier}" in text:
            page_breaks.append((start_page + 1, index))
            start_page = index

page_breaks = page_breaks[2:]
page_breaks.append((page_breaks[-1][1] + 1, num_pages))


def pdf_split(fname, start, end=None):

    inputpdf = PdfFileReader(open(fname, "rb"))
    output = PdfFileWriter()

    num_pages = inputpdf.numPages
    if start:
        start -= 1
    if not start:
        start = 0
    if not end or end > num_pages:
        end = num_pages

    for i in range(start, end):
        if i < start:
            continue
        output.addPage(inputpdf.getPage(i))

    fname_no_pdf = fname
    if fname[:-4].lower() == '.pdf':
        fname_no_pdf = fname[:-4]
    out_filename = f"{fname_no_pdf}-{start + 1}-{end}.pdf"
    file_list.append(out_filename)
    with open(out_filename, "wb") as outputStream:
        output.write(outputStream)


def send(debit_note, data, email):
    debit_ = settings.debit_name[:-4]
    subject = f"ΕΚΚΑΘΑΡΙΣΗ {debit_}"
    body = data
    sender_email = settings.EMAIL
    receiver_email = email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    filename = debit_note

    #binary mode
    with open(filename, "rb") as attachment:

        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # ASCII
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(settings.EMAIL, settings.EMAIL_PASS)
    connection.sendmail(sender_email, receiver_email, text)


def find_agency_clearing(pdf_):
    with pdfplumber.open(pdf_) as pdf:
        for index, page in enumerate(pdf.pages):
            text = page.extract_text()
            for agency in settings.agency_list:
                if agency["agency"] in text:
                    send(debit_note=pdf_, data=settings.data, email=agency["email"])


if __name__ == "__main__":

    for i in page_breaks:
        x, y = i
        pdf_split(settings.debit_name, x, y)

    for i in file_list:
        find_agency_clearing(i)

