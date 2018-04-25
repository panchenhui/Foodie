import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity



class Recommender(object):

    def __init__(self):
        self.recomm_n = 10
        url = 'https://inf552-69068.firebaseio.com/reviews.json'
        review_df = pd.read_json(url, orient='index')
        review_df = review_df.reset_index(drop=True)
        review_df = review_df.drop(['date', 'text'], axis=1)
        review_df = review_df.dropna(how='any')
        self.review_df = self.create_index(review_df)
        self.rating_matrix, self.item_sim_matrix, self.item_matrix_neighbor = self.sparse_matrix_similarity(self.review_df)




    def create_index(self,df):
        # create new number indexes for business and users
        b_i = 0
        u_i = 0
        business_id_trans = {}
        business_id_n = []
        user_id_trans ={}
        user_id_n =[]
        for _, row in df.iterrows():
            if row.business_id in business_id_trans.keys():
                business_id_n.append(business_id_trans[row.business_id])
            else:
                business_id_trans[row.business_id]=b_i
                business_id_n.append(business_id_trans[row.business_id])
                b_i = b_i+1
            if row.user_id in user_id_trans.keys():
                user_id_n.append(user_id_trans[row.user_id])
            else:
                user_id_trans[row.user_id]=u_i
                user_id_n.append(user_id_trans[row.user_id])
                u_i = u_i+1
        df['business_id_n'] = business_id_n
        df['user_id_n'] = user_id_n
        return df


    def sparse_matrix_similarity(self,df):
        user_n = df['user_id_n'].max()+1
        business_n = df['business_id_n'].max()+1
        rating_mat = sparse.lil_matrix((user_n,business_n))
        for _, row in df.iterrows():
            rating_mat[row.user_id_n - 1, row.business_id_n - 1] = row.stars_review
        item_sim_mat = cosine_similarity(rating_mat.T)
        least_to_most_sim_indexes = np.argsort(item_sim_mat, axis=1)[:, ::-1]
        # [:,::-1] means reverse the sequence of the index

        neighborhood_size = 50
        neighborhoods = least_to_most_sim_indexes[:, :neighborhood_size]
        return rating_mat, item_sim_mat, neighborhoods

    def predict_rating(self,user_id,rating_mat,item_sim_mat,neighborhoods):
        n_users = rating_mat.shape[0]
        n_items = rating_mat.shape[1]
        # To find the items rated according to the id of users
        items_reted_by_this_user = rating_mat[user_id].nonzero()[1]

        # create a empty list for storing each item's rating a user might give to
        out = np.zeros(n_items)

        # Iterate to calculate the rating using item-based formulation
        for item_to_rate in range(n_items):
            # Find the overlap item id both in neighborhood set and items rated by the specific user that we want to predict
            relevant_items = np.intersect1d(neighborhoods[item_to_rate], items_reted_by_this_user)
            # write result into 'out' list by using item-based formulation
            out[item_to_rate] = rating_mat[user_id, relevant_items] * item_sim_mat[item_to_rate, relevant_items] / \
                                item_sim_mat[item_to_rate, relevant_items].sum()
        pre_ratings = np.nan_to_num(out)
        return  pre_ratings


    def recommender(self, user_id,recommend_n,pre_ratings,rating_mat,df):
        # Get item indexes sorted by prediected rating
        item_index_sorted_by_pre_rating = list(np.argsort(pre_ratings))[::-1]

        # Find items that have been rated by user
        items_reted_by_this_user = rating_mat[user_id].nonzero()[1]

        # exclude the item that has been rated by user
        unrated_items_by_pre_rating = [item for item in item_index_sorted_by_pre_rating if
                                       item not in items_reted_by_this_user]

        predict_list = unrated_items_by_pre_rating[:recommend_n]
        return df['business_id'].iloc[predict_list]

    def pre_rate_recommend(self, u_id):
        # u_id_n = int(self.review_df [self.review_df['user_id'] == u_id].index[0])
        pre_rate = self.predict_rating(100,self.rating_matrix,self.item_sim_matrix,self.item_matrix_neighbor)
        recommend_business = self.recommender(100, self.recomm_n, pre_rate, self.rating_matrix, self.review_df)
        return recommend_business
