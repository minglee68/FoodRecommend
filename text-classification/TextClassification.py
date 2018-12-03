import csv
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics

data = []
target = []
target_name = ['good food', 'bad food']
with open('Reviews.csv', mode='r') as review_file:
    review_reader = csv.reader(review_file)
    line_count = 0
    for row in review_reader:
        if line_count == 0:
            line_count += 1
            continue
        data.append(row[9])
        if float(row[6]) > 4.0:
            target.append(1)
        else:
            target.append(2)

t_target = np.array(target)

text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])

text_clf.fit(data, t_target)
predicted = text_clf.predict(data)
print(np.mean(predicted == t_target))
print(metrics.classification_report(t_target, predicted, target_names=target_name))
