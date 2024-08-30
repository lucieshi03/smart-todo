from flask import Flask, request, jsonify, render_template
import joblib
import pickle
import pandas as pd

# import clean_up function from ml.py
from ml import clean_up

app = Flask(__name__)

# Load the model and vectorizer
model = joblib.load('nb.joblib')
vectorizer = joblib.load('vec.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_task():
    task = request.json.get('task-input')
    # Clean and vectorize the task
    cleaned_text = clean_up(task)
    vec_text = vectorizer.transform([cleaned_text])
    prediction = model.predict(vec_text)
    return jsonify({'category': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
