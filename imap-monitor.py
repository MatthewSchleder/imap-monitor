from datetime import datetime
import imaplib
import time
import smtplib
from dotenv import load_dotenv
import os


def check_for_new_email(mail, sender_email):
    mail.select("inbox")
    status, data = mail.search(None, '(UNSEEN FROM "{}")'.format(sender_email))
    mail_ids = []
    for block in data:
        mail_ids += block.split()

    # Mark emails as read
    for e_id in mail_ids:
        mail.store(e_id, "+FLAGS", "\\Seen")

    return len(mail_ids) > 0


def send_email(username, password, recipient, subject, body):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(username, password)
    message = f"To: {recipient}\nSubject: {subject}\n\n{body}"
    server.sendmail(username, recipient, message)
    server.quit()


def main():
    load_dotenv()
    USERNAME = os.environ["YOUR_EMAIL"]
    PASSWORD = os.environ["APP_PASSWORD"]
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    POLL_TIME = 1  # Number of seconds to check email
    POLL_LOGGING_MESSAGE = 120  # Number of iterations before writing to console, there is slightly more time than just the poll, due to searching for the email
    RESPONSE_SUBJECT = "Email Subject"
    RESPONSE_BODY = """\
Hi there!

This is the response email body

Best,
Matt
"""

    # Create IMAP connection
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(USERNAME, PASSWORD)

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(USERNAME, PASSWORD)
        poll_count = 0
        print(
            f"Monitoring {USERNAME} emails that are sent from {SENDER_EMAIL}, checking every {POLL_TIME} seconds. you will receive updates about every {POLL_TIME * POLL_LOGGING_MESSAGE} seconds"
        )

        while True:
            poll_count = poll_count + 1
            if check_for_new_email(mail, SENDER_EMAIL):
                send_email(
                    USERNAME,
                    PASSWORD,
                    SENDER_EMAIL,
                    RESPONSE_SUBJECT,
                    RESPONSE_BODY,
                )
                print(
                    f"Email from {SENDER_EMAIL} found! Sent response email to {SENDER_EMAIL} at {datetime.now().strftime('%b %d, %Y %H:%M:%S.%f')}."
                )
            elif poll_count >= POLL_LOGGING_MESSAGE:
                poll_count = 0
                print(
                    f"No email located yet. Still waiting... Timestamp: {datetime.now().strftime('%b %d, %Y %H:%M:%S.%f')}"
                )

            time.sleep(POLL_TIME)

    except KeyboardInterrupt:
        print("Program interrupted by user. Logging out.")
    finally:
        mail.logout()


if __name__ == "__main__":
    main()
