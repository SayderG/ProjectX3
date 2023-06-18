import pandas as pd

import numpy as np
import pickle
from functions import make_features, find_best_time_series_params, fit_lgbm_model
from tqdm import tqdm


def generate_model(train_path: str = 'training_data.csv'):
    df = pd.read_csv(f'trains/{train_path}', index_col='date')
    df.index = pd.to_datetime(df.index)

    rmse, lag, window = find_best_time_series_params(df)
    model_lgbm = fit_lgbm_model(df, lag, window)

    with open('models/traffic_forecast_model', 'wb') as f:
        pickle.dump(model_lgbm, f)


if __name__ == '__main__':
    generate_model()
