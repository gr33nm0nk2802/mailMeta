#!/usr/bin/python3

import email
import re,sys
import argparse
from colorama import Fore, Back, Style

print(Fore.GREEN+"""
                         _ _ __  __      _        
         _ __ ___   __ _(_) |  \/  | ___| |_ __ _ 
        | '_ ` _ \ / _` | | | |\/| |/ _ \ __/ _` |
        | | | | | | (_| | | | |  | |  __/ || (_| |
        |_| |_| |_|\__,_|_|_|_|  |_|\___|\__\__,_|

	    	    Made with ❤️️  gr33nm0nk2802                                      
   
   A tool to analyze email header to identify spoofed emails 
	""")

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="enter the raw(original) email file",type=str)
args=parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

# Reading the file Need to take the file as command line arguments argparse
f = open(args.file)
msg = email.message_from_file(f)
f.close()

parser.print_help()
print(Style.RESET_ALL)
parser = email.parser.HeaderParser()
headers = parser.parsestr(msg.as_string())


meta={
	"message-id":"",
	"spf-record":False,
	"dkim-record":False,
	"dmarc-record":False,
	"spoofed":False,
	"ip-address":"",
	"sender-client":"",
	"spoofed-mail":"",
	"dt":"",
	"content-type":"",
	"subject":""
}

for h in headers.items():

	# Message ID
	if h[0].lower()=="message-id":
		meta["message-id"]=h[1]


	# Mail server sending the mail
	if h[0].lower()=="received":
		meta["sender-client"]=h[1]

	# Authentication detected by mail server
	if h[0].lower()=="authentication-results":

		if(re.search("spf=pass",h[1])):
			meta["spf-record"]=True;

		if(re.search("dkim=pass",h[1])):
			meta["dkim-record"]=True
	
		if(re.search("dmarc=pass",h[1])):
			meta["dmarc-record"]=True

		if(re.search("does not designate",h[1])):
			meta["spoofed"]=True
			
		if(re.search("(\d{1,3}\.){3}\d{1,3}", h[1])):
			ip=re.search("(\d{1,3}\.){3}\d{1,3}", h[1])
			meta["ip-address"]=str(ip.group())
			# print("IP Address: "+ip.group()+"\n")

	if h[0].lower()=="reply-to":
		meta["spoofed-mail"]=h[1]

	if h[0].lower()=="date":
		meta["dt"]=h[1]

	if h[0].lower()=="content-type":
		meta["content-type"]=h[1]

	if h[0].lower()=="subject":
		meta["subject"]=h[1]

print(Fore.BLUE+"\n=========================Results=========================\n"+Style.RESET_ALL)

print(Fore.GREEN+"[+] Message ID"+meta["message-id"])

if(meta["spf-record"]):
	print(Fore.GREEN+"[+] SPF Records: PASS")
else:
	print(Fore.RED+"[+] SPF Records: FAIL")

if(meta["dkim-record"]):
	print(Fore.GREEN+"[+] DKIM: PASS")
else:
	print(Fore.RED+"[+] DKIM: FAIL")

if(meta["dmarc-record"]):
	print(Fore.GREEN+"[+] DMARC: PASS")
else:
	print(Fore.RED+"[+] DMARC: FAIL")

if(meta["spoofed"] and (not meta["spf-record"]) and (not meta["dkim-record"]) and (not meta["dmarc-record"])):
	print(Fore.RED+"[+] Spoofed Email Received")
	print(Fore.RED+"[+] Mail: "+meta["spoofed-mail"])
	print(Fore.RED+"[+] IP-Address:  "+meta["ip-address"])
else:
	print(Fore.GREEN+"[+] Authentic Email Received")
	print(Fore.GREEN+"[+] IP-Address:  "+meta["ip-address"])

print(Fore.GREEN+"[+] Provider "+meta["sender-client"])
print(Fore.GREEN+"[+] Content-Type: "+meta["content-type"])
print(Fore.GREEN+"[+] Date and Time: "+meta["dt"])
print(Fore.GREEN+"[+] Subject: "+meta["subject"]+"\n\n")