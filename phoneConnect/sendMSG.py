
import smtplib


# And imghdr to find the types of our images  Probably not necessary if i have brain
import imghdr


def sendText(to, text):
    from email.message import EmailMessage
    
    # Create the container email message.
    msg = EmailMessage()
    msg['Subject'] = text
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = 'CarefulComet98@gmail.com'
    msg['To'] = to

    #with open('image.jpg', 'rb') as fp:
    #   img_data = fp.read()
    #msg.add_attachment(img_data, maintype='image',subtype=imghdr.what(None, img_data))

    try:
       server = smtplib.SMTP_SSL('smtp.gmail.com',465)
       server.ehlo()
       server.login("CarefulComet98@gmail.com", "temoc420")
       server.send_message(msg)
       server.close()
       
       print("Successfully sent email")
       
       
    except SMTPException:
       print("Error: unable to send email")