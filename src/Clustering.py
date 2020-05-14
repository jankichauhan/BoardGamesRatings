import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from kmodes.kmodes import KModes
from itertools import chain


class Clustering():
    def __init__(self):
        print("in init")
        self.board_game_data = pd.read_csv('board_game_data.csv')
        self.board_game_data.columns = ['board_game_id', 'name', 'year', 'minplayer', 'maxplayer', 'playingtime',
                                        'avgratings',
                                        'designer', 'category', 'mechanic', 'publisher', 'age', 'rank']
        self.unique_publishers = self.publisher_list()
        self.one_hot_encoding()

    def run_cluster(self):
        columns = self.board_game_data.columns.tolist()
        columns = [c for c in columns if
                   c not in ['board_game_id', 'name', 'year', 'minplayer', 'maxplayer', 'playingtime',
                                        'avgratings','designer', 'category', 'mechanic', 'publisher', 'age', 'rank']]
        print(columns)
        cluster_df = self.board_game_data[columns]
        km = KModes(n_clusters=15, init='Huang', n_init=10, verbose=1)
        clusters = km.fit_predict(cluster_df)
        print(km.cluster_centroids_)

        centroids = km.cluster_centroids_
        for i in range(centroids.shape[0]):
            if sum(centroids[i, :]) == 0:
                print("\ncluster " + str(i) + ": ")
                print("no cluster")
            else:
                print("\ncluster " + str(i) + ": ")
                cent = centroids[i, :]
                for j in cluster_df.columns[np.nonzero(cent)]:
                    print(j)

    def publisher_list(self):
        print("in publisher list")
        self.board_game_data = self.board_game_data.fillna("not define")
        self.board_game_data['designer'] = self.board_game_data['designer'].str.replace(':', ', ')
        self.board_game_data['category'] = self.board_game_data['category'].str.replace(':', ', ')
        self.board_game_data['mechanic'] = self.board_game_data['mechanic'].str.replace(':', ', ')
        self.board_game_data['publisher'] = self.board_game_data['publisher'].str.replace(':', ', ')
        unique_publishers = self.board_game_data['publisher'].tolist()
        unique_publishers = [publisher.split(', ') for publisher in unique_publishers]
        unique_publishers = set(chain(*unique_publishers))
        return unique_publishers

    def one_hot_encoding(self):
        print("in one hot encoding")
        for publisher in self.unique_publishers:
            self.board_game_data["pub_"+publisher] = self.board_game_data.publisher.apply(lambda x: 1 if publisher in x else 0)



Clustering().run_cluster()