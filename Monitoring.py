"""
Dieses Programm Loggt 3 System werte und Prüft diese auf Schwellenwerte. Dazu Zählt die Festplattenauslastung die Anzahl der Prozesse und die Ram Rauslastung.

Um das Programm zu starten muss Diese Datei  ausgeführt werden Drücken sie dafür, sofern sie Pycharm benutzen, mit der Recten Maustaste in das Programm
und wählen sie Run Monitoring.

"""

#Imports
import threading
from tkinter import *
import asyncio
from datetime import datetime
import tkinter.messagebox
import psutil
import socket
from enum import Enum
import configparser
from Alarm import alarm
from Alarm import getIniPath
import os

#Variablen
iniPath = getIniPath()
configparser = configparser.ConfigParser()
configparser.sections()
configparser.read(iniPath)
window = Tk()
logCpu = False
logRam = False
logHdd = False
wasCritical = False
runningProcess = True
alertProcessCount = int(configparser['ALERTVALUES']['alertProcessCount'])
criticalProcessCount = int(configparser['ALERTVALUES']['criticalProcessCount'])
alertRamCount = int(configparser['ALERTVALUES']['alertRamCount'])
criticalRamCount = int(configparser['ALERTVALUES']['criticalRamCount'])
alertHddCount = int(configparser['ALERTVALUES']['alertHddCount'])
criticalHddCount = int(configparser['ALERTVALUES']['criticalHddCount'])
logFilePath = configparser['LOGPATH']['filename']
critical = " Kritisch: "
alert = " Warnung: "
lastSend = datetime.now()
labelMessage = StringVar()
labelMessage2 = StringVar()
labelMessage3 = StringVar()
logIntervalCpu = int(configparser['INTERVAL']['logIntervalCpu'])
logIntervalRam = int(configparser['INTERVAL']['logIntervalRam'])
logIntervalHdd = int(configparser['INTERVAL']['logIntervalHdd'])
emailInterval = int(configparser['INTERVAL']['emailInterval'])

#holt den IniPat aus Alarm
def setPath(path):
    global iniPath
    iniPath = getIniPath()

#Enum Class
class LogLevel(Enum):
    alert = " Warnung: "
    critical = " Kritisch: "
    normal = ""

#Starten der Module (Setzen der booleans)
#kann vereichfacht werden Bsp
#def startCpu():
#    global logCpu
#    logCpu = !logCpu
#wurde jedoch nicht verwendet um if/else zu verwenden, da dieses im Moodle Modul im Fokus steht
def startCpu():
    global logCpu
    if logCpu:
        logCpu = False
        print("Cpu Moduls beendet")
    else:
        logCpu = True
        print("Cpu Moduls gestartet")

def startRam():
    global logRam
    if logRam:
        logRam = False
        print("Ram Moduls beendet")
    else:
        logRam = True
        print("Ram Moduls gestartet")

def startHdd():
    global logHdd
    if logHdd:
        logHdd = False
        print("Hdd Moduls beendet")
    else:
        logHdd = True
        print("Hdd Moduls gestartet")

#Help Box
def startHelp():
    tkinter.messagebox.showinfo("Infobox", "Wählen sie das zu loggende Modul aus, ein weiterer Klick deaktiviert das Modul")

#Beendet das Programm
def exitProgram():
    """beendet das Program

    und tschüß
    """
    window.quit()
    window.withdraw()


#GUI Deklaration versieht das Fenster verschiedenen Buttons und labeln muss später definiert werden da dieses auf methoden zugreift
window.geometry("400x400")
buttonCpu = Button(window,text="Cpu",command=startCpu)
buttonRam = Button(window,text="Ram",command=startRam)
buttonHdd = Button(window,text="Hdd",command=startHdd)
buttonHelp = Button(window,text="Help",command=startHelp)
buttonExit = Button(window,text="Exit",command=exitProgram)
label = Label(window, textvariable=labelMessage, relief=RAISED)
label.pack()
label2 = Label(window, textvariable=labelMessage2, relief=RAISED)
label2.pack()
label3 = Label(window, textvariable=labelMessage3, relief=RAISED)
label3.pack()
buttonCpu.pack()
buttonRam.pack()
buttonHdd.pack()
buttonHelp.pack()
buttonExit.pack()


#Module um den jeweiligen System wert auszulesen und an die Methode zum Log schreiben zu übergeben.
#Methoden laufen Asynchron und in einem endloss loop, damit sich die Methoden nicht von selbst beenden.
#Prüft auf 2 verschiedene Werte (Kritisch und Warnung)
async def cpuModule():
    global wasCritical
    while runningProcess:
        await asyncio.sleep(0.5)
        while logCpu:
            countProcesses = psutil.pids()

            print(len(countProcesses))
            if len(countProcesses) > criticalProcessCount:
                cpuAlertCrit = "Anzahl laufender Prozesse: " + str(len(countProcesses))
                writeLog(cpuAlertCrit, LogLevel.critical)
                labelMessage.set(cpuAlertCrit)
                wasCritical = True

               # if (datetime.now() - lastSend).seconds > 20:
                #    tmp = threading.Thread(target=sendEmail)
                 #   tmp.daemon = True
                  #  tmp.start()
            elif len(countProcesses) > alertProcessCount:
                    cpuAlert = "Anzahl laufender Prozesse: " + str(len(countProcesses))
                    writeLog(cpuAlert, LogLevel.alert)
                    labelMessage.set(cpuAlert)

            await asyncio.sleep(logIntervalCpu)

async def ramModule():
    global wasCritical
    while runningProcess:

        await asyncio.sleep(0.5)
        while logRam:
            ram = psutil.virtual_memory().percent
            print(ram)
            if ram > criticalRamCount:
                ramUsage = "Auslastung Ram in %: " + str(ram)
                writeLog(ramUsage, LogLevel.critical)
                labelMessage2.set(ramusageCrit)
                wasCritical = True
                #if (datetime.now() - lastSend).seconds > 20:
                 #   tmp = threading.Thread(target=sendEmail)
                  #  tmp.daemon = True
                   # tmp.start()
            elif ram > alertRamCount:
                    ramusageCrit = "Auslastung Ram in %: " + str(ram)
                    writeLog(ramusageCrit, LogLevel.alert)
                    labelMessage2.set(ramusageCrit)
            await asyncio.sleep(logIntervalRam)

async def hddModule():
    global wasCritical
    while runningProcess:
        await asyncio.sleep(0.5)

        while logHdd:
            hdd = psutil.disk_usage("c:\\").percent
            print(hdd)
            if hdd > criticalHddCount:
                hddusageCrit = "Auslastung HDD in %: " + str(hdd)
                writeLog(hddusageCrit, LogLevel.critical)
                labelMessage3.set(hddusageCrit)
                wasCritical = True
                #if (datetime.now() - lastSend).seconds > 20:
                    #(datetime(2013,12,30,23,59,59)- datetime(2013,12,30,23,59,59)).total_seconds()
                    #tmp = threading.Thread(target=sendEmail)
                    #tmp.daemon = True
                    #tmp.start()
            elif hdd > alertHddCount:
                hddusage = "Auslastung HDD in %: " + str(hdd)
                writeLog(hddusage, LogLevel.alert)
                labelMessage3.set(hddusage)
            else:
                hddusage = "Auslastung HDD in %: " + str(hdd)
                writeLog(hddusage, LogLevel.normal)
                labelMessage3.set(hddusage)
            await asyncio.sleep(logHdd)

#Bekommt durch die Module einen string mit den geloggten werden und schreibt diese in eine Logdatei.
#zusätzlich wird über die enums ein wert ausgelesen (" Kritisch: " , " Warnung: " welcher an den String gehangen wird
#Logs werden per Email verschickt, wenn durch die Log Methoden der Boolean "wasCritical" gesetzt wurde ein bestimmter
#Zeitintervall überschritten wurde (verhindert das x mal die Sekunde logs gesendet werden)
def writeLog(msg, x):
    global labelMessage
    global wasCritical
    logdata = open(logFilePath, 'a')
    if(x.value == " Kritisch: " or x.value == " Warnung: "):

        logdata.write("\t \t" + str(datetime.now())+ x.value + socket.gethostname() + " " + msg + "\n" )
    else:
        logdata.write(str(datetime.now()) + x.value + socket.gethostname() + " " + msg + "\n")
    if wasCritical and (datetime.now() - lastSend).seconds > emailInterval:
        print("writelog mail")
        wasCritical = False
        tmp = threading.Thread(target=sendEmail)
        tmp.daemon = True
        tmp.start()

    logdata.close()



#wird durch die WriteLog methode getriggert. triggert das Email verschicken in der Alarm.py setzt außerdem den zeitstempel neu
#nach dem eine neue Email versendet werden kann. Löscht den aktuellen log
def sendEmail():
    global lastSend
    lastSend = datetime.now()
    alarm()
    try:
        os.remove(logFilePath)
    except Exception as e:
        print(e)

#Main Methode der Asynchronen Methoden führt die aufgeführten Module in einem Asynchronen zyclus aus.
async def main():
        await asyncio.gather(cpuModule(),ramModule(),hddModule())

#Startet die Main Methode für die Asynchjronen Methoden (wird benötigt damit das ganze nicht automatisch sondern in einem
#gesondertem Thread ausgeführt werden kann.
def startAsync():
    asyncio.run(main())

#Hier wird das Treading initialisiert
if __name__ == "__main__":
    #help(exitProgram)

    thread2 = threading.Thread(target=startAsync)
    thread2.daemon = True
    thread2.start()
    window.mainloop()
    window.quit()




