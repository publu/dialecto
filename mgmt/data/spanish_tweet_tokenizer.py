from nltk.tokenize import TweetTokenizer
from nltk import ngrams
import csv 
import os


def utf8encoder(text):
    try:
        text = unicode(text, 'utf-8')
    except TypeError:
        return text

def collect_tweets(filename):
    tweet_text = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            #print "Tweet in row: " + row[0]
            tweet_text.append(row[0])
    return tweet_text
            
def returnBigramModel(sentences):
    d = {}
    for sent in sentences:
        for i in sent:
            if i[0] in d:
                if i[1] in d[i[0]]:
                    d[i[0]][i[1]] += 1
                else:
                    d[i[0]][i[1]] = 1
            else:
                d[i[0]] = {}
                d[i[0]][i[1]] = 1
    for key in d.keys():
        total = sum(d[key].values())
        for skey in d[key].keys():
            d[key][skey] = float(d[key][skey])/total
    return d          
            
            
            
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

#Get all the filnemaes in the directory except for this file
filenames = os.listdir(os.getcwd())
filenames.remove('spanish_tweet_tokenizer.py')
#print filenames
tweets_list = []

#Store each individual tweet from across all files in a list
for name in filenames:
    tweets_list.extend(collect_tweets(name))
    
tweet_word_tokens = []
for tweet in tweets_list:
    #print "Printing tweet\n"
    #print tweet
    #print "Done tweet\n"
    tweet_word_tokens.append(tknzr.tokenize(tweet))

#for i in tweet_word_tokens:
#    print "Tweet tokens"
#    print i
tweet_bigram = returnBigramModel([list(ngrams(tweet, 2)) for tweet in tweet_word_tokens])

print "Finished making ngram"
print tweet_bigram
    
    
    
    