import sys
import operator


def main(arguments):
  f = arguments[3]      #Command line argument initialization
  f1 = arguments[2]
  with open(arguments[1]) as file_read:

#initialize all the required dictionaries
    inv_dict = dict()
    df_value = dict()
    idf_value = dict()
    tfdoc_dict = dict()
    TFIDF_score = dict()
    doc_count = 0

#Read the input corpus file and create inverted index of the terms
    for line in file_read:
      line = line.rstrip()
      split_line = line.split('\t')
      doc_id = split_line[0]
      doc_terms = split_line[1]
      doc_count += 1
      terms = doc_terms.split(" ") #split terms on whitespace
      tfdoc_dict[doc_id] = dict()  #Calculate TF and store it
      #print(doc_id)
      #print(terms)
      for word in terms:
        idf_value[word] = 0
        #Count the term frequency and add it
        if word not in tfdoc_dict[doc_id]:
          tfdoc_dict[doc_id][word] = 1
        else:
          tfdoc_dict[doc_id][word] += 1
        
        #Calculate the doc frequency for the term
        if word not in df_value:
          df_value[word] = 1
        else:
          if(doc_id not in inv_dict[word]):
            df_value[word] +=1

        #add all the terms of the document into inverted index
        if word not in inv_dict:
          inv_dict[word] = []
          inv_dict[word].append(doc_id)

        else:
          if(doc_id not in inv_dict[word]):
            inv_dict[word].append(doc_id)
              
#############################################################

  #create TF dictionary and store the TF values
  terms_totalcount = dict()
  for i in tfdoc_dict:
    terms_totalcount[i] = 0
    for j in tfdoc_dict[i]:
      terms_totalcount[i] += tfdoc_dict[i][j]

  for i in tfdoc_dict:
    for j in tfdoc_dict[i]:
      tfdoc_dict[i][j] = tfdoc_dict[i][j]/terms_totalcount[i]

  #create IDF dictionary and store the IDF values
  terms_lists = list(inv_dict.keys())
  for k in terms_lists:
    idf_value[k] = doc_count/df_value[k]

  #Calculate weights for TF-IDF
  for i in tfdoc_dict:
    TFIDF_score[i] = dict()
    for j in tfdoc_dict[i]:
      TFIDF_score[i][j] = tfdoc_dict[i][j] * idf_value[j]
  
  #Write GetPostings for the given query texts in the file
  with open(f) as query_file:
    for line1 in query_file:
      line1 = line1.rstrip()
      terms1 = line1.split(" ")
      #print(terms1)      
      for term1 in terms1:
        ofile = open(f1,"a")
        ofile.write("GetPostings\n")
        ofile.write(term1+"\n")
        posting_val = " ".join(inv_dict[term1])
        ofile.write("Postings list:"+" "+posting_val)
        ofile.write("\n")
        ofile.close()
        
      DaatAnd(inv_dict,line1,TFIDF_score,arguments[2])
      DaatOr(inv_dict,line1,TFIDF_score,arguments[2])
        
      ofile1 = open(f1,"a")  
      ofile1.write("\n")
      
      ofile1.close()
  query_file.close()
      
#find DaatAnd results
def DaatAnd(inv_value,l,TFIDF_score,outfile):
  input_query = dict()
  result = []
  l = l.rstrip()
  split_term = l.split(" ")
  inc = 0
  for term in split_term:
    input_query[term] = inv_value[term]

  for k in range(len(split_term)-1):
    list1 = input_query[split_term[k]]
    list2 = input_query[split_term[k+1]]

    if (inc > 0):
      list1 = result

    #perform intersection operation on the posting lists
    result_new = []
    a = 0
    b = 0
    while(a<len(list1) and b<len(list2)):
      if(list1[a] == list2[b]):
        inc = inc+1
        result_new.append(list1[a])
        a = a+1
        b = b+1
      else:
        inc = inc+1
        if(list1[a]<list2[b]):
          a = a+1
        else:
          b = b+1
      result = result_new

  print_and(result, outfile, split_term, inc, inv_value, l, TFIDF_score)
  
    
def print_and(result, outfile, split_term, inc, inv_value, l, TFIDF_score):
  result_str = " ".join(result)
  f = open(outfile,"a")
  f.write("DaatAnd")
  if(len(result)>0):
    f.write("\n"+" ".join(split_term))
    f.write("\nResults:"+" "+result_str)
    f.write("\nNumber of documents in results:"+" "+str(len(result)))
    f.write("\nNumber of comparisons:"+" "+str(inc))
    rank_list = TFIDF_rank(inv_value, l, result, TFIDF_score, outfile)
    f.write("\nTF-IDF")
    f.write("\nResults:"+" "+rank_list)
  else:
    f.write("\n"+" ".join(split_term))
    f.write("\nResults: empty")
    f.write("\nNumber of documents in results: 0")
    f.write("\nNumber of comparisons:"+str(inc))
    f.write("\nTF-IDF")
    f.write("\nResults: empty")
  f.close()

#find Daat0r results
def DaatOr(inv_value,l,TFIDF_score,outfile):
  input_query = dict()
  result = []
  l = l.rstrip()
  split_term = l.split(" ")
  count_val = 0
  for term in split_term:
    input_query[term] = inv_value[term]

  for k in range(len(split_term)-1):
    list3 = input_query[split_term[k]]
    list4 = input_query[split_term[k+1]]

    if (count_val > 0):
      list3 = result
    
    #perform union operation on the posting lists
    result_new = []
    a = 0
    b = 0
    
    while(a<len(list3) and b<len(list4)):
      if(list3[a] == list4[b]):
        count_val = count_val+1
        result_new.append(list3[a])
        a = a+1
        b = b+1
      else:
        count_val = count_val+1
        if(list3[a]<list4[b]):
          result_new.append(list3[a])
          a = a+1
        else:
          result_new.append(list4[b])
          b = b+1
    
    while(a<len(list3)):
      count_val = count_val + 1
      result_new.append(list3[a])
      a = a+1
    while(b<len(list4)):
      count_val = count_val + 1    
      result_new.append(list4[b])
      b = b+1
      
    result = result_new
    
  print_or(result, outfile, split_term, count_val, inv_value, l, TFIDF_score)


def print_or(result, outfile, split_term, count_val, inv_value, l, TFIDF_score):
  result_str = " ".join(result)
  f = open(outfile,"a")
  f.write("\nDaatOr")
  if(len(result)>0):
      f.write("\n"+" ".join(split_term))
      f.write("\nResults:"+" "+str(result_str))
      f.write("\nNumber of documents in results:"+" "+str(len(result)))
      f.write("\nNumber of comparisons:"+" "+str(count_val))
      rank_list = TFIDF_rank(inv_value,l, result, TFIDF_score, outfile)
      f.write("\nTF-IDF")
      f.write("\nResults:"+" "+rank_list)
      f.write("\n")
  else:
      f.write("\n"+" ".join(split_term))
      f.write("\nResults: empty")
      f.write("\nNumber of documents in results: 0")
      f.write("\nNumber of comparisons:"+" "+str(count_val))
      f.write("\nTF-IDF")
      f.write("\nResults: empty")
      f.write("\n")
  f.close()
  
def TFIDF_rank(inv_value,l, result, TFIDF_score, outfile):
  list_tfidf = []
  a = 0
  score_value = dict()
  l = l.rstrip()
  query = l.split(" ")
  for value in result:
    score_value[value] = 0
    for term in query:
      if(value in inv_value[term]):
        score_value[value] += TFIDF_score[value][term]

  #Sort the TF-IDF values based on ranks 
  rank_sorting = sorted(score_value.items(), key = operator.itemgetter(1), reverse = True)

  for b in rank_sorting:
      list_tfidf.append(b[a])

  list_tfidf_str = " ".join(list_tfidf)
  return list_tfidf_str


if __name__== "__main__":
  arguments = sys.argv
  main(arguments)
