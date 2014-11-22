# Mapper 1

# Mapper to parse and filter any input text split into sentences.
# Input: text data
# Extracts sentences, makes up other info
# Filters for conditions --> no RT, contains certain hashtag/word(s), certain length, remove hashtags... etc.
# Output: (text, date, user)

import sys
import json
from tweet_filter import tweet_text_filter

# input comes from STDIN (standard input)
for line in sys.stdin:
	sublines = line.split('.')
	for line in sublines:
		# Extract info
		tweet_time = 'N/A'
		tweet_text = line.decode('utf-8').strip()
		tweet_user = 'N/A'							

		# Clean tweet and filter, output to STDOUT
		tweet_text = tweet_text_filter(tweet_text)
		if tweet_text:
			# write the results to STDOUT (standard output), tab-delimited;
			print '%s\t%s\t%s' % (tweet_text, tweet_time, tweet_user)