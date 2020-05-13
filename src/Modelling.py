import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


class Model:

    def __init__(self, X, y):
        print("in init")
        self.X = X
        self.y = y

        self.X_train,self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2)


    def LinearReg(self):
        linear_model = LinearRegression().fit(self.X_train, self.y_train)
        predictions = linear_model.predict(self.X_test)
        print(mean_squared_error(self.y_test, predictions))


    def RandomForest(self):
        random_forest = RandomForestRegressor().fit(self.X_train, self.y_train)
        predictions = random_forest.predict(self.X_test)
        print(mean_squared_error(self.y_test, predictions))


    def GradientBoost(self):
        gradient_boost = GradientBoostingRegressor().fit(self.X_train, self.y_train)
        predictions = gradient_boost.predict(self.X_test)
        print(mean_squared_error(self.y_test, predictions))
