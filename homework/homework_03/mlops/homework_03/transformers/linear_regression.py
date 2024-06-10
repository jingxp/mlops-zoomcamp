import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def export(df):

    numerical = ['trip_distance']
    categorical = ['PULocationID', 'DOLocationID']
    target = 'duration'

    dicts = df[categorical + numerical].to_dict(orient='records')
    dv = DictVectorizer()

    X = dv.fit_transform(dicts)
    y = df[target].values

    lr = LinearRegression()
    lr.fit(X, y)

    print(lr.intercept_)

    return lr, dv
