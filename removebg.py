from flask import Flask, request, send_file, render_template_string
from rembg import remove
import io

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Image Background Remover</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; text-align: center; padding-top: 50px; }
        .container { width: 80%; margin: auto; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h2 { color: #333; }
        #uploadForm { margin-top: 20px; }
        #uploadForm input[type=file] { margin-bottom: 10px; }
        #uploadForm button { cursor: pointer; padding: 10px 20px; background: #00adee; border: none; color: white; }
        #uploadForm button:hover { background: #007ba7; }
        #imagePreview { margin-top: 20px; }
        #imagePreview img { max-width: 100%; max-height: 400px; border: 1px solid #ddd; }
        .spinner { margin: 20px auto; width: 50px; height: 50px; border: 5px solid rgba(0, 0, 0, 0.1); border-radius: 50%; border-top: 5px solid #333; animation: spin 1s linear infinite; display: none; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
             .download-btn {
            display: none;
            margin-top: 20px;
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .download-btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Image Background Remover</h2>
        <form id="uploadForm" method="post" enctype="multipart/form-data">
            <input type="file" name="image" required>
            <button type="submit">Upload Image</button>
        </form>
        <div id="imagePreview"></div>
        <a id="downloadLink" class="download-btn">Download Image</a>
        <div class="spinner" id="loadingSpinner"></div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', function(e) {
            e.preventDefault();
            var formData = new FormData(this);
            var loadingSpinner = document.getElementById('loadingSpinner');
            var imagePreview = document.getElementById('imagePreview');
            var downloadLink = document.getElementById('downloadLink');
            loadingSpinner.style.display = 'block';
            imagePreview.innerHTML = '';
            downloadLink.style.display = 'none';

            fetch('/', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.blob())
            .then(blob => {
                var imgURL = URL.createObjectURL(blob);
                var img = document.createElement('img');
                img.src = imgURL;
                imagePreview.appendChild(img);
                loadingSpinner.style.display = 'none';
                
                downloadLink.href = imgURL;
                downloadLink.download = 'processed_image.png';
                downloadLink.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                loadingSpinner.style.display = 'none';
            });
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No image file in request', 400
        
        file = request.files['image']
        if file.filename == '':
            return 'No selected file', 400

        # Used rembg to remove the background
        input_image = file.read()
        output_image = remove(input_image)

        return send_file(io.BytesIO(output_image), mimetype='image/png')

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
