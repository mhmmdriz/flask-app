import numpy as np
import tensorflow as tf
import io
import logging
import sys
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = Flask(__name__)

# Muat model di level global
try:
    model = load_model('Model V2B2.h5')
    logging.info('Model berhasil dimuat')
except Exception as e:
    logging.exception('Error saat memuat model')
    model = None

class_names = ['battery', 'biological', 'cardboard', 'clothes', 'glass', 'metal', 'paper', 'plastic', 'shoes', 'trash']

@app.route('/')
def home():
    return 'Flask server is running'

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model tidak tersedia'}), 500
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        image = image.resize((224, 224))

        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array)
        class_index = np.argmax(predictions)
        class_name = class_names[class_index]
        probability = predictions[0][class_index]

        return jsonify({
            'prediction': class_name,
            'probability': float(probability)
        })
    except Exception as e:
        logging.exception('Error saat melakukan prediksi')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
