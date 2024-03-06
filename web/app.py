from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        # Save the file to a desired location or storage service
        file.save('uploads/' + file.filename)  # Adjust the path as needed
        return 'File uploaded successfully!'
    else:
        return 'No file uploaded.'



if __name__ == '__main__':
    app.run(debug=True)
