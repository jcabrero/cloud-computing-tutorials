from flask import Flask, request, jsonify, send_file
import numpy as np
from PIL import Image
from io import BytesIO
from minio import Minio
from minio.error import S3Error
import os
import base64

app = Flask(__name__)

#env_from_b64 = lambda x: base64.b64decode(os.getenv(x)).decode()

# Minio configurations
MINIO_ENDPOINT = os.getenv("minio_endpoint")
print(os.getenv("minio_access_key"))
MINIO_ACCESS_KEY = os.getenv("minio_access_key")
print(os.getenv("minio_secret_key"))
MINIO_SECRET_KEY = os.getenv("minio_secret_key")
MINIO_INPUT_BUCKET_NAME = os.getenv("minio_bucket")
MINIO_OUTPUT_BUCKET_NAME = os.getenv("minio_bucket")

def download_from_minio(filename):
    try:
        # Initialize Minio client
        minio_client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False  # Change to True if using HTTPS
        )

        # Download the file from Minio
        response = minio_client.get_object(
            bucket_name=MINIO_INPUT_BUCKET_NAME,
            object_name=filename
        )

        # Read the content of the file
        image_data = response.read()

        return image_data

    except S3Error as err:
        print(f"Minio error: {err}")
        return None

def upload_to_minio(filename, image_data):
    try:
        # Initialize Minio client
        minio_client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False  # Change to True if using HTTPS
        )

        # Upload the grayscale image to Minio
        minio_client.put_object(
            bucket_name=MINIO_INPUT_BUCKET_NAME,
            object_name=filename,
            data=BytesIO(image_data),
            length=len(image_data),
            content_type='image/jpeg'
        )

        print(f"Grayscale image '{filename}' uploaded to Minio.")
    except S3Error as err:
        print(f"Minio upload error: {err}")



def rgb_to_gray(image):
    # Convert RGB to grayscale using a weighted sum
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])


@app.route('/', methods=['GET'])
def index():
    # Read pod name from /etc/hostname
    with open('/etc/hostname') as f:
        pod_name = f.read()

    # Build the formatted HTML response
    response = f"""
    <html>
    <head>
        <title>Flask App</title>
    </head>
    <body>
        <h1>Hello!</h1>
        <p>Pod <strong>{pod_name.strip()}</strong> answered the request.</p>
        <ul>
            <li>MINIO_ENDPOINT: {MINIO_ENDPOINT}</li>
            <li>MINIO_ACCESS_KEY: {MINIO_ACCESS_KEY}</li>
            <li>MINIO_SECRET_KEY: {MINIO_SECRET_KEY}</li>
            <li>MINIO_INPUT_BUCKET_NAME: {MINIO_INPUT_BUCKET_NAME}</li>
        </ul>
    </body>
    </html>
    """
    return response


@app.route('/test', methods=['GET'])
def test(): 
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grayscale Image Form</title>
</head>
<body>

    <h2>Grayscale Image Conversion</h2>
    
    <form action="/grayscale" method="post">
        <label for="filename">Enter the image filename:</label>
        <input type="text" id="filename" name="filename" required>
        <br>
        <input type="submit" value="Convert to Grayscale">
    </form>

</body>
</html>
"""


@app.route('/grayscale', methods=['POST'])
def grayscale(): 
    # Get the binary data from the request
    filename = request.args.get('filename')
    
    
    if not filename:
        filename = request.form.get('filename')
    print("filename: ", filename)
    if not filename:
        return jsonify({'error': 'Filename parameter is required.'}), 400

    # Download the image from Minio
    image_data = download_from_minio(filename)

    # Convert binary data to NumPy array
    #image_array = np.array(Image.open(BytesIO(image_data)))
    image_array = Image.open(BytesIO(image_data))
    # Convert RGB to grayscale
    #gray_array = rgb_to_gray(image_array)
    gray_array = image_array.convert('LA')
    # Create a PIL image from the grayscale array
    grayscale_image = Image.fromarray(np.uint8(gray_array))

    # Save the grayscale image to a BytesIO object
    output_buffer = BytesIO()
    grayscale_image.save(output_buffer, format="PNG")

    # Get the binary data of the grayscale image
    output_binary = output_buffer.getvalue()
    
    # Upload the grayscale image back to Minio
    new_file = f"grayscale_{filename}"
    upload_to_minio(new_file, output_binary)

    print("Sending file")
    return jsonify({"new_file": new_file})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)