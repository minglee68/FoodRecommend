import config_list
import itertools

class Recommender:

    support1 = {}
    support2 = {}
    support3 = {}

    min_supports = 0
    threshold_2 = 0.0
    threshold_3 = 0.0
    min_evidence_3 = 0
    
    def __init__(self):
        self.min_supports = config_list.min_supports
        self.threshold_2 = config_list.threshold_2
        self.threshold_3 = config_list.threshold_3
        self.min_evidence_3 = config_list.min_evidence_3

    def train(self, data):
        Baskets = data.getBaskets()

        for user in Baskets:
            basket = Baskets[user]

            self.updateSupport1(basket)
            self.updateSupport2(basket)
            self.updateSupport3(basket)

    def predict(self, profile, q):
        if self.predictPair(profile, q) == 1:
            return 1
        return self.predictTriple(profile, q)

    def updateSupport1(self, basket):
        for item in basket:
            if item in self.support1:
                self.support1[item] += 1
            else:
                self.support1[item] = 1

    def updateSupport2(self, basket):
        if len(basket) >= 2:
            for pair in itertools.combinations(basket, 2):
                int_pair = self.IntPair(pair)
                if int_pair in self.support2:
                    self.support2[int_pair] += 1
                else:
                    self.support2[int_pair] = 1

    def updateSupport3(self, basket):
        _basket = []
        for elem in basket:
            if self.support1[elem] >= self.min_supports:
                _basket.append(elem)

        basket = _basket

        if len(basket) >= 3:
            for triple in itertools.combinations(basket, 3):
                int_triple = self.IntTriple(triple)
                if int_triple in self.support3:
                    self.support3[int_triple] += 1
                else:
                    self.support3[int_triple] = 0

    def predictPair(self, profile, q):
        if len(profile) < 1:
            return 0

        evidence = 0
        for s in profile:
            if s in self.support1:
                den = self.support1[s]
            else:
                continue
            
            item = self.IntPair((s, q))
            if item in self.support2:
                if self.support2[item] < self.min_supports:
                    continue
                if float(self.support2[item]) / float(den) >= self.threshold_2:
                    evidence += 1
            else:
                continue

        if evidence != 0:
            return 1

        return 0

    def predictTriple(self, profile, q):
        if len(profile) < 2:
            return 0

        evidence = 0
        for p in itertools.combinations(profile, 2):
            pair = self.IntPair(p)
            if pair in self.support2:
                den = self.support2[pair]
            else:
                continue

            t = (q,) + p
            item = self.IntTriple(t)
            if item in self.support3:
                if self.support3[item] < self.min_supports:
                    continue
                if float(self.support3[item]) / float(den) >= self.threshold_3:
                    evidence += 1
            else:
                continue
        
        if evidence > self.min_evidence_3:
            return 1

        return 0

    def IntPair(self, pair):
        list_pair = list(pair)
        list_pair.sort()
        return tuple(list_pair)

    def IntTriple(self, triple):
        list_triple = list(triple)
        list_triple.sort()
        return tuple(list_triple)
        



