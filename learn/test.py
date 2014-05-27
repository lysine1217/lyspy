# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame, Series

from lyspy.learn.dataset import DataSet
from lyspy.learn.error_model import *

"""
Test is a class to test supervised training
It summarize results predicts by models and DataSet's target

"""


class Test:

    def __init__(self, model=None, dataset=None, error_func=square_errors):

        self.model      = model
        self.dataset    = dataset
        self.input      = self.dataset.input
        self.target     = self.dataset.target
        
        self.error_func = error_func

        if self.model != None and self.dataset != None:
            if error_func == class_errors:
                self.test(binary=1)
            else:
                self.test()


    def test(self, binary=0):

        self.result      = self.model.predict(self.dataset, binary)
        self.sum_error   = self.error_func(self.result, self.target)

        print "Test    cases : ", len(self.result)
        print "Sum     Error : ", self.sum_error * len(self.result)
        print "Average Error : ", self.sum_error
        
        
    def compare(self, index=None):
        """
        compare results and targets
        it is possible to check specific case by setting index

        """

        if index==None:
            index = range(len(self.dataset))
        elif isinstance(index, int):
            index = [index]

        for i in index:
            print "Case "+str(i)+" : "
            print "- input : ", self.input[i]
            print "- target: ", self.target[i]
            print "- result: ", self.result[i]
            print "- error : ", self.target[i]-self.result[i]
            print ""

