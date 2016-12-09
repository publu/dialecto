from nltk.tokenize import TweetTokenizer
from nltk import ngrams
import csv 
import os
import pickle
import random
from itertools import islice

class tweet_classifier:
    
    def __init__(self):
        """
        The init function does the following functions:
            1. Creates an nltk tweet tokenizer object
            2. Retrieves all the filenames of the tweet CSV files present in this directory
            3. Stores every tweet from every CSV in a list called tweets_list
            4. Splits every tweet in tweet_list to it's individual tokens and stores tokens in a 2D list tweet_word_tokens[tweets][tweet_i_tokens]
            5. Creates a unigram model and stores it in a dictionary 2D dictionary
        """
        self.tweets_list = []
        self.tweet_word_tokens = [] 
        self.tweet_bigram = {}
        self.tweets_list_f = {}
        self.test_tweets = {}
        self.unigram = {}
        self.filename_countries = {}
        
        #Create the nltk tokenizer object
        self.tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
        
        #Get all the filenames in the directory except for this file
        self.filenames = os.listdir(os.getcwd())
        self.filenames.remove(os.path.basename(__file__))
        if 'unigram.pkl' in self.filenames:
            self.filenames.remove('unigram.pkl')
        self.filenames.remove('results')
        
        #Store each individual tweet in a list, and store each list in a dictionary with filenames as key
        print "Now collecting tweets..."
        l = len(self.filenames)
        i = 0.0
        total_tweets = 0.0
        for name in self.filenames:
            #make a new entry in the dictionary for this filename
            self.tweets_list_f[name] = []
            #self.tweets_list.extend(self.collect_tweets(name))
            self.tweets_list_f[name] = self.collect_tweets(name)
            total_tweets += len(self.tweets_list_f[name])
            i += 1
            p = round((float(i)/l * 100), 1)
            print "Percent complete: " + str(p)
        print "Done collecting tweets."
        print str(total_tweets) + "tweets collected\n"
        
        #Tokenize each individual tweet into tokens and store it all in a 2D list, 
        #with each object in the list being a list of tweet tokens
        j = 0.0
        print "Now tokenizing tweets..."
        for name in self.filenames:
            for tweet in self.tweets_list_f[name]:
                self.tweet_word_tokens.append(self.tknzr.tokenize(tweet))
            j += 1
            p = round((float(j)/l * 100), 1)
            print "Percent complete: " + str(p)
        print "Done tokenizing tweets.\n"
        
    
    def utf8encoder(self, text):
        """
        Convert the text to UTF-8
        """
        try:
            text = unicode(text, 'utf-8')
        except TypeError:
            return text
            
    def take(self, n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, n))
        
    def collect_tweets(self, filename):
        """
        Opens CSV given by filename and stores each tweet in a list
        """
        tweet_text = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            reader.next()
            for row in reader:
                #print "Tweet in row: " + row[0]
                tweet_text.append(row[1])
                self.filename_countries[filename] = row[2]
        return tweet_text
        
    def tweet_tokens_by_country(self):
        tweet_tokens_by_country = []
        tokens_by_country = {}
        #Initialize the dictionary of countries so that each country has a list already
        for country in self.filename_countries.values():
            tokens_by_country[country] = []
            
        for name in self.filenames:
            tweet_tokens_by_country = []
            #For every tweet in that filename
            for tweet in self.tweets_list_f[name]:
                #tokenize it and add it to the list
                tweet_tokens_by_country.append(self.tknzr.tokenize(tweet))
            #Extend the list of tokens for that country with the tokens that we collected for this file
            tokens_by_country[self.filename_countries[name]].extend(tweet_tokens_by_country)
        return tokens_by_country
        
    def five_most_uncommon(self):
        tokens_by_country = self.tweet_tokens_by_country()
        #Create a unigram for each country
        for country in tokens_by_country:
            unigram = self.createUnigramModel(tokens_by_country[country])
            n_items = self.take(5, unigram.iteritems())
            for i in n_items:
                print "Country: " + country + ", " + str(i)
            
        
        
    def createUnigramModel(self, tweet_token_list):
        """
        Returns a unigram model in a dictionary that holds the probability of a
        single token appearing in all of the tweets
        
        unigram[token] = p
        """
        unigram = {}
        total = 0.0
        #Count the number of times a single token appears in the entire body of text
        print "Now building unigram"
        for tweet in tweet_token_list:
            for token in tweet:
                total += 1
                if token in unigram:
                    unigram[token] += 1
                else:
                    unigram[token] = 1
        print "33% completed..."  
        #Calculate the probability of a single token across the entire unigram
        #Divide the number of times we encountered a particular token by the total
        
        for token in unigram:
            #obtain the rough percentage of each token in the entire body of text
            unigram[token] = float(unigram[token]/total)
            #normalize it
        print "66% completed..." 
        maxVal = max(unigram.values())
        print maxVal
        minVal = min(unigram.values())
        print minVal
        for token in unigram:
            unigram[token] = float((unigram[token] - minVal)/(maxVal - minVal))
        print "100% completed\n" 
        print "Now sorting unigram in ascending order..."
        unigram = sorted(unigram.items(), key=lambda x:x[1])
        print "Done"
        self.unigram = unigram
        return unigram
    
    def run_filter(self):
        l = len(self.filenames)
        i = 0.0
        deleted = 0
        #For every tweet account 
        print "Now running filter..."
        for name in self.filenames:
            #For every tweet in that account
            for tweet in self.tweets_list_f[name]:
                #If it is flagged
                if self.filter_tweet(tweet):
                    deleted += 1
                    self.tweets_list_f[name].remove(tweet)
            i += 1
            p = round((float(i)/l * 100), 1)
            print "Percent complete: " + str(p)
        print "Filtering complete"
        print str(deleted) + " tweets filtered\n"
        
    def merge_tweets(self):
        all_tweets = []
        for key in self.tweets_list_f.keys():
            all_tweets.extend(self.tweets_list_f[key])
        return all_tweets
        
    def createBigramModel(self, tweet_token_list):
        """
        Create a bigram model with every single tweet token via list comprehension
        """
        bigram = self.bigramModel([list(ngrams(tweet, 2)) for tweet in self.tweet_word_tokens])
        print "Finished making bigram"
        print self.bigram
        return bigram
    
    def split_train_test(self):
        """
        Splits the tweets into 80% training and testing data
        """
        self.test_tweets = {}
        for name in self.filenames:
            #For 20% of the data in this account
            self.test_tweets[name] = []
            for i in range(int(len(self.tweets_list_f[name])*.2)):
                #Choose a random tweet from the list of tweets in that account
                tweet = random.choice(self.tweets_list_f[name])
                #Add it to the list of test tweets2
                self.test_tweets[name].append(tweet)
                #delete the tweet from the training list
                self.tweets_list_f[name].remove(tweet)
                
    def filter_tweet(self, tweet):
        """
        Returns true if a tweet has a token probability product greater than the acceptable treshold
        """
        total_token_probability = 1.0
        for token in tweet:
            if token in self.unigram:
                total_token_probability = total_token_probability * self.unigram[token]
        if total_token_probability > 0.001:
            return True 
        else:
            return False
            
    def save_filtered_tweets(self):
        cwd = os.getcwd()
        cwd += "\\results\\results.csv"
        outtweets = []
        with open(cwd, 'wb') as csvFile:
            writer = csv.writer(csvFile)
            
            #For every filename
            for name in self.filenames:
                #For every tweet in that account
                for tweet in self.tweets_list_f[name]:
                    #Create a list containing the tweet and the country it's from
                    #outtweets = [[tweet,"country], [t,c], [t,c]]
                    outtweets.append([tweet,self.filename_countries[name]])
            writer.writerows(outtweets)
            
    def save_train_test(self):
        cwd = os.getcwd()
        cwd1 = cwd + "\\results\\train.csv"
        cwd2 = cwd + "\\results\\test.csv"
        outtweets = []
        outtweets2 = []
        with open(cwd1, 'wb') as csvFile:
            writer = csv.writer(csvFile)
            #For every filename
            for name in self.filenames:
                #For every tweet in that account
                for tweet in self.tweets_list_f[name]:
                    #Create a list containing the tweet and the country it's from
                    #outtweets = [[tweet,"country], [t,c], [t,c]]
                    outtweets.append([tweet,self.filename_countries[name]])
            writer.writerows(outtweets)
            
        with open(cwd2, 'wb') as csvFileTest:
            writer2 = csv.writer(csvFileTest)
            for name in self.filenames:
                #For every tweet in that account
                for tweet in self.test_tweets[name]:
                    #Create a list containing the tweet and the country it's from
                    #outtweets2 = [[tweet,"country], [t,c], [t,c]]
                    outtweets2.append([tweet,self.filename_countries[name]])
            writer2.writerows(outtweets2)
       
    def save_unigram(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
    def load_unigram(self, name ):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)
            
    def main(self):
        c = raw_input("What do you want to do?\n[1] Filter data\n[2] Split data into training and test set\n: ")
        if int(c) == 1:
            u = self.createUnigramModel(self.tweet_word_tokens)
            self.save_unigram(u, 'unigram')
            self.run_filter()
            self.save_filtered_tweets()
        elif int(c) == 2:
            self.split_train_test()
            self.save_train_test()
        elif int(c) == 3:
            self.five_most_uncommon()
        else:
            print "Invalid input"
            
c = tweet_classifier()
c.main()


    