import io

import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model("./models/waste_classification_v1.keras")

class_names = [
    "Dry-waste",
    "E-waste",
    "Hazardous-waste",
    "Wet-waste",
]

IMG_SIZE = (224, 224)


def preprocess_image(img):
    img = img.resize(IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    return img_array


def predict_waste_type(img):
    # img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = preprocess_image(img)
    prediction = model.predict(img_array)
    predicted_class_index = tf.argmax(prediction[0]).numpy()
    confidence = tf.reduce_max(prediction[0]).numpy()
    predicted_class = class_names[predicted_class_index]
    return predicted_class, confidence


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    try:
        img = Image.open(io.BytesIO(file.read()))
    except Exception as e:
        return jsonify({"error": f"Invalid image: {str(e)}"}), 400

    predicted_class, confidence = predict_waste_type(img)
    return jsonify({"prediction": predicted_class, "confidence": float(confidence)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
