from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import base64
import json
import os

app = Flask(__name__)
CORS(app)

# Model loading function
def load_model_and_labels():
    try:
        model = tf.keras.models.load_model('model/best_model.h5')
        with open('model/class_indices.json', 'r') as f:
            class_indices = json.load(f)
            labels = {v: k for k, v in class_indices.items()}
        return model, labels
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        # Return a simple demo model and labels for testing
        return None, {"0": "₹10", "1": "₹20", "2": "₹50", "3": "₹100", "4": "₹200", "5": "₹500", "6": "₹2000"}

# Load model and labels
model, labels = load_model_and_labels()

def process_image(image_data):
    # Remove header from base64 string
    image_data = image_data.split(',')[1]
    # Decode base64 image
    image_bytes = base64.b64decode(image_data)
    # Convert to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Preprocess
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        # Get image data from request
        image_data = request.json['image']
        # Process image
        processed_image = process_image(image_data)
        
        if model is not None:
            # Make prediction with actual model
            predictions = model.predict(processed_image)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
        else:
            # Demo mode - simulate detection
            import random
            predicted_class = random.randint(0, 6)
            confidence = random.uniform(0.8, 0.99)
        
        if confidence > 0.7:
            denomination = labels[str(predicted_class)]
            return jsonify({
                'success': True,
                'denomination': denomination,
                'confidence': confidence
            })
        else:
            return jsonify({
                'success': True,
                'denomination': 'No currency detected',
                'confidence': confidence
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Create required directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('model', exist_ok=True)
    # Start server
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
