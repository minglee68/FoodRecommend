import config_list
import csv

class FoodRatingData:
    Baskets = {}
    numRatingsOfProducts = {}
    accRatingsOfProducts = {}

    like_threshold = 0.0
    outlier_threshold = 0
    outlier_threshold_small = 0

    def __init__(self):
        self.like_threshold = config_list.like_threshold
        self.outlier_threshold = config_list.outlier_threshold
        self.outlier_threshold_small = config_list.outlier_threshold_small

    def load(self, ftrain):
        with open(ftrain, mode='r') as train_file:
            train_reader = csv.reader(train_file)
            for row in train_reader:
                user = row[0]
                product = row[1]
                rating = float(row[2])

                if product in self.numRatingsOfProducts:
                    self.numRatingsOfProducts[product] += 1
                    self.accRatingsOfProducts[product] += rating
                else:
                    self.numRatingsOfProducts[product] = 1
                    self.accRatingsOfProducts[product] = rating

                if rating >= self.like_threshold:
                    if user not in self.Baskets:
                        self.Baskets[user] = []
                    self.Baskets[user].append(product)

    def removeOutliers(self):
        outliers = []
        for userId in self.Baskets:
            basket = self.Baskets[userId]
            if len(basket) > self.outlier_threshold:
                outliers.append(userId)
                continue
            if len(basket) < self.outlier_threshold_small:
                outliers.append(userId)

        for userId in outliers:
            del self.Baskets[userId]

    def getBaskets(self):
        return self.Baskets

