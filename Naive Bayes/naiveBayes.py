# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:53:01 2018
@author: Sadri Shehu ssheh
"""
import pandas as pd
import functools as funct
import pprint 

class naiveBayes():
    
    """
    Naive Bayes eshte algoritem i cili bazohet ne frekuencen e ngjarjeve per te 
    predikuar nese nje ngjarje do te ndodhe ne te ardhmen.
    Ky algoritem bazohet ne formulen e propabiliteti e njohur si Teorema e Byesit
    Teorema e Bayesit:
        P(H|E) =  P(E/H)*P(H) / P(E)
        
    P(H|E) : Propabiliteti(HipotezaEvidences), 
    P(E/H) : Propabiliteti(Evidenca/Hipoteza), 
    P(H) : Propabiliteti(Hipoteza), 
    P(E) : Propabiliteti(Evidenca)
    """
    
    dataBaza = None
    propabilitetiAtributitKlase = {}
    AtributiKlase = None
    """
    hipoteza : vektor{"Emri Atributit (1)" : "Vlera e atributit (1)" ... "Emri Atributit (n)" : "Vlera e atributit (n)"}
    """
    hipoteza = None
    propabilitetiAtributeve = {}
    
    def __init__(self, shteguDataBaze, AtributiKlase = None):
        """
        Parametrat e metodes:
        ---------------------
        shteguDataBaze : string
            Shtegu per filen CSV te bazes se te dhenave i cili permban te dhenat
            te cilat perdoren per trajnim te algoritmit
            
        AtributiKlase : string
            Percaktimi i Atributit Klase te bazes se te dhenave i cili do te perdoret
            e dhene e cila do te predikohet nga algoritmi
            
        Metoda eshte inicializuese per klasen naiveBayes.py,
        kjo eshte metoda fillestare e cila do te sherbej per 
        inicializimin e parametrave te klases dhe futjen e te dhenave ne algoritem
        """
        self.dataBaza = pd.read_csv(shteguDataBaze)
        self.AtributiKlase = AtributiKlase
        
    def kalkulo_propabilitetin_AtributitKlase(self):
        """
        Kthen vleren e probabilitetit te elementeve brenda Atributit Klase.
        Atributi klase duhet te jepet paraprakisht ne metoden inicializuese
        te klases naiveBayes.py
        
        Parametrat:
        -----------
        Metoda aktuale nuk merr parametra.
        """
        
        vlerat_klases = list(set(self.dataBaza[self.AtributiKlase]))
        
        lista_klases = list(self.dataBaza[self.AtributiKlase])
        
        for i in vlerat_klases:
            self.propabilitetiAtributitKlase[i] = round((lista_klases.count(i)/float(len(lista_klases))), 3)
        print("Vlerat e propabilitetit te atributit klase: \n", self.propabilitetiAtributitKlase, "\n")
        
    def gjej_propabilitetin_Atributeve(self, atributi, tipi_atributit, tipi_klases):
        """
        Ndan atributet e klases ne nje liste e cila ben te mundur logaritjen e 
        propabiliteteve individuale te atributeve brenda bazes se te dhenave
        
        Procesi kryhet ne forme automatike dhe metoda nuk ka nevoj te thirret
        apo inicializohet duke marre parasysh qe do te mbushet me te dhena ne
        metoden Kalkulo_propabilitetin_kushtezues()
        
        Parametrat:
        -----------
            atributi : string
                Atributet individuale te bazes se te dhenave
            tipi_atributit : string
                Te dhenat te cilat i perman atributi individual te cilat do te 
                ndahen ne baze te tipit
            tipi_klases : string
                Duke u bazuar ne tipin e atributit klase predikon klasen te ciles
                i perket atributi per te cilin po kalkulojme propabilitetin
        """
        listo_Atributet_Individuale = list(self.dataBaza[atributi])
        
        lista_klases = list(self.dataBaza[self.AtributiKlase])
        
        totaliAtributeve = 1
        
        for i in range(0, len(listo_Atributet_Individuale)):
            if lista_klases[i] == str(tipi_klases) and str(listo_Atributet_Individuale[i]) == str(tipi_atributit):
                totaliAtributeve += 1
        return round(totaliAtributeve/float(lista_klases.count(tipi_klases)), 3)
    
    def Kalkulo_propabilitetin_kushtezues(self, hipoteza):
        """
        Metoda per kalkulimin e propabilitetit te hipotezes me evidencat te cilat
        jane pjese e te dhenave te cilat i ka trajtuar algoritmi
        Kjo metod ben shumezimin e te gjitha propabiliteteve individuale te atributeve
        me propabilitetin e atributit klase. 
        Permes kesaj metode kryhet predikimi i algoritmit
        
        (Hipoteza|Evidenca) = P(Evidenca1|Hipoteza) x P(Evidenca2|Hipoteza) x ... x P(EvidenceN|Hipoteza) x P(Hipoteza)
        ndarë për P(Evidencat)
        
        Parametrat:
        -----------
            hipoteza : vektor{"Emri Atributit (1)" : "Vlera e atributit (1)" ... "Emri Atributit (n)" : "Vlera e atributit (n)"}
        """
        for i in self.propabilitetiAtributitKlase:
            self.propabilitetiAtributeve[i] = {}
            for j in hipoteza:
                self.propabilitetiAtributeve[i].update({ hipoteza[j]:self.gjej_propabilitetin_Atributeve(j, hipoteza[j], i) })                
        pprint.pprint(self.propabilitetiAtributeve)
        
    def klasifiko(self):
        """
        Metoda e cila kthen rezultatin e arritur nga algoritmi.
        Kjo metode kthen klasen ne te cilen takon predikimi te cilin e ben algoritmi
        duke kthyer nje vlere te llogaritur te propabilitetit
        
        print("\nRezultati: ")
        for i in self.propabilitetiAtributeve:
            print(i, " ==> ", 
                  "{0:.8f}".format(funct.reduce(lambda x, y: x*y, self.propabilitetiAtributeve[i].values())*self.propabilitetiAtributitKlase[i]))
        """   
        print("\nRezultati: ")
        
        for i in self.propabilitetiAtributeve:
            VektoriVlerave = list(self.propabilitetiAtributeve[i].values())
            VleratIndividuale = 0
            for j in VektoriVlerave:
                VleratIndividuale = VleratIndividuale + (j * self.propabilitetiAtributitKlase[i])*100
            print(i, "==>", round(VleratIndividuale, 4))