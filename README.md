## imap-monitor

### Motivation

We want to build a house! Here is the process that we will be going through just to get the opportunity to buy the lot we want.

1. Join the new build waitlist.
1. Once a new set of lots becomes available, everyone on the waitlist will receive an email announcing the available lots, and the dates they will be released.
1. On the date mentioned in the prior email, **EVERYONE** receives an email at a hand-selected time from the builder, at the same time.
1. **ONLY** the first few people to send an email to their email queue will be allowed an appointment.
1. If you are fast enough to get an appointment, you will be able to purchase one of the available lots.

We were told by the sales agent that people would take off work and refresh their emails all day, knowing that the email will be received some time through that day. Why would we click the refresh button all day when we have the power of python!

### Getting started

This repo assumes you are using gmail to receive and send emails.

1. Log into your gmail account.
1. Navigate to https://mail.google.com/mail/u/0/#settings/fwdandpop
1. Update the IMAP access to be True
1. Enable 2FA if you don't already have it enabled
1. Create an app password using this document: https://support.google.com/accounts/answer/185833?hl=en
1. Copy the app password (with the spaces)
1. Update the `.env.example` file in this repo to `.env`
1. Update the values in `.env` to be your email, app password, and the sender email you want to monitor for/respond to.
1. Update the `imap-monitor.py` RESPONSE_SUBJECT and RESPONSE_BODY to your liking, along with the POLL_TIME variable to update the amount of time that the script will check your email inbox
1. Run `pip install -r requirements.txt`
1. To run the script:
   1. `python imap-monitor.py`
1. To end the script:
   1. `Ctrl+C`
