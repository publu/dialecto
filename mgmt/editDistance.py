import csv
from nltk.tokenize import word_tokenize
import re
from time import sleep

def levenshtein(sentOne, sentTwo):
    #variables used to calculate edit distance
    left = 0
    right = 0
    middle = 0
    
    editMatrix = []
    
    #add virtical arrays for the second word and add numbers
    for num in range(0, len(sentTwo)):
        editMatrix.append([])
        editMatrix[num].append(num)
    #add numbers for the first sentences
    for num in range(1, len(sentOne)):
        editMatrix[0].append(num)

    #2D matrix is made
    #print(editMatrix)

    #incriment the row
    for row in range(1, len(sentTwo)):
        #incriment the col
        for col in range(1, len(sentOne)):
            #find left
            left = editMatrix[row][col- 1] + 1
            #find right
            right = editMatrix[row - 1][col] + 1
            #find middle
            if (sentOne[col] == sentTwo[row]):
                #print("MATCH========")
                #print(sentOne[col])
                #print(sentTwo[row])
                middle = editMatrix[row - 1][col - 1]
            else:
                middle = editMatrix[row - 1][col - 1] + 2

            editMatrix[row].append(min(left, right, middle))

    #print (editMatrix)

    return editMatrix[len(sentTwo) - 1][len(sentOne) - 1]

def mainFunction (numOfLoops, countryOne, countryTwo):

    editDistance = 5
    
    #emoji code
    try:
        #Wide UCS-4 build
        emoji_pattern = re.compile(u'['
                                   u'\U0001F300-\U0001F64F'
                                   u'\U0001F680-\U0001F6FF'
                                   u'\u2600-\u26FF\u2700-\u27BF]+',
                                   re.UNICODE)
    except re.error:
        #Narrow UCS-2 build
        emoji_pattern = re.compile(u'('
                                   u'\ud83c[\udf00-\udfff]|'
                                   u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                                   u'[\u2600-\u26FF\u2700-\u27BF]|'
                                   u'\ud83d[\u25A0-\u25FF])+',
                                   re.UNICODE)
    
    
    
    for i in range(numOfLoops):
        tweetsOne = []
        tweetsTwo = []
        
        fileOne = 'data/' + countryOne[i] + '_tweets' + '.csv'
        fileTwo = 'data/' + countryTwo[i+1] + '_tweets' + '.csv'
        
        #debugging purposes
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(fileOne + " " + fileTwo)
        print(i)
        
        
        #importing all the tweets for acocunt 1
        with open(fileOne, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #ignore the first line
                if (row[0] == "text" or row[0] == " " or row[0] == ""):
                    continue
                teststring = unicode(row[0], 'utf-8')
                teststring = emoji_pattern.sub(r'', teststring)
                
                row[0] = teststring
                tweetsOne.append(row[0])
    
        #importing all the tweets for acocunt 2
        with open(fileTwo, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #ignore the first line
                if (row[0] == "text" or row[0] == " " or row[0] == ""):
                    continue
                teststring = unicode(row[0], 'utf-8')
                teststring = emoji_pattern.sub(r'', teststring)
                
                row[0] = teststring
                tweetsTwo.append(row[0])

        currentT = ""
        tempT = ""
        
        currentTWords = []
        tempTWords = []
        
        #beginning of edit distance
        for i in range(0, len(tweetsOne) -1):
            #words are now stored in here
            currentT = tweetsOne[i]
            currentTWords = currentT.split()
            
            #tweet comparing
            for j in range(0, len(tweetsTwo) -1):
                if i == j:
                    continue
                else:
                    tempT = tweetsTwo[j]
                    tempTWords = tempT.split()
                    
                    #at this point we have both words and both sets of words, now we find the edit distance
                    distance = levenshtein(currentTWords, tempTWords)
                    
                    if distance <= editDistance:
                        print ("done")
                        print("--------------------------------------")
                        print("Current")
                        print(currentTWords)
                        print("------------------")
                        print("Comparing")
                        print(tempTWords)
                        print("--------------------------------------")
                        print("++++++++++++++++++++++++++++++++++++++++++")
                        print(distance)
                        print("++++++++++++++++++++++++++++++++++++++++++")





if __name__ == '__main__':
    chile 	=	["latercera", "Emol", "TVN", "CNNChile", "Cooperativa"]
    arg		=	["eltreceoficial", "LANACION", "clarincom", "24conurbano", "populardiario"]
    col 	=	["NoticiasRCN", "ELTIEMPO", "elespectador", "elpaiscali"]
    mex		=	["CNNMex", "NTelevisa_com", "lopezdoriga", "EPN"]
    spain	=	["abc_es", "informacion_es", "elperiodico", "_rebelion_org", "Overwatch_Esp", "radiocable"]
    usa 	=	["ElNuevoDia", "primerahora", "LaOpinionLA", "elnuevoherald", "vivelohoy", "despiertamerica"]

    #CHILE - SELF
    mainFunction(4, chile, chile)

    #ARGENTINA - SELF
    mainFunction(4, arg, arg)

    #COLUMBIA - SELF
    mainFunction(3, col, col)

    #MEXICO - SELF
    mainFunction(3, mex, mex)

    #SPAIN - SELF
    mainFunction(5, spain, spain)

    #USA - SELF
    mainFunction(5, usa, usa)

    #CHILE - ARGENTINA
    mainFunction(4, chile, arg)

    #CHILE - COLUMBIA
    mainFunction(4, col, chile)

    #CHILE - MEXICO
    mainFunction(4, mex, chile)

    #CHILE - SPAIN
    mainFunction(5, chile, spain)

    #CHILE - USA
    mainFunction(5, chile, usa)

    #ARGENTINA - COLUMBIA
    mainFunction(4, col, arg)

    #ARGENTINA - MEXICO
    mainFunction(4, mex, arg)

    #ARGENTINA - SPAIN
    mainFunction(5, arg, spain)

    #ARGENTINA - USA
    mainFunction(5, arg, usa)

    #COLUMBIA - MEXICO
    mainFunction(3, col, mex)

    #COLUMBIA - SPAIN
    mainFunction(4, col, spain)

    #COLUMBIA - USA
    mainFunction(4, col, usa)

    #MEXICO - SPAIN
    mainFunction(4, mex, spain)

    #MEXICO - USA
    mainFunction(4, mex, usa)

    #SPAIN - USA
    mainFunction(5, usa, spain)



