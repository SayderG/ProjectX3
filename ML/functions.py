import pandas as pd
from tqdm import tqdm
import lightgbm as lgb
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

def make_features(data, max_lag, rolling_mean_size):
    "function helper to generate important features for model training"
    data['year'] = data.index.year
    data['month'] = data.index.month
    data['day'] = data.index.day
    data['hour'] = data.index.hour
    data['dayofweek'] = data.index.dayofweek
    
    cat_columns=['year','month','day','hour','dayofweek','street']
    for col in cat_columns:
        data[col]=data[col].astype('category')
    

    lag_cols = []
    new_data = pd.DataFrame()
    for i in range(1, max_lag + 1):
        column_name = "lag_" + str(i)
        new_data[column_name] = data['number_of_cars'].shift(i)
        lag_cols.append(column_name)
    
    data = pd.concat([data, new_data], axis=1)
    data['rolling_mean'] = data[lag_cols].rolling(rolling_mean_size).mean().values[:, -1]
    
    return data


def find_best_time_series_params(df):
    best_rmse = 60
    lag = 0
    window = 0
    tscv = TimeSeriesSplit(n_splits=5)
    scoring_metric='neg_mean_squared_error'

    for i in tqdm(range(5, 100, 5)):
        for k in tqdm(range(2, 50, 5)):
            data = df.copy(deep=True)
            make_features(data, i, k)
            data = data.dropna()
            target = data['number_of_cars']
            features = data.drop(['number_of_cars'], axis=1)
    
            
            model_lgbm = lgb.LGBMRegressor()
            scores = cross_val_score(model_lgbm, features, target, cv=tscv, scoring=scoring_metric)
            rmse = np.sqrt(np.abs(np.mean(scores)))
            
            if rmse < best_rmse:
                best_rmse = rmse
                lag = i
                window = k

    print('Best RMSE:', best_rmse)
    print('Lag:', lag)
    print('Window:', window)

    return (best_rmse,lag,window)





def fit_lgbm_model(df,lag,window):
    data = df.copy(deep=True)
    make_features(data, lag, window)
    data = data.dropna()
    target = data[['number_of_cars']]
    features = data.drop(['number_of_cars'], axis=1)
    model_lgbm = lgb.LGBMRegressor()
    model_lgbm.fit(features,target)
    return model_lgbm