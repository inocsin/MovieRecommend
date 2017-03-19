import numpy as np
class Recommend(object):
    def __init__(self, data, dist="pearsSim"):
        self.data = np.mat(data);
        self.sim = getattr(self, dist)
        self.similarDict = {}
        self.singularNum = 0 # the Nth singular value that consist of the 90% of total singular value
        # update the similarDict
        self.svdSimMat(self.sim)

    def update(self, simFunc):
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
        xformedItems = self.data.T * U[:,:self.singularNum] * Sig.I

        for i in range(m - 1):
            for j in range(i + 1, m):
                similarity = simFunc(xformedItems[i,:].T, xformedItems[j,:].T)
                self.similarDict[(i,j)] = similarity

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
        unratedItems = np.nonzero(self.data[user, :].A == 0)[1]
        if len(unratedItems) == 0:
            print "You have rated everthing"
            return 0
        itemScores = []
        for item in unratedItems:
            est = self.estScore(user, item)
            itemScores.append((item, est))
        return sorted(itemScores, key=lambda i: i[1], reverse=True)[:N]
