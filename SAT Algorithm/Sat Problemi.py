#Definimi i funksioneve te nevojshme        
def kontrollo(x):
    for i in range(len(x)):
        if x[i]==-1:
            return True
    return False

def kontrolloZgjidhjen(zgjidhja,formula):
    for i in range(len(formula)):
        tempArray = returnArray(len(formula[i]))
        for j in range(len(formula[i])):
            tempArray[j] = tempFunction(formula[i][j][0],formula[i][j][1],zgjidhja)
        if(kontrolloArray(tempArray) == 0):
            return False
    return True
                                
def tempFunction(x,y,zgjidhja):
    if(y==1):
        return zgjidhja[x-1]
    else:
        if(zgjidhja[x-1]==0):
            return 1
        else:
            return 0
        
def returnArray(nrAnetareve):
    array = []
    for i in range(nrAnetareve):
        array.append(-1)
    return array

def kontrolloArray(array):
    temp = array[0]
    for i in range(1,len(array),1):
        temp = temp or array[i]
    return temp

def gjeneroZgjidhje(zgjidhja,n=0,M=2):
    if(n==len(zgjidhja)):
        return True
    for i in range(M):
        zgjidhja[n]=i
        if(kontrollo(zgjidhja)):
            if(gjeneroZgjidhje(zgjidhja,n+1,M)):
                return True
        else:
            if(kontrolloZgjidhjen(zgjidhja,formula)):
                return True
            else:
                zgjidhja[n]=-1
            
    else:
        return False
import numpy as np

#Leximi i SAT fajll-it
file = open('uf20-0100.cnf','r')
data = file.read()
data = data.split('\n')

#Gjetja e numrit te variablave
temp = data[7].split(' ')
numriVariablave = temp[2]
numriVariablave =int(numriVariablave)

formula = []
for rresht in data:    
    rreshti=rresht.strip()
    list = []
    ## Nje rresht duhet te filloj me numer ose me shenje negative (-)
    if rreshti[0] == '%':
        break
    if (rreshti[0].isdigit()) or (rreshti[0].startswith("-")):
        anetaretRreshtit = rreshti.split()
        for numer in anetaretRreshtit:
            try:
                numer_int = int(numer)
                if numer_int < 0:
                    list.append( (abs(numer_int), 0) )
                elif numer_int > 0:         ## Eliminimi i zerove ne fund
                    list.append( (numer_int, 1) )
            except:
                print("Gabim gjate konvertimit", rreshti)
        formula.append(list)

zgjidhja = []
for i in range(numriVariablave):
    zgjidhja.append(-1)
    
if(gjeneroZgjidhje(zgjidhja)):
    print("Zgjidhja u caktua : ",zgjidhja)
else:
    print("Zgjidhja nuk mund te caktohet")


    