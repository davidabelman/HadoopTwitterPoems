Introduction
============
Toy project aiming to automatically create 'poetry' (rhyming couplets)
from Tweets meeting a certain criteria (for example, a certain hashtag).
Project to use Hadoop Streaming with Python scripts to parse and
filter tweets, find rhymes, and order appropriately.

Usage
=====
A mapreduce style job running locally using STDIN and STDOUT can be initiated with:
>> cat tweet_data/some_twitter_stream_data.txt | python map1_tweets.py | sort -k1,1 | python reduce1.py | python map2.py | sort | python reduce2.py | python map3.py | sort -r | python reduce3.py

Note that map1_tweets.py can be replaced by map1_text.py if we wish to input a plain text document, splitting at sentence boundaries.

Method
======
3 layers of MapReduce take place. Firstly, unique tweets are picked, with the earliest unique tweet being selected (to attribute original author). Secondly, rhyming tweets are grouped together. Thirdly, optimal pairs of tweets are selected from this rhyme group (based on scantion and overlapping words). Most of the logic that is not trivial is performed within the 3rd mapper (checking for scan, checking for semantic similarities, pairing optimal sets of lines together, etc.)

Getting Twitter data
====================
Can be done in 2 ways. Either use the Twitter firehose to fill 'firehose.txt', at a rate of 100MB per 10 minutes, or so. get_twitter_1pc.py should be run to do this (overwrites file each time). Other option, allowing more subject specific tweets, is to run python get_tweets.py. Within this file we can edit the search term (see Twitter documentation for building search queries) to include exact phrases, exclude terms (such as 'RT', etc.) and also set how many pages of tweets (each 100 tweets long) we would like to pull.

Running MapReduce
=================
As above, run:
>> cat tweet_data/some_twitter_stream_data.txt | python map1_tweets.py | sort -k1,1 | python reduce1.py | python map2.py | sort | python reduce2.py | python map3.py | sort -r | python reduce3.py
Note that we filter the tweets within 'map1_tweets.py' using the external module 'filter_tweets.py'. Within this, we can specify words that the tweets must start with, and/or conditions on words in the tweets, length of tweets (limiting to 5-8 words works well)

Uploading to website
====================
The output from reducer3.py should be copied and pasted into a Python file, and actually acts as a module within the Flask application. Thus a poem about Obama should be created as 'obama.py', saved within app.py. Then a link can be added to the main webpage, and the module will be loaded within the flask app when the link is clicked.