import re
import os.path
import tokeniseTweet as tk
import tweetSentiment as ts

# filename could be optional? If format is called from another module/python script
# we can just assume that there's only one filename that contains all the tweet data
# to be cleaned. I can change it to either accept a filename or a huge string, filename
# might be more efficient when the tweet data gets bigger.
#
# format :: String -> String
# Take an input of tweet data, adds new lines to make it easier to read
def format(filename):
    f = open(filename, 'r')
    fileInput = f.read()
    f.close()

    fileOutput = fileInput.replace("{", "\n{\n").replace("},", "\n},\n").replace("}]", "}\n]").replace("[{", "[\n{").replace(",\"", ",\n\"")

    g = open("cleanTweets.txt", 'w')
    g.write(fileOutput)
    g.close()

# Fix the JSON formatting by removing one specific comma from each tweet object
def fixComma(usefulData):
    fixedList = []
    langIndex = 0
    i = 0

    while i < len(usefulData):
        item = usefulData[i]

        if item[1:5] == "lang":
            langIndex = i

        if (langIndex + 1) == i:
            if item == "},\n":
                oldLine = usefulData[i-1]
                newLine = oldLine[:-2] + "\n"
                fixedList[i-1] = newLine

        # temp = item.replace("\n", '')
        # if temp == ",":
        #     item = ""

        fixedList.append(item)
        i += 1

    return fixedList

# Fix some random parentheses that ruin the JSON formatting
# Inefficient, pls fix? Works using a stack, and if it finds a
# naughty naughty bracket it just delets it and moves on in life.
# Also now fixes rogue commas between tweet objects!
def fixFormatting(filename):
    stack = []
    commaCount = 0
    f = open(filename, 'r')
    content = f.read()
    f.close()

    g = open(filename, 'w')
    for item in content:
        try:
            if '{' in item:
                stack.append(1)
            elif '}' in item:
                if stack[-1] == 1:
                    stack.pop()
        except IndexError:
            item = ''

        if stack == []:
            if ',' in item:
                commaCount += 1
            if commaCount > 1:
                item = ''
        else:
            commaCount = 0

        g.write(item)
    g.close()

# Note: first set of hashtags, favs and retweets are from the deepest embedded
# tweet, the last set is from the top level tweet.
# Add/Remove cases here to include/remove tweet metadata
#
# isUseful :: String -> Bool
def isUseful(line, hashtagFlag):
    lineLength = len(line)

    if hashtagFlag:
        return True

    if line[1:5] == "text" or line[1:5] == "name" or line[1:5] == "lang" or  line[1:5] == "urls":
        return True
    elif line[1:9] == "location" or line[1:9] == "verified" or line[1:9] == "hashtags":
        return True
    elif line[1:10] == "time_zone":
        return True
    elif line[1:11] == "created_at" or line[1:11] == "description":
        return True
    elif line[1:12] == "screen_name":
        return True
    elif line[1:14] == "retweet_count": ##or line[1:14] == "friends_count":
        return True
    elif line[1:15] == "favorite_count" or line[1:15] == "statuses_count":
        return True
    elif line[1:16] == "followers_count":
        return True
    # elif line[1:17] == "favourites_count":
    #     return True
    elif line[1:24] == "in_reply_to_screen_name":
        return True

    return False

# Again takes a filename, but can be changed to take a string instead.
# IMPORTANT: The input should have already been passed through the format function,
# so that the lines contain less irrelevant content, for example excess parentheses.
# Outputs to a new file which is currently overwritten each time the function is called.
#
# extract :: String -> String
def extract(filename, outputNumber, itemsBeingTracked):
    f = open(filename, 'r')
    usefulData = ["[{\n"]
    tweetID = 0
    hashtagFlag = False
    newTweet = True
    newCreated = True
    endOfTweet = False

    usefulData.append("\"clNum\":" + str(tweetID) + ",\n")

    for line in f:
        # The timestamp_ms line is only found at the end of every top level tweet, is not
        # included in quoted tweets/sub tweets. RegEx is used  because the value is diff each time.
        if re.match("\"timestamp_ms\":\"[0123456789]*\"\}", line):
            usefulData.append("},\n")
            usefulData.append("\n")
            endOfTweet = True
            newTweet = True
            newCreated = True

        elif isUseful(line, hashtagFlag):
            if endOfTweet:
                usefulData.append("{\n")
                tweetID += 1
                usefulData.append("\"clNum\":" + str(tweetID) + ",\n")
                endOfTweet = False

            # Set the flag if a hashtag sub section is entered
            if line[1:13] == "hashtags\":[\n":
                hashtagFlag = True

            if line[1:9] == "urls\":[\n":
                hashtagFlag = True

            # Fix language tag problems
            if line[1:5] == "lang":
                if line[-2] != ",":
                    line = line[:-2] + "\",\n"


            # After the first created_at line has been added, delete any future occurences of that line
            if line[1:11] == "created_at" and newCreated:
                newCreated = False
            elif line[1:11] == "created_at" and not newCreated:
                line = ""

            # Adds a tag to each tweet to say which keyword it is reated to
            # if multiple keywords are being tracked
            if line[1:5] == "text" and newTweet:
                tokens = tk.toke(line[8:-3])
                if tokens != []:
                    lineToAdd = "\"tokens\":["
                    for item in tokens:
                        lineToAdd += "\""+ str(item) + "\","

                    lineToAdd = lineToAdd[:-1] +  "],\n"
                    usefulData.append(lineToAdd.decode('unicode_escape').encode('ascii','ignore'))

                newTweet = False
                lowerLine = line.lower()
                found = False
                for item in itemsBeingTracked:
                    if item.lower() in lowerLine:
                        found = True
                        usefulData.append("\"tag\":\"" + str(item) + "\",\n")
                if found == False:
                    newTweet = True

                polarity = ts.sentimentAnalysis(line)
                sentimentLine = "\"polarity\":" + "\"" + str(polarity) + "\",\n"
                usefulData.append(sentimentLine)

            if line[1:5] == "text":
                temp = line[8:-3].replace("\"", "'").replace("\\","")
                line = line[:8] + temp + line[-3:]


            usefulData.append(line.decode('unicode_escape').encode('ascii','ignore'))

        # Check if hashtag sub section has ended, all to do with syntax
        if (hashtagFlag):
            if line == "],\n":
                hashtagFlag = False

    f.close()

    usefulData = fixComma(usefulData)
    # FIXED final close bracket with comma
    usefulData[-2] = '}]'

    g = open("./tweets/usefulTweetData" + str(outputNumber) + ".json", 'w')
    for item in usefulData:
        g.write(item)
    g.close()


# Combines the format function and extract, only requirement is that
# twitter_data.json file exists.
def blitz():
    if os.path.exists("aws_output.txt"):
        # print("Cleaning...")
        format("aws_output.txt")
        extract("cleanTweets.txt")
        # print("Cleaning complete. Output in /tweets/usefulTweetData.json\n")
    else:
        print("\nERROR:\nFile aws_output.txt not found\n")

# Don't call main, import tweetCleaner.py into other modules or into the interactive
# terminal using 'import tweetCleaner as cl', then call funtions e.g 'cl.extract("cleanTweets.txt")'
def main():
    return "Don't call main"

if __name__ == "__main__":
    main()
