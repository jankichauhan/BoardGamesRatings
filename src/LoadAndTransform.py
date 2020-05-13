import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.Modelling import Model

class LoadAndTransform():
    def __init__(self):
        print("in init")
        self.df_data = pd.read_csv('board_game_data.csv')
        self.df_data.columns = ['board_game_id', 'name', 'year', 'minplayer', 'maxplayer', 'playingtime', 'avgratings',
                                'designer', 'category', 'mechanic', 'publisher', 'age', 'rank']
        self.board_game_data = self.df_data

    def tranform(self):
        self.df_data = pd.read_csv('board_game_data.csv')
        self.df_data.columns = ['board_game_id', 'name', 'year', 'minplayer', 'maxplayer', 'playingtime', 'avgratings',
                                'designer', 'category', 'mechanic', 'publisher', 'age', 'rank']
        self.board_game_data = self.df_data
        self.board_game_data = self.board_game_data.fillna('not define')
        self.board_game_data['designer'] = self.board_game_data['designer'].str.replace(':', ', ')
        self.board_game_data['category'] = self.board_game_data['category'].str.replace(':', ', ')
        self.board_game_data['mechanic'] = self.board_game_data['mechanic'].str.replace(':', ', ')
        self.board_game_data['publisher'] = self.board_game_data['publisher'].str.replace(':', ', ')

    def data_for_modelling(self):
        columns = self.board_game_data.columns.tolist()
        columns = [c for c in columns if
                   c not in ['board_game_id', 'name', 'year', 'rank', 'designer', 'category', 'mechanic', 'publisher']]
        target = 'avgratings'

        X = self.board_game_data[columns].values
        y = self.board_game_data[target].values

        print(X)
        print(y)

        # for col in columns:
        #     plt.scatter(self.board_game_data[col], self.board_game_data[target], alpha=0.4)
        #     plt.xlabel(col)
        #     plt.ylabel(target)
        #     plt.show()

        ml_model = Model(X,y)
        ml_model.LinearReg()
        ml_model.RandomForest()
        ml_model.GradientBoost()


LoadAndTransform().tranform()
LoadAndTransform().data_for_modelling()