# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:40:52 2018

@author: ssheh
"""

import pandas as pd

class naiveBayes():
    dataBaza = None
    dataBazaTestuese = None
    propabilitetiAtributitKlase = {}
    propabilitetiAtributeve = {}
    
    def __init__(self, shteguDataBaze, shteguDataBazeTestuese, AtributiKlase = None):
        
        self.dataBazaTestuese = pd.read_csv(shteguDataBazeTestuese)
        self.dataBaza = pd.read_csv(shteguDataBaze)
        self.AtributiKlase = AtributiKlase    
    def kalkulo_propabilitetin_AtributitKlase(self):
        
        vlerat_klases = list(set(self.dataBaza[self.AtributiKlase]))
        
        lista_klases = list(self.dataBaza[self.AtributiKlase]) 
        
        for i in vlerat_klases:
            self.propabilitetiAtributitKlase[i] = round((lista_klases.count(i)/float(len(lista_klases))), 3)
        print("Vlerat e propabilitetit te atributit klase: \n", self.propabilitetiAtributitKlase, "\n")
        
    def kalkulo_propabilitetin_Atributeve(self):
               
        for col in self.dataBazaTestuese.columns:
            atributet = list(set(self.dataBazaTestuese[col]))
            vlerat_atributeve = list(self.dataBazaTestuese[col])
            #lista_klases = list(self.dataBaza[col])
        
            for i in atributet:
                self.propabilitetiAtributeve[i] = round((vlerat_atributeve.count(i)/float(len(vlerat_atributeve))), 3)
        
            print(self.propabilitetiAtributeve)
    
        