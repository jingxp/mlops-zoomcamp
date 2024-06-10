import mlflow
import mlflow.sklearn

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

mlflow.set_tracking_uri('http://mlflow:5000')
@data_exporter
def export_data(data):
    lr_model, dv = data
    with mlflow.start_run():
        print(mlflow.get_tracking_uri())
        mlflow.sklearn.log_model(lr_model,"models")
        mlflow.sklearn.log_model(dv, "dict_vectorizer")


