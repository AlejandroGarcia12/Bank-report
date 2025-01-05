import email
import imaplib
from datetime import datetime, timedelta
import re
from email.header import decode_header
from utils.utils import get_last_month_date_range, get_transaction_type

def get_info_from_mails(MAIL_USERNAME, MAIL_PASSWORD):
    info = []
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(MAIL_USERNAME, MAIL_PASSWORD)

        # Select the mailbox you want to check
        mail.select('inbox')

        # Get the date range for last month
        start_date, end_date = get_last_month_date_range()
        print(f"Date range: {start_date} to {end_date}")

        # Search for emails from your bank with a specific subject from last month
        status, messages = mail.search(
            None,
            f'(SINCE {start_date} BEFORE {end_date} FROM "notificaciones@lulobank.com" (OR SUBJECT "Compra realizada" SUBJECT "Pago PSE exitoso"))' 
        )

        # Get the list of email IDs

        email_ids = messages[0].split()
        for email_id in email_ids:
            # Fetch the email by ID
            res, msg = mail.fetch(email_id, '(RFC822)')
            for response in msg:
                if not isinstance(response, tuple):
                    continue
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')
                date_tuple = email.utils.parsedate_tz(msg["Date"])
                if not date_tuple:
                    raise ValueError("Invalid date format")
                local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                now_time_minus_10 = datetime.now() - timedelta(minutes=10)
                # Check if the email falls within the specific time range
                # if not (now_time_minus_10 <= local_date.time()):
                #     continue
                
                body = str(response[1])
                fix = False
                if "Compra" in subject:
                    pattern = r'Realizaste.*?por\s[\$\d,]+(?:\.\d+)?'
                    split_patern = "compra en "
                else:
                    pattern = r'Hiciste.*?por\s[\$\d,]+(?:\.\d+)?'
                    split_patern = "pago a "
                    fix = True
                purchase = re.search(pattern, body)
                entity, amount = purchase.group().split(split_patern)[-1].split(" por ")
                trans_type = get_transaction_type(entity)
                if fix:
                    amount = amount.replace('.', ',')
                    amount += ".00"
                if trans_type != "Descartada":
                    info.append([local_date.strftime('%d-%b-%Y %H:%M:%S'), entity, amount,trans_type])
        # Close the connection
        mail.logout()
        return info

    except Exception as e:
        print(f"An error occurred: {e}")