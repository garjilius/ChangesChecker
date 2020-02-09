# Import requests (to download the page)
# Import Time (to add a delay between the times the scape runs)
import datetime
import hashlib
import smtplib
import sys
import time
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

#sys.stdout = open('checkerlog.txt', 'w')

def telegram_bot_sendtext(bot_message):
    bot_token = 'bot-token-here'
    bot_chatID = 'receiver-chat-id-here'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


test = telegram_bot_sendtext("Bot Rebooted on " + platform.system() + " " + platform.release())
#prints the bot's response to a sent message
#print(test)

def sendMail(mess):
    message = MIMEMultipart()
    message['From'] = "address_send"
    message['To'] = "address_dest"
    message['Subject'] = "Webpage has Changed"

    message_content = MIMEText(mess, "plain")
    message.attach(message_content)

    try:
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login("emailaddress", "password")
        mail.sendmail(message["From"], message["To"], message.as_string())
        print("Mail successfully sent")
        mail.close()
    except:
        sys.stderr.write("There is a problem.")
        sys.stderr.flush()
    return

def hashurl(urlToHash):
    # set the headers like we are a browser,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(urlToHash, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
   #print(str(soup) + "\n")
    hashobj = hashlib.md5(soup.encode())
    sitehash = hashobj.hexdigest()
    return sitehash

hashes1 = []
sourcefile = open('siteslist.txt','r')
urls = sourcefile.readlines()

print("URLS TO CHECK BELOW")
for i in range(len(urls)):
    print(urls[i].strip())
    hashed = hashurl(urls[i].strip())
    hashes1.append(hashed)

while True:
    for i in range(len(hashes1)):
        rehashed = hashurl(urls[i].strip())
        if hashes1[i] != rehashed:
            hashes1[i] = rehashed
            toSend = urls[i] + " has changed at " + str(datetime.datetime.now().time())
            print("CHANGE IN URL " + urls[i].strip() + " at " + str(datetime.datetime.now().time()) + " - new hash " + rehashed)
            #sendMail(toSend)
            telegram_bot_sendtext(toSend)

    print("Checked at " + str(datetime.datetime.now().time()))
    time.sleep(60)
    #telegram_bot_sendtext("I'm still alive!")
    continue


