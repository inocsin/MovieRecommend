import numpy as np
class Recommend(object):
    def __init__(self, data, dist = "pearsSim"):
        self.data = data;
        self.sim = getattr(self, dist)

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

    
