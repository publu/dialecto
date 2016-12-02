from nltk.tokenize import TweetTokenizer
from nltk import ngrams
import csv 
import os
import pickle

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
        self.unigram = {}
        self.filename_countries = {}
        
        #Create the nltk tokenizer object
        self.tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
        
        #Get all the filnemaes in the directory except for this file
        self.filenames = os.listdir(os.getcwd())
        self.filenames.remove(os.path.basename(__file__))
        #self.filenames.remove('test_unigram.pkl')
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
                self.filename_countries[filename] = row[1]
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
       
    def save_unigram(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
    def load_unigram(self, name ):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)
            
    def main(self):
        self.createUnigramModel(self.tweet_word_tokens)
        self.run_filter()
        self.save_filtered_tweets()
            
c = tweet_classifier()
c.main()


    