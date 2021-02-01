import preprocessor as p
import json
import re
import string
import datetime, pytz
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from cltk.corpus.swadesh import Swadesh
from cltk.stop.classical_hindi.stops import STOPS_LIST


stopwords_en = set(stopwords.words('english'))
#stopwords_hi = set(stopwords.words('hindi'))
stopwords_pt = set(stopwords.words('portuguese'))

punct_sent = string.punctuation
punct_list = []
for i in range(0,len(punct_sent)):
    punct_list.append(punct_sent[i])

punct_set = set(punct_list)

""" adding hashtags field"""
def hashtags(parsed_tweet,sent):
    ht = parsed_tweet.hashtags
    txt = ""
    if ht is not None:
        x = ""
        for i in range(0,len(ht)):
            y = re.sub("#","",ht[i].match)
            txt = re.sub(ht[i].match,"",sent)
            x = x + " " + y
        tweet["hashtags"] = x
    return txt


""" adding tweet_urls field"""
def all_urls(parsed_tweet, sent):
    url = parsed_tweet.urls
    txt = ""
    if url is not None:
        x = ""
        for i in range(0,len(url)):
            y = url[i].match
            txt = re.sub(url[i].match,"",sent)
            x = x + " " + y
        tweet["tweet_urls"] = x
    return txt



""" adding tweet_emoticons field """
def emos(parsed_tweet, sent):
    emo = parsed_tweet.emojis
    smi = parsed_tweet.smileys
    txt = ""
    if (emo is not None) and (smi is not None):
        a = ""
        for i in range(0,len(emo)):
            b = emo[i].match
            sent = sent.replace(b,"")
            a = a + " " + b
        #print(b)
        x = ""
        for j in range(0,len(smi)):
            y = smi[j].match
            sent = sent.replace(y,"")
            x = x + " " + y
        tweet["tweet_emoticons"] = a + " " + x
        


    elif smi is not None:
        x = ""
        for i in range(0,len(smi)):
            y = smi[i].match
            sent = sent.replace(y,"")
            x = x + " " + y
        tweet["tweet_emoticons"] = x

    elif emo is not None:
        x = ""
        for i in range(0,len(emo)):
            y = emo[i].match
            sent = sent.replace(y,"")
            x = x + " " + y
        tweet["tweet_emoticons"] = x
    return sent

""" adding mentions field"""
def mentions(parsed_tweet,sent):
    men = parsed_tweet.mentions
    txt = ""
    if men is not None:
        x = ""
        for i in range(0,len(men)):
            y = re.sub("@","",men[i].match)
            txt = re.sub(men[i].match,"",sent)
            x = x + " " + y
        tweet["mentions"] = x
    return txt


""" adding customized text_xx field """
def text_field(language,sent):
    #english tweets
    if language == "en":
        tweet["tweet_lang"] = "en"        
        word_tokens = word_tokenize(sent)
        filtered_list = [w for w in word_tokens if not (w in stopwords_en.union(punct_set))]
        filtered_sent = ' '.join(filtered_list)
        tweet["text_en"] = filtered_sent
        
    
    #portuguese tweets
    elif language == "pt":
        tweet["tweet_lang"] = "pt"
        word_tokens = word_tokenize(sent)
        filtered_list = [w for w in word_tokens if not (w in stopwords_pt.union(punct_set))]
        filtered_sent = ' '.join(filtered_list)
        tweet["text_pt"] = filtered_sent
        tweet["country"] = "Brazil"

    #hindi tweets
    elif language == "hi":
        tweet["tweet_lang"] = "hi"
        word_tokens = word_tokenize(sent)
        filtered_list = [w for w in word_tokens if not (w in set(STOPS_LIST).union(punct_set))]
        filtered_sent = ' '.join(filtered_list)
        tweet["text_hi"] = filtered_sent
        tweet["country"] = "India"
    
    return
    

"""adding date field and verified field"""
def date_field():
    created_at = tweet["created_at"]
    ts = time.strftime('%Y-%m-%dT%H:00:00Z', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
    tweet["tweet_date"] = ts
    tweet["verified"] = tweet["user"]["verified"]
    

""" function to handle replies"""
def tweet_reply():
    #original tweet
    if(tweet["in_reply_to_user_id"] == "null"):
        tweet["tweet_text"] = tweet["text"]
        if "poi_name" not in tweet:
            tweet["poi_name"] = tweet["user"]["screen_name"]
            tweet["poi_id"] = tweet["user"]["id"]
        tweet["replied_to_tweet_id"] = "Null"
        tweet["replied_to_user_id"] = "Null"
    #if it's a reply
    else:
        tweet["tweet_text"] = tweet["text"]
        tweet["reply_text"] = tweet["text"]
        if "poi_name" not in tweet:
            tweet["poi_name"] = tweet["in_reply_to_screen_name"]
            tweet["poi_id"] = tweet["in_reply_to_user_id"]
        tweet["replied_to_tweet_id"] = tweet["in_reply_to_status_id"] 
        tweet["replied_to_user_id"] = tweet["in_reply_to_user_id"] 



#get json data
with open('narendramodi.json') as file:
    alltweets = file.readlines()
    for raw_tweet in alltweets:
        tweet = json.loads(raw_tweet)
        
        tweet_txt = tweet["text"]
        sent = tweet["text"]
        tweet_language = tweet["lang"]
        parsed = p.parse(tweet_txt)
        sent = emos(parsed,sent)
        sent = hashtags(parsed,sent)
        sent = mentions(parsed,sent)
        sent = all_urls(parsed,sent)
        
        text_field(tweet_language,sent)
        date_field()
        tweet_reply()
        saveFile = open('POI.json','a')
        json.dump(tweet, saveFile)
        saveFile.write("\n")
        
    saveFile.close()
    file.close()


