import config_list
import csv
from MovieRatingData import MovieRatingData
from Recommender import Recommender

class Main:

    def __init__(self):

        data = MovieRatingData()
        ftrain = config_list.training
        ftest = config_list.testing

        data.load(ftrain)

        data.removeOutliers()

        rec = Recommender()
        rec.train(data)

        self.test(ftest, rec)

    def test(self, ftest, rec):
        
        error = [[0,0],[0,0]]
        
        users = {}
        q_positive = {}
        q_negative = {}

        with open(ftest, mode='r') as test_file:
            test_reader = csv.reader(test_file)
            for row in test_reader:
                user = row[0]
                product = row[1]
                rating = float(row[2])
                d_type = row[3]

                if user not in users:
                    users[user] = []
                    q_positive[user] = []
                    q_negative[user] = []

                if d_type == 'c':
                    if rating >= config_list.like_threshold:
                        users[user].append(product)
                else:
                    if rating >= config_list.like_threshold:
                        q_positive[user].append(product)
                    else:
                        q_negative[user].append(product)


        for user in users:
            products = users[user]

            for q in q_positive[user]:
                error[1][rec.predict(products, q)] += 1

            for q in q_negative[user]:
                error[0][rec.predict(products, q)] += 1

        if error[0][1] + error[1][1] > 0:
            print('Precision : {:.3f}'.format(float(error[1][1])/float(error[0][1] + error[1][1])))
        else:
            print('Precision : undefined')

        if error[1][0] + error[1][1] > 0:
            print('Recall : {:.3f}'.format(float(error[1][1])/float(error[1][0] + error[1][1])))
        else:
            print('Recall : undefined')

        if error[1][0] + error[1][1] > 0:
            print('All case accuracy : {:.3f}'.format(float(error[1][1] + error[0][0])/float(error[0][0] + error[0][1] + error[1][0] + error[1][1])))
        else:
            print('All case accuracy : undefined')

        print(error[0][0], error[0][1])
        print(error[1][0], error[1][1])

Main()
