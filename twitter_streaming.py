#import os to check file sizes
import os
import tweetCleaner as tc
import config as config
import sys

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Import PyMongo to access the database
# from pymongo import MongoClient

#Variables that contains the user credentials to access Twitter API
access_token = config.accessToken
access_token_secret = config.accessTokenSecret
consumer_key = config.consumerKey
consumer_secret = config.consumerSecret

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        global filenumber
        global f
        #gets the current size of the file to be appended
        streamingFilename = "streaming_out" + str(filenumber) + ".txt"
        filesize = os.path.getsize(streamingFilename)

        # sys.stdout.write("\rFile filled: " + str(int(filesize/50)) + "%")
        # sys.stdout.flush()

        #if the file exceeds 500bytes a new text file is created
        if filesize > 500:
            f.close()

            # Clean the tweets, output them to a file called usefulTweetData.txt
            # with a filenumber, then delete the old raw data file
            tc.format(streamingFilename)
            tc.extract("cleanTweets.txt", filenumber, config.itemsToTrack)
            tc.fixFormatting("./tweets/usefulTweetData" + str(filenumber) + ".json")
            os.remove(streamingFilename)

            # print ("\nCleaned file number " + str(filenumber) + "\n")

            filenumber += 1
            streamingFilename = "streaming_out" + str(filenumber) + ".txt"
            f = open(streamingFilename, "a+")


        #The data is written to the end of the current file 'f'
        f.write(data + "\n")
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #Creates a file with a changable suffix
    filenumber = 1
    f = open("streaming_out" + str(filenumber) + ".txt", "a+")

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track = config.itemsToTrack)
