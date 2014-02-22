#!/usr/bin/python
#-*- coding: utf-8 -*-
#
#Define vocabulary and stopwords for LDA
#

import numpy as np

class Vocabulary:

    def __init__(self, v, stopwords=[]):
        self.v = v
        self.lst_stopwords = stopwords
        self.dic_stopwords = dict()
        self.cnt_words     = dict()
        
        self.frq_words    = []
        self.dic_words     = dict()

        for wd in self.lst_stopwords:
            self.dic_stopwords[wd] = 1

    def __getitem__(self, sth):
        if isinstance(sth, str) :
            if sth in self.dic_words:
                return self.dic_words[sth]
            else:
                return -1
        elif isinstance(sth, int):
            if sth>=0 and sth < len(self.frq_words):
                return self.frq_words[sth]
            else:
                return False
        else:
            return False

    def process_documents(self, docs):

        """
        Count words in documents 
        and sort them to index the top frequent v words
        
        """

        for doc in docs:
            for wd in doc:
                if wd in self.dic_stopwords:
                    continue
                if wd in self.cnt_words:
                    self.cnt_words[wd] += 1
                else:
                    self.cnt_words[wd] = 1

        self.frq_pairs = sorted(self.cnt_words.items(), key=lambda x:-x[1])
        self.frq_words = [wd[0] for wd in self.frq_pairs]
        
        if(len(self.frq_words) > self.v):
            self.frq_words = self.frq_words[:self.v]

        for i, wd in enumerate(self.frq_words):
            self.dic_words[wd] = i

    def read_nonstopwords(self, nonstopwords):
        
        self.frq_words = nonstopwords
        if len(self.frq_words) > self.v:
            self.frq_words = self.frq_words[:self.v]

        for i, wd in enumerate(self.frq_words):
            if wd not in self.dic_words:
                self.dic_words[wd] = i


    def transform_documents(self, docs):
        
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
                    

                
            
            
        
        