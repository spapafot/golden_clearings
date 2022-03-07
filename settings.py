import os

start_date = "01/01/2022"
end_date = "15/01/2022"
debit_name = "2020042.pdf"  # name of the pdf file to split and send
identifier = "11 745"  # usually the postal code is enough as an identifier, always at the top of the page

""" Everything below this line can be configured once,  email, agency list and standard 'Dear Partners' message """

EMAIL = os.environ.get("EMAIL")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

# make sure that the agency names are registered in FORTHCrs with the same names, addd them all here
agency_list = [
    {"agency": "SOMETHING TRAVEL", "email": "email@gmail.com"},
    {"agency": "SOMETHING ELSE TRAVEL", "email": "another_email@gmail.com"},
    ...
]

data = f"Αγαπητοί συνεργάτες, \n\n" \
       f"Σας αποστέλουμε εκκαθάριση εισιτηρίων για την περίοδο {start_date}-{end_date}\n\n" \
       f"Παρακαλούμε για την εξόφληση στον παρακάτω λογαριασμό\n\n" \
       f"Στοιχεία τιμολόγησης:\n\n" \
       f"Με εκτίμηση\n" \
       f"Για το πρακτορείο"
