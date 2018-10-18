#!/usr/bin/env python3

from flask import Flask, render_template
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

app = Flask(__name__)

referenceSonde = "28-0317229e0bff"

def getTemp(sauvegardeStatus):
    fichSonde = open("/sys/bus/w1/devices/" + referenceSonde + "/w1_slave")
    contenu = fichSonde.read()
    fichSonde.close()
    secondeLigne = contenu.split("\n")[1]
    temperatureData = secondeLigne.split(" ")[9]
    temperature = float(temperatureData[2:])
    temperature = temperature / 1000
    if sauvegardeStatus == True :
        enregistrement(temperature)
    return temperature

def enregistrement(temperature):
    d = datetime.now()
    annee = str(d)[:4]
    jour = str(d)[:10]
    repertoire = '/home/pi/AppTempRasp/temperatures/' + annee + '/'
    if not os.path.isdir(repertoire):
        os.makedirs(repertoire)
    fich_Temp = repertoire + jour + '.txt'
    if os.path.exists(fich_Temp):
        f = open(fich_Temp, "a")
    else:
        f = open(fich_Temp, "w")
    time = d.strftime("%H:%M")
    print(str(time) + " " + str(temperature), file=f)
    f.close()

def fichierVersListe(cheminFich):
    f = open(cheminFich, "r")
    points = []
    temperatures = []
    for line in f:
        points.append([line[0:2], line[3:5], line[6:len(line) - 1]])
        temperatures.append(float(line[6:len(line) - 1]))
    f.close()
    return [points, temperatures]

def minMaxTemp(liste, minOrMax):
    newListe = []
    for i in liste :
        newListe.append(i[2])
    if minOrMax == "min" :
        index = newListe.index(min(newListe))
    else :
        index = newListe.index(max(newListe))
    return liste[index][0] + ":" + liste[index][1] + " " + liste[index][2]

def moyenneListe(liste):
    res = 0
    for i in liste:
        res += i
    return (res/len(liste))


@app.route("/getTemp")
def affTemp():
    return render_template('index.html', temp=getTemp(True))

@app.route("/graphTemp")
def graphTempToday():
    return graphTemp(None)

@app.route("/graphTemp/<date>")
def graphTemp(date):
    if date is None:
        d = datetime.now()
        titre = "Température actuelle : " + str(getTemp(False))  + " °C"
    else:
        d = datetime.strptime(date, '%Y%m%d')
        strMonth = str(d.month)
        strDay = str(d.day)
        if len(strMonth) == 1:
            strMonth = "0" + strMonth
        if len(strDay) == 1:
            strDay = "0" + strDay
        dateTitle = strDay + "/" + strMonth + "/" + str(d.year)
        titre = "Statistiques du " + dateTitle
    pointsAndTemp = fichierVersListe("/home/pi/ProjetGraphTemp/temperatures/" + str(d)[:4] + "/" + str(d)[:10] + ".txt")
    temperatures = pointsAndTemp[1]
    nextDate = d + timedelta(days=1)
    prevDate = d - timedelta(days=1)
    return render_template(
        'graphTemp.html',
        d = d.strftime("%Y-%m-%d"),
        titre = titre,
        temp = getTemp(False),
        points = pointsAndTemp[0],
        tempMin = round(min(temperatures), 1),
        tempMax = round(max(temperatures), 1),
        tempMoy = round(moyenneListe(temperatures), 1),
        prevDate = prevDate.strftime("%Y%m%d"),
        nextDate = nextDate.strftime("%Y%m%d")
    )

@app.route("/statTemp")
def statTempToday() :
    return statTemp(None)

@app.route("/statTemp/<date>")
def statTemp(date):
    if date is None:
        d = datetime.now()
    else:
        d = datetime.strptime(date, '%Y%m%d')
    pointsAndTemp = fichierVersListe("/home/pi/ProjetGraphTemp/temperatures/" + str(d)[:4] + "/" + str(d)[:10] + ".txt")
    temperatures = pointsAndTemp[1]
    return render_template(
        'statTemp.html',
        d = d.strftime("%Y-%m-%d"),
        tempMin = minMaxTemp(pointsAndTemp[0], "min"),
        tempMax = minMaxTemp(pointsAndTemp[0], "max"),
        tempMoy = round(moyenneListe(temperatures), 1)
    )


app.run(debug=True, host='0.0.0.0', port=5000)
