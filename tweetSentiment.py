from textblob import TextBlob

def sentimentAnalysis(text):
    r = TextBlob(text)
    polarity = r.sentiment.polarity
    return polarity
