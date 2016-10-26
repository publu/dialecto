import tweepy
from collections import deque
import csv
import re
from time import sleep

#Twitter API credentials
consumer_key = "SV58jiykYH6UE9cJB21CegNMF"
consumer_secret = "DQK88ZvmcM15aGTskSjnnSXNg8rDvqKy9GnH9wrmWSXa34ok1T"
access_key = "118191893-ZTHPSE3NZ7lkpMjEuHhrhiZLf9pKKKup40Pjlcrf"
access_secret = "hHxny6xs7uuisYYFLHP0Ip6tNcBpuaUblRRF9RQWPJ79d"

def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow

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
	
	# if the file exists, get id 
	file_name = '%s_tweets.csv' % screen_name

	last_id = int(list(get_last_row(file_name))[0])

	print "last tweet %s" % last_id

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,since_id=last_id)

	time = 5
	if(len(new_tweets) != 0):
		#save most recent tweets
		alltweets.extend(new_tweets)

		oldest = alltweets[0].id

		#keep grabbing tweets until there are no tweets left to grab

		while len(new_tweets) > 0:
			print "before %s but after %s" % ((oldest),(last_id) )
			if(int(oldest)<int(last_id) ):
				print "deleting"
				new_tweets = []
			else:
				#all subsiquent requests use the max_id param to prevent duplicates
				new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
				
				#save most recent tweets
				alltweets.extend(new_tweets)
				
				#update the id of the oldest tweet less one
				oldest = alltweets[-1].id - 1

				print "%s tweets so far" % (len(alltweets))
		
		outtweets = []
		added =0
		deleted=0
		#transform the tweepy tweets into a 2D array that will populate the csv	
		for tweet in alltweets:
			if(last_id < tweet.id): #if the id is newer
				text = tweet.text.encode("utf-8")
				id_str = tweet.id_str.encode("utf-8")
				text = re.sub(r'http\S+', "", text)	# cleaning urls
				text = re.sub(r'[\"#]', "", text)	# cleaning quotes and hashtags
				text = re.sub(r'[\n]', "", text)	# cleaning quotes and hashtags
				outtweets.append([id_str,text,country])
				added +=1
			else:
				deleted +=1
		print "total deleted: %s & total added: %s" % ((deleted),(added))
		#outtweets = [[screen_name, tweet.text.encode("utf-8")] for tweet in alltweets]
		
		if(len(outtweets) > 450):
			time = 450	#7.5 mins == 1/2 of the 15 min window
		else:
			time = len(outtweets)

		#write the csv

		with open(file_name, 'a') as f:
			writer = csv.writer(f)
			#writer.writerow(["id_str","text","class"])
			writer.writerows(outtweets)

	else:
		time = 0
		print "no new tweets found."

	print "now we wait %s seconds..." % str(time)
	#sleep(time)
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	chile 	=	["latercera", "Emol", "TVN", "CNNChile", "Cooperativa"]
	arg		=	["eltreceoficial", "LANACION", "clarincom", "24conurbano", "populardiario"]
	col 	=	["NoticiasRCN", "ELTIEMPO", "elespectador", "elpaiscali"]
	mex		=	["NTelevisa_com", "lopezdoriga", "EPN", "EugenioDerbez", "CNNMex"]
	spain	=	["abc_es", "informacion_es", "elperiodico", "_rebelion_org", "Overwatch_Esp", "radiocable"]
	usa 	=	["ElNuevoDia", "LaOpinionLA", "elnuevoherald","vivelohoy","despiertamerica"]

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