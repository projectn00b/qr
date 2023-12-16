import os
from PIL import Image
import qrcode
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def generate_qr_code_with_image(url, image_path, output_path):
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        return

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

        # Save the result
        blended_img.save(output_path)
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route("/generate_qr")
def generate_qr():
    url = "https://example.com"
    image_path = "invite.png"
    output_path = "output.jpg"

    generate_qr_code_with_image(url, image_path, output_path)

    # Return JSON data
    return jsonify({"output_path": output_path})
    
@app.route("/")  # Route for serving the HTML file
def index():
    return render_template("index.html")

@app.route("/script.js")  # Route for serving the JavaScript file
def script():
    return render_template("script.js")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for detailed error messages (for development)
