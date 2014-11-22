# Pipes twitter 1% firehose into a file whilst it is being run
# Just call python get_twitter_1pc.py
# All saved into 'firehose.txt' file (NOTE, OVERWRITES LAST FIREHOSE)
# "https://stream.twitter.com/1/statuses/sample.json?q=-RT+-http+-t.co%0A&lang=en" ignores retweets, links, and is english only

import oauth2 as oauth
import urllib2 as urllib
import json

# Credentials
access_token_key = open('/Users/davidabelman/Dropbox/hadoop/access_token_for_twitter/access_token_key.txt').readlines()[0]
access_token_secret = open('/Users/davidabelman/Dropbox/hadoop/access_token_for_twitter/access_token_secret.txt').readlines()[0]

consumer_key = open('/Users/davidabelman/Dropbox/hadoop/access_token_for_twitter/consumer_key.txt').readlines()[0]
consumer_secret = open('/Users/davidabelman/Dropbox/hadoop/access_token_for_twitter/consumer_secret.txt').readlines()[0]

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  total_tweet_count = 0
  filename = '/Users/davidabelman/Dropbox/hadoop/tweet_data/firehose.txt'
  url = "https://stream.twitter.com/1/statuses/sample.json?q=-RT+-http+-t.co%0A&lang=en"
  parameters = []
  with open(filename, 'w') as outfile:
    response = twitterreq(url, "GET", parameters)
    for line in response:
      outfile.write(line)
      # outfile.write('\n')
      total_tweet_count += 1
      if total_tweet_count%10==0:
        print 'Total tweets saved... %s' %total_tweet_count

if __name__ == '__main__':
  fetchsamples()
