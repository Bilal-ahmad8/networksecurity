from flask import Flask, request, render_template, send_file
from networksecurity.utils.ml_utils.models_util import NetworkModel
from networksecurity.utils.common import load_object
from networksecurity.pipeline.training_pipeline import TrainingPipeline
import pandas as pd



app = Flask(__name__)

@app.route('/')
def homepage():
    # Render the HTML form when the user accesses the root URL
    return render_template('table.html')

@app.route('/train')
def train():
    pipeline = TrainingPipeline()
    model_trainer_artifact = pipeline.run_pipeline()
    return "Training Successful!"

@app.route('/predict', methods=['POST'])
def inferencing():
    # Check if the 'file' is in the request files
    if 'file' not in request.files:
        return "No file part", 400  # If no file part is present in the request

    file = request.files['file']  # Retrieve the file from the request

    # Check if the file has a filename
    if file.filename == '':
        return "No selected file", 400  # If no file is selected

    try:
        # Read the uploaded CSV file into pandas dataframe
        data = pd.read_csv(file)
        print('Data read successfully')

        # Load preprocessor and model
        preprocessor = load_object('final_model/preprocessor.pkl')
        model = load_object('final_model/model.pkl')

        # Create the model object
        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        # Make predictions (assuming the model has a predict method)
        predictions = network_model.predict(data)

        # Add predictions to the data
        data['Predicted_columns'] = predictions

        # Save the result to a new CSV file
        output_file = 'predicted_outputs/outputs.csv'
        data.to_csv(output_file, index=False)

        return send_file(output_file, as_attachment=True, download_name='predictions.csv')

    except Exception as e:
        return f"Error processing the file: {e}", 500  # Handle any errors





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)