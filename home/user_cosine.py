import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import correlation, cosine
import sklearn.metrics as metrics
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise_distances
import sqlite3


def findksimilarusers(user_id, dataframe, metric='cosine', k=6):
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(dataframe)

    distances, indices = model_knn.kneighbors(dataframe.iloc[user_id - 1, :].values.reshape(1, -1), n_neighbors=k + 1)
    similarities = 1 - distances.flatten()
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == user_id:
            continue;

    return similarities, indices



def get_listened_songs(user1, user2, df7):
    common_songs = df7[df7.user_id_id == user1].merge(
        df7[df7.user_id_id == user2],
        on="song_id_id",
        how="inner")
    common_songs=common_songs[(common_songs.count_x==0)&(common_songs.count_y != 0)]
    return common_songs.song_id_id

def predict_userbased(user_id, item_id, dataframe):
    prediction = 0
    similarities, indices = findksimilarusers(user_id, dataframe)  # similar users based on cosine similarity
    mean_rating = dataframe.loc[user_id , :].mean()  # to adjust for zero based indexing
    sum_wt = np.sum(similarities)
    product = 1
    wtd_sum = 0

    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == user_id:
            continue;
        else:
            dataframe_diff = dataframe.iloc[indices.flatten()[i], item_id - 1] - np.mean(
                dataframe.iloc[indices.flatten()[i], :])
            product = dataframe_diff * (similarities[i])
            wtd_sum = wtd_sum + product

    prediction = int(round(mean_rating + (wtd_sum / sum_wt)))

    return prediction

def get_predictions(user1,df7,df2):
        rated_movies = df7[(df7['user_id_id'] == user1) & (df7['count'] != 0)]
        new_prediction = pd.Series([], name='new_prediction')
        for item in rated_movies.song_id_id:
            prediction=predict_userbased(user1,item,df2)
            new_prediction=new_prediction.append(pd.Series(prediction))

        actual=pd.Series(rated_movies['count'],name='actual')
        return actual,new_prediction


def song_pred(input_user_id):
    path='../db.sqlite3'
    con=sqlite3.connect(path) #connecting to database
    df=pd.read_sql_query("SELECT * FROM home_listencount",con) # reading the table
    df.fillna(0,inplace=True)
    df2=df.pivot(index='user_id_id',columns='song_id_id',values='count') #making a matrix
    #print(df)
    df2.fillna( 0, inplace = True )

    #calculating pearson similarity
    pearison_sim= 1-pairwise_distances(df2.as_matrix(),metric="cosine")
    similarity_matrix=pd.DataFrame(pearison_sim)
    sim,indi=findksimilarusers(input_user_id,df2)
    indi=np.delete(indi,0)
    indi=indi+1
    df7 = df2.unstack().reset_index(name='count')
    df3=pd.Series(name='item')
    df10=pd.Series(name='prediction')
    userlist=indi
    for user in userlist:
        f1=get_listened_songs(input_user_id,user,df7)
        df3=pd.concat([df3,f1])
    df3=df3.drop_duplicates()

    for item in df3:
        prediction=predict_userbased(input_user_id,item,df2)
        df10=df10.append(pd.Series(prediction))

    df3=df3.reset_index(drop=True)
    df10=df10.reset_index(drop=True)
    dict={'item':df3,'prediction':df10}

    dframe=pd.DataFrame(dict)
    dframe=dframe.sort_values(by='prediction',ascending=False)

    org_actual = pd.Series(name='org_actual')
    org_predicted = pd.Series(name='org_predicted')

    for item in df7['user_id_id'].unique():
        nikhil, esor = get_predictions(item,df7,df2)
        org_actual = org_actual.append(nikhil)
        org_predicted = org_predicted.append(esor)

    mse=mean_squared_error(org_actual,org_predicted)
    #print(mse**0.5)

    #print(dframe)
    return (dframe['item'][:3])









