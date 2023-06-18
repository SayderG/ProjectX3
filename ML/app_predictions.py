import pickle
import pandas as pd
import numpy as np


def get_prediction(values, columns):
    with open('ML/models/traffic_forecast_model', 'rb') as f:
        model_lgbm = pickle.load(f)

    np.random.seed(0)
    # Create a DataFrame with the desired structure
    data = pd.DataFrame(values, columns=columns)

    # Convert the 'date' column to datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Set the 'date' column as the index
    data.set_index('date', inplace=True)

    data['year'] = data.index.year
    data['month'] = data.index.month
    data['day'] = data.index.day
    data['hour'] = data.index.hour
    data['dayofweek'] = data.index.dayofweek

    cat_columns = ['year', 'month', 'day', 'hour', 'dayofweek', 'street']
    for col in cat_columns:
        data[col] = data[col].astype('category')

    # Drop the 'number_of_cars' column from the new data
    features = data

    # Make predictions using your trained model
    predictions = model_lgbm.predict(features)
    # Add the predictions to the data DataFrame
    data['predictions'] = predictions
    # Display the generated dataset

    return data


if __name__ == '__main__':
    get_prediction()
