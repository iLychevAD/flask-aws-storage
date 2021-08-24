import os
from flask import Flask, render_template, request, redirect, send_file, jsonify
from s3_functions import list_files, upload_file, show_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = os.environ["BUCKET"]

@app.route("/")
def home():
    contents = list_files(BUCKET)
    return render_template('index.html')

@app.route("/health")
def health_check():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route("/pics")
def list():
    contents = show_image(BUCKET)
    return render_template('collection.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return redirect("/")

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(BUCKET)
    app.run(host="0.0.0.0", debug=True)
