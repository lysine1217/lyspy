#-*- coding: utf-8 -*-

"""
Vocabulary
"""
import os
from collections import defaultdict
import numpy as np

import lyspy.data.en


class Vocabulary:

    """
    Vocabulary is a data structure to save the basic word level information.
    It can used to process sentences to transform them into integers or vectors

    """    

    def __init__(self, v=None, stopwords=None):

        """
        Set vocabularies and stopwords
        """

        self.word2dex = dict()
        self.dex2word = dict()
        self.wordnum  = 0

        if v!= None:
            self.set_vocabulary(v)


        self.is_stopword = dict()
        
        if stopwords != None:
            self.set_stopword(stopwords)


        """
        Optional Word Information

        - cnt: counts for each word ( may be used in tfidf )
        - word2vec: word vectors ( may be used in semantic composition )

        """

        self.wordcnt  = defaultdict(int)
        self.word2vec = dict()
        

    def __getitem__(self, sth):

        """
        Get item method just change word and its index currently

        """

        if isinstance(sth, str) :
            if sth in self.word2dex:
                return self.word2dex[sth]
            else:
                return -1
        elif isinstance(sth, int):
            if sth in self.dex2word:
                return self.dex2word[sth]
            else:
                return False
        else:
            return False


    def set_vocabulary(self, v):

        if isinstance(v, list):
            for i, w in enumerate(v):
                self.word2dex[w] = i
                self.dex2word[i] = w

        if isinstance(v, dict):
            for i, w in enumerate(v.keys()):
                self.word2dex[w] = i
                self.dex2word[i] = w
            

    def set_stopwords(self, stopwords):
        for word in stopwords:
            self.is_stopword[word] = True



    def read_vectors(self, filepath=None):

        """
        Read default vectors saved in data/en/
        """

        if filepath==None:
            filepath = os.path.join(os.path.dirname(lyspy.data.en.__file__), "vectors.txt")
            
        f = open(filepath, "r").readlines()
        for line in f:
            line = line.split()
            word = line[0]
            vec  = map(float, line[1:])
            self.word2vec[word] = vec
            

    def read_vocabulary(self, filepath=None):
        
        """
        Read default vocabularies
        """

        if filepath==None:
            filepath = os.path.join(os.path.dirname(lyspy.data.en__file__), "top1000_nostop.txt")

        f = map(str.strip(), open(filepath, "r").readlines())
        self.set_vocabulary(f)


        
    def process(self, doc, cap=0):

        """
        This function counts words in the documents
        and register words that did not appear before
        
        """

        for wd in doc:
            if wd in self.is_stopword:
                continue

            if wd not in self.word2dex:
                self.word2dex[wd] = self.wordnum
                self.dex2word[self.wordnum] = wd
                self.wordnum += 1

            self.wordcnt[wd] += 1


    def transform(self, doc):
        
        lst_result = []
        for doc in docs:
            lst_wd = []
            for wd in doc:
                if wd in self.dic_words:
                    lst_wd.append(self.dic_words[wd])
                else:
                    continue
            lst_result.append(lst_wd)
        return lst_result
                    

                
            
            
        
        
