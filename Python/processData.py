import numpy as np
import os
import pickle
import time

class processData(object):
    def __init__(self, trainningDir, movieTitle, probe, qualifying):
        """
        :param trainningDir:
        :param movieTitle:
        :param probe:
        :param qualifying:
        :return:
        There are 17770 movies (from 1 to 17770) and 2649429 customers (from 1 to 2649429)
        """
        self.trainningDir = trainningDir
        self.movieTitle = movieTitle
        self.probe = probe
        self.qualifying = qualifying
        # parameter
        self.customer = 2649429
        self.movieNum = 100 # 17770
        self.movieLimit = 'mv_0000100.txt'
        # data file
        self.probeDict = {}
        self.qualifyDict = {}
        self.movieDict = {}
        self.ratingData = 0 # lazy evaluation
        # self.ratingData = np.zeros((self.customer, self.movieNum))

    def loadProbe(self):
        fdProbe = open(self.probe)
        key = -1
        list = []
        while True:
            line = fdProbe.readline().strip()
            if line != "":
                # print line
                if line[-1] == ":":
                    if key != -1:
                        self.probeDict[key] = list
                    key = int(line[:-1])
                    list = []
                else:
                    list.append(int(line))
            else:
                break
        self.probeDict[key] = list
        fdProbe.close()
        if os.path.exists('./data/dumpfile/probeDict.pkl'):
            os.remove('./data/dumpfile/probeDict.pkl')
        output = open('./data/dumpfile/probeDict.pkl','wb')
        pickle.dump(self.probeDict, output)
        output.close()
        # print self.probeDict

    def loadQualify(self):
        fdQualify = open(self.qualifying)
        key = -1
        list = []
        while True:
            line = fdQualify.readline().strip()
            if line != "":
                if line[-1] == ":":
                    if key != -1:
                        self.qualifyDict[key] = list
                    key = int(line[:-1])
                    list = []
                else:
                    customerId, date = line.split(",")
                    list.append(int(customerId))
            else:
                break

        self.qualifyDict[key] = list
        fdQualify.close()
        if os.path.exists('./data/dumpfile/qualifyDict.pkl'):
            os.remove('./data/dumpfile/qualifyDict.pkl')
        output = open('./data/dumpfile/qualifyDict.pkl','wb')
        pickle.dump(self.qualifyDict, output)
        output.close()
        # print self.qualifyDict

    def loadMovie(self):
        fdMovie = open(self.movieTitle)
        while True:
            line = fdMovie.readline().strip()
            if line != "":
                # print line
                movieID, year, name = line.split(",")[0:3] # No. 72 can be split in four part
                self.movieDict[int(movieID)] = (year, name)
            else:
                break
        fdMovie.close()
        if os.path.exists('./data/dumpfile/movieDict.pkl'):
            os.remove('./data/dumpfile/movieDict.pkl')
        output = open('./data/dumpfile/movieDict.pkl','wb')
        pickle.dump(self.movieDict, output)
        output.close()
        # print self.movieDict

    def loadRating(self):
        self.ratingData = np.zeros((self.customer, self.movieNum))
        # print os.getcwd()
        files = os.listdir(self.trainningDir)
        # print files
        for file in files:
            # considering the memory size of computer, only use the first 100 movies
            if file > self.movieLimit:
                break
            key = -1
            fd = open(self.trainningDir + file)
            while True:
                line = fd.readline().strip()
                if line == "":
                    break
                if line[-1] == ":":
                    key = int(line[:-1])
                else:
                    customer, rate, date = line.split(',')
                    if int(customer) <= self.customer:
                        self.ratingData[int(customer)-1][key-1] = int(rate)
                        print "customer: " + str(int(customer)-1) + " movie: " + str(key-1) + " rating: " + str(self.ratingData[int(customer)-1][key-1])
            fd.close()
        print "From loadRating()" 
        print np.shape(self.ratingData)
        print np.nonzero(self.ratingData[:][0])
        if os.path.exists('./data/dumpfile/ratingData.npy'):
            os.remove('./data/dumpfile/ratingData.npy')
        np.save('./data/dumpfile/ratingData.npy',self.ratingData)

    def loadFromTxtFile(self):
        time1 = time.time()
        print "Loading probe.txt"
        self.loadProbe()
        print "Loading qualifying.txt"
        self.loadQualify()
        print "Loading movie_titles.txt"
        self.loadMovie()
        print "Loading training_set"
        self.loadRating()
        print "Sucessfully load files from txt"
        time2 = time.time()
        print "Time spend: " + str(time2 - time1) + 's'
        # print self.probeDict[1]
        # print self.qualifyDict[1]
        # print self.movieDict[1]
        # print self.ratingData[0][0]

    def loadFromDumpFile(self):
        time1 = time.time()
        if os.path.exists('./data/dumpfile/probeDict.pkl'):
            pkl_file = open('./data/dumpfile/probeDict.pkl','rb')
            self.probeDict = pickle.load(pkl_file)
            pkl_file.close()
            print "Load probeDict.pkl successfully"
        else:
            print "Cannot find file probeDict.pkl"

        if os.path.exists('./data/dumpfile/qualifyDict.pkl'):
            pkl_file = open('./data/dumpfile/qualifyDict.pkl','rb')
            self.qualifyDict = pickle.load(pkl_file)
            pkl_file.close()
            print "Load qualifyDict.pkl successfully"
        else:
            print "Cannot find file qualifyDict.pkl"

        if os.path.exists('./data/dumpfile/movieDict.pkl'):
            pkl_file = open('./data/dumpfile/movieDict.pkl','rb')
            self.movieDict = pickle.load(pkl_file)
            pkl_file.close()
            print "Load movieDict.pkl successfully"
        else:
            print "Cannot find file movieDict.pkl"

        if os.path.exists('./data/dumpfile/ratingData.npy'):
            self.ratingData = np.load('./data/dumpfile/ratingData.npy')
            print "Load ratingData.npy successfully"
        else:
            print "Cannot find file ratingData.npy"

        time2 = time.time()
        print "Time spend: " + str(time2 - time1) + "s"
        # print self.probeDict[1]
        # print self.qualifyDict[1]
        # print self.movieDict[1]
        # print self.ratingData[0][0]
