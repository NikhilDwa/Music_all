import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import correlation, cosine
import sklearn.metrics as metrics
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise_distances
import sqlite3


# This function finds k similar items given the item_id and listen_count matrix M
def findksimilaritems(item_id, listen_count, metric='correlation', k=6):
    similarities = []
    indices = []
    listen_count = listen_count.T
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(listen_count)

    distances, indices = model_knn.kneighbors(listen_count.iloc[item_id - 1, :].values.reshape(1, -1), n_neighbors=k + 1)
    similarities = 1 - distances.flatten()
    # print( '{0} most similar items for item {1}:\n'.format(k,item_id))
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == item_id:
            continue;

            # else:
            # print ('{0}: Item {1} :, with similarity of {2}'.format(i,indices.flatten()[i]+1, similarities.flatten()[i]))

    return similarities, indices


def predict_itembased(user_id, item_id, listen_count, metric='correlation', k=3):
    prediction = wtd_sum = 0
    similarities, indices = findksimilaritems(item_id, listen_count)  # similar users based on correlation coefficients
    sum_wt = np.sum(similarities)
    product = 1

    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == item_id:
            continue;
        else:
            product = listen_count.iloc[user_id - 1, indices.flatten()[i]] * (similarities[i])
            wtd_sum = wtd_sum + product
    prediction = int(round(wtd_sum / sum_wt))
    # print('\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id, item_id, prediction))

    return prediction


def get_common_songs(user1, df2, df7):
    common_songs = df7[(df7['user_id_id'] == user1) & (df7['count'] != 0)]
    new_prediction = pd.Series([], name='new_prediction')
    for item in common_songs.song_id_id:
        prediction = predict_itembased(user1, item, df2)
        new_prediction = new_prediction.append(pd.Series(prediction))

    actual = pd.Series(common_songs['count'], name='actual')
    return actual, new_prediction


def get_songs(user_id, item_id):
    path = './db.sqlite3'
    con = sqlite3.connect(path)  # connecting to database
    df = pd.read_sql_query("SELECT * FROM home_listencount", con)  # reading the table
    df.fillna(0, inplace=True)
    df2 = df.pivot(index='user_id_id', columns='song_id_id', values='count')  # making a matrix
    df2.fillna(0, inplace=True)

    # find similarity_matrix
    item_dataframe = df2.T
    pearison_sim = 1 - pairwise_distances(item_dataframe.as_matrix(), metric="correlation")
    similarity_matrix = pd.DataFrame(pearison_sim)
    # print(similarity_matrix)
    simi, indi = findksimilaritems(item_id, df2)
    indi = np.delete(indi, 0)
    indi = indi + 1
    # print(indi)

    predicted = pd.Series(name='prediction')
    for item in indi:
        predict = predict_itembased(user_id, item, df2)
        predicted = predicted.append(pd.Series(predict))

    predicted = predicted.reset_index(drop=True)
    item = pd.Series(name='item')

    for values in indi:
        item = item.append(pd.Series(values))

    item = item.reset_index(drop=True)
    dict = {'item': item, 'predicted': predicted}
    prediction_dataframe = pd.DataFrame(dict)
    prediction_dataframe = prediction_dataframe.sort_values(by='predicted', ascending=False)

    # print(prediction_dataframe)


    df7 = df2.unstack().reset_index(name='count')
    org_actual = pd.Series(name='org_actual')
    org_predicted = pd.Series(name='org_predicted')
    for item in df7['user_id_id'].unique():
        nikhil, esor = get_common_songs(item, df2, df7)
        org_actual = org_actual.append(nikhil)
        org_predicted = org_predicted.append(esor)

    mse = mean_squared_error(org_actual, org_predicted)
    #print(mse**0.5)
    return (prediction_dataframe['item'][:7])



