# IMAP-Checker
A Web API To Check Valid Mail Accounts

## Description
This is a Web API that Checks Valid Mail and Password by IMAP.
There is also a CLI Version of it.

### Installing

```
git clone https://github.com/TheSpeedX/IMAP-Checker.git
python3 -m pip install requirements.txt
```

### Starting Server

Start Server:
```python3 server.py```

Now To check send JSON data POST Request to:
```http://yourdomain.com/check```
The JSON data format: ```{"email":"mail@domain.com","password":"mypassword"}```

### Starting Command Line Version

Start CLI:
```python3 checker.py -i inputfile```

### TODO
[ ] Add MultiThreading<br>
[ ] Auto Search IMAP for Unknown Domains<br>


#### Credits
Made With ❤ By SpeedX 
