#Definimi i funksioneve te nevojshme
class SAT:
    formula = []
    zgjidhja = []
    satFile = []
    numriVariablave = 0
    def __init__(self,satFile):
        #Leximi i sat-file
        file = open(satFile,'r')
        self.satFile = file.read()
        self.satFile = self.satFile.split('\n')
        
        #Gjetja e numrit te variablave
        temp = self.satFile[7].split(' ')
        numriVariablave = temp[2]
        numriVariablave =int(numriVariablave)

        #Gjetja e formules
        for rresht in self.satFile:    
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
                self.formula.append(list)
        
        #Mbushja e zgjidhjes me vlera -1
        for i in range(numriVariablave):
            self.zgjidhja.append(-1)
        
        #Gjenerimi i zgjidhjes
        if(self.gjeneroZgjidhje()):
            print("Zgjidhja u caktua : ",self.zgjidhja)
        else:
            print("Zgjidhja nuk mund te caktohet")
    
    #Funksioni kontrollo, roli i te cilit eshte me shiku nese variablat e zgjidhjes kane ndonje vlere -1
    #Nese ka vlere -1 dmth ende nuk eshte caktuar zgjidhja
    def kontrollo(self,x):
        for i in range(len(x)):
            if x[i]==-1:
                return True
        return False
    
    #Funskioni Kontrollo i cili kontrollon nese zgjidhja e gjeneruar e kenaq ekuacionin
    def kontrolloZgjidhjen(self):
        for i in range(len(self.formula)):
            tempArray = self.returnArray(len(self.formula[i]))
            for j in range(len(self.formula[i])):
                tempArray[j] = self.tempFunction(self.formula[i][j][0],self.formula[i][j][1],self.zgjidhja)
            if(self.kontrolloArray(tempArray) == 0):
                return False
        return True

    #Nje funksion temp i cili ndihmon ne kthimin nga 0 ne 1 
    def tempFunction(self,x,y,z):
        if(y==1):
            return z[x-1]
        else:
            if(z[x-1]==0):
                return 1
            else:
                return 0

    #Funskion i cili krijon nje array me numer te caktuar te variablave
    def returnArray(self,nrAnetareve):
        array = []
        for i in range(nrAnetareve):
            array.append(-1)
        return array

    #Funksioni i cili e kryen OR logjik ne mes te variablave ne nje array
    def kontrolloArray(self,array):
        temp = array[0]
        for i in range(1,len(array),1):
            temp = temp or array[i]
        return temp
    
    #Funksioni i cili gjeneron zgjidhje
    def gjeneroZgjidhje(self,n=0,M=2):
        if(n==len(self.zgjidhja)):
            return True
        for i in range(M):
            self.zgjidhja[n]=i
            if(self.kontrollo(self.zgjidhja)):
                if(self.gjeneroZgjidhje(n+1,M)):
                    return True
            else:
                if(self.kontrolloZgjidhjen()):
                    return True
                else:
                    self.zgjidhja[n]=-1
        else:
            return False

#Gjetja e zgjidhjes per nje file te caktuar
fileName = 'uf20-01.cnf'
objSat = SAT(fileName)    
