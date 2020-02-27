import hashlib
import telegramfunctions as t
import time
import platform
import requests
import os
from bs4 import BeautifulSoup
from threading import Thread
from sensibledata import MYID
import json
from datetime import datetime


os.environ['TZ'] = 'Europe/Rome'
time.tzset()

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

t.send_message("Bot Rebooted on " + platform.system() + " " + platform.release(), MYID)

def hashurl(urlToHash):
    # set the headers like we are a browser,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    sitehash = "placeholder"
    try:
        response = requests.get(urlToHash, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        #print(soup)
        hashobj = hashlib.md5(soup.encode())
        sitehash = hashobj.hexdigest()
    except:
        print("Connection fail " + urlToHash)
        logf = openlog()
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        logf.write("Connection fail " + urlToHash + " " + date_time+"\n")
        logf.close()
    return sitehash

logf = openlog()
urls = ""
urlsdict = {}
try:
    fp = open('urlshashes.json','r')
    urlsdict = json.loads(fp.read())
    fp.close()

    print("INITIAL LINKS AND HASHES")
    for x, y in urlsdict.items():
        print(x, y)
except Exception as e:
    print(e)
    for i in range(len(urls)):
        for url in urls:
            urlsdict[url.strip()] = hashurl(url.strip())
    with open('urlshashes.json', 'w') as fp:
        json.dump(urlsdict, fp)
        fp.close()

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
                if (text.lower().find("lastlog") >= 0):
                    t.send_message(getlastlog(),id)
            time.sleep(self.durata)

threadBot = BotThread(1)
threadBot.start()

while True:
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    logf = openlog()
    for i in range(len(urls)):
        rehashed = hashurl(urls[i].strip())
        if urlsdict.get(urls[i].strip(),"NOHASH") != rehashed:
            urlsdict[urls[i].strip()] = rehashed
            toSend = urls[i].strip() + " has changed at " + date_time
            print("CHANGE IN URL " + urls[i].strip() + " at " + date_time + " - new hash " + rehashed)
            logf.write("CHANGE IN URL " + urls[i].strip() + " at " + date_time + " - new hash " + rehashed+"\n")
            with open('urlshashes.json', 'w') as fp:
                json.dump(urlsdict, fp)
                fp.close()
            #sendMail(toSend)
            t.send_message(toSend,MYID)

    print("Checked at " + date_time)
    logf.write("Checked at " + date_time+"\n")
    logf.close()
    time.sleep(300)
    #telegram_bot_sendtext("I'm still alive!")

