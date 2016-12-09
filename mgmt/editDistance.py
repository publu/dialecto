import csv
from nltk.tokenize import word_tokenize
import re
from time import sleep
from decimal import *

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

def mainFunction (numOfLoops, countryOne, countryTwo, unwantedTweets):

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
                        
                        if tempT not in unwantedTweets:
                            unwantedTweets.append(tempT)
                        if currentT not in unwantedTweets:
                            unwantedTweets.append(currentT)

def makeNewFiles(country, unwantedTweets, master, masterT):
    for i in range(len(country)):
        tweets = []
        file_name = 'data/' + country[i] + '_tweets.csv'
        new_file_name = 'editDistanceData/' + country[i] + '_tweets.csv'

        #importing all the tweets for acocunt
        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                teststring = unicode(row[0], 'utf-8')
                if teststring not in unwantedTweets:
                    tweets.append([row[0],row[1]])
                    if (row[0] == "text" or row[0] == " " or row[0] == ""):
                        continue
                
                    #if(len(master) != 0):
                    #       print(Decimal(len(masterT))/Decimal(len(master)))
                
                    if (len(master) == 0 or Decimal(len(masterT))/Decimal(len(master)) > .2):
                        master.append([row[0],row[1]])
                    else:
                        masterT.append([row[0],row[1]])
                        #TEMPORARY CODE UNTIL WE GET REAL DATA
                        #tweets.append([row[0], teststring, row[2]])
        
        #making new file
        with open(new_file_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(tweets)



if __name__ == '__main__':
    master_name = 'editDistanceData/' + 'MASTER_tweets.csv'
    master_t_name = 'editDistanceData/' + 'MASTER20_tweets.csv'
    master = []
    masterT = []
    unwantedTweets = []
    
    chile 	=	["latercera", "Emol", "TVN", "CNNChile", "Cooperativa"]
    arg		=	["eltreceoficial", "LANACION", "clarincom", "24conurbano", "populardiario"]
    col 	=	["NoticiasRCN", "ELTIEMPO", "elespectador", "elpaiscali"]
    mex		=	["CNNMex", "NTelevisa_com", "lopezdoriga", "EPN"]
    spain	=	["abc_es", "informacion_es", "elperiodico", "_rebelion_org", "Overwatch_Esp", "radiocable"]
    usa 	=	["ElNuevoDia", "primerahora", "LaOpinionLA", "elnuevoherald", "vivelohoy", "despiertamerica"]

    #CHILE - SELF
    mainFunction(4, chile, chile, unwantedTweets)
    
    #ARGENTINA - SELF
    mainFunction(4, arg, arg, unwantedTweets)
    
    #COLUMBIA - SELF
    mainFunction(3, col, col, unwantedTweets)
    
    #MEXICO - SELF
    mainFunction(3, mex, mex, unwantedTweets)
    
    #SPAIN - SELF
    mainFunction(5, spain, spain, unwantedTweets)
    
    #USA - SELF
    mainFunction(5, usa, usa, unwantedTweets)
    
    #CHILE - ARGENTINA
    mainFunction(4, chile, arg, unwantedTweets)
    
    #CHILE - COLUMBIA
    mainFunction(4, col, chile, unwantedTweets)
    
    #CHILE - MEXICO
    mainFunction(4, mex, chile, unwantedTweets)
    
    #CHILE - SPAIN
    mainFunction(5, chile, spain, unwantedTweets)
    
    #CHILE - USA
    mainFunction(5, chile, usa, unwantedTweets)
    
    #ARGENTINA - COLUMBIA
    mainFunction(4, col, arg, unwantedTweets)
    
    #ARGENTINA - MEXICO
    mainFunction(4, mex, arg, unwantedTweets)
    
    #ARGENTINA - SPAIN
    mainFunction(5, arg, spain, unwantedTweets)
    
    #ARGENTINA - USA
    mainFunction(5, arg, usa, unwantedTweets)
    
    #COLUMBIA - MEXICO
    mainFunction(3, col, mex, unwantedTweets)
    
    #COLUMBIA - SPAIN
    mainFunction(4, col, spain, unwantedTweets)
    
    #COLUMBIA - USA
    mainFunction(4, col, usa, unwantedTweets)
    
    #MEXICO - SPAIN
    mainFunction(4, mex, spain, unwantedTweets)
    
    #MEXICO - USA
    mainFunction(4, mex, usa, unwantedTweets)
    
    #SPAIN - USA
    mainFunction(5, usa, spain, unwantedTweets)

    
    
    print (unwantedTweets)

    #remake files
    #CHILE
    makeNewFiles(chile, unwantedTweets, master, masterT)
    #ARGENTINA
    makeNewFiles(arg, unwantedTweets, master, masterT)
    #COLUMBIA
    makeNewFiles(col, unwantedTweets, master, masterT)
    #MEXICO
    makeNewFiles(mex, unwantedTweets, master, masterT)
    #SPAIN
    makeNewFiles(spain, unwantedTweets, master, masterT)
    #USA
    makeNewFiles(usa, unwantedTweets, master, masterT)

    #making new file
    with open(master_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(master)
    #making new file
    with open(master_t_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(masterT)

