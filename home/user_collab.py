import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
import sqlite3


def findksimilarusers(user_id, listen_count, metric='correlation', k=5):
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(listen_count)
    distances, indices = model_knn.kneighbors(listen_count.iloc[user_id - 1, :].values.reshape(1, -1), n_neighbors=k + 1)
    similarities = 1 - distances.flatten()
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == user_id:
            continue
    return similarities, indices


def get_user_similar_movies(user1, user2, df7):
    uncommon_movies = df7[df7.user_id_id == user1].merge(
        df7[df7.user_id_id == user2],
        on="song_id_id",
        how="inner")
    uncommon_movies = uncommon_movies[(uncommon_movies.count_x == 0) & (uncommon_movies.count_y != 0)]
    return uncommon_movies.song_id_id


def predict_userbased(user_id, item_id, listen_count):
    similarities, indices = findksimilarusers(user_id, listen_count)  # similar users based on cosine similarity
    mean_rating = listen_count.loc[user_id, :].mean()  # to adjust for zero based indexing
    sum_wt = np.sum(similarities)
    wtd_sum = 0
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == user_id:
            continue
        else:
            listen_count_diff = listen_count.iloc[indices.flatten()[i], item_id - 1] - np.mean(
                listen_count.iloc[indices.flatten()[i], :])
            product = listen_count_diff * (similarities[i])
            wtd_sum += product
    prediction = int(round(mean_rating + (wtd_sum / sum_wt)))
    return prediction


def error(df7, df2):
    org_actual = pd.Series(name='org_actual')
    org_predicted = pd.Series(name='org_predicted')

    def get_listened_songs(user1):
        listened_songs = df7[(df7['user_id_id'] == user1) & (df7['count'] != 0)]
        new_prediction = pd.Series([], name='new_prediction')
        for item in listened_songs.song_id_id:
            prediction = predict_userbased(user1, item, df2)
            new_prediction = new_prediction.append(pd.Series(prediction))
        actual = pd.Series(listened_songs['count'], name='actual')
        return actual, new_prediction

    for item in df7['user_id_id'].unique():
        nikhil, esor = get_listened_songs(item)
        org_actual = org_actual.append(nikhil)
        org_predicted = org_predicted.append(esor)
    mse = mean_squared_error(org_actual, org_predicted)
    return mse ** 0.5


def song_pred(input_user_id):
    path = './db.sqlite3'
    con = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM home_listencount", con)
    df.fillna(0, inplace=True)
    df2 = df.pivot(index='user_id_id', columns='song_id_id', values='count')
    df2.fillna(0, inplace=True)
    sim, indi = findksimilarusers(input_user_id, df2)
    indi = np.delete(indi, 0)
    indi += 1
    df7 = df2.unstack().reset_index(name='count')
    df3 = pd.Series(name='item')
    df10 = pd.Series(name='prediction')
    userlist = indi
    for user in userlist:
        f1 = get_user_similar_movies(input_user_id, user, df7)
        df3 = pd.concat([df3, f1])
    df3 = df3.drop_duplicates()
    for item in df3:
        prediction = predict_userbased(input_user_id, item, df2)
        df10 = df10.append(pd.Series(prediction))
    df3 = df3.reset_index(drop=True)
    df10 = df10.reset_index(drop=True)
    dicts = {'item': df3, 'prediction': df10}
    dframe = pd.DataFrame(dicts)
    dframe = dframe.sort_values(by='prediction', ascending=False)
    return dframe['item'][:6]
