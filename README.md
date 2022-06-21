# Automate WhatsApp Response w/ Python

# Prerequisite

1. npm i -g nodemode localtunnel
2. pip install flask twilio pymongo dnspython

## Step

1. Open a terminal TAB
   a. nodemon main.py
2. Open a second terminal TAB (to get a url to redirect whatsapp response from whatsapp to first tab server)
   a. nodemon --watch "main.py" --exec "lt --subdomain adrian --port 5000" --delay 2
