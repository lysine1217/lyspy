#!/usr/bin/python2.7
#
# KMeans
#


import numpy as np

class KMeans:

    # lst should be reformed like [[1.0,2.0],[3.0,4.0]]
    def __init__(self, lst=[], k=2):

        if lst != [] :
            self.setdata(lst, k)

    def setdata(self, lst, k=None):

        self.lst  = np.array(lst)
        self.n    = len(lst)
        self.dim  = len(lst[0])
        self.nd   = [0]*self.n
        self.kc   = []

        self.err  = 0.0
        self.perr = 0.0

        if k != None:
            self.k = k


        # set center of i cluster to random choosed point
        for i in xrange(self.k):
            self.kc.append(lst[np.random.randint(self.n)])

        # change its type into numpy array
        self.kc   = np.array(self.kc)


    def train(self, iterations):

        for ii in xrange(iterations):

            flag = 0

            # expectation phases
            for i in xrange(self.n):
                min_distance = 100000000
                for j in xrange(self.k):
                    ij_distance = np.linalg.norm(self.lst[i]-self.kc[j])
                    if ij_distance < min_distance:
                        min_distance = ij_distance
                        self.nd[i] = j
                        flag = 1

            if(flag==0):
                return ;

                        
            # maximization phases
            self.kcount = [0]*self.k
            self.ksum   = [[0.0]*self.dim]*self.k
        
            for i in xrange(self.n):
                self.kcount[self.nd[i]] += 1
                self.ksum[self.nd[i]] += self.lst[i]

            for i in xrange(self.k):
                self.kc[i] = self.ksum[i] / self.kcount[i]

        
            # calc error
            self.err = 0.0

            for i in xrange(self.n):
                self.err += np.linalg.norm(self.lst[i]-self.kc[self.nd[i]])

            print "error %.6lf" %self.err

            # check convergence
            
            if np.abs(self.err - self.perr) < 0.0001:
                print "Convergence"
                break
            else:
                self.perr = self.err


    def predict(self, lst):

        rlst = [0]*len(lst)
        

        # find the center for each item in the list
        for i, item in enumerate(lst):
            min_distance = 100000000
            for j in xrange(self.k):
                ij_distance = np.linalg.norm(np.array(item) - self.kc[j])
                if ij_distance < min_distance:
                    min_distance = ij_distance
                    rlst[i] = j


        return rlst


    def demoForKmeans(self):

        # randomly genrate two group for demo
        lst = []
        for i in xrange(100):
            lst.append(np.random.normal(0,1,2))

        for i in xrange(100):
            lst.append(np.random.normal(3,1,2))

        np.random.shuffle(lst)
        self.setdata(lst, 2)

        # train for the list
        self.train(100)

        # display points from matplotlib

        import matplotlib.pylab as pylab

        xlst = self.lst.T[0]
        ylst = self.lst.T[1]

        for i in xrange(len(xlst)):
            x = xlst[i]
            y = ylst[i]

            if self.nd[i]==0:
                pylab.scatter(x,y,color="blue")
            else:
                pylab.scatter(x,y,color="green")

    
        for i in xrange(2):
            pylab.scatter(self.kc[i][0], self.kc[i][1], s=30, color="red",marker="v")

            
