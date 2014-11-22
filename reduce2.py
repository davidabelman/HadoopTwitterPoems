# Reducer 2

# Reducer to collect rhyming tweets together
# Input: (rhyme code, last word, text, date, user)
# Groups together all rhyming tweets into one list, which is output with the rhyme code for next mapper
# Output: (rhyme code, [last word, text, date, user] |&| [last word, text, date, user] |&| etc.)
# where the lists within the output are tab separated. Note that rhyme only output if 2 or more different words in the set.

import sys

# Keep track of current rhyme code
current_rhyme_code = None
current_tweet_store = []
current_last_word_set = []

# input from STDIN
for line in sys.stdin:
	# Parse the input
	try:
		rhyme_code, last_word, tweet_text, tweet_time, tweet_user, tweet_id = line.split('\t')
	except:
		# Silently ignore line if cannot parse (could add a counter here to send to mapreduce boss)
		continue
	
	# If first time on algo run, or same old rhyme code as before, append the tweet data into the list
	if rhyme_code == current_rhyme_code or not current_rhyme_code:
		print "Same rhyme code", rhyme_code
		current_tweet_store.append('%s\t%s\t%s\t%s\t%s' %(last_word, tweet_text, tweet_time, tweet_user, tweet_id) ) 
		current_last_word_set.append(last_word)

	# Else, if rhyme code is a new one, print out to STDOUT the results if 2 rhymes in old one
	else:
		print "New rhyme code", rhyme_code
		if len(set(current_last_word_set))>=2:
			print "%s|&|" %(current_rhyme_code),
			print '|&|'.join([tab_separated_tweet.strip() for tab_separated_tweet in current_tweet_store])
		# Reset the tweet store to only store this data
		current_tweet_store = ['%s\t%s\t%s\t%s\t%s' %(last_word, tweet_text, tweet_time, tweet_user, tweet_id)]
		current_last_word_set = [last_word]
	current_rhyme_code = rhyme_code

# Remember to print out the final one which wouldn't have been printed yet
if len(current_tweet_store)>=2 and len(set(current_last_word_set))>=2:
	print "%s|&|" %(rhyme_code),
	print '|&|'.join([tab_separated_tweet.strip() for tab_separated_tweet in current_tweet_store])
