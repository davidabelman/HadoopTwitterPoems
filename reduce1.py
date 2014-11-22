# Reducer 1

# Reducer to collect unique filtered tweets
# Input: (text, date, name)
# Selects only earliest date for tweet using min function
# Output: (text, date, name)

import sys
import dateutil.parser as dparser

# Keep track of created_time of first tweet of specific text
current_tweet_time_parsed = None
current_tweet_text = None
current_tweet_user = None
current_tweet_id = None

# input from STDIN
for line in sys.stdin:
	# Parse the input
	try:
		tweet_text, tweet_time, tweet_user, tweet_id = line.strip().split('\t')
	except:
		# Silently ignore line if cannot parse (could add a counter here to send to mapreduce boss)
		continue

	# Parse time of tweet
	tweet_time_parsed = dparser.parse(tweet_time, fuzzy=True)

	# If first tweet, or same tweet as previous, see if it was tweeted earlier
	if not current_tweet_text or (tweet_text == current_tweet_text):
		if not current_tweet_time_parsed or tweet_time_parsed < current_tweet_time_parsed:
			current_tweet_time_parsed = tweet_time_parsed
			current_tweet_text = tweet_text
			current_tweet_user = tweet_user
			current_tweet_id = tweet_id
		else:
			# Not the newest, so we don't do anything with it
			continue
	else:
		# This is a new tweet (not seen before), so spit out the previous unique tweet (earliest version of it)
		print '%s\t%s\t%s\t%s' %(current_tweet_text, current_tweet_time_parsed, current_tweet_user, current_tweet_id)
		current_tweet_time_parsed = tweet_time_parsed
		current_tweet_text = tweet_text
		current_tweet_user = tweet_user
		current_tweet_id = tweet_id

# Remember to print out the final one which wouldn't have been printed yet
print '%s\t%s\t%s\t%s' %(current_tweet_text, current_tweet_time_parsed, current_tweet_user, current_tweet_id)
