import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.Modelling import Model
from collections import Counter
from itertools import chain

class LoadAndTransform():
    def __init__(self):
        print("in init")
        self.df_data = pd.read_csv('board_game_data.csv')
        self.df_data.columns = ['board_game_id', 'name', 'year', 'minplayer', 'maxplayer', 'playingtime', 'avgratings',
                                'designer', 'category', 'mechanic', 'publisher', 'age', 'rank']
        self.board_game_data = self.df_data

        self.unique_publishers = []
        self.unique_categories = []
        self.unique_designers = []

    def tranform(self):
        self.df_data = pd.read_csv('board_game_data.csv')
        self.df_data.columns = ['board_game_id', 'name', 'year', 'minplayer', 'maxplayer', 'playingtime', 'avgratings',
                                'designer', 'category', 'mechanic', 'publisher', 'age', 'rank']
        self.board_game_data = self.df_data
        self.board_game_data = self.board_game_data.fillna("not define")
        self.board_game_data['designer'] = self.board_game_data['designer'].str.replace(':', ', ')
        self.board_game_data['category'] = self.board_game_data['category'].str.replace(':', ', ')
        self.board_game_data['mechanic'] = self.board_game_data['mechanic'].str.replace(':', ', ')
        self.board_game_data['publisher'] = self.board_game_data['publisher'].str.replace(':', ', ')

        self.get_categorical_list()
        self.one_hot_encoding()
        self.data_for_modelling()


    def data_for_modelling(self):
        columns = self.board_game_data.columns.tolist()
        columns = [c for c in columns if
                   c not in ['board_game_id','avgratings', 'name', 'year', 'rank', 'designer', 'category', 'mechanic', 'publisher', 'cat_not define','pub_not define','des_not define', 'cat_(Uncredited)']]
        target = 'avgratings'

        X = self.board_game_data[columns].values
        y = self.board_game_data[target].values

        print(columns)
        print(self.board_game_data.shape)

        # for col in columns:
        #     plt.scatter(self.board_game_data[col], self.board_game_data[target], alpha=0.4)
        #     plt.xlabel(col)
        #     plt.ylabel(target)
        #     plt.show()

        ml_model = Model(X,y)
        # ml_model.LinearReg()
        ml_model.RandomForest(columns)
        # ml_model.GradientBoost()
        # ml_model.grid_search_cv_gb()
        # ml_model.grid_search_cv_rf()

    def get_categorical_list(self):
        board_game_data_copy = self.board_game_data.copy()
        board_game_data_copy = board_game_data_copy[board_game_data_copy['rank'] != 0]
        board_game_data_copy = board_game_data_copy[board_game_data_copy['designer'] != '(Uncredited)']
        board_game_data_copy = board_game_data_copy[board_game_data_copy['designer'] != 'not define']
        board_game_data_copy = board_game_data_copy[board_game_data_copy['designer'] != ' ']
        board_game_data_copy = board_game_data_copy[board_game_data_copy['publisher'] != '(Self-Published)']
        board_game_data_copy = board_game_data_copy[board_game_data_copy['publisher'] != '(Web published)']
        board_game_data_copy = board_game_data_copy.sort_values("rank")

        board_game_data_copy['mechanic'] = board_game_data_copy['mechanic'].str.rsplit(',').str[0]
        board_game_data_copy['designer'] = board_game_data_copy['designer'].str.rsplit(',').str[0]
        board_game_data_copy['category'] = board_game_data_copy['category'].str.rsplit(',').str[0]
        board_game_data_copy['publisher'] = board_game_data_copy['publisher'].str.rsplit(',').str[0]

        board_game_data_copy = board_game_data_copy[:1000]

        category_count = board_game_data_copy.groupby(['category']).count()[['name']]
        self.unique_categories = list(category_count.sort_values('name', ascending=False).head(10).index)

        desinger_count = board_game_data_copy.groupby(['designer']).count()[['name']]
        self.unique_designers = list(desinger_count.sort_values('name', ascending=False).head(10).index)

        publisher_count = board_game_data_copy.groupby(['publisher']).count()[['name']]
        publisher_count = publisher_count[publisher_count.index != '(Web published)']
        publisher_count = publisher_count[publisher_count.index != '(Self-Published)']
        self.unique_publishers = list(publisher_count.sort_values('name', ascending=False).head(10).index)

    def category_list(self):
        unique_categories = self.board_game_data['category'].tolist()
        unique_categories = [category.split(', ') for category in unique_categories]
        unique_categories = set(chain(*unique_categories))
        return unique_categories

    def designer_list(self):
        unique_designers = self.board_game_data['designer'].tolist()
        unique_designers = [designer.split(', ') for designer in unique_designers]
        unique_designers = set(chain(*unique_designers))
        return unique_designers

    def one_hot_encoding(self):
        for category in self.unique_categories:
            self.board_game_data["cat_"+category] = self.board_game_data.category.apply(lambda x: 1 if category in x else 0)
        for publisher in self.unique_publishers:
            self.board_game_data["pub_"+publisher] = self.board_game_data.publisher.apply(lambda x: 1 if publisher in x else 0)
        for designer in self.unique_designers:
            self.board_game_data["des_"+designer] = self.board_game_data.designer.apply(lambda x: 1 if designer in x else 0)




LoadAndTransform().tranform()
# LoadAndTransform().data_for_modelling()