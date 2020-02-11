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

#sys.stdout = open('checkerlog.txt', 'a')
def openlog():
    try:
        logfile = open("checkerlog.txt", "a")
        return logfile
    except:
        print("couldn't open log file")

def telegram_bot_sendtext(bot_message):
    bot_token = 'token-here'
    bot_chatID = 'chat-id-here'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


test = telegram_bot_sendtext("Bot Rebooted on " + platform.system() + " " + platform.release())
#prints the bot's response to a sent message
#print(test)

"""
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
"""

def hashurl(urlToHash):
    # set the headers like we are a browser,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    sitehash = "placeholder"
    try:
        response = requests.get(urlToHash, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        hashobj = hashlib.md5(soup.encode())
        sitehash = hashobj.hexdigest()
    except:
        print("Connection fail " + urlToHash)
        logf = openlog()
        logf.write("Connection fail " + urlToHash + " " + str(datetime.datetime.now().time())+"\n")
        logf.close()
    return sitehash

hashes1 = []

logf = openlog()

try:
    sourcefile = open('siteslist.txt', 'r')
    logf.write("Sites List Opened\n")
except:
    print("Please make sure a file called siteslist.txt, with one url to check per line, is in the same folder as the program")
    logf.write("Sites List Open Failure\n")

urls = sourcefile.readlines()
sourcefile.close()
if len(urls) < 1:
    raise Exception("No urls to check!")

print("URLS TO CHECK BELOW")
logf.write("URLS TO CHECK:\n")
logf.writelines(urls)
for i in range(len(urls)):
    print(urls[i].strip())
    hashed = hashurl(urls[i].strip())
    hashes1.append(hashed)

logf.write("\n")
logf.close()

while True:
    logf = openlog()
    for i in range(len(hashes1)):
        rehashed = hashurl(urls[i].strip())
        if hashes1[i] != rehashed:
            hashes1[i] = rehashed
            toSend = urls[i] + " has changed at " + str(datetime.datetime.now().time())
            print("CHANGE IN URL " + urls[i].strip() + " at " + str(datetime.datetime.now().time()) + " - new hash " + rehashed)
            logf.write("CHANGE IN URL " + urls[i].strip() + " at " + str(datetime.datetime.now().time()) + " - new hash " + rehashed+"\n")
            #sendMail(toSend)
            telegram_bot_sendtext(toSend)

    print("Checked at " + str(datetime.datetime.now().time()))
    logf.write("Checked at " + str(datetime.datetime.now().time())+"\n")
    logf.close()
    time.sleep(300)
    #telegram_bot_sendtext("I'm still alive!")

