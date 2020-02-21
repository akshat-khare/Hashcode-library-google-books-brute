#!/usr/bin/env python
# coding: utf-8

# In[12]:


import itertools
import pprint
import sys
# filename = "a_example.txt"
filename = sys.argv[1]
f = open(filename)
tempstr = f.readline()
temparr = map(int,tempstr.split(" "))

numBooks = temparr[0]
numLib = temparr[1]
numDays = temparr[2]

tempstr = f.readline()
scoreArr = map(int,tempstr.split(" "))

numBooksInLib = []
numDaysToSignUp = []
shippingCapacity = []
booksAvailible = []

for i in range(numLib):
    tempstr = f.readline()
    temparr = map(int,tempstr.split(" "))
    temp = temparr[0]
    numBooksInLib.append(temparr[0])
    numDaysToSignUp.append(temparr[1])
    shippingCapacity.append(temparr[2])
    tempstr = f.readline()
    temparr = map(int,tempstr.split(" "))
    booksAvailibleTemp = []
    for j in range(temp):
        booksAvailibleTemp.append(temparr[j])
    booksAvailible.append(booksAvailibleTemp)


# In[13]:


def scoreSet(coveredset):
    temp = 0
    for i in coveredset:
        temp += scoreArr[i]
    return temp


# In[17]:


def writeBestAnswer(bestAnswer):
    tempstr = ""
    permut = bestAnswer[0]
    coveredset = bestAnswer[1]
    coveredsetdic = bestAnswer[2]
    tempstr += str(len(coveredsetdic)) + "\n"
    for i in permut:
        tempstr += str(i) + " " + str(len(coveredsetdic[i])) + "\n"
        tempstr += " ".join( map(str,list(coveredsetdic[i]))  ) + "\n"
    
    f = open(filename+"out","w")
    f.write(tempstr)
    f.close()


# In[19]:


def solveSubProblem(permut,problem, coveredset, coveredsetdic):
    global bestAnswer
    global bestScore
    if (len(problem)==0):
        thisscore = scoreSet(coveredset)
        if(thisscore>bestScore):
#             print("change")
            realpermut = []
            for i in permut:
                if i in coveredsetdic:
                    realpermut.append(i)
            bestAnswer = (realpermut,coveredset, coveredsetdic, scoreSet(coveredset))
            bestScore = thisscore
            print(bestScore)
            writeBestAnswer(bestAnswer)
    else:
        thislib = problem[0][0]
        thislibCapacity = problem[0][1]
        thislibbooks = set(booksAvailible[thislib])
#         print(problem, thislibbooks, coveredset)
        thislibbooks = thislibbooks - coveredset
        if(len(thislibbooks)<=thislibCapacity):
            tempcoveredsetdic = coveredsetdic.copy()
            tempcoveredsetdic[thislib] = thislibbooks
            tempcoveredset = coveredset | thislibbooks
            solveSubProblem(permut,problem[1:], tempcoveredset, tempcoveredsetdic)
#             return 
        else:
            for selectionsCombinations in list(itertools.combinations(thislibbooks, thislibCapacity)):
                selectionsCombinations = set(selectionsCombinations)
                tempcoveredsetdic = coveredsetdic.copy()
                tempcoveredsetdic[thislib] = selectionsCombinations
                tempcoveredset = coveredset | selectionsCombinations
                solveSubProblem(permut,problem[1:], tempcoveredset, tempcoveredsetdic)
#             return


# In[ ]:


bestScore = 0
bestAnswer = None
for libraryPermutation in list(itertools.permutations(range(numLib))):
    newCapacities = [0 for i in range(numLib)]
    tempNumDays = numDays
    for tempiter in range(numLib):
        thislib = libraryPermutation[tempiter]
        thislibSignUpTime = numDaysToSignUp[thislib]
        if(thislibSignUpTime>tempNumDays):
            continue
        else:
            tempNumDays -= thislibSignUpTime
            numBooksThisLib = numBooksInLib[thislib]
            shippingCapacityThisLib = shippingCapacity[thislib]
            tempCapacity = min(shippingCapacityThisLib * (tempNumDays/shippingCapacityThisLib), numBooksThisLib)
            newCapacities[thislib] = tempCapacity
            
            
    problem = []
    for tempiter in list(libraryPermutation):
        if(newCapacities[tempiter]==0):
            continue
        else:
            problem.append((tempiter, newCapacities[tempiter]))
    solveSubProblem(libraryPermutation,problem, set({}), dict({}))
print(bestAnswer)

