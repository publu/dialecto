from nltk.tokenize import TweetTokenizer
from nltk import ngrams
import csv 
import os

class tweet_classifier:
    
    def __init__(self):
        """
        The init function does the following functions:
            1. Creates an nltk tweet tokenizer object
            2. Retrieves all the filenames of the tweet CSV files present in this directory
            3. Stores every tweet from every CSV in a list called tweets_list
            4. Splits every tweet in tweet_list to it's individual tokens and stores tokens in a 2D list tweet_word_tokens[tweets][tweet_i_tokens]
            5. Creates a bigram model and stores it in a dictionary 2D dictionary
        """
        self.tweets_list = []
        self.tweet_word_tokens = [] 
        self.tweet_bigram = {}
        self.tweets_list_f = {}
        
        #Create the nltk tokenizer object
        self.tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
        
        #Get all the filnemaes in the directory except for this file
        self.filenames = os.listdir(os.getcwd())
        self.filenames.remove(os.path.basename(__file__))
        
        #Store each individual tweet in a list, and store each list in a dictionary with filenames as key
        print "Now collecting tweets..."
        for name in self.filenames:
            self.tweets_list_f[name] = []
            #self.tweets_list.extend(self.collect_tweets(name))
            self.tweets_list_f[name] = self.collect_tweets(name)
        print "Done collecting tweets."

        #print "Now collecting tweets..."
        #for name in self.filenames:
        #    self.tweets_list.extend(self.collect_tweets(name))
        #print "Done collecting tweets."
        
        #Tokenize each individual tweet into tokens and store it all in a 2D list, 
        #with each object in the list being a list of tweet tokens
        print "Now tokenizing tweets..."
        for name in self.filenames:
            for tweet in self.tweets_list_f[name]:
                self.tweet_word_tokens.append(self.tknzr.tokenize(tweet))
        print "Done tokenizing tweets."
        #print self.tweet_word_tokens[1][1]
        ##Tokenize each individual tweet into tokens 
        #print "Now tokenizing tweets..."
        #for name in self.filenames:
        #    for tweet in self.tweets_with_filenames[name]:
        #            self.tweet_word_tokens_with_filenames[name] = []
        #            self.tweet_word_tokens_with_filenames[name].append(self.tknzr.tokenize(tweet))
        #print "Done tokenizing tweets."
        
    
    def utf8encoder(self, text):
        """
        Convert the text to UTF-8
        """
        try:
            text = unicode(text, 'utf-8')
        except TypeError:
            return text
    
    def collect_tweets(self, filename):
        """
        Opens CSV given by filename and stores each tweet in a list
        """
        tweet_text = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                #print "Tweet in row: " + row[0]
                tweet_text.append(row[0])
        return tweet_text
                
    def bigramModel(self, tweetNgram):
        """
        Returns a bigram model as a dictionary
        
        Input format:
            tokens = ['el', 'carro', 'va']
            tweetNgram = nltk.ngrams(tokens)
            tweetNgram = [('el', 'carro'), ('carro', 'va')]
            
        Output format:
            d[tweet_token1][tweet_token_after_token1] = Probability of seeing these two tokens together
            Ex:
            d['el']['carro'] = 0.5
        """
        d = {}
        total = 0.0
        for t in tweetNgram:
            for i in t:
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
            
        for key in d.keys():
            for skey in d[key].keys():
                d[key][skey] = float(d[key][skey])/total
        return d       
        
    def createUnigramModel(self, tweet_token_list):
        """
        Returns a unigram model in a dictionary that holds the probability of a
        single token appearing in all of the tweets
        
        unigram[token] = p
        """
        unigram = {}
        total = 0.0
        #Count the number of times a single token appears in the entire body of text
        for tweet in tweet_token_list:
            for token in tweet:
                total += 1
                if token in unigram:
                    unigram[token] += 1
                else:
                    unigram[token] = 1
                    
        #Calculate the probability of a single token across the entire unigram
        #Divide the number of times we encountered a particular token by the total
        for token in unigram:
            unigram[token] = float(unigram[token]/total)
        return unigram
        
    def createBigramModel(self, tweet_token_list):
        """
        Create a bigram model with every single tweet token via list comprehension
        """
        bigram = self.bigramModel([list(ngrams(tweet, 2)) for tweet in self.tweet_word_tokens])
        print "Finished making bigram"
        print self.bigram
        return bigram


c = tweet_classifier()
u = c.createUnigramModel(c.tweet_word_tokens)
print sorted(u.items(), key=lambda x:x[1])
    
    