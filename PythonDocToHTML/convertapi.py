from flask import Flask, request, send_file, jsonify
import os
import uuid
from spire.doc import Document, FileFormat
from bs4 import BeautifulSoup

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/convert", methods=['GET', 'POST'])
def convert_doc_to_html():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]

    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, file_id + ".docx")
    output_path_full = os.path.join(OUTPUT_FOLDER, file_id + "_full.html")
    output_body_path = os.path.join(OUTPUT_FOLDER, file_id + "_body.html")

    uploaded_file.save(input_path)

    # Convert DOCX → HTML
    document = Document()
    document.LoadFromFile(input_path)
    document.HtmlExportOptions.ImageEmbedded = True
    document.SaveToFile(output_path_full, FileFormat.Html)
    document.Dispose()

    # Extract only <body> content
    with open(output_path_full, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body.decode_contents()  # Extract inner HTML

    # Remove evaluation warning from output
    body_content = body_content.replace(
        "Evaluation Warning: The document was created with Spire.Doc for Python.", ""
    )

    # Save cleaned HTML body content
    with open(output_body_path, "w", encoding="utf-8") as f:
        f.write(body_content)

    return send_file(output_body_path, as_attachment=True, download_name="converted_body.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
