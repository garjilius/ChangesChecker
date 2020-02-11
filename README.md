# ChangesChecker
Simple python script to check if a webpage has changed and notify it via mail/telegram

NOTE:
You'll need a sensibledata.py containing variable TOKEN (the token for your telegram bot)
Same for receiver chat id. (MYID variable)

I wanted a page checker that wasn't based on a check on words, but on a hash of the whole page's source code. 
So I'm using a MD5 hash on the html response. 

The list of URLS that need to be checked must be inside a TXT (siteslist.txt), that must be placed in the same folder of the script. 
One URL per line.

I realize the code's a bit messy but it's the first time I even see python - so I apologize if something looks stupid!
