import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split,KFold,cross_val_score,GridSearchCV
import matplotlib.pyplot as plt


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
        print(r2_score(self.y_test, predictions))
        print(explained_variance_score(self.y_test, predictions))



    def RandomForest(self, features):
        random_forest = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=90, max_features=5, max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_impurity_split=None, min_samples_leaf=3,
                      min_samples_split=12, min_weight_fraction_leaf=0.0,
                      n_estimators=1000, n_jobs=None, oob_score=False,
                      random_state=None, verbose=0, warm_start=False).fit(self.X_train, self.y_train)
        predictions = random_forest.predict(self.X_test)
        print(mean_squared_error(self.y_test, predictions))
        print(r2_score(self.y_test, predictions))
        print(explained_variance_score(self.y_test, predictions))
        print(random_forest.feature_importances_)
        print(predictions)
        print(self.y_test)

        feat_scores = pd.DataFrame({'Fraction of Samples Affected': random_forest.feature_importances_},
                                   index=features)
        feat_scores = feat_scores.sort_values(by='Fraction of Samples Affected')
        feat_scores.plot(kind='barh')
        plt.show()



    def GradientBoost(self):
        gradient_boost = GradientBoostingRegressor(learning_rate=0.2, n_estimators=1000, max_features=20 ).fit(self.X_train, self.y_train)
        predictions = gradient_boost.predict(self.X_test)
        print(mean_squared_error(self.y_test, predictions))
        print(r2_score(self.y_test, predictions))
        print(explained_variance_score(self.y_test, predictions))
        print(predictions)
        print(self.y_test)

    def grid_search_cv_rf(self):
        param_grid = {
            'bootstrap': [True],
            'max_depth': [80, 90, 100, 110],
            'max_features': [2, 3],
            'min_samples_leaf': [3, 4, 5],
            'min_samples_split': [8, 10, 12],
            'n_estimators': [1000, 2000, 3000]
        }
        rf_gridsearch = GridSearchCV(RandomForestRegressor(),
                                     param_grid,
                                     n_jobs=-1,
                                     verbose=True)
        rf_gridsearch.fit(self.X_train, self.y_train)

        print("best parameters:", rf_gridsearch.best_params_)

        print(rf_gridsearch.best_estimator_)

    def grid_search_cv_gb(self):
        gb_grid = {'n_estimators': [1000, 2000, 3000],
                   'min_samples_leaf': [1, 2, 3],
                   'max_depth': [5, 10, 15],
                   'max_features': [10, 15, 20],
                   'learning_rate': [.05, .1, .15, .2]}
        gb_gridsearch = GridSearchCV(GradientBoostingRegressor(),
                                     gb_grid,
                                     n_jobs=-1,
                                     verbose=True,
                                     scoring='accuracy')
        gb_gridsearch.fit(self.X_train, self.y_train)

        print("best parameters:", gb_gridsearch.best_params_)

        print(gb_gridsearch.best_estimator_)
