import pandas as pd
import sqlite3


def popular_song():
    path = './db.sqlite3'
    con = sqlite3.connect(path)
    listen_song = pd.read_sql_query("SELECT * FROM home_listencount", con)
    song_total_listen = listen_song.groupby(['song_id_id']).mean()
    song_total_listen = song_total_listen.drop(['listen_count_id', 'user_id_id'], axis=1)
    song_total_listen = song_total_listen.sort_values(by='count', ascending=False)
    final = song_total_listen.unstack().reset_index(name='count')
    final = final.drop(['level_0'], axis=1)
    return final['song_id_id'][:8]
