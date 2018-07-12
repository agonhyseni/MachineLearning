import csv
import random
from collections import Counter
import time
import matplotlib.pyplot as plt

nrOfFirstColumn = 2
nrOfLastColumn = 8
iterations = 5
minSize = 500
maxDepth = 4
nFeatures = 3

class Node:    
    def __init__(self, left, right, splitIndex, splitValue):
        self.left = left
        self.right = right
        self.splitValue = splitValue
        self.splitIndex = splitIndex               
        
class Tree:
    def __init__(self):
        self.root = None
        
    def processDataset(self, filename):        
        fileToOpen = open(filename, "r")
        self.dataset = list(csv.reader(fileToOpen))         
        self.dataset = [x[nrOfFirstColumn:nrOfLastColumn] for x in self.dataset[1:-1]]          
       
        for row in range(len(self.dataset)):
            for column in range(len(self.dataset[0]) - 1):
                self.dataset[row][column] = float(self.dataset[row][column].strip())
            self.dataset[row][column + 1] = int(self.dataset[row][column + 1].strip())   
            
    def getSplit(self, splitIndex, splitValue, data):       
        left = []
        right = []
        
        for row in data:
            if row[splitIndex] < splitValue:
                left.append(row)
            else:
                right.append(row)
        
        return left, right
    
    def evaluateGini(self, left, right):        
        classes = list(set([row[-1] for row in self.dataset]))
        
        scoreLeft = scoreRight = 0
        sizeLeft, sizeRight = float(len(left)), float(len(right))      

        for classVal in classes:
            if sizeLeft > 0:
                proportionLeft = [row[-1] for row in left].count(classVal) / sizeLeft
                scoreLeft += proportionLeft ** 2
            
            if sizeRight > 0:
                proportionRight = [row[-1] for row in right].count(classVal) / sizeRight           
                scoreRight += proportionRight ** 2              
        
        return (1.0 - scoreLeft) * (sizeLeft / (sizeLeft + sizeRight)) + (1.0 - scoreRight) * (sizeRight / (sizeLeft + sizeRight))
   
    def getBestSplit(self, data, nFeatures = None):
        if nFeatures is None:
            features = range(len(data[0]) - 1)                
        else:
            possibleFeatures = list(range(len(data[0]) - 1))
            random.shuffle(possibleFeatures)            
            features = possibleFeatures[0:nFeatures]    
        
        bestLeft = bestRight = None
        bestGini, bestSplitIndex, bestSplitValue = 100, -1, -1  
      
        for index in features:
            for row in data:               
                left, right = self.getSplit(index, row[index], data)               
                gini = self.evaluateGini(left, right)           
                
                if  gini < bestGini:
                    bestGini = gini
                    bestSplitIndex = index
                    bestSplitValue = row[index]
                    bestLeft = left
                    bestRight = right 
        
        return Node(bestLeft, bestRight, bestSplitIndex, bestSplitValue)
    
    def terminal(self, group):
        outcomes = [row[-1] for row in group]
    
        return max(set(outcomes), key = outcomes.count)
    
    def splitNode(self, node, minSize, maxDepth, nFeatures = None):        
        left, right = node.left, node.right      
        
        if not left or not right:
            node.left = node.right = self.terminal(node.left + node.right)
            return
        
        if maxDepth <= 0:
            node.left = self.terminal(node.left)
            node.right = self.terminal(node.right)
            return
        
        if len(left) <= minSize:
            node.left = self.terminal(left)
        else:
            node.left = self.getBestSplit(left, nFeatures)
            self.splitNode(node.left, minSize, maxDepth - 1, nFeatures)
            
        if len(right) <= minSize:
            node.right = self.terminal(right)
        else:
            node.right = self.getBestSplit(right, nFeatures)
            self.splitNode(node.right, minSize, maxDepth - 1, nFeatures)

    def growTree(self, minSize, maxDepth, nFeatures = None):        
        self.root = self.getBestSplit(self.dataset, nFeatures)
        self.splitNode(self.root, minSize, maxDepth - 1, nFeatures)
        
    def predict(self, row, node = None):
        if node is None:
            node = self.root
            
        if row[node.splitIndex] < node.splitValue:
            if isinstance(node.left, Node):
                return self.predict(row, node.left)
            else:
                return node.left
        else:
            if isinstance(node.right, Node):
                return self.predict(row, node.right)
            else:
                return node.right        
            
class RandomForest:
    def __init__(self, filename, minSize, maxDepth, numTrees):
        self.filename = filename
        self.minSize = minSize
        self.maxDepth = maxDepth
        self.numTrees = numTrees
    
    def growForest(self):
        self.forest = []                   
        
        for i in range(self.numTrees):
            t0 = time.time()
            tree = Tree()
            tree.processDataset(self.filename)
            tree.growTree(self.minSize, self.maxDepth, nFeatures)
            self.forest.append(tree)
            t1 = time.time()
            print(str(i) + ": " + str(t1 - t0))
        print(" ")
    
    def predict(self, row):
        predictions = []
        
        for tree in self.forest:
            predictions.append(tree.predict(row))
                    
        data = Counter(predictions)
        return data.most_common(1)[0][0] 

def testForest(numTrees, minSize, maxDepth):
    forest = RandomForest("trainA.txt", minSize, maxDepth, numTrees)
    forest.growForest()
    
    testFileToOpen = open("testA.txt", "r") 
    testSet = list(csv.reader(testFileToOpen))        
    testSet = [x[nrOfFirstColumn:nrOfLastColumn] for x in testSet[1:-1]]    
       
    for row in range(len(testSet)):
        for column in range(len(testSet[0]) - 1):
            testSet[row][column] = float(testSet[row][column].strip())
        testSet[row][column + 1] = int(testSet[row][column + 1].strip())
        
    numRight = 0
    
    for row in testSet:
        if forest.predict(row) == row[-1]:
            numRight += 1   
    print(str(numRight) + "/" +str(len(testSet)))
    return (float(numRight) * 100)/float(len(testSet))      
            

print("Min size: " + str(minSize))
print("Max depth: " + str(maxDepth))
averages = [0, 0, 0, 0]
averagesFinal = [0, 0, 0, 0]
averageTimes = [0, 0, 0, 0]
averageTimesFinal = [0, 0, 0, 0]
for i in range(iterations):   
    print("*********************************************************")
    print("Iteration: " + str(i))
    print("_________________________________________________________")            
    for i, numTrees in enumerate((1, 5, 10, 50), start = 0):
        t0 = time.time()    
        print(" ")
        percentage = testForest(numTrees, minSize, maxDepth)
        print(str(numTrees) + " trees percentage: " + str(percentage) + "%")
        averages[i] += percentage
        t1 = time.time()
        averageTimes[i] += (t1 - t0)
        print(str(numTrees) + " trees: Total time" + ": " + str(t1 - t0))
        print("_________________________________________________________")
              
print("Average percentages: ")
for i, numTrees in enumerate((1, 5, 10, 50), start = 0):
    print(str(numTrees) + " trees: " + str(round(averages[i]/float(iterations),3)) + "%" )
    print("Average time: " + str(round(averageTimes[i]/float(iterations),3)) + " seconds")
    averagesFinal[i] = round(averages[i]/float(iterations),3)
    averageTimesFinal[i] = round(averageTimes[i]/float(iterations),3)
     
print("\nDiagram shows the accuracy:")    
plt.plot([1,5,10,50], averagesFinal)
plt.ylabel('Percentage')
plt.xlabel('Nr. of trees')
plt.axis([0, 50, min(averagesFinal)-10, 100])
plt.show()

print("\nDiagram shows the time:")   
plt.plot([1,5,10,50], averageTimesFinal)
plt.ylabel('Nr. of Seconds')
plt.xlabel('Nr. of trees')
plt.axis([0, 55, 0, (max(averageTimesFinal)+5)])
plt.show()
    

