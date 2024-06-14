from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

app = Flask(__name__)

# Example data: features might include previous geographic points, time, etc.
data = {
    'previous_lat': [40.7128, 34.0522, 41.8781, 29.7604, 39.7392],
    'previous_long': [-74.0060, -118.2437, -87.6298, -95.3698, -104.9903],
    'new_lat': [40.7138, 34.0532, 41.8791, 29.7614, 39.7402],
    'new_long': [-74.0050, -118.2427, -87.6288, -95.3688, -104.9893]
}

df = pd.DataFrame(data)

# Prepare the data
X = df[['previous_lat', 'previous_long']]
y = df[['new_lat', 'new_long']]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Route to predict new geographic point
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get previous_lat, previous_long, new_lat, new_long from the form
    previous_lat = float(request.form['previous_lat'])
    previous_long = float(request.form['previous_long'])

    # Predict new_lat and new_long
    new_data = np.array([[previous_lat, previous_long]])
    new_point = model.predict(new_data)

    # Create the response
    response = {
        'predicted_lat': new_point[0][0],
        'predicted_long': new_point[0][1]
    }

    return render_template('result.html', result=response)

if __name__ == '__main__':
    app.run(debug=True)

