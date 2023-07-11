import smtplib

import smtplib,ssl

import mailtrap as mt

def sendmail(message):
    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@example.com", name="Mailtrap Test"),
        to=[mt.Address(email="nachikul1993@gmail.com")],
        subject="You are awesome!",
        text="Congrats for sending test email with Mailtrap!",
    )
    client = mt.MailtrapClient(token="ed281926dbc0f23ba91b50664a9240c9")
    client.send(mail)

def sendmailtoconsole(message):
    finalmsg ="""\
    Subject: Pull Requests Summary
        
    """+message
    print(finalmsg)


