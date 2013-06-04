#!/usr/bin/python
#coding=utf-8
import cgi
import os
import getpass
import random
import cgitb; cgitb.enable()

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass
from datetime import datetime

def htmlcheck(u):#check for illegal characters
	illegal = "<>"
	k = 0
	ln = len(illegal)
	while (k < ln):
		if (u.find(illegal[k]) != -1):
			return True
		else:
			k += 1
	return False

def hl(string):
    fbuff = open("./ccp.txt","r")
    i0 = fbuff.read()
    fbuff.close()
    i1 = int(i0) % 3
    if (i1 == 0):
        string = '<p style="background-color:#ffa954;" title="' + identifier + '">' + string + '</p>'
    elif (i1 == 1):
        string = '<p style="background-color:#4adfff;" title="' + identifier + '">' + string + '</p>'
    else:
        string = '<p style="background-color:#44ed50;" title="' + identifier + '">' + string + '</p>'
    i1 += 1
    fbuff = open("./ccp.txt","w")
    fbuff.write(str(i1))
    fbuff.close()
    return string
        

form = cgi.FieldStorage()
htmlstr = form.getvalue("append")
identifier = form.getvalue("id")
b3 = str(datetime.now())
b3 += " " + cgi.escape(os.environ["REMOTE_ADDR"]) + " " + identifier + "\n"
b4 = cgi.escape(os.environ["REMOTE_ADDR"])

f = open("./log.txt","a")
f.write(b3)
f.close()

print "Content-type: text/html; charset=utf-8\n"

if ((file == []) and (htmlstr == None)):
	print '<html><script>window.location="./";</script></html>'
elif ((not (file == [])) and (htmlstr == None)):
    print '<html><head><title>Mad Words</title><head><body><center>A sentence is required, please submit your image with the a sentence!<br>' + b3 + '</center><br><br><br>'
    f = open("./index.html","r")
    b0 = f.read()
    f.close()
    b0 = b0.strip("\n")
    b0 = b0.split("\n")
    b0 = "".join(b0)
    b1 = b0.find("<body>")
    b2 = len(b0)
    b1 += 6
    print b0[b1:b2]
elif (htmlcheck(htmlstr)):
    print '<html><head><title>Mad Words</title><head><body><center>Detected HTML Code, please get rid of them!<br>' + b3 + '</center><br><br><br>'
    f = open("./index.html","r")
    b0 = f.read()
    f.close()
    b0 = b0.strip("\n")
    b0 = b0.split("\n")
    b0 = "".join(b0)
    b1 = b0.find("<body>")
    b2 = len(b0)
    b1 += 6
    print b0[b1:b2]
elif (not htmlcheck(htmlstr)):
    if (len(htmlstr) < 10):
        print '<html><head><title>Mad Words</title><head><body><center>The sentence needs to have at least 10 characters!<br>' + b3 + '</center><br><br><br>'
        f = open("./index.html","r")
        b0 = f.read()
        f.close()
        b0 = b0.strip("\n")
        b0 = b0.split("\n")
        b0 = "".join(b0)
        b1 = b0.find("<body>")
        b2 = len(b0)
        b1 += 6
        print b0[b1:b2]
    else:
        htmlstr = hl(htmlstr)
        if ("fi" in form.keys()):
            if form["fi"].file:
                fn = "./files/" + os.path.basename(form["fi"].filename)
                z1 = form["fi"].file.read()
                z = open(fn, "wb")
                z.write(z1)
                z.close()
                htmlstr += '<img src="./' + fn + '">'
        f = open("./index.html","r")
        b0 = f.read()
        f.close()
        b0 = b0.strip("\n")
        b0 = b0.split("\n")
        b0 = "".join(b0)
        b1 = b0.find("</div>")
        b2 = len(b0)
        b5 = b0[0:b1] + " " + htmlstr + "\n" + b0[b1:b2]
        f = open("./index.html","w")
        f.write(b5)
        f.close()
        print '<html><script>window.location="./";</script></html>'