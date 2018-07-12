# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 17:00:34 2018

@author: ssheh
"""

from naiveBayesNew import naiveBayes

k = naiveBayes(shteguDataBaze = "DataFrame.csv", shteguDataBazeTestuese = "DataFrameTest.csv", AtributiKlase = "AQI Category" )

k.kalkulo_propabilitetin_AtributitKlase()
k.kalkulo_propabilitetin_Atributeve()