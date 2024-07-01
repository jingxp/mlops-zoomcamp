#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from datetime import datetime
import argparse


os.environ["S3_ENDPOINT_URL"] = "http://localhost:4566"
os.environ["INPUT_FILE_PATTERN"] = "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
os.environ["OUTPUT_FILE_PATTERN"] = "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def create_fake_df():
    data = [
            (None, None, dt(1, 1), dt(1, 10)),
            (1, 1, dt(1, 2), dt(1, 10)),
            (1, None, dt(1, 2, 0), dt(1, 2, 59)),
            (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
            ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    data_df = pd.DataFrame(data, columns=columns)
    return data_df

def write_input_to_s3(year, month):
    input_file = os.environ["INPUT_FILE_PATTERN"].format(year=year, month=month)
    df_input = create_fake_df()
    
    options = {
        'client_kwargs': {
            'endpoint_url': os.getenv("S3_ENDPOINT_URL")
            }
        }

    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

def main():
    parser = argparse.ArgumentParser(description="Indicate the year and month to analysis")
    parser.add_argument('--year', type=int, help="Year")
    parser.add_argument('--month', type=int, help="month")
    args = parser.parse_args()
    
    year = args.year
    month = args.month
    write_input_to_s3(year, month)
    command = "python batch.py --year 2024 --month 1"
    os.system(command)

if __name__ == '__main__':
    main()