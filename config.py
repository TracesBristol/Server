from stop_words import get_stop_words
import getKeywords as getK

itemsToTrack = getK.returnKeywords('keywords.json')
words_to_ignore = get_stop_words('english')
words_to_ignore = [x.decode('unicode_escape').encode('ascii','ignore') for x in words_to_ignore]

accessToken = "YOUR ACCESS_TOKEN"
accessTokenSecret = "YOUR ACCESS_TOKEN_SECRET"
consumerKey = "YOUR CONSUMER_KEY"
consumerSecret = "YOUR CONSUMER_SECRET"