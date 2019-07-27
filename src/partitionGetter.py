import csv
import re
from numpy import empty
from numpy import zeros
import os
from nexus import NexusReader

def getMSA(fileName):
    with open(fileName, 'r') as file:
        formattedString = file.read().replace(" ", "").replace("\n", "").replace("\t", "")
        taxas = re.findall(r"TAXLABELS(.*?)\;", formattedString)
        taxas = re.findall(r"\[\d+\]'(.*?)'", taxas[0])

        taxaDict = {}

        #Get taxa into a dictionary  for[taxaName] = {a,t,c,t,c,a,d,a,t,c,c,d,a}
        for taxa in taxas:
            taxaDict[taxa] = ""
        
        
        regex = r"BEGINCharacters.*?MATRIX(.*?)[;]"
        characters = re.findall(regex, formattedString)
        characters = characters[0][1:] + "'"

        regex = r"(.*?)'(.+?)'"
        characters = re.findall(regex, characters)

        for match in characters:
            taxaDict[match[0]] = taxaDict[match[0]] + match[1]
            
            
    for value in taxaDict:
        numColumns = len(taxaDict[value])
        
    #Now we have all the bases in a dictionary. 

    #Make array of columns of the MSA
    i = 0
    species = len(taxaDict)
    msa = empty([numColumns,species],str)
    for value in taxaDict:
        j=0
        for base in taxaDict[value]:
            msa[j][i] = base
            j += 1
        i += 1

    i = 0
    for col in msa:
        j = 0
        for base in col:
            tmp = msa[i][j]
            b = tmp == "."
            if (msa[i][j] == "."):
                msa[i][j] = msa[i][0]
            j += 1
        i += 1

    return msa

def getSplits(nBlock):

    splitList = []

    for row in nBlock:
        r = r".*TAB  (.*),"
        row = row.replace("\t","TAB")
        split = re.findall(r, row)
        split = split[0].split(" ")
        splitList.append(split)

    i = 0
    for split in splitList:
        splitList[i] = list(map(int, split))
        i += 1
        

    return splitList

#Tells if there is a partition in a msa column
def isPartition(col):
    previousBase = None
    for base in col:
        if(base != previousBase and previousBase != None):
            return True
        previousBase = base

    return False


def getSets(col):
    setDict = {}
    i = 0
    for base in col:
        setDict.setdefault(base, None)
        if (setDict[base] is None):
            setDict[base] = [i]
        else:
            setDict[base].append(i)
        i += 1
    
    temp = []
    for ind in setDict:
        arr = setDict[ind]
        arr = map(lambda x: x+1, arr)
        temp.append(list(arr))
    return temp


def matchSplit(partition, splitList, numSpecies):
    scoreList = zeros([len(splitList)])
    i = 0

    for split in splitList:
        inverse = getSplitPartition(split, numSpecies)
        scoreList[i] = distance(inverse, partition, numSpecies)
        i += 1
        
    highest = 0
    for i, score in enumerate(scoreList):
        if (score > highest):
            highest = score
            pos = i+1

    return pos


def partSep(p,q,x,y):
    retDict = {}

    for part in p:
        if(part.count(x) > 0 and part.count(y) > 0):
            retDict['pTogether'] = True
            break
        else:
            retDict['pTogether'] = False
        
    for part in q:
        if(part.count(x) > 0 and part.count(y) > 0):
            retDict['qTogether'] = True
            break
        else:
            retDict['qTogether'] = False

    return retDict


def distance(p,q, numSpecies):
    s = r = u = v = 0

    for i in range(1,numSpecies+1):
        for j in range(1,numSpecies+1):
            if (i != j):
                a = partSep(p,q,i,j)

                if(a['pTogether'] and a['qTogether']):
                    s += 1
                if (not a['pTogether'] and not a['qTogether']):
                    r += 1
                if (not a['pTogether'] and a['qTogether']):
                    u += 1
                if ( a['pTogether'] and not a['qTogether']):
                    v += 1
    rand = (r+s)/(r+s+u+v)
    return rand


def getSplitPartition(split,numSpecies):
    inverse = []
    for i in range(1,numSpecies+1):
        if(i not in split):
            inverse.append(i)
    
    return [split,inverse]



def runPG(fileName):
    from os.path import dirname, join
    current_dir = dirname(__file__)
    file_path = join(current_dir, fileName)

    n = NexusReader('/Users/benlonghurst/Documents/GitHub/Split-Network-Interpreter/Nexus_Examples/beesProcessed.nex')

    msa = getMSA(file_path)
    splits = getSplits(n.splits.block[6:-2])

    colSplit = zeros([len(msa)],int)
    i = 0
    for col in msa:
        if (isPartition(col)):
            partition = getSets(col)
            colSplit[i] = matchSplit(partition, splits, n.taxa.ntaxa)
            print(colSplit[i])
        else:
            colSplit[i] = 0
            print("False")

        i += 1

    arr = {}
    arr["msa"] = msa # _/
    arr["colSplit"] = colSplit # _/
    arr["n"] = n
    arr["splits"] = splits

    return arr

# arr = runPG('beesProcessed.nex')
# x = 1