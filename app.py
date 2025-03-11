from flask import Flask, request, render_template, send_file
from networksecurity.utils.ml_utils.models_util import NetworkModel
from networksecurity.utils.common import load_object
from networksecurity.pipeline.training_pipeline import TrainingPipeline
import pandas as pd

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Welcome'

@app.route('/train')
def train():
    pipeline = TrainingPipeline()
    model_trainer_artifact = pipeline.run_pipeline()
    return "Training Successful!"

@app.route('/predict', methods=['POST'])
def inferencing():
    file = request.files['file']  # Get the file from the request
    data = pd.read_csv(file)
    print('Data read successfully')

    # Uncomment and update paths to load your preprocessor and model correctly
    preprocessor = load_object('final_model/preprocessor.pkl')
    model = load_object('final_model/model.pkl')

    # Create the model object
    network_model = NetworkModel(preprocessor=preprocessor, model=model)

    # Make predictions (assuming the model has a predict method)
    predictions = network_model.predict(data)
    data['Predicted_columns'] = predictions
    data.to_csv('predicted_outputs/outputs.csv', index=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)