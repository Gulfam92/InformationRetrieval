import json

with open('/datafile.json') as f:
    alltweets = f.readlines()
    org_tweet = []
    counter = dict()
    for raw_tweet in alltweets:
        tweet = json.loads(raw_tweet)
        
        if (tweet["in_reply_to_user_id"] is None):
            if(tweet["user"]["id"] == 18839785):
                #print("Narendra Modi tweets:")
                org_tweet.append(tweet["id"])
                
                f1 = open("datafile.json",'a')
                json.dump(tweet, f1)
                f1.write("\n")
                f1.close()
                
    print(org_tweet," length: ",len(org_tweet))    
    
    n = len(org_tweet)
    for i in range(0,n):
        counter[org_tweet[i]] = 0

    #counter
    for raw_tweet in alltweets:
        tweet = json.loads(raw_tweet)
        
        if (tweet["in_reply_to_user_id"] == 18839785):
            for i in range(0,len(org_tweet)):
                if(tweet["in_reply_to_status_id"] == org_tweet[i]):
                    counter[org_tweet[i]] = counter[org_tweet[i]] + 1
                
    print(counter,"length: ",len(counter))
    tot_count = 0
    for i in range(0,len(org_tweet)):
        tot_count = tot_count + counter[org_tweet[i]]
    print(tot_count)
    
    for raw_tweet in alltweets:
        #print(type(raw_tweet))
        #print(punct_set)
        tweet = json.loads(raw_tweet)
        reply_id = tweet["in_reply_to_status_id"]
        for i in range(0,n):
                if(counter[org_tweet[i]]>=20):
                    
                    x = org_tweet[i]
    
                    if(reply_id == x):
                        f1 = open("datafile.json",'a')
                        json.dump(tweet, f1)
                        f1.write("\n")
                        f1.close()
                   
    f.close()