from ast import keyword
from distutils.command.config import config
import enum
import tweepy
import configparser
import numpy as np
from PIL import Image
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from wordcloud import WordCloud, STOPWORDS

_stopwords = set(STOPWORDS).add("rt")

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 20)


def genWordcloud(text):
    font_path = "./static/Regular.ttf"
    print(text)
    mask = np.array(Image.open("./static/mask.png"))
    
    # Custom fonts
    wordcloud = WordCloud(height=500,width=800,mask=mask,font_path = font_path, background_color="white", min_font_size=10, colormap='Dark2', stopwords=_stopwords).generate(text)
    
    # Normal Fonts 
    # wordcloud = WordCloud(height=500,width=800,mask=mask, background_color="white", min_font_size=10, colormap='Dark2', stopwords=_stopwords).generate(text)
    
    
    wordcloud.recolor(color_func=grey_color_func, random_state=3)
    wordcloud.to_file("./static/image.png")


 
def getAPI():
    #read config
    # config = configparser.ConfigParser()
    # config.read("./config.ini")
    

    # api_key = config["twitter_creds"]["api_key"]
    # api_key_secret = config["twitter_creds"]["api_key_secret"]

    # access_token = config["twitter_creds"]["access_token"]
    # access_token_secret = config["twitter_creds"]["access_token_secret"]

    api_key = "1kqyZtD7cj3u4Ox3b4ynZzjdc"
    api_key_secret = "Bv6hS7J8YFWxnamN97A2s2SdPTdqsQnWgPk4jZk7VobdUtE80E"

    access_token = "913417844045615104-IxIp8Aw5lRWD8on0WcfpMOiV6UZONpO"
    access_token_secret = "RwVpHxy0LEOFZLNovgflQ2viZEaIvqTWhUb5Ndmoqr8w4"

    #auth
    auth = tweepy.OAuthHandler(api_key,api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    

    return tweepy.API(auth)



def getTweetsFromHashtag(tag):
    api = getAPI()
    limit = 100
    keyword = tag
    tweets = api.search_tweets(q=keyword,count=limit, tweet_mode='extended')
    bagOfWords = [];

    for i,tweet in enumerate(tweets):
        words = getWords(tweet.full_text)
        bagOfWords.extend(words)
        print(i+1," ")
    

    stringOfTweets = " ".join(bagOfWords)


    genWordcloud(stringOfTweets)

    


def getTweetsFromUser(userName):
    api = getAPI()
    limit = 100
    
    tweets = api.user_timeline(screen_name=userName,count=limit, tweet_mode='extended')
    bagOfWords = [];

    for i,tweet in enumerate(tweets):
        words = getWords(tweet.full_text)
        bagOfWords.extend(words)
        print(i+1," ")
    

    stringOfTweets = " ".join(bagOfWords)
    genWordcloud(stringOfTweets)

    

                
    

def getWords(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", tweet)
    tweet = re.sub(r"(?:\@|https?\://)\S+", "", tweet)
    tweetTokens = word_tokenize(tweet)
    stop_words = set(stopwords.words('english'))

    filtered_sentence = [w for w in tweetTokens if not w.lower() in stop_words]
    return filtered_sentence



    

