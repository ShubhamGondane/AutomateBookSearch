from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import config as config
# set up the SMTP server

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(config.access["user"], config.access["app_password"])

def sendEmail(books):
	message = "Found these Books on AbeBooks \n"
	i = 1
	for book in books:
		message += str(i) + ". " + book[0]+" by " + book[1] + " for $ %.2f" % book[2]
		message += "\n"
		message += "Get it here: " + str(book[3])
		message += "\n"
		message += "\n"
		i += 1
	msg = MIMEMultipart()
	msg['From']=config.access["user"]
	msg['To']=config.access["user"]
	msg['Subject']="Books to buy"

	msg.attach(MIMEText(message, 'plain'))
	s.send_message(msg)
