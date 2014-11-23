# Reducer 3

# Reducer to export final output in desired format
# Input: (score, text, date, user, text, date, user)
# Can output to correct format (e.g. for HTML, javascript, or whatever)
# HTML is unescaped here
# Currently prints to screen, and this must then be copied to a file.py (e.g. obama.py) within the Flask app

import sys
import dateutil.parser as dparser
import HTMLParser
from tweet_filter import total_lines

h= HTMLParser.HTMLParser()
counter = 0

# Specify HTML output format and location
def return_python_module(id, text, name, date):
	date = dparser.parse(date, fuzzy=True)
	date_string = date.strftime('%B %d, %Y')
	return """
		<blockquote class="twitter-tweet" lang="en" link="https://twitter.com/%s/status/%s">
			<p>%s</p>
			<twittername>&mdash; @%s</twittername> 
			<twitterdate>%s</twitterdate>
		</blockquote>
	""" %(name,id,text,name,date_string)


# Output introduction
print "\n==================================\n"
print "COPY AND PASTE THE BELOW INTO A .PY FILE:"
print "\n==================================\n"

print 'title = "FILL TITLE HERE"'
print 'desc = "FILL DESCRIPTION HERE"'
print 'poem = """'

# input from STDIN
for line in sys.stdin:
	# Stop at 4th couplet
	if counter==total_lines:
		continue

	# Parse the input
	try:
		score, tweet1_text, tweet1_time, tweet1_user, tweet1_id, tweet2_text, tweet2_time, tweet2_user, tweet2_id  = line.split('\t')
	except:
		# Silently ignore line if cannot parse (could add a counter here to send to mapreduce boss)
		continue
	
	print '%s\t%s\t%s\thttps://twitter.com/%s/status/%s' %(h.unescape(tweet1_text.strip()), tweet1_user.strip(), dparser.parse(tweet1_time, fuzzy=True).strftime('%B %d, %Y'), tweet1_user.strip(), tweet1_id.strip())
	print '%s\t%s\t%s\thttps://twitter.com/%s/status/%s' %(h.unescape(tweet2_text.strip()), tweet2_user.strip(), dparser.parse(tweet2_time, fuzzy=True).strftime('%B %d, %Y'), tweet2_user.strip(), tweet2_id.strip())

	# Increase counter
	counter+=2

# Ending
print '"""'
print "\n==================================\n"
print "COPY AND PASTE THE ABOVE INTO A .PY FILE:"
print "\n==================================\n"
