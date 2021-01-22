# -*- coding: utf-8 -*-


import json
import urllib
# if you are using python 3, you should 
import urllib.request 


IRModels = ['BM25IRMOD','DFRIRMOD3','LMIRMOD1']

for modname in IRModels:
    with open("/home/gulfam_ubuntu/Desktop/Gulfam-Projects/IR/proj3/upload/outfile3_"+modname+".txt","a") as outfn:
        with open("/home/gulfam_ubuntu/Desktop/Gulfam-Projects/IR/proj3/upload/test_queries.txt") as testqry:
            x = testqry.readline()
            while x:
                x = x.strip('\n').replace(":","")
                splt_qry = x.split(" ",1)

                qid = splt_qry[0]
                qrytext = splt_qry[1]
                
                qrytext_url = 'text_en: ('+qrytext+')'+'OR '+'text_ru: ('+qrytext+')'+'OR '+'text_de: ('+qrytext+')'
                solr_qry = urllib.parse.quote(qrytext_url)
                inurl = 'http://18.223.168.208:8983/solr/'+modname+'/select?q='+solr_qry+'&fl=id%2Cscore&wt=json&indent=true&rows=20'

                # write output result data in the given trec_eval format
                data = urllib.request.urlopen(inurl).read()
                docs = json.loads(data)['response']['docs']
                
                # the ranking should start from 1 and increase
                rank = 1
                for doc in docs:
                    outfn.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + modname + '\n')
                    rank += 1
                x = testqry.readline()
    outfn.close()            



