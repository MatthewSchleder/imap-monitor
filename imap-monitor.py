from datetime import datetime
import imaplib
import time
import smtplib
from dotenv import load_dotenv
import os
import simpleaudio as sa


def login(USERNAME, PASSWORD, IMAP_SERVER):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(USERNAME,PASSWORD)
    mail.select("inbox")
    return mail


def check_for_new_email(mail, sender_email):
    try:
        mail.select("inbox")
        status, data = mail.search(None, '(UNSEEN FROM "{}")'.format(sender_email))
        mail_ids = []
        for block in data:
            mail_ids += block.split()

        # Mark emails as read
        for e_id in mail_ids:
            mail.store(e_id, "+FLAGS", "\\Seen")
    except Exception as e:
        print(e)

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
    SEARCH_FRAGMENT = os.environ["SENDER_SEARCH_FRAGMENT"]
    FINAL_RECIPIENT = os.environ["FINAL_RECIPIENT"]
    POLL_TIME = 0.5  # Number of seconds to check email
    POLL_LOGGING_MESSAGE = 1200  # Number of iterations before writing to console, there is slightly more time than just the poll, due to searching for the email
    RESPONSE_SUBJECT = "Email Subject"
    RESPONSE_BODY = """\
Hi there,

This is the body of the email!

Thanks,
Matt
"""
    try:
        mail = login(USERNAME, PASSWORD, "imap.gmail.com")
        poll_count = 0
        print(
            f"Monitoring {USERNAME} emails that are sent from {SEARCH_FRAGMENT}, checking every {POLL_TIME} seconds. you will receive updates about every {POLL_TIME * POLL_LOGGING_MESSAGE} seconds"
        )

        while True:
            poll_count = poll_count + 1
            if check_for_new_email(mail, SEARCH_FRAGMENT):
                print(
                    f"Email from {SEARCH_FRAGMENT} found at {datetime.now().strftime('%b %d, %Y %H:%M:%S.%f')}!"
                )
                send_email(
                    USERNAME,
                    PASSWORD,
                    FINAL_RECIPIENT,
                    RESPONSE_SUBJECT,
                    RESPONSE_BODY,
                )
                print(
                    f"Sent response email to {FINAL_RECIPIENT} at {datetime.now().strftime('%b %d, %Y %H:%M:%S.%f')}."
                )
                alert_sound = sa.WaveObject.from_wave_file("audio/email-sent.wav")
                play_obj = alert_sound.play()
                play_obj.wait_done()
                exit(0)
            elif poll_count >= POLL_LOGGING_MESSAGE:
                poll_count = 0
                print(
                    f"No email located yet. Still waiting... Timestamp: {datetime.now().strftime('%b %d, %Y %H:%M:%S.%f')}"
                )

            time.sleep(POLL_TIME)

    except KeyboardInterrupt:
        print("Program interrupted by user. Logging out.")
    except Exception as e:
        print('Logging in again')
        main()
    finally:
        mail.logout()


if __name__ == "__main__":
    main()
