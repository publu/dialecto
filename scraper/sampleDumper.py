import tweepy
import csv
import re
from time import sleep

#Twitter API credentials
consumer_key = "SV58jiykYH6UE9cJB21CegNMF"
consumer_secret = "DQK88ZvmcM15aGTskSjnnSXNg8rDvqKy9GnH9wrmWSXa34ok1T"
access_key = "118191893-ZTHPSE3NZ7lkpMjEuHhrhiZLf9pKKKup40Pjlcrf"
access_secret = "hHxny6xs7uuisYYFLHP0Ip6tNcBpuaUblRRF9RQWPJ79d"

def get_all_tweets(screen_name, country):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	print "Setting country to %s" % country
	print "Getting Tweets from %s" % screen_name

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	#only do it once
	print "before %s" % (oldest)
		
	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
	#save most recent tweets
	alltweets.extend(new_tweets)
		
	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
		
	print "%s tweets so far" % (len(alltweets))
	
	outtweets = []
	#transform the tweepy tweets into a 2D array that will populate the csv	
	for tweet in alltweets:
		text = tweet.text.encode("utf-8")
		text = re.sub(r'http\S+', "", text)	# cleaning urls
		text = re.sub(r'[\"#:]', "", text)	# cleaning quotes and hashtags
		outtweets.append([text, country])

	#outtweets = [[screen_name, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["text","class"])
		writer.writerows(outtweets)
	
	print "now we wait 15 seconds..."
	sleep(15)
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	chile 	=	["latercera", "Emol", "TVN", "CNNChile", "Cooperativa"]
	arg		=	["eltreceoficial", "LANACION", "clarincom", "24conurbano", "populardiario"]
	col 	=	["NoticiasRCN", "ELTIEMPO", "elespectador", "elpaiscali"]
	mex		=	["CNNMex", "NTelevisa_com", "lopezdoriga", "EPN"]
	spain	=	["abc_es", "informacion_es", "elperiodico", "_rebelion_org", "Overwatch_Esp", "radiocable"]
	usa 	=	["ElNuevoDia", "primerahora", "LaOpinionLA", "elnuevoherald", "vivelohoy", "despiertamerica"]

	for account in chile:
		get_all_tweets(account, "Chile")
	for account in arg:
		get_all_tweets(account, "Argentina")
	for account in col:
		get_all_tweets(account, "Colombia")
	for account in mex:
		get_all_tweets(account, "Mexico")
	for account in spain:
		get_all_tweets(account, "Spain")
	for account in usa:
		get_all_tweets(account, "USA")