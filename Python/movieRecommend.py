import numpy as np
import pickle
import os
from scipy.sparse.linalg import svds
from scipy import sparse

class movieRecommend(object):
    """
    In data, each row represent a customer rating, each column represent an item, e.g. movies
    """
    def __init__(self, data, dist="pearsSim", load=False, sparse=True):
        # self.data = np.array(data)
        self.data = np.array(data)
        print self.data[:][0]
        print np.shape(self.data)
        self.sim = getattr(self, dist)
        self.similarDict = {}
        self.singularNum = 0 # the Nth singular value that consist of the 90% of total singular value
        # update the similarDict
        self.sparse = sparse
        if load == True:
            self.loadFromDumpFile()
        else:
            self.svd(self.sim)


    def loadFromDumpFile(self):
        if os.path.exists('./data/dumpfile/similarDict.pkl'):
            pkl_file = open('./data/dumpfile/similarDict.pkl','rb')
            self.similarDict = pickle.load(pkl_file)
            pkl_file.close()
            print "Load similarDict.pkl successfully"
        else:
            print "Cannot find file similarDict.pkl"
            os._exit()

    def saveToDumpFile(self):
        if os.path.exists('./data/dumpfile/similarDict.pkl'):
            os.remove('./data/dumpfile/similarDict.pkl')
        output = open('./data/dumpfile/similarDict.pkl','wb')
        pickle.dump(self.similarDict, output)
        output.close()
        print "Save file to similarDict.pkl successfully"


    def svd(self, simFunc):
        if self.sparse == True:
            self.sparseSvds(simFunc)
        else:
            self.svdSimMat(simFunc)

    def ecludSim(self, A, B):
        "A and B is n * 1 vector"
        return 1.0 / (1.0 + np.linalg.norm(A - B))

    def pearsSim(self, A, B):
        "A and B is n * 1 vector"
        if len(A) < 3 :
            return 1.0
        return 0.5 + 0.5 * np.corrcoef(A, B, rowvar=0)[0][1]

    def cosSim(self, A, B):
        "A and B is n * 1 vector"
        num = float(A.T * B)
        denom = np.linalg.norm(A) * np.linalg.norm(B)
        return 0.5 + 0.5 * (num/ denom)

    def svdSimMat(self, simFunc = pearsSim):
        """
        Using svd to get similarity matrix bewteen each pair of items
        Using dict to store similarity matrix, similar[(i,j)] = sim, where i < j
        :return:
        """
        n, m = np.shape(self.data) # n is number of user, m is number of items
        U, Sigma, VT = np.linalg.svd(self.data)
        # print Sigma
        total = sum(Sigma ** 2) * 0.9 # to get the 90% information
        count = 0
        cur_sum = 0
        for i in range(len(Sigma)):
            count = count + 1
            cur_sum = cur_sum + Sigma[i] ** 2
            if cur_sum >= total:
                break
        self.singularNum = count
        Sig = np.mat(np.eye(self.singularNum) * Sigma[:self.singularNum])
        xformedItems = self.data.T.dot(U[:,:self.singularNum]).dot(Sig.I)

        for i in range(m - 1):
            for j in range(i + 1, m):
                similarity = simFunc(xformedItems[i,:].T, xformedItems[j,:].T)
                self.similarDict[(i,j)] = similarity

        # save dict to dumpfile
        self.saveToDumpFile()

    def sparseSvds(self, simFunc = pearsSim):
        n, m = np.shape(self.data) # n is number of user, m is number of items
        SinNum = min(100,min(self.data.shape)-1)
        U, S, VT = svds(sparse.csr_matrix(self.data.astype('float')), k=SinNum)
        print "Sigma"
        print S
        Sig = np.mat(np.eye(SinNum) * S)
        # xformedItems = self.data.T.dot(U).dot(Sig.I)
        xformedItems = sparse.csr_matrix(self.data).T.dot(sparse.csr_matrix(U)).dot(Sig.I)
        # print S

        for i in range(m - 1):
            for j in range(i + 1, m):
                similarity = simFunc(xformedItems[i,:].T, xformedItems[j,:].T)
                self.similarDict[(i,j)] = similarity

        # save dict to dumpfile
        self.saveToDumpFile()


    def estScore(self, user, item):
        m = np.shape(self.data)[1]
        simTotal = 0.0
        rateSimTotal = 0.0
        for i in range(m):
            userRating = self.data[user, i]
            if userRating == 0 or i == item: continue
            key = 0
            # make sure that key is valid
            if i < item:
                key = (i, item)
            else:
                key = (item, i)
            similarity = self.similarDict[key]
            simTotal += similarity
            rateSimTotal += similarity * userRating
        if simTotal == 0: return 0
        else: return rateSimTotal / simTotal



    def recommend(self, user, N = 10):
        # np.nonzero returns tuple(rowindex, colindex)
        unratedItems = np.nonzero(self.data[user, :] == 0)[0]
        if len(unratedItems) == 0:
            print "You have rated everthing"
            return 0
        itemScores = []
        for item in unratedItems:
            est = self.estScore(user, item)
            itemScores.append((item, est))
        return sorted(itemScores, key=lambda i: i[1], reverse=True)[:N]
