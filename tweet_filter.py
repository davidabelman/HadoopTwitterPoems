# Function to filter tweet text as appropriate

banned_terms = ['RT', 'http', '@', '#']   # Tweet will be removed if any of these are included
allowed_length = [3, 10]   # Tweet must be between these lengths of words

def tweet_text_filter(text):
	"""
	Function applied to each tweet text to see if tweet valid for poetry
	If tweet passes, tweet text is returned
	If not, 'None' is returned
	"""
	# Measure length
	text_split = text.split(' ')
	if len(text_split)<allowed_length[0] or len(text_split)>allowed_length[1]:
		return None

	# Look for banned terms
	for word in banned_terms:
		if word in text:
			return None
	
	# Encode
	text = text.encode('ascii', 'ignore').lower()
	return text