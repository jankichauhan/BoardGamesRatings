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

        self.X_train,self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3)


    def LinearReg(self):
        linear_model = LinearRegression().fit(self.X_train, self.y_train)
        predictions = linear_model.predict(self.X_test)
        print("Linear Regression MSE : ", mean_squared_error(self.y_test, predictions))
        print("Linear Regression R2 score :", r2_score(self.y_test, predictions))
        print(explained_variance_score(self.y_test, predictions))



    def RandomForest(self, features):
        random_forest = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=90, max_features=19, max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_impurity_split=None, min_samples_leaf=3,
                      min_samples_split=10, min_weight_fraction_leaf=0.0,
                      n_estimators=2000, n_jobs=None, oob_score=False,
                      random_state=None, verbose=0, warm_start=False).fit(self.X_train, self.y_train)
        predictions = random_forest.predict(self.X_test)
        print("Random Forest MSE : ", mean_squared_error(self.y_test, predictions))
        print("Random Forest R2 score :", r2_score(self.y_test, predictions))
        print(explained_variance_score(self.y_test, predictions))
        self.feature_score(random_forest,features)



    def GradientBoost(self, features):
        gradient_boost = GradientBoostingRegressor(learning_rate=0.05, max_depth=5, max_features=10,
                          min_samples_leaf=2, n_estimators=1000).fit(self.X_train, self.y_train)
        predictions = gradient_boost.predict(self.X_test)
        print("Gradient Boost MSE : ", mean_squared_error(self.y_test, predictions))
        print("Gradient Boost R2 score :", r2_score(self.y_test, predictions))
        print(explained_variance_score(self.y_test, predictions))
        self.feature_score(gradient_boost, features)

    # Plotting feature score
    def feature_score(self, model, features):
        feat_scores = pd.DataFrame({'Fraction of Samples Affected': model.feature_importances_},
                           index=features)
        feat_scores = feat_scores.sort_values(by='Fraction of Samples Affected')
        feat_scores.plot(kind='barh')
        plt.show()

    # Grid search logic
    def grid_search_cv(self, model):

        model_search = ''

        if model == 'rf':
            param_grid = {
                'bootstrap': [True],
                'max_depth': [80, 90, 100, 110],
                'max_features': [2, 3],
                'min_samples_leaf': [3, 4, 5],
                'min_samples_split': [8, 10, 12],
                'n_estimators': [1000, 2000, 3000]
            }
            model_search = GridSearchCV(RandomForestRegressor(),
                                         param_grid,
                                         n_jobs=-1,
                                         verbose=True)
        elif model == 'gb':
            param_grid = {'n_estimators': [1000, 2000, 3000],
                       'min_samples_leaf': [1, 2, 3],
                       'max_depth': [5, 10, 15],
                       'max_features': [10, 15, 20],
                       'learning_rate': [.05, .1, .15, .2]}
            model_search = GridSearchCV(GradientBoostingRegressor(),
                                         param_grid,
                                         n_jobs=-1,
                                         verbose=True,
                                         scoring='neg_mean_squared_error')
        else:
            print("Not a valid model")
            return None

        model_search.fit(self.X_train, self.y_train)

        print("Results for: ", model)
        print("best parameters:", model_search.best_params_)
        print(model_search.best_estimator_)

        return model_search.best_estimator_



