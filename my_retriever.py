from __future__ import division
import math


class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    # Method to apply query to index
    def forQuery(self,query):
        dic = {}
        candidate = self.getCandidate(query)
        
        
        #to calculate the binary term weighting 
        if self.termWeighting == 'binary':
            #to calculate the term weighting of candidate documents
            for i in candidate:
                cos = 0
                length = 0
                #to calculate the length of document
                #if there is term in index, length plus 1
                for term in self.index.keys():
                    if i in self.index[term].keys():
                        length +=1
                        #to get the score
                        #if the term is in qury, score plus 1
                        if term in query.keys():
                            cos += 1
                length = math.sqrt(length)
                dic[i] = cos/length 
                

        #to calculate the tf term weighting
        if self.termWeighting == 'tf': 
            #to calculate the term weighting of candidate documents
            for i in candidate:
                cos = 0
                length = 0   
                #to calculate the length of document
                #if there is term in index, length plus index[term][i] ** 2
                for term in self.index.keys():
                    if i in self.index[term].keys():
                        length += self.index[term][i] * self.index[term][i]
                        #to get the score
                        #if the term is in qury, score plus index[term][i] * query[term]
                        if term in query.keys():
                            cos += self.index[term][i] * query[term]
                #print('i=' ,i,'length =', length,'cos = ',cos)
                length = math.sqrt(length)
                dic[i] = cos/length
                
                
        #to calculate the tfidf term weighting                
        if self.termWeighting == 'tfidf':
            #use function getSizeOfCollection() to compute the number of documents in collection
            d = self.getSizeOfCollection() 
            for i in candidate:
                cos = 0
                length = 0
                n = 0                
                for term in self.index.keys():
                    if i in self.index[term].keys():
                        #to get the df value of the term
                        n = len(self.index[term]) 
                        idf = math.log(d/n)
                        tfidf = idf * self.index[term][i]
                        length += tfidf * tfidf
                        if term in query.keys():
                            cos += tfidf * query[term]*idf
                #print('i=' ,i,'length =', length,'cos = ',cos)
                length = math.sqrt(length)
                dic[i] = cos/length
                
                
        #use function getTop10() get the top 10 of document in term weighting         
        top10 = self.getTop10(dic)
        return top10  



    #to get the top 10 of document in term weighting    
    def getTop10(self,dic): 
        orderDictList = sorted(dic.items(), key = lambda x:x[1], reverse = True)
        top = [x[0] for x in orderDictList[:10]]
        return top


    
    #to get the document which contains one or more words in query 
    def getCandidate(self, query):
        candidate = []
        for word in query.keys():
            if word in self.index.keys():
                for docid in self.index[word].keys():
                    candidate += [docid]
        return candidate
 
    
    
    #total number of documents in collection
    def getSizeOfCollection(self):
        allDocIds = []
        for dic in list(self.index.values()):
            docids = list(dic.keys())
            allDocIds += docids
        allDocIds = set(allDocIds)
        sizeOfCollection = max(allDocIds)
        return sizeOfCollection