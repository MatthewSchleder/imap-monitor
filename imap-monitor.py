from datetime import datetime
import imaplib
import time
import smtplib
from dotenv import load_dotenv
import os
from itertools import chain


def locate_last_uid(USERNAME, PASSWORD):
    # if need to restrict mail search.
    criteria = {}
    uid_max = 0

    def search_string(uid_max, criteria):
        c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [
            ("UID", "%d:*" % (uid_max + 1))
        ]
        return "(%s)" % " ".join(chain(*c))
        # Produce search string in IMAP format:
        #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)

    # Get any attachemt related to the new mail

    # Getting the uid_max, only new email are process

    # login to the imap
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(USERNAME, PASSWORD)
    # select the folder
    mail.select("inbox")

    result, data = mail.uid("SEARCH", None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]
    if uids:
        uid_max = max(uids)
        # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.
    # Logout before running the while loop
    mail.logout()
    print(f"UID MAX is {uid_max}")
    return uid_max


def check_for_new_email(mail, sender_email, uid_max):
    mail.select("inbox")
    status, data = mail.search(
        None, f'(UID {uid_max + 1}:* UNSEEN FROM "{sender_email}")'
    )
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
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(username, recipient, message)
    server.quit()


def main():
    load_dotenv()
    USERNAME = os.environ["YOUR_EMAIL"]
    PASSWORD = os.environ["APP_PASSWORD"]
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    uid_max = locate_last_uid(
        USERNAME, PASSWORD
    )  # This is used so we don't have to search everything
    POLL_TIME = 1  # Number of seconds to check email
    POLL_LOGGING_MESSAGE = 120  # Number of iterations before writing to console
    RESPONSE_SUBJECT = "I love you Allie"
    RESPONSE_BODY = """
Hi there,

Thanks for being my kisses.

Love,
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
            f"Monitoring {USERNAME} emails that are sent from {SENDER_EMAIL}, checking every {POLL_TIME} seconds. you will receive updates every {POLL_TIME * POLL_LOGGING_MESSAGE} seconds"
        )

        while True:
            poll_count = poll_count + 1
            if check_for_new_email(mail, SENDER_EMAIL, uid_max):
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
                uid_max = locate_last_uid(USERNAME, PASSWORD)
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
