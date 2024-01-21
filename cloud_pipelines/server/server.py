from flask import Flask, request, jsonify, send_file
import numpy as np
from PIL import Image
from io import BytesIO
from minio import Minio
from minio.error import S3Error

app = Flask(__name__)

# Minio configurations
MINIO_ENDPOINT = 'minio:9000'
MINIO_ACCESS_KEY = 'ARl1xYLr9Or8Jo4W5e6E'
MINIO_SECRET_KEY = 'aMwUjJF3GjaGeq6Tt8scB6jzROvxpl8wF1syqMMC'
MINIO_INPUT_BUCKET_NAME = 'initial'
MINIO_OUTPUT_BUCKET_NAME = 'grayscale'

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
            bucket_name=MINIO_OUTPUT_BUCKET_NAME,
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

@app.route('/grayscale', methods=['POST'])
def grayscale(): 
    # Get the binary data from the request
    filename = request.args.get('filename')
    if not filename:
        filename = request.form.get('filename')

    print("filename: ", filename, flush=True)

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
