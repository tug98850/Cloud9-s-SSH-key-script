#! /usr/bin/python
# be careful when using this script because it will read all of your email (whic
#h means email that do not have the subject ECE_1111 will be READ AS WELL)
import re, smtplib, email, imaplib

email_addr = "" #enter the email address as a string
passwd = "" #enter the corresponding password as a string
SMTP_server = "imap.gmail.com" 
mail = imaplib.IMAP4_SSL(SMTP_server, 993)
mail.login(email_addr,passwd)
mail.select('inbox')

type, data = mail.search(None, 'X-GM-RAW', 'subject: ECE_1111') #only look through emails with subject ECE_1111

mail_ids = data[0]
id_list = mail_ids.split()
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

for i in range(latest_email_id, first_email_id, -1):
    typ, data = mail.fetch(str(i), '(RFC822)')
    for response_part in data: #do not put data[0][1]
        if isinstance(response_part, tuple):
            msg = str(email.message_from_string(data[0][1])).replace('=', '')
            msg = msg.replace('3D', '=')
            msg = msg.replace('\r', '') #remove ^M in the vim file
            msg = msg.replace('\n', '') #replace all the line break
            msg = msg.replace('rsa', 'rsa ') #add a space after rsa
            msg = msg.replace('==', '== ') #add a space after ==
            msg = msg.replace('ssh', '\nssh') #ssh key has to be on its own line
 in order to work
            msg = msg.replace('@cloud9.amazon.com', '@cloud9.amazon.com \n') #en
d of ssh key line (beginning and the end of every ssh key is the same)
            email_from = email.message_from_string(response_part[1])['from']
            email_subject = email.message_from_string(response_part[1])['subject
']
            email_reg_expression = re.findall(r'[\w.-]+@[\w.-]+', email_from)
            print(email_reg_expression[0][0:8]) #make sure to include [0] to get only email because findall is a tuple doc: https://developers.google.com/edu/python/regular-expressions (findll and groups)
            if email_subject == "ECE_1111":
                path = '/home/{0}/.ssh/authorized_keys'.format(email_reg_expression[0][0:8]) # [0] to get only the email [0:8] get only the first 8 characters (because the first 8 characters make up the username of the user in the system, a Linux VM instance that I ran on)
                file = open(path, 'a+') #a+ is to add to the file without deleting any old stuff, can use w as well but that will delete all the all stuff
                file.write(str(msg)) #make sure to convert msg into string before write to file (to avoid errors)
                print(str(msg))
                print("Process completed")

mail.logout(); 
