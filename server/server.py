from flask import Flask, Response, request, jsonify
import os

FILE_STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stored_files')

app = Flask(__name__)

@app.route('/list-files', methods=['GET'])
def list_files():
    list_of_files = os.listdir(FILE_STORAGE_PATH)
    return jsonify({'files': list_of_files})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'candidate_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file_dict = request.files
    file = file_dict['candidate_file']
    if file.filename == '':
        return jsonify({'error': 'filename is not given'}), 400
    
    file.save(os.path.join(FILE_STORAGE_PATH, f'{file.filename}'))
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/upload-files', methods=['POST'])
def upload_files():
    if not request.files:
        return jsonify({'error': 'You must send at least one file.'}), 400

    file_dict = request.files
    for _, file in file_dict.items():
        if file.filename == '':
            return jsonify({'error': 'filename is not given'}), 400
        file.save(os.path.join(FILE_STORAGE_PATH, f'{file.filename}'))
    return jsonify({'message': 'files uploaded successfully'})


@app.route('/delete-files', methods=['POST'])
def delete_files():
    if not request.files:
        return jsonify({'error': 'You must send at least one file.'}), 400

    file_dict = request.files
    for _, file in file_dict.items():
        if file.filename == '':
            return jsonify({'error': 'filename is not given'}), 400
        target_file_path = os.path.join(FILE_STORAGE_PATH, f'{file.filename}')
        if not os.path.exists(target_file_path):
            return jsonify({'error': f'{file.filename} does not exist'})
        os.remove(target_file_path)
    return jsonify({'message': 'File deleted successfully'})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=55000, debug=True)
