# Mapper 2

# Mapper to extract last word, find rhyme code
# Input: (text, date, name)
# Extracts final word, looks up in rhyme code dictionary
# If existing in dictionary, sends to reducer
# Output: (rhyme code, last word, text, date, user)

import sys
import re
from tweet_filter import get_last_word

# Create temporary rhyming table lookup
f = open('program_data/exact_rhyme_table.txt').readlines()
rhyme_codes = {}
for line in f:
	(word, syl, code) = line.strip().split(' ')
	rhyme_codes[word] = code

# input comes from STDIN (standard input)
for line in sys.stdin:
	# Parse the input
	try:
		tweet_text, tweet_time, tweet_user, tweet_id = line.strip().split('\t')
	except:
		continue

	# Extract last word and remove any punctuation
	last_word = get_last_word(tweet_text)

	# Look up last word in rhyme code dictionary
	rhyme_code = rhyme_codes.get(last_word, None)

	# If in dictionary, print to STDOUT
	if rhyme_code:
		print '%s\t%s\t%s\t%s\t%s\t%s' %(rhyme_code, last_word, tweet_text, tweet_time, tweet_user, tweet_id)