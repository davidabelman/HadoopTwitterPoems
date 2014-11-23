# Function to filter tweet text as appropriate
# Can add words that tweets must have (and/or condition on these), length of words of tweet, banned words, etc.

sizes = ['big', 'small', 'huge','tiny', 'large', 'mini', 'enormous', 'gigantic']
swearwords = ['fuck', 'shit', 'bastard', 'bitch', 'whore', 'cunt', 'piss', 'damn', 'cock', 'crap', 'fag', 'slut', 'retard', 'shitting', 'fucking', 'fucken', 'friggin', 'frigging', 'pussy', 'dick']
colours = ['red', 'green', 'blue', 'yellow', 'orange', 'grey', 'gray', 'white', 'black', 'brown']
religion = ['jew', 'muslim', 'islam', 'christian', 'buddhist', 'buddha', 'jehov', 'hindu']
intriguing = ['alluring', 'captivating', 'seductive', 'intriguing', 'tantalising', 'tantalizing', 'irresistable']
banned_terms = ['RT', 'http', '@', '#']   # Tweet will be removed if any of these are included
banned_terms = ['http', '@', 'bae', 'ugh', '#', 'mic']
allowed_length = [2,15]   # Tweet must be between these lengths of words
first_words = ""   # Leave blank to ignore this condition
must_have_terms_AND = []   # Terms that tweet must have (all of them) - can leave as blank list
must_have_terms_OR = []   # Terms that tweet must have (1 or more of them) - can leave as blank list
words_in_tweet1 = ""   # Terms that first line of couplet must contain - can leave as blank string
words_in_tweet2 = ""    # Terms that second line of couplet must contain - can leave as blank string
scan_pattern_mode = [14,15]
randomness = True
total_lines = 16

def remove_punctuation(input):
	"""
	Returns text with no punctuation
	"""
	import re
	regex = re.compile('[^a-zA-Z]')
	if type(input)==list:
		return [regex.sub('', x) for x in input]
	else:
		return regex.sub('', input)
	

def get_last_word(text):
	"""
	Gets last word in a string without any punctuation
	"""
	last_word = text.split(' ')[-1]	
	return remove_punctuation(last_word)


def passes_tweet_text_filter(text):
	"""
	Function applied to each tweet text to see if tweet valid for poetry
	If tweet passes, True is returned
	If not, 'False' is returned
	"""
	# Measure length
	text_split = text.split(' ')
	if len(text_split)<allowed_length[0] or len(text_split)>allowed_length[1]:
		print "wrong length"
		return False

	# Look for banned terms
	for word in banned_terms:
		if word in text:
			print "banned word"
			return False

	# Ensure must have words (AND condition) are in the text
	if len(must_have_terms_AND)>=1:
		for word in must_have_terms_AND:
			if word.lower() not in text.lower():
				print "doesn't have required words (AND condition)"
				return False

	# Check if first words of tweet are valid (skip by leaving 'first_words' blank, above)
	if first_words:
		first_words_split = first_words.lower().split(' ')
		first_word_length = len(first_words_split)
		if text.lower().split(' ')[0:first_word_length] != first_words_split[0:first_word_length]:
			print "starts with wrong word/phrase"
			return False

	# Find the last word, skip if only 1 letter (i.e. emoticon)
	last_word = get_last_word(text)
	if len(last_word) == 1:
		print "ends in 1 letter word"
		return False

	# Ensure must have words (OR condition) are in the text
	if len(must_have_terms_OR)>=1:
		has_word_OR = False
		for word in text_split:
			if word in must_have_terms_OR:
				has_word_OR = True
				continue
		if not has_word_OR:
			print "doesn't have required word (OR condition)"
			return False
	
	return True

def passes_tweet_user_filter(user):
	"""
	TODO
	Will return True or False based on conditions for user:
	e.g. gender, country, age (depending what is available or can be deduced speedily)
	"""
	return True