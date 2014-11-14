# Mapper 1

# Mapper to parse and filter tweets
# Input: stream of Twitter data
# Extracts name, date, tweet text
# Filters for conditions --> no RT, contains certain hashtag/word(s), certain length, remove hashtags... etc.
# Output: (text, date, user)

import sys
import json
from tweet_filter import tweet_text_filter

# input comes from STDIN (standard input)
for line in sys.stdin:
	# Convert to json
	try:
		json_line = json.loads(line)
		# print json_line
		# print "-----\n\n"
	except:
		continue

	# Extract info
	tweet_time = json_line['created_at']
	tweet_text = json_line['text']
	tweet_retweeted = json_line['retweeted']
	tweet_retweet_count = json_line['retweet_count']
	tweet_user = json_line['user']['screen_name']
	tweet_lang = json_line['user']['lang']

	# Reject if not English
	if tweet_lang != 'en':
		continue

	# Clean tweet and filter, output to STDOUT
	tweet_text = tweet_text_filter(tweet_text)
	if tweet_text:
		# write the results to STDOUT (standard output), tab-delimited;
		print '%s\t%s\t%s' % (tweet_text, tweet_time, tweet_user)