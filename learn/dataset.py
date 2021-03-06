# -*- coding: utf-8 -*-

"""
DataSet
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def read_dataset_csv(dataset_file):
    """
    pass file to pandas.read_csv
    """

    return DataSet(pd.read_csv(dataset_file))



class DataSet:

    """
    DataSet:

    DataSet is a class to handle training data. It used DataFrame from pandas as 
    basic structure. Both supervised dataset and unsupervised dataset can use this 
    class as a container. 
    

    """

    def __init__(self, dataset, bias=False, format=0):

        """
        Initialize the DataSet
        
        dataset is raw panda DataFrame or plain list which can be interpreted by DataFrame
        input and target will both be a numpy array
        targets should be set when dataset is used in supervised training by set_target

        Args:
        
        dataset: list or panda's dataframe
        bias: add a constant bias to dataset
        format: 0 to 2 are available. detailed format are followings.

        0) [[variables]]*cases
        1) [[input], [target]]*cases
        2) [inputs, targets]


        """

        # dataset pandas container
        self.dataset        = None
        self.input_dataset  = None
        self.target_dataset = None

        # numpy array container
        self.input          = None
        self.target         = None

        # input and target counts
        self.ni             = 0
        self.nt             = 0

        # supervise or unsupervise
        self.supervise      = False 

        # bias
        self.bias           = bias

        # index list for variables and targets
        self.vlst    = []
        self.ilst    = []
        self.tlst    = [] 

        # initialization
        if format == 0:


            self.dataset   = pd.DataFrame(dataset)
        
            # add constant bias to dataset as a variables

            if self.bias == True:
                bias_array = pd.DataFrame(np.ones(len(self.dataset)), columns=["Bias"])
                self.dataset = self.dataset.join(bias_array)

            # index list for variables and targets
            # all dataset will be set as variable initially

            self.vlst      = self.dataset.columns.tolist()
            self.ilst      = self.dataset.columns.tolist()
            self.tlst      = []

            # initially all variables in dataset will be set as input variables

            self.input_dataset = self.dataset[self.ilst]
            self.target_dataset = self.dataset[self.tlst]

            # input and target are generated from DataFrame to boost speed of processing

            self.input  = self.dataset.values
            self.target = None

            # number of variables and targets

            self.ni        = len(self.ilst)
            self.nt        = len(self.tlst)

            # supervise flag will set to be true when set_target is executed

            self.supervise = False


        elif format == 1:

            # [[input], [target] * cases

            # preprocess: combine input and target first

            nlst = []
            for p, q in dataset:
                nelem = p + q
                nlst.append(nelem)



            # count dimensions for input and target
            input_dim   = len(dataset[0][0])
            target_dim  = len(dataset[0][1])
            all_dim     = input_dim + target_dim

            # create dataset and columns

            self.dataset = pd.DataFrame(nlst)
            self.vlst    = [i for i in xrange(0, all_dim)]

            target_columns = [i for i in xrange(input_dim, all_dim)]


            # add constant bias to dataset as a variables

            if self.bias == True:
                bias_array = pd.DataFrame(np.ones(len(self.dataset)), columns=["Bias"])
                self.dataset = self.dataset.join(bias_array)
                self.vlst.append("Bias")
                target_columns.append("Bias")


            # set targets

            self.set_target(target_columns)

        elif format==2:

            # [inputs, targets]

            self.input_dataset   = pd.DataFrame(dataset[0])
            self.target_dataset  = pd.DataFrame(dataset[1])

            # add bias

            if self.bias == True:
                bias_array = pd.DataFrame(np.ones(len(self.dataset)), columns=["Bias"])
                self.input_dataset = self.input_dataset.join(bias_array)

            # recalculate columns names to prevent collision
            self.ilst      = ["Input_"]*self.input_dataset.shape[0]
            self.tlst      = ["Target_"]*self.target_dataset.shape[0]

            for i, v in enumerate(self.input_dataset.columns):
                self.ilst[i] += str(v)

            for i, v in enumerate(self.target_dataset.columns):
                self.tlst[i] += str(v)

            # reset columns name

            self.input_dataset.columns  = self.ilst
            self.target_dataset.columns = self.tlst

            # normal information

            self.dataset = pd.concat(self.input_dataset, self.target_dataset)
            self.vlst = self.ilst + self.tlst

            self.ni   = len(self.ilst)
            self.nt   = len(self.tlst)

            self.input  = self.input_dataest.values
            self.target = self.target_dataset.values

            self.supervise = True            

        else:
            return



    def __len__(self):
        
        return len(self.dataset)

    def __repr__(self):
        """
        return current status of DataSet
        """
        res = ""

        # basic information about the dataset
        
        if self.supervise:
            res += "supervised dataset\n"
        else:
            res += "unsupervised dataset\n"
        
        res += "cases: "+str(len(self.dataset))+"\n"
        res += "input  dimension: " + str(len(self.ilst))+", index: "+str(self.ilst)+"\n"
        if self.supervise:
            res += "target dimension: "+str(len(self.tlst))+", index: "+str(self.tlst)+"\n"

        res += "\n"

        # add several cases information

        if self.supervise:
            input_str  = map(str.rstrip, str(self.input_dataset).split("\n"))
            target_str = map(str.rstrip, str(self.target_dataset).split("\n"))

            for i in xrange(min(len(input_str), len(target_str))):
                s1 = input_str[i]
                s2 = target_str[i]
                if s1=="" and s2=="":
                    res += "\n"
                else:
                    res += s1 + "   |   "+s2 + "\n"

        else:
            res += str(self.input_dataset)


        #TODO: ouput will collasped when dimensions is large

        return res

    def __getitem__(self, i):
        """
        getitem will fetch training case with index i
        if it is a supervise dataset getitem will return  a [input[i], target[i]]
        else it will return only input[i]
        """
        
        if self.supervise:
            return [self.input[i], self.target[i]]
        else:
            return self.input[i]

    def __setitem__(self, i, v):
        self.dataset[i] = v


    def get_target(self, i):
        return self.target[i]


    def get_input(self, i):
        return self.input[i]


    def set_target(self, dex, setinput=True):
        """
        set target by index from self.dataset
        This automaticly set input variables that are not contained in target
        """

        if isinstance(dex, list):
            self.tlst = dex
        else:
            self.tlst = [dex]

        if setinput == True:
            self.ilst = [x for x in self.vlst if x not in self.tlst]

        self.target_dataset = self.dataset[self.tlst]
        self.input_dataset  = self.dataset[self.ilst]
        
        self.target    = self.target_dataset.values
        self.input     = self.input_dataset.values
        self.supervise = True


    def set_target_startswith(self, prefix, setinput=True):
        """
        set target by prefix
        index whose prefix matches with the argument will be set as target
        """

        tlst = [dex for dex in self.vlst if isinstance(dex, str) and dex.startswith(prefix)]
        self.set_target(tlst, setinput)


    def set_target_endswith(self, suffix, setinput=True):
        """
        set target by suffix
        """

        tlst = [dex for dex in self.vlst if isinstance(dex, str) and dex.endswith(suffix)]
        self.set_target(tlst, setinput)

    
    def set_input_startswith(self, prefix):
        """
        set input variables by prefix
        """
                
        ilst = [dex for dex in self.vlst if isinstance(dex, str) and dex.startswith(prefix)]
        self.set_input(ilst)

    def set_input_endswith(self, suffix):
        """
        set input variables by suffix
        """

        ilst = [dex for dex in self.vlst if isinstance(dex, str) and dex.endswith(suffix)]
        self.set_input(ilst)


    def set_input(self, dex):

        if isinstance(dex, list):
            self.ilst = dex
        else:
            self.ilst = [dex]

        self.input_dataset = self.dataset[self.ilst]
        self.input = self.dataset[dex].values

    def del_target(self, dex):
        """
        delete variables from target
        """

        self.tlst.remove(dex)
        self.target_dataset = self.dataset[self.tlst]
        self.target = self.target_datset.values

    def del_input(self, dex):
        
        self.ilst.remove(dex)
        self.input_dataset = self.dataset[self.ilst]
        self.input = self.input_dataset.values


    def add_dataset(self, dataset):
        """
        Add variables to dataset, variables will be set to be members of input, 
        remember to reset input or target if necessary
        """
        
        self.dataset = self.dataset.join(dataset)
        self.vlst.extend(dataset.columns.tolist())
        self.ilst.extend(dataset.columns.tolist())

        self.input_dataset  = self.dataset[self.ilst]
        self.target_dataset = self.dataset[self.tlst]

        self.input  = self.input_dataset.values
        self.target = self.target_dataset.values

        self.ni = len(self.ilst)
        self.nt = len(self.tlst)


    def add_bias(self):
        """
        Add bias to dataset
        """

        bias_array = pd.DataFrame(np.ones(len(self.dataset)), columns=["Bias"])
        self.dataset = self.dataset.join(bias_array)
        self.vlst.append("Bias")
        self.ilst.append("Bias")

        self.input_dataset = self.dataset[self.ilst]
        self.input = self.input_dataset[self.ilst]
        self.ni = len(self.ilst)


    def clear_target(self):
        """
        clear fields of targets

        """

        self.input_dataset  = self.dataset
        self.target_dataset = None

        self.input  = self.dataset.values
        self.target = None

        self.supervise = False



    def normalize_factor(self, dex, factors=None, remove_prev_factor=True):
        """
        Tranform factors into 1-to-n encodings,
        for examples, ["male", "female"] will be transform to [[1,0],[0,1]]
        if factors are None, n will be numbers of all possible factors
        """

        factor_cnt = 0
        fdict = dict()

        # register all factors
        
        if factors == None:
            for v in self.dataset[dex]:
                if not fdict.has_key(v):
                    fdict[v] = factor_cnt
                    factor_cnt += 1

        else:
            factor_cnt = len(factors)
            for i,v in enumerate(factors):
                fdict[v] = i


        # remove previous factors
        if remove_prev_factor:
            if dex in self.vlst:
                self.vlst.remove(dex)
            if dex in self.ilst:
                self.ilst.remove(dex)
            if dex in self.tlst:
                self.tlst.remove(dex)

            

                
        # transform factors into list
        
        flst = []
        for v in self.dataset[dex]:
            nlst = [0]*factor_cnt
            nlst[fdict[v]] = 1
            flst.append(nlst)

        # create columns names ( dex + "_" + factor )

        clst = [str(dex)]*factor_cnt
        for i,v in fdict.items():
            clst[v] += "_"+str(i)


        # create pandas dataframe and add dataset
    
        factor_dataframe = pd.DataFrame(flst, columns=clst)
        self.add_dataset(factor_dataframe)


        
    def normalize_minmax_value(self, dex, max_value=None, min_value=None):

        """
        scale all values to (-1, 1)

        """


        if max_value == None:
            max_value = self.dataset[dex].max()
        
        if min_value == None:
            min_value = self.dataset[dex].min()

        mean_value = (max_value + min_value)/2.0
        diff_value = max_value - min_value


        # update dataset
        self.dataset[dex]   = (self.dataset[dex] - mean_value)/diff_value
        self.input_dataset  = self.dataset[self.ilst]
        self.target_dataset = self.dataset[self.tlst]

        # update matrix
        self.input   = self.input_dataset.values
        self.target  = self.target_dataset.values


    def normalize_affine_value(self, dex, multi_value=1.0, bias_value=0.0):
        """
        transfrom all value to a*v+b
        """

        # update dataset
        self.dataset[dex]   = (self.dataset[dex]*multi_value)+bias_value
        self.input_dataset  = self.dataset[self.ilst]
        self.target_dataset = self.dataset[self.tlst]

        # update matrix
        self.input   = self.input_dataset.values
        self.target  = self.target_dataset.values

        
    def normalize_gauss_value(self, dex, mean_value=None, dev_value=None):
        
        if mean_value == None:
            mean_value = self.dataset[dex].mean()

        if dev_value == None:
            dev_value = self.dataset[dex].std()

        
        # update dataset
        self.dataset[dex] = (self.dataset[dex] - mean_value)/dev_value
        self.input_dataset  = self.dataset[self.ilst]
        self.target_dataset = self.dataset[self.tlst]

        # update matrix
        self.input   = self.input_dataset.values
        self.target  = self.target_dataset.values



    def normalize_boolean(self, dex):

        # update dataset
        self.dataset[dex] = self.dataset[dex].astype(float)
        self.input_dataset  = self.dataset[self.ilst]
        self.target_dataset = self.dataset[self.tlst]

        # update matrix
        self.input   = self.input_dataset.values
        self.target  = self.target_dataset.values

        
    def shuffle_cases(self):
        self.dataset = self.dataset.reindex(np.random.permutation(self.dataset.index))

        # reset input and target
        self.input_dataset  = self.dataset[self.ilst]
        self.target_dataset = self.dataset[self.tlst]

        self.input  = self.input_dataset.values
        self.target = self.target_dataset.values

    def split(self, ratio=[0.8, 0.2, 0.0], shuffle=True):

        """
        Split data into three(two) parts
    
        Training dataset ( default 80% )
        Validate dataset ( default 20% )
        Test dataset( default 0% )

        """

        # shuffle all cases
        if shuffle:
            self.shuffle_cases()


        # split all dataset into three cases

        train_threshold    = ratio[0]
        validate_threshold = ratio[0] + ratio[1]
        test_threshold     = ratio[0] + ratio[1] + ratio[2]


        train_lst    = []
        validate_lst = []
        test_lst     = []


        if shuffle:
            self.shuffle_cases()

        for i in xrange(len(self.dataset)):
            r = np.random.random()
            if r < train_threshold:
                train_lst.append(i)
            elif r < validate_threshold:
                validate_lst.append(i)
            else:
                test_lst.append(i)


        # create DataSet respectively

        train_dataset      = DataSet(self.dataset.ix[train_lst])
        validate_dataset   = DataSet(self.dataset.ix[validate_lst])
        test_dataset       = DataSet(self.dataset.ix[test_lst])

        # set target and variables for three dataset

        train_dataset.set_input(self.ilst)
        validate_dataset.set_input(self.ilst)
        test_dataset.set_input(self.ilst)

        train_dataset.set_target(self.tlst, False)
        validate_dataset.set_target(self.tlst, False)
        test_dataset.set_target(self.tlst, False)

        return train_dataset, validate_dataset, test_dataset



    def to_list(self):
        """
        transform dataset into plain list
        if dataset is supervised dataset, the output will be [[[case1 input],[case1 target]], ...]
        else the output will be [[case1 input], ...]
        """

        rlst = []
        if self.supervise:
            for i in xrange(len(self.input)):
                rlst.append([self.input[i].tolist(), self.target[i].tolist()])
        else:
            for i in xrange(len(self.input)):
                rlst.append(self.input[i].tolist())


        return rlst

    def save_dataset(self, filename):
        """
        TODO
        """
        w = open(filename, "w")


        
        

        







