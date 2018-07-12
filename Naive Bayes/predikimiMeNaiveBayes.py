# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:54:46 2018

@author: ssheh

Testimi i algoritmit te naiveBayes.py
"""
import csv
from naiveBayes import naiveBayes

reader = csv.DictReader(open('TeDhenatTestuese.csv'))
#k = naiveBayes(shteguDataBaze = "Iris.csv", AtributiKlase = "Species" )
#k = naiveBayes(shteguDataBaze = "WaterBears.csv", AtributiKlase = "Species" )
k = naiveBayes(shteguDataBaze = "TeDhenatTrajnuese.csv", AtributiKlase = "Klasa" )
k.kalkulo_propabilitetin_AtributitKlase()
#k.hipoteza = {"SepalLengthCm":"5.1","SepalWidthCm":"3.5","PetalLengthCm":"1.4","PetalWidthCm":"0.2"}
#k.hipoteza = {"SSI":"30.16","BTWa":"26.05","BTWs":"20.87","BTWp":"19.98","BTWL":"0.5","BTPA":"0.77"}
#k.hipoteza = {"Instanca1":"0","Instanca2":"1","Instanca3":"1","Instanca4":"2","Instanca5":"3","Instanca6":"5"}
for row in reader:
    k.hipoteza = row
    k.Kalkulo_propabilitetin_kushtezues(k.hipoteza)
    k.klasifiko()		
    print("\n\n")