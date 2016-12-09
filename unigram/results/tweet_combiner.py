import csv

def add_string_c(tweet, key):
    for i in range(len(d[key])):
        #print d[key][i]
        l = len(tweet) + len(d[key][i])
        #print l
        if l < 1024:
            s = d[key][i] + tweet
            #print s
            d[key][i] = s
            return True
    return False
            
def save_combined_tweets(tweet_dict):
    outtweets = []
    filename = raw_input("Enter a results filename: ")
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        #For every country
        for key in tweet_dict.keys():
            #For every combined tweet in that country
            for ctweet in tweet_dict[key]:
                #Format the output: [[tweet1, countrya], [tweet2, countrya], [tweet1, countryb]]
                outtweets.append([ctweet, key])
        writer.writerows(outtweets)
        
        
#Open the results file
#countries = set()
d = {}
tweets = []
countries = []
#print "Now opening file..."
filename = raw_input("Enter an input filename: ")
with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tweet = row[0]
        c = row[1]
        tweets.append(tweet)
        countries.append(c)
        d[c] = []
print "Done opening file\n"  
total = len(tweets)
j = 0.0
print "Now merging..."
for i in range(len(tweets)):
    tweet = tweets[i]
    c = countries[i]
    if not add_string_c(tweet, c):
            d[c].append(tweet)
    j += 1
    p = round((j/total * 100), 4)
    print "Percent complete: " + str(p)
            
save_combined_tweets(d)
            