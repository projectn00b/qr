import os
from PIL import Image
import qrcode
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

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

    qr_img = qr.make_image(fill_color="black",
                           back_color="white").convert('RGB')

    # Correct way to access the static file
    static_file_path = os.path.join(app._static_folder, image_path)
    overlay_img = Image.open(static_file_path)
    overlay_img = overlay_img.resize(qr_img.size).convert('RGB')

    # Diagnostic print
    print(f"QR Image Size: {qr_img.size}, Mode: {qr_img.mode}")
    print(f"Overlay Image Size: {overlay_img.size}, Mode: {overlay_img.mode}")

    # Blend the images
    blended_img = Image.blend(qr_img, overlay_img, alpha=0.5)
    # Generate a timestamp-based file name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"output_{timestamp}.jpg"
    output_path = os.path.join(app._static_folder, filename)
    blended_img.save(output_path)

    # Return only the filename, not the full path
    return filename
  except Exception as e:
    print(f"An error occurred: {e}")
    return None


@app.route("/generate_qr")
def generate_qr():
  url = "https://example.com"
  static_file_path = os.path.join(app._static_folder, "invite.png")
  output_path = generate_qr_code_with_image(url, static_file_path)

  if output_path:
    return jsonify({"output_path": output_path})
  else:
    return jsonify(
        {"error": "An error occurred while generating the QR code."})


@app.route("/")
def index():
  static_file_path = os.path.join(app._static_folder, "invite.png")
  image_path = generate_qr_code_with_image("https://example.com",
                                           static_file_path)
  return render_template("index.html", image_path=image_path)


@app.route('/static/<path:filename>')
def static_files(filename):
  return send_from_directory(app._static_folder, filename)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
