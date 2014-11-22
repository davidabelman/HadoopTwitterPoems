# Mapper 3

# Mapper to take rhyming lines and pick best 2 lines
# Input: (rhyme code, [last word, text, date, user] |&| [last word, text, date, user] |&| etc.)
# Choose best pair from each rhyme group
# Do this by assessing scantion of each line, multiplying scores together
# TODO: add semantic similarity too 
# Output: (rhymecode, text, date, user)

import sys
from random import shuffle, random
from tweet_filter import remove_punctuation, words_in_tweet1, words_in_tweet2, scan_pattern_mode, randomness
import itertools
import string
from nltk.corpus import cmudict
import re
import itertools
pronunciations = cmudict.dict()

def create_banned_word_pairs():
	"""
	Create list of banned pairs of words (that rhyme but shouldn't go together)
	Output format as a list of sets:
	[set('tonight', 'night'),
	 set('tonight', 'nite'),
	 set('tonight', 'tonite')...]
	"""
	banned_last_word_sets = [
	['tonight','night','nite','tonite','2night','2nite'],
	['anywhere','everywhere','where','nowhere','wear'],
	['to','2','too'],
	['sometime','time','thyme'],
	['sometimes','times'],
	['though','thou','tho'],
	['anymore','more'],
	['their','there'],
	['day','today'],
	['be','bee'],
	['we','wee'],
	['asleep','sleep'],
	['dis','this'],
	['mow','now','yo'],
	['ever','forever'],
	['them','em'],
	['unreal','real'],
	['way','away'],
	['no','know'],
	['hear','here'],
	['gary', 'dairy'],
	['while', 'awhile'],
	['alot', 'a lot'],
	['her','in']
	]
	banned_pairs = []
	for s in banned_last_word_sets:
		pairs = [x for x in itertools.combinations(s,2)]
		for p in pairs:
			banned_pairs.append(set(p))
	return banned_pairs
banned_last_word_pairs = create_banned_word_pairs()

def create_common_word_list(path = 'program_data/common_words.txt', length=300):
	"""
	Uses 5000 word list of words to pick out X most common
	All lower case in output
	"""
	# from http://www.wordfrequency.info/top5000.asp
	f = open(path).readlines()
	words = []
	counter = 0
	for line in f:
		try:
			(rank, word, pos, freq, dispersion) = line.strip().split()
			words.append(word.lower())
			counter += 1
			if counter == length:
				break
		except:
			None		
	return words
most_common_words = create_common_word_list()
most_common_words.append('is')

def filter_for_double_subject(tweet1_text, tweet2_text, words_in_tweet1, words_in_tweet2):
	"""
	Detect whether two chosen subjects are included in tweet1 and tweet2.
	Swap order if required so all pairs are in same order (Subject1, Subject2)
	Return tweets as [tweet1, tweet2] (or [False, False])
	"""
	# print "Testing subjects...", words_in_tweet1, words_in_tweet2
	# print tweet1_text
	# print tweet2_text
	# print
	if words_in_tweet1 in tweet1_text and words_in_tweet2 in tweet2_text:
		return 'keep'
	elif words_in_tweet1 in tweet2_text and words_in_tweet2 in tweet1_text:
		return 'swap'
	else:
		return False

def is_word(word):
	"""
	Returns if the word is an English known word
	"""
	if pronunciations.get(word):
		return True
	else:
		return False


def score_scan_pattern(scan_pattern, mode):
	"""
	Given a scan pattern (e.g. ['2', '1', '0', '0', '1', '2', '2', '2', '2', '2'])
	Provides a score based on number of 1s and 2s
	Currently set up for 01010101 type scoring.
	"""
	minimal = 0.01  # Minimal score in case nothing returned. If 0, we may have no lines.
	_0s = scan_pattern.count('0')
	_1s = scan_pattern.count('1')
	_2s = scan_pattern.count('2')
	_total = len(scan_pattern)

	if type(mode)==list:
		if _total in mode:
			return 1
		else:
			return 0

	if mode == '8 beat':
		if _total==13:
			return 1
		else:
			return 0

	if mode == '12 syllable':
		if _total==12:
			return 1
		else:
			return 0	

	if mode == '7 syllable':
		if _total==7:
			return 1
		else:
			return 0	

	if mode == '5 syllable':
		if _total==5:
			return 1
		else:
			return 0	

	if mode == '4 syllable':
		if _total==4:
			return 1
		else:
			return 0	

	if mode == '3 syllable':
		if _total==3:
			return 1
		else:
			return 0	

	if mode == '11 syllable':
		if _total==11:
			return 1
		else:
			return 0	

	if mode == '14 syllable':
		if _total==14:
			return 1
		else:
			return 0	
	
	if mode == '8 beat loose':
		if _total==13:
			return 1
		if _total==12 or _total==14:
			return 0.5
		else:
			return 0		

	if mode == '4 beat':
		if _total==7:
			return 1
		else:
			return 0

	if mode == '4 beat loose':

		if _total<=6:
			return 0

		if _total>8: #12
			return 0

		if _total>10 and _total<=12:
			return minimal

		if _1s>5:
			return minimal

		if _1s+_2s<4:
			return minimal

		if _1s==5:
			return 0.04

		if _1s==4 and _0s+_2s==4:
			return 1

		if _1s==4 and _total<=8 and _total>=6:
			return 0.5

		if _total==6:
			return 0.5

		if _1s==3 and _2s==1 and _total<=9 and _total>=7:
			return 0.5

		if _1s==4 and _total>8:
			return 0.25

		if _1s==3 and _total<=7:
			return 0.08

		if _1s==3 and _2s>1 and _total>7:
			return 0.25

		if _1s==2 and _2s>=2 and _total>=7:
			return 0.2

		if _1s==1 and _2s>=3:
			return 0.06

		if _2s>=4:
			return 0.03

		return 0

	return "Unknown mode"


def get_scan_pattern(line, debug=False):
	"""
	Outputs a string scan pattern of form ['2', 2, '1', '0', 2, 2, '1', '0', '2'] for sentence
	0 = no stress
	1 = stress
	2 = could be either
	Also outputs a score for percentage of words recognised
	Output is [['2','2','1'...] 0.86]
	"""
	# Debug mode, as gets a little hairy
	if debug:
		print "Debug mode on:"

	# Remove all punctuation
	exclude = set(string.punctuation)
	line = ''.join(ch for ch in line if ch not in exclude)

	# Split line into words
	words = line.split(' ')

	# Final list to populate
	final_list = []

	# Initialise counts for words recognised vs. not
	words_recognised = 0
	words_not_recognised = 0

	# Go through each word, will append to a big list in the end
	for word in words:

		# Look up pronuncation from CMU dict
		pron = pronunciations.get(word)

		# If it exists in CMU dict, carry on (if not, we will estimate, see below)
		if pron:
			words_recognised += 1
			initial_vowel_stress_list = []
			for sound in pron:
				# Pull out numbers only (i.e. vowel stresses)
				initial_vowel_stress_list.append( [x[-1] for x in sound if x[-1] in ('0','1','2')] )

			# If only one possible pronunciation, use this if more than 1 syllable
			# If only 1 syllable, this should be ['2'] if common word (i.e. can be used as 0 or 1)
			# or it should be ['1'] if it is a non common word
			if len(initial_vowel_stress_list)==1:
				# If [['1', '0']] for instance, we just use this as our result
				if len(initial_vowel_stress_list[0])>1:
					output_word = initial_vowel_stress_list[0] # i.e. leave it as it is
				else:
					# Now we have a 1 syllable word - check to see if common
					if initial_vowel_stress_list[0]==['2']:
						output_word = initial_vowel_stress_list[0] # i.e. leave it as it is
					else:
						if word in most_common_words:
							output_word = ['2'] # i.e. common word, could be stressed or not
						else:
							output_word = ['1'] # not common word, likely to be stressed
				
			# If multiple pronunciations, e.g. [['1'], ['1']] OR [['1', '0'], ['1', '0']] OR [['1', '0'], ['1']] OR [['1', '0'], ['0', '1']]
			# We want to change to '2' if either a 0 or 1 is possible for a certain syllable
			if len(initial_vowel_stress_list)>1:
				output_word = [] # will be list like [0,1,0,2] when we've finished
				# Note that we don't attempt for examples like [['1', '0'], ['1']], which fail on this. All variations need the same length
				try:
					# Loop through each variation
					for i in range(len(initial_vowel_stress_list[0])):
						possible_stresses = [x[i] for x in initial_vowel_stress_list]
						# If 1/0 or 2, we output 2
						if '2' in possible_stresses or ('0' in possible_stresses and '1' in possible_stresses):
							output_vowel = '2'
						# Otherwise we output 0/1 depending on what it is
						else:
							output_vowel = possible_stresses[0]  # which will be either 0 or 1
						output_word.append(output_vowel)
				except:
					# [['1', '0'], ['1']] - we will just choose the first pronunciation, as differing lengths, too complicated
					output_word = initial_vowel_stress_list[0]			
		
		# No pronuncation found in CMU dict, we need to estimate
		else:
			words_not_recognised +=1

			# Sub consonants with spaces
			no_cons = re.sub('[bcdfghjklmnpqrstvwxz]+',' ',word)
			vowel_list = no_cons.split()  #i.e. o a a
			syllables = len(vowel_list)  #i.e. 3
			
			# If 2 syllables, replace with [1,0] etc as shown here
			syllables_lookup = {0:['2'], 1:['2'], 2:['1','0'], 3:['1','0','2'], 4:['1','0','2','0']}
			initial_vowel_stress_list = 'Estimated'
			
			# i.e. output_word = ['1','0','2'] when we look it up in syllables_lookup
			if syllables<=4:
				output_word = syllables_lookup[syllables]
			else:
				# If 5 or more syllables, just use this
				output_word = ['1','0','2','0','0']

		final_list.append(output_word)

		# Print debug info
		if debug:
			print "Word in question:", word
			print "Found pronunciations:", initial_vowel_stress_list
			print "Our final result:", output_word
			print

	if debug:
		print "Our initial sentence was:", line
		print "Our final list of pronunciations is:", final_list
		print

	# Return in format [['1'], ['1'], ['1', '0'], [2], ['1', '0'], ['1', '0', '2'], ['1', '0'], ['1', '0', '0'], [0, 1]]
	chain = itertools.chain(*final_list)

	# Also calculate % of words recognised
	pc_words_recognised = words_recognised*1.0 / (words_recognised+words_not_recognised)

	# Return as list
	return [list(chain), pc_words_recognised]


def calculate_overlap_score(t1, t2):
	"""
	Calculates number of overlapping words between 2 tweets
	"""
	# Convert sentence into list of words
	tweet1_list = remove_punctuation(t1.split(' '))
	tweet2_list = remove_punctuation(t2.split(' '))
	# Remove any common words
	tweet1_list = [x for x in tweet1_list if x not in most_common_words]
	tweet2_list = [x for x in tweet2_list if x not in most_common_words]
	# TODO: expand wordset using wordnet?
	# Count the overlap
	overlap_count = 1 + len( set(tweet1_list).intersection(set(tweet2_list)) )
	return overlap_count

def map3_parse(line):
	tweets_parsed = []
	line = line.split('|&|')
	rhyme_code = line[0]
	tweets = line[1:]
	for tweet in tweets:
		last_word, tweet_text, tweet_time, tweet_user, tweet_id = tweet.strip().split('\t')
		tweets_parsed.append([last_word, tweet_text, tweet_time, tweet_user, tweet_id])

		# So now for this particular rhyme we have a list of lists:
		# [
		# 	[last_word, tweet_text, tweet_time, tweet_user, tweet_id],
		# 	[last_word, tweet_text, tweet_time, tweet_user, tweet_id],
		# 	[last_word, tweet_text, tweet_time, tweet_user, tweet_id]
		# ]
	return tweets_parsed


def rank_all_pairs_of_tweets(tweets_parsed):
	"""
	Given a set of parsed tweets in format:
	[
		[last_word, tweet_text, tweet_time, tweet_user, tweet_id],
		[last_word, tweet_text, tweet_time, tweet_user, tweet_id],
		[last_word, tweet_text, tweet_time, tweet_user, tweet_id] ... etc. 
	]
	Looks at all combinations of pairs of tweets and scores their viability on various factors
	Returns list of tweet paris with their ranking:
	[
		[([tweet1data], [tweet2data]), 0.0625]
		[([tweet2data], [tweet3data]), 0.9]
		[([tweet1data], [tweet3data]), 0.125]
	]
	"""
	tweet_pair_ranking = []
	keep_or_swap = False
	for tweet1 in tweets_parsed:
		for tweet2 in tweets_parsed:
			
			# If same last word, skip the scoring
			last_word_1 = tweet1[0]
			last_word_2 = tweet2[0]
			if remove_punctuation(last_word_1)==remove_punctuation(last_word_2):
				continue

			# If last word not a word, skip the scoring
			if not is_word(last_word_1) or not is_word(last_word_2):
				continue
			
			# If banned pair of last words, skip the scoring:
			last_words = set([last_word_1, last_word_2])
			if last_words in banned_last_word_pairs:
				continue

			# If we want 2 subjects to appear, this is done here
			# We return either 'keep', 'swap' or False
			if words_in_tweet1 and words_in_tweet2:
				keep_or_swap = filter_for_double_subject(tweet1[1],tweet2[1], words_in_tweet1, words_in_tweet2)
				# If it returned false, just continue
				if not keep_or_swap: # i.e. returned False
					continue				

			# Add scan scores
			scan_pattern_1, pc_words_recognised_1 = get_scan_pattern(tweet1[1])
			scan_pattern_2, pc_words_recognised_2 = get_scan_pattern(tweet2[1])
			tweet1_scan_score = score_scan_pattern(scan_pattern_1, scan_pattern_mode)
			tweet2_scan_score = score_scan_pattern(scan_pattern_2, scan_pattern_mode)
			total_scan_score = tweet1_scan_score*tweet2_scan_score

			# Calculate percentage of words recognised scores
			total_words_recognised_score = pc_words_recognised_1*pc_words_recognised_2
			
			# Calculate semantic similarity score (if scan score>0, otherwise don't waste time on it)
			if total_scan_score>0:
				overlap_score = calculate_overlap_score(tweet1[1], tweet2[1])				
			else:
				overlap_score = 1
			
			# Combine the various scores
			total_score_for_pair = 100.0* total_scan_score * overlap_score * total_words_recognised_score		
			if randomness:
				# Multiply by number between 1 and 1.1
				total_score_for_pair = total_score_for_pair*(random()/10.0+1)
			if total_score_for_pair > 0:
				if keep_or_swap=='keep':
					tweet_pair_ranking.append([(tweet1, tweet2), total_score_for_pair])
				else:
					tweet_pair_ranking.append([(tweet2, tweet1), total_score_for_pair])

	return tweet_pair_ranking

def print_highest_scoring_pair(tweet_pair_ranking):
	"""
	Given a ranking of pairs of tweets, rank them by score, and print the highest scoring pair to a line
	This will then be taken and dealt with by reducer
	"""
	# Sort by score, which is in the second slot (index[1])
	tweet_pair_ranking.sort(key = lambda x: x[1], reverse=True)

	# Print the top scoring tweet for this rhyme group
	tweet_pair = tweet_pair_ranking[0]
	score = tweet_pair[1]
	tweet1_data = tweet_pair[0][0]
	tweet2_data = tweet_pair[0][1]
	print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' %(score, tweet1_data[1], tweet1_data[2], tweet1_data[3], tweet1_data[4], tweet2_data[1], tweet2_data[2], tweet2_data[3], tweet2_data[4])


########### MAIN START OF SCRIPT ###########

# input comes from STDIN (standard input)
for line in sys.stdin:
	# Parse the line, which is a group of rhymes
	try:
		tweets_parsed = map3_parse(line)
	# Or fail silently and skip the rhyme if we can't parse correctly
	except:		
		continue

	# Score each possible pair of lines within the rhyme set
	if tweets_parsed:
		# Calculate score for each possible pair and return as a big list of [ [(tweet1, tweet2), score], [(tweet2, tweet3), score] ... ]
		tweet_pair_ranking = rank_all_pairs_of_tweets(tweets_parsed)
		
		# Output best scoring pair of lines as one line for the reducer to deal with
		if tweet_pair_ranking:
			print_highest_scoring_pair(tweet_pair_ranking)
			