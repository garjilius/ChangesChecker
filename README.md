# ChangesChecker
Simple python script to check if a webpage has changed and notify it via mail/telegram

NOTE:
You'll need to create your bot and change the bot token inside the code.
Same for receiver chat id.

If you're planning to use mail (disabled in code) you'll need to fill in your login/password details.

I wanted a page checker that wasn't based on a check on words, but on a hash of the whole page's source code. 
So I'm using a MD5 hash on the html response. 

I realize the code's a bit messy but it's the first time I even see python - so I apologize if something looks stupid!
