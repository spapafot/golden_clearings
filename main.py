import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfplumber
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

start_date = "01/07/2021"
end_date = "15/07/2021"
debit_name = "4714.pdf"

pdf_file = PyPDF2.PdfFileReader(debit_name)
num_pages = pdf_file.getNumPages()
page_breaks = []
start_page = 0
EMAIL = "*@gmail.com"
EMAIL_PASS = "*"
file_list = []

data = f"Αγαπητοί συνεργάτες, \n\n" \
       f"Σας αποστέλουμε εκκαθάριση εισιτηρίων για την περίοδο {start_date}-{end_date}\n\n" \
       f"Παρακαλούμε για την εξόφληση στον παρακάτω λογαριασμό\n\n" \
       f"Στοιχεία τιμολόγησης:\n\n" \
       f"GALAXY MARITIME S.A. (BRANCH OFFICE)\n" \
       f"MACHIS ANALATOU 111\n" \
       f"11 745 ATHENS\n" \
       f"TEL: 2109561630\n" \
       f"VAT NR: 996997078\n\n" \
       f"Με εκτίμηση\n" \
       f"Για το πρακτορείο"

MILANO_EMAIL = "spapafot@gmail.com"
TAKIS_TRAVEL_EMAIL = "vickyvasileiou7@gmail.com"

agency_list = [{"agency": "TAKIS TRAVEL", "email": TAKIS_TRAVEL_EMAIL},
               {"agency": "MILANO TRAVEL", "email": MILANO_EMAIL},
               {"agency": "AFOI BARKABAS", "email": EMAIL},
               {"agency": "MAI TRAVEL", "email": EMAIL},
               {"agency": "BALKAN LINE", "email": EMAIL},
               {"agency": "LAGOS THEODOROS", "email": EMAIL}]

with pdfplumber.open(debit_name) as pdf:
    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        if "11 745 ATHENS" in text:
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
    debit_ = debit_name[:-4]
    subject = f"ΕΚΚΑΘΑΡΙΣΗ {debit_}"
    body = data
    sender_email = email
    receiver_email = email
    password = EMAIL_PASS

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = debit_note  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(EMAIL, EMAIL_PASS)
    connection.sendmail(sender_email, receiver_email, text)


def find_agency_clearing(pdf_):
    with pdfplumber.open(pdf_) as pdf:
        for index, page in enumerate(pdf.pages):
            text = page.extract_text()
            for agency in agency_list:
                if agency["agency"] in text:
                    send(debit_note=pdf_, data=data, email=agency["email"])


for i in page_breaks:
    x, y = i
    pdf_split(debit_name, x, y)

for i in file_list:
    find_agency_clearing(i)

