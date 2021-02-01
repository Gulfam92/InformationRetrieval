from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_TOKEN=""
ACCESS_SECRET=""

class listener(StreamListener):

    def on_data(self, data):
        
        try:
            if 'RT @' not in data:
                print (data)
                with open("tweets_POI_1.json", 'a') as tn:
                        tn.write (data)

        except Exception as ex:
            print (ex)
            
        return(True)

    def on_error(self, status):
        print (status)


auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
                        
twitterStream = Stream(auth, listener())
twitterStream.filter(follow=["18839785","1447949844","1346439824","405427035",
                             "111944435","1339835893","15764644","216776631",
                             "30354991","25073877","1028620936176656384","13124602",
                            "762402774260875265","105155795","131574396"],
    languages=['hi','pt','en'])


