"""
Diese Datei ist für den Email versand und das Prüfen des Ini Pfades zuständig sollte
Die Ini sollte im Bestem Fall in iniPath angegeben werden. Das Programm unterstüzt keine erstellung einer Ini Datei. (Ist leicht möglich war aber in
den Aufgaben nicht gefordert ;)  )
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application
import ssl
import configparser
import smtplib
iniset = False

#Der Path zur Ini muss angegeben werden. sollte dieser nicht angegeben werden wird danach Gefragt.
iniPath = 'C:/Users/lukas.kapust/Desktop/java test/test.ini'
configparser = configparser.ConfigParser()
filename = "";
#checks if it can locate the required ini else it ask for the path
def getIniPath():
    global iniPath
    global filename
    while ~iniset:
        try:
            configparser.sections()
            configparser.read(iniPath)
            filename = configparser['LOGPATH']['filename']
            return iniPath
            break
        except:
            iniPath = input("Geben sie den INI Pfad an")


#Logt sich in einen SMTP Server ein (in meinem Falle Gmail), erstellt eine Email mit kurzem Text und der Log Datei im Anhang und versendet diese.
def alarm():
    global filename
    sender = configparser['EMAIL']['sender']
    password = configparser['EMAIL']['password']
    smtp_server = configparser['EMAIL']['smtp_server']
    port = int(configparser['EMAIL']['port'])
    receiver = configparser['EMAIL']['receiver']

    message = MIMEMultipart()
    message["From"] = sender
    message["to"] = receiver
    message["Subject"] = "Logs"
    body = MIMEText("Here are the awesome logs")

    fo = open(filename, 'rb')
    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="txt")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)

    message.attach(body)
    message.attach(attach)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
            print("versendet")

    except Exception as e:
        print(e)



