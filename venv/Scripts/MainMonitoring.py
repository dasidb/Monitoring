# Immports
import asyncio
import sys
import shutil
import datetime
import psutil
import os
import socket
import smtplib
import ssl
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from email.message import EmailMessage
from email.mime.image import MIMEImage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import email
from tkinter import *
from tkinter import simpledialog
import multiprocessing
import tkinter.messagebox
import tkinter




# Initialising global variables
startCPU = False
startHDD = False
startProcesses = False
startRam = False
idleProcess = True




window = Tk()

#Methods to change the Booleans for the logging modules
#They are connected to buttons
def changeCPU():
    global startCPU
    if startCPU == False:
        startCPU = True
        print("CPU Modul gestartet")
    else:
        startCPU = False
        print("CPU Modul beendet")

def changeHDD():
    global startHDD
    if startHDD == False:
        startHDD = True
        print("HDD Modul gestartet")
    else:
        startHDD = False
        print("HDD Modul beendet")

def changeProcess():
    global startProcesses
    if startProcesses == False:
        startProcesses = True
        print("Process Modul gestartet")
    else:
        startCPU = False
        print("Process Modul beendet")

def changeRam():
    global startRam
    if startRam == False:
        startRam = True
        print("Ram Modul gestartet")
    else:
        startRam = False
        print("Ram Modul beendet")

def startProgramm():
    window.withdraw()
    window.quit()

def displayHelp():
    tkinter.messagebox.showinfo("Help","blablabla text blabla")

#Implementation of different buttons
buttoCPU = Button(window, text="CPU",command=changeCPU)
buttoHDD = Button(window, text="HDD",command=changeHDD)
buttoProcess = Button(window, text="Process",command=changeProcess)
buttoRam = Button(window, text="Ram",command=changeRam)
buttonStart = Button(window, text='Programm Starten', command=startProgramm)
buttonInfotext = Button(window,text="Hilfe",command=displayHelp)

buttoCPU.pack()
buttoHDD.pack()
buttoProcess.pack()
buttoRam.pack()
buttonInfotext.pack()
buttonStart.pack()
window.mainloop()
#print(userInput)












#Send SMTP message with a logfile (txt) applied

def sendEmail():
    sender = 'lukas.kapusttest@gmail.com'
    password = 'onYNvafdDOAbgySlhzvK'
    smtp_server = 'smtp.gmail.com'
    port = 587
    receivers = 'lukas.kapust@web.de'
    #message = """From: From Person <lukas.kapusttest@gmail.com>
    #To: To Person <lukas.kapust@web.de>
    #Subject: SMTP e-mail test
    
    #This is a test e-mail message.
    #"""
    #context = ssl.create_default_context()

    #mailObject = email.message.Message.add_header('Content-Disposition', 'attachment; filename="C:/Users/lukas.kapust/Desktop/java test/logdata.txt"')
    message = MIMEMultipart()
    #message = EmailMessage()
    message["From"] = sender
    message["to"] = receivers
    message["Subject"] = "Logs"
    body = "Here you get the Logs"
    filename = "C:/Users/lukas.kapust/Desktop/java test/logdata.txt"

    #message.set_content(body)
    #message.add_attachment(filename, filename=filename)
    #attach the file and add the txt extension
    fo = open(filename, 'rb')
    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="txt")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)

    # Attachment and HTML to body message.
    message.attach(attach)
    #message.attach(HTML_Contents)




   # with open(filename,"rb") as attachement:

     #   part = MIMEBase("application", "octet-stream")
     #   part.set_payload(attachement.read())
    #    encoders.encode_base64(part)
     #   part.add_header("Content-Disposition", f"attachment; filename= {filename}")
     #   message.attach(part)

   # text = message.as_string()


    context = ssl.create_default_context()
    #try catch finally block to connect to the smtp host over a specific port
    #starttls is recquired otherwhise the connection get refused

    try:

        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender, password)
        server.sendmail(sender, receivers, message.as_string())
        #server.send_message(message)
        print("versendet")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

#sendEmail()

#let the user choose which module he wanna use this method isnt used anymore because of the
#implementation of the buttons
def selectionOptions():
    print(startCPU)
    hasSelected = False
    choices = ["CPU", "Festplatte", "Prozesse","RAM"]
    selectedChoices = []
    while(~hasSelected):
        print(choices , "\n")
        for x in selectedChoices:
            if x in choices :
                print(x + " selected")
            else:
                print (x + " deselected")

        choice = input("auswahl")
        if choice in choices :
            if choice in selectedChoices :
                selectedChoices.remove(choice)
            else:
                selectedChoices.append(choice)
        elif choice == "z" or choice == "Z":

            return selectedChoices
            hasSelected == True
        else:
            print("die eingabe war ungültig")

#method to set the booleans for the modules true = module is running in a thread false = module wont run
#this method isnt used anymore cause of the implementation of the buttons
def startmodules(choice) :
    global startCPU
    global startRam
    global startProcesses
    global startHDD
    print(startCPU, "before")
    if "CPU" in choice:
        startCPU = True
        print(startCPU, "after")
    if "Festplatte" in choice:
        startHDD = True

    if "Prozesse" in choice:
        startProcesses = True

    if "RAM" in choice:
        startRam = True

#this method is called in the Modules when a specific value is reached
def writeToLog(msg):
    print("wird aufgerufen")
    logdata = open('C:/Users/lukas.kapust/Desktop/java test/logdata.txt', "a")
    logdata.write(str(datetime.now())+ " " + socket.gethostname() + " " +  msg + "\n")



choices = selectionOptions();
print(choices, "das ist choices")
startmodules(choices)



#start of the different log Modules with 2 different values one for writing to log the other is for sending
#an email
async def  startCpuModule():
# An der stelle könnte auch eine liste über psutil.process_iter(): erstellt werden
#Jedoch ist die ausgabe über psutil.pids() performanter


       while startCPU:
            print("CPU")
            #numberofprocess = []
            #test = psutil.Process
            countProcesses = psutil.pids()
            startHDD = True
            if len(countProcesses) > 200:


                writeToLog(" Count of processes: " + str(len(countProcesses)))
                if len(countProcesses) > 300:
                    print()
                    #send log email
            #for proc in psutil.process_iter():
              #  numberofprocess.append(proc)
          #  print(len(numberofprocess))
            await asyncio.sleep(1)

    #Hier wird der belete Festplatten speicher ausgegeben
    #Könnte auch über psutil gelöst werden, jedoch wollte ich verschiedene ansätze verwenden
async def startHarddiskModule():

        while startHDD:

            usage = shutil.disk_usage("C:\\").used / shutil.disk_usage("c:\\").total * 100

            if usage > 70 :
                msg = "Disk Usage in % " + str(usage)

                writeToLog(msg)
                if usage > 90 :
                  print()
                    #send email with log data


            await asyncio.sleep(1)
async def startProcessModule():

       while startProcesses:

            await asyncio.sleep(0.1)
async def startRamModule():

        while startRam:
            mem = psutil.virtual_memory().percent
            if mem > 70:
                memStr = " Ram Usage in %: " + str(mem)

                writeToLog(str(mem))
                if mem > 90:
                   print()
                    #send email
            await asyncio.sleep(1)


#the default method to call async methods i choosed this to ensure that logs are written seperatly
#i might think about implement multithreadingprocesses instead of asyncio
async def main():

    await asyncio.gather(startCpuModule(), startHarddiskModule(), startRamModule(), startProcessModule())
    print("Main")
    #asyncio.create_task(startCpuModule())
  #  asyncio.create_task(startHarddiskModule())
   # asyncio.create_task(startLogdataModule())
    #asyncio.create_task(startProcessModule())



#the call to run the async methods
asyncio.run(main())







# schreibt den String in die Logdatei











