from flask import Flask, request, send_file, render_template_string, after_this_request
from PyPDF2 import PdfMerger
import os
import io

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>PDF Merger</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; text-align: center; padding-top: 50px; }
        .container { width: 80%; margin: auto; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h2 { color: #333; }
        .form-group { margin-top: 20px; }
        .button {
            cursor: pointer;
            padding: 10px 20px;
            background: #00adee;
            border: none;
            color: white;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 10px;
            display: inline-block;
        }
        .button:hover {
            background: #007ba7;
        }
        .file-input { display: none; }
        #fileList { margin-top: 20px; }
        #fileList div { padding: 5px; border-bottom: 1px solid #ddd; }
        .spinner { display: none; margin: 20px auto; width: 50px; height: 50px; border: 5px solid rgba(0, 0, 0, 0.1); border-radius: 50%; border-top: 5px solid #333; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .download-btn {
            display: none;
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
        }
        .download-btn:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h2>PDF Merger</h2>
        <form id="uploadForm" enctype="multipart/form-data">
            <label for="pdf-input">Select PDF files (you can select multiple by clicking with CTRL or SHIFT):</label>
            <input type="file" name="pdf" class="file-input" accept=".pdf" multiple>
            <div class="form-group">
                <button type="button" id="addMore" class="button">Add More PDFs</button>
            </div>
            <button type="submit" class="button">Merge PDFs</button>
        </form>
        <div id="fileList"></div>
        <a id="downloadLink" class="download-btn button">Download Merged PDF</a>
        <div class="spinner" id="loadingSpinner"></div>
    </div>

    <script>
        let allFiles = [];
        
        document.getElementById('addMore').onclick = function(e) {
            const fileInput = document.querySelector('input[type=file]');
            fileInput.click();
        };
        
        document.querySelector('input[type=file]').onchange = function(e) {
            for (let i = 0; i < this.files.length; i++) {
                allFiles.push(this.files[i]);
            }
            updateFileList();
        };

        function updateFileList() {
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '';
            allFiles.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.textContent = file.name;
                fileList.appendChild(fileItem);
            });
        }

        document.getElementById('uploadForm').onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData();
            allFiles.forEach(file => {
                formData.append('pdfs', file);
            });
            
            const loadingSpinner = document.getElementById('loadingSpinner');
            const downloadLink = document.getElementById('downloadLink');
            loadingSpinner.style.display = 'block';
            downloadLink.style.display = 'none';

            fetch('/', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                downloadLink.href = url;
                downloadLink.download = 'merged_document.pdf';
                downloadLink.style.display = 'block';
                loadingSpinner.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                loadingSpinner.style.display = 'none';
            });
        };
    </script>
</body>
</html>
'''



@app.route('/', methods=['GET', 'POST'])
def upload_pdfs():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdfs')
        merger = PdfMerger()

        for pdf in pdf_files:
            merger.append(pdf)

        merged_pdf = io.BytesIO()
        merger.write(merged_pdf)
        merger.close()
        merged_pdf.seek(0)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(merged_pdf)
            except Exception as error:
                app.logger.error("Error removing merged PDF file", error)
            return response

        return send_file(merged_pdf, mimetype='application/pdf', as_attachment=True, download_name='merged_document.pdf')

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
