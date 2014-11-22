import urllib2, sys
from urllib import quote_plus as clean_url
import json

# Primary input info
human_readable_query = """
"i love it when" -RT -http -t.co
"""
pages_target = 200  # 100 ~ 25MB
initial_id_position = ''   # Should be blank, only value if crashed prev and want to continue
# ifeelike 534340931160641535

# Print data to screen (saved to file anyway)
show_sample_data_on_screen = False
show_all_texts_on_screen = True

# Functions
def build_request_string(base,parameters):
	"""
	Add parameters to a base request string
	Parameters is a key value dictionary
	Base is the base URL before any parameters added
	"""
	request_string = base
	for k in parameters:
		v = parameters[k]
		if v:
			request_string += str(k)
			request_string += '='
			request_string += str(v)
			request_string += '&'
	return request_string[:-1]  # Take off the last '&' on the return value

# Get the filename to save results to
try:
	filename = sys.argv[1]+'.txt'
	filename = '/Users/davidabelman/Dropbox/hadoop/tweet_data/'+filename
except:
	print "PLEASE PROVIDE A FILENAME (.TXT WILL BE ADDED) TO SAVE TO. EXITING."
	sys.exit()

# Start timer
import time
start_time = time.time()

# Get the access token (not stored here for security purposes)
access_token = open('/Users/davidabelman/Dropbox/hadoop/access_token_for_twitter/access_token.txt').readlines()[0]

# Info to create the request (see https://dev.twitter.com/rest/public/search for advice on OR, AND, NOT etc.)
request_string_base = 'https://api.twitter.com/1.1/search/tweets.json?'
parameters_to_add = {
	'q':clean_url(human_readable_query),
	'geocode' : '',
	'lang' : 'en',
	'count' : 100,
	'until' : '',  # only take tweets before this date (format: 2012-09-30)
	'since_id' : '',  # only takes tweets with ID more recent than this one (format: 12345)
	'max_id' : initial_id_position,  # only takes tweets with ID older than this one (format: 12345)
	'include_entities' : ''
}


# Main script
total_tweet_count = 0
total_page_count = 0
for i in range(pages_target):
	# Show user a counter
	total_page_count += 1
	print "\nPulling %s/%s pages of data (%s seconds so far)" %(total_page_count, pages_target, int(time.time()-start_time))

	# Build the request string with latest data (max_id changes between iterations at bottom of loop)
	request_string = build_request_string(request_string_base, parameters_to_add)
	print "(Request string is %s)" %request_string

	# Pull data from Twitter
	request = urllib2.Request(request_string)
	request.add_header('Authorization', b'Bearer ' + access_token)
	resp = urllib2.urlopen(request)

	# Parse data
	try:
		data = json.load(resp)
	except:
		print "Couldn't deal with JSON, skipping these 100..."
		continue
	statuses = data['statuses']
	max_id = data['search_metadata']['max_id_str']
	with open(filename, 'a') as outfile:
		for line in statuses:
			json.dump(line, outfile)
			outfile.write('\n')
			total_tweet_count += 1
		outfile.close()
	
	# Update the max_id for the next search (note we are actually passed back the full query string to use, but not using this)	
	try:
		last_id = str(statuses[-1]['id'] - 1)
		parameters_to_add['max_id'] = last_id
		print 'Last ID was: %s. If crash occurs, search back from here.' %last_id
	except:
		print "====================="
		print "No more results returned."
		break

	# Optional - print all text to screen as we go
	if show_all_texts_on_screen:
		print "\n===========================\nNext 100:"
		l = [x['text'] for x in statuses]
		for i in l:
			print i

# Print the JSON data (only the last 100 results) to screen
if show_sample_data_on_screen:
	print("Result:")
	print(json.dumps(data, indent=7, separators=(',', ': ')))

# Print final message
total_time = time.time()-start_time
print "====================="
print "%s tweets were pulled in %s seconds. Results written to %s." %(total_tweet_count, total_time, filename)
print "Exiting."
print "====================="