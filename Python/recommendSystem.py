from movieRecommend import *
from processData import *

class recommendSystem(object):
    def __init__(self, dataLoad=True, svdLoad=True):
        self.process_data = processData("./data/training_set/", "./data/movie_titles.txt", "./data/probe.txt", "./data/qualifying.txt")
        if dataLoad == True:
            self.process_data.loadFromDumpFile()
            self.recommed = movieRecommend(self.process_data.ratingData, dist="pearsSim", load=svdLoad)

        else:
            self.process_data.loadFromTxtFile()
            # print "From recommendSystem()"
            # print np.nonzero(self.process_data.ratingData[:,0])
            self.recommed = movieRecommend(self.process_data.ratingData, dist="pearsSim", load=svdLoad)

    def recommend(self, user, N=10):
        """
        user starts from 1 to max_user
        :param user:
        :param N:
        :return:
        """
        result = self.recommed.recommend(user-1, N)
        print "The top " + str(len(result)) + " recommendation for user " + str(user) + " is:"
        print "MovieID\tMovie Name\tYear\tEst Score"
        for item in result:
            year, name = self.process_data.movieDict[int(item[0])+1]
            print str(item[0]+1) + '\t' + str(name) + '\t' + str(year) + '\t' + str(item[1])
