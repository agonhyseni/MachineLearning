# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:53:01 2018

@author: ssheh

Naive Bayes eshte algoritem i cili bazohet ne frekuencen e ngjarjeve per te 
predikuar nese nje ngjarje do te ndodhe ne te ardhmen.

Ky algoritem bazohet ne formulen e propabiliteti e njohur si Teorema e Byesit

Teorema e Bayesit:
                                        Propabiliteti(Evidenca/Hipoteza)*Propabiliteti(Hipoteza)
    Propabiliteti(Hipoteza\Evidenca) =  ________________________________________________________
        
                                                        Propabiliteti(Evidenca)
"""

import pandas as pd

#Percaktimi i Propabilitetit te evidencave te klases
propabiliteti_klases = {}

#Leximi i te dhenave nga baza e te dhenave
data = pd.read_csv('tabele_shembull.csv')
#Caktimi i atributit klase
Atributi_klase = "Atributi_Klase"

#Percaktimi i evidencave ne atributin klase
vlerat_klases = list(set(data[Atributi_klase]))
#Lista e evidencave te atributit klase
lista_klases = list(data[Atributi_klase])
 
#Perderisa ne liste ka nje evidence
for i in vlerat_klases:
    #Numero evidencen kusht/Numri i te gjitha evidencave ne klase
    propabiliteti_klases[i] = lista_klases.count(i)/float(len(lista_klases))
    
print("Vektori i klases: ", propabilitei_klases)
