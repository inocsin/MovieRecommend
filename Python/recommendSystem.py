from movieRecommend import *
from processData import *

class recommendSystem(object):
    def __init__(self, load=True):
        self.process_data = processData("./data/training_set/", "./data/movie_titles.txt", "./data/probe.txt", "./data/qualifying.txt")
        if load == True:
            self.process_data.loadFromDumpFile()
            self.recommed = movieRecommend(self.process_data.ratingData, dist="pearsSim", load=True)

        else:
            self.process_data.loadFromTxtFile()
            self.recommed = movieRecommend(self.process_data.ratingData, dist="pearsSim", load=False)

    def recommend(self, user, N=10):
        result = self.recommed.recommend(user, N)
        print "The top " + str(len(result)) + " recommendation is:"
        print "MovieID\tMovie Name\tYear\tEst Score"
        for item in result:
            year, name = self.process_data.movieDict[int(item[0])]
            print str(item[0]) + '\t' + str(year) + '\t' + str(name) + '\t' + str(item[1])





