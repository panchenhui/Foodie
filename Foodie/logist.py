import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer

class Logistc(object):
    def __init__(self):
        url = 'https://inf552-69068.firebaseio.com/reviews.json'
        review_df = pd.read_json(url, orient='index')
        # reset the index (or maybe not need)
        # review_df = review_df.reset_index(drop=True)
        document = review_df['text'].values

        # set the target as review_star above 4
        review_df['rate_level'] = review_df['stars_review'] > 4

        target = review_df['rate_level']
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        vectorizer_train = self.vectorizer.fit_transform(document).toarray()
        words = self.vectorizer.get_feature_names()

        # We use logistic regression that performs best here to train and predict
        self.model_lg = LogisticRegression()
        parameters = {'C': [1e-2, 1e-1, 1, 1e2], 'penalty': ['l2', 'l1']}
        grid = GridSearchCV(self.model_lg, parameters, cv=5)
        grid.fit(vectorizer_train, target)
        self.model_lg = LogisticRegression(penalty=grid.best_params_['penalty'], C=grid.best_params_['C'])
        self.model_lg.fit(vectorizer_train, target)

        # Check it out top 30 keywors that contribute to the 5 stars rating
        n = 30
        self.top_words = self.get_top_values(self.model_lg.coef_[0], n, words)

    def get_top_values(self,lst, n, labels):
        return [labels[i] for i in np.argsort(lst)[::-1][:n]]  # np.argsort by default sorts values in ascending order

    def predict_rating_direction(self,input_words):
        vectorizer_to_predict = self.vectorizer.transform(input_words).toarray()
        predict = self.model_lg.predict(vectorizer_to_predict)
        return predict


