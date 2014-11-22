# Mapper 1

# Mapper to parse and filter tweets
# Input: stream of Twitter data
# Extracts name, date, tweet text, id
# Filters for conditions --> no RT, contains certain hashtag/word(s), certain length, remove hashtags... etc.
# Output: (text, date, user, id)

import sys
import json
from tweet_filter import passes_tweet_text_filter, passes_tweet_user_filter

# input comes from STDIN (standard input)
for line in sys.stdin:
	# Convert to json
	try:
		json_line = json.loads(line)
		# Extract info
		tweet_time = json_line['created_at']
		tweet_text = json_line['text']
		tweet_retweeted = json_line['retweeted']
		tweet_retweet_count = json_line['retweet_count']
		tweet_user = json_line['user']['screen_name']
		tweet_lang = json_line['user']['lang']
		tweet_id = json_line['id']		
		print "success loading"		
	except:
		print "failed to load"
		continue

	# Reject if not English
	if tweet_lang != 'en':
		print "not english"
		continue

	# Filter by user data
	if not passes_tweet_user_filter(tweet_user):
		print "user not passed"
		continue

	# Filter by conditions on text (e.g. banned words, length etc.)
	if not passes_tweet_text_filter(tweet_text):
		print "text not passed"
		continue

	# Encode and write the results to STDOUT (standard output), tab-delimited;
	try:
		tweet_text = tweet_text.encode('ascii', 'ignore').lower().replace('\n',' ')
		print '%s\t%s\t%s\t%s' % (tweet_text, tweet_time, tweet_user, tweet_id)
	except:
		print "can't encode ascii"
	