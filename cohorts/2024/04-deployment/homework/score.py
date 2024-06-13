#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import argparse

def read_data(filename, categorical):
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def load_model(model_path):
    with open(model_path, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def duration_prediction(model, dv, df, categorical):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred

def main(year, month):
    categorical = ['PULocationID', 'DOLocationID']
    filename = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    df = read_data(filename, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    model_path = 'model.bin'
    dv, model = load_model(model_path)
    predictions = duration_prediction(model, dv, df, categorical)
    df_result = df[['ride_id']].copy()
    df_result['predictions'] = predictions
    print(df_result['predictions'].mean())
    
    output_file = f'yellow_tripdata_{year:04d}-{month:02d}.parquet'
    df_result.to_parquet(output_file,
                         engine='pyarrow',
                         compression=None,
                         index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--year', type=int, required=True, help='Year to process')
    parser.add_argument('--month', type=int, required=True, help='Month to process')

    args = parser.parse_args()
    main(args.year, args.month)


