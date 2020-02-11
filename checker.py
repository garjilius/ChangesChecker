import datetime
import hashlib
import telegramfunctions as t
import time
import platform
import requests
from bs4 import BeautifulSoup
from threading import Thread

def openlog():
    try:
        logfile = open("checkerlog.txt", "a")
        return logfile
    except:
        print("couldn't open log file")

def getlastlog():
    logfile = open("checkerlog.txt","r")
    logs = logfile.readlines()
    return logs[-1]

def getalllogs():
    logfile = open("checkerlog.txt", "r")
    logs = logfile.readlines()
    return str(logs).strip('[]')

t.send_message("Bot Rebooted on " + platform.system() + " " + platform.release(), MYCHATID)

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
urls = ""

try:
    sourcefile = open('siteslist.txt', 'r')
    logf.write("Sites List Opened\n")
    urls = sourcefile.readlines()
    sourcefile.close()
except:
    print("Please make sure a file called siteslist.txt, with one url to check per line, is in the same folder as the program")
    logf.write("Sites List Open Failure\n")

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


class BotThread (Thread):
    def __init__(self, durata):
        Thread.__init__(self)
        self.durata = durata
    def run(self):
        last_update_id = None
        while True:
            updates = t.get_updates(last_update_id)
            if len(updates["result"]) > 0:
                last_update_id = t.get_last_update_id(updates) + 1
                #t.echo_all(updates)
                text, id = t.get_last_chat_id_and_text(updates)
                if (text.find("lastlog") >= 0):
                    t.send_message(getlastlog(),id)

            time.sleep(0.5)
            time.sleep(self.durata)

threadBot = BotThread(1)
threadBot.start()

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
            t.send_message(toSend,MYCHATID)

    print("Checked at " + str(datetime.datetime.now().time()))
    logf.write("Checked at " + str(datetime.datetime.now().time())+"\n")
    logf.close()
    time.sleep(300)
    #telegram_bot_sendtext("I'm still alive!")

