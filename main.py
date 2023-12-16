import os
from PIL import Image
import qrcode
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS  # Import the CORS extension
from datetime import datetime  # Import the datetime module

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Define a static folder to serve static files like favicon.ico
app._static_folder = os.path.abspath("static")
def generate_qr_code_with_image(url, image_path):
    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Load and resize the overlay image
        overlay_img = Image.open(image_path)
        overlay_img = overlay_img.resize(qr_img.size).convert('RGB')

        # Diagnostic print to check sizes and modes
        print(f"QR Image Size: {qr_img.size}, Mode: {qr_img.mode}")
        print(f"Overlay Image Size: {overlay_img.size}, Mode: {overlay_img.mode}")

        # Blend the images
        blended_img = Image.blend(qr_img, overlay_img, alpha=0.5)

        # Generate a timestamp-based file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f"output_{timestamp}.jpg"

        # Save the result
        blended_img.save(output_path)

        return output_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
@app.route("/generate_qr")
def generate_qr():
    url = "https://example.com"
    image_path = "invite.png"

    output_path = generate_qr_code_with_image(url, image_path)

    if output_path:
        # Return JSON data
        return jsonify({"output_path": output_path})
    else:
        return jsonify({"error": "An error occurred while generating the QR code."})

@app.route("/")  # Route for serving the HTML file
def index():
    image_path = generate_qr_code_with_image("https://example.com", "invite.png")
    return render_template("index.html")

@app.route("/script.js")  # Route for serving the JavaScript file
def script():
    return render_template("script.js")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app._static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host="0.0.0.0")  # Change port to the desired value