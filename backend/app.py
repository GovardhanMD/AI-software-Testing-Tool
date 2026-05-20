from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import database
import test_generator
import executor

app = Flask(__name__, static_folder='../frontend')
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

database.init_db()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('../frontend', 'dashboard.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    return jsonify({
        'message': 'File uploaded successfully',
        'filename': file.filename,
        'filepath': filepath
    })

@app.route('/api/generate-tests', methods=['POST'])
def generate_tests():
    data = request.json
    filename = data.get('filename')
    use_ai = data.get('use_ai', False)
    api_key = data.get('api_key', '')
    
    if not filename:
        return jsonify({'error': 'Filename required'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if filename.endswith('.json'):
        test_cases = test_generator.generate_api_test_cases(content)
    elif use_ai and api_key:
        test_cases = test_generator.generate_test_cases_ai(content, filename, api_key)
    else:
        test_cases = test_generator.generate_test_cases_simple(content, filename)
    
    return jsonify({
        'test_cases': test_cases,
        'count': len(test_cases)
    })

@app.route('/api/execute-tests', methods=['POST'])
def execute_tests():
    data = request.json
    test_cases = data.get('test_cases', [])
    filename = data.get('filename', 'unknown')
    
    if not test_cases:
        return jsonify({'error': 'No test cases provided'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    code_file = filepath if os.path.exists(filepath) else None
    
    execution_result = executor.execute_test_cases(test_cases, code_file)
    
    run_id = database.save_test_run(
        filename,
        execution_result['total'],
        execution_result['passed'],
        execution_result['failed'],
        execution_result['results']
    )
    
    return jsonify({
        'run_id': run_id,
        'execution_result': execution_result
    })

@app.route('/api/get-test-runs', methods=['GET'])
def get_test_runs():
    runs = database.get_all_runs()
    return jsonify({'runs': runs})

@app.route('/api/get-test-runs/<int:run_id>', methods=['GET'])
def get_test_run(run_id):
    run = database.get_run_by_id(run_id)
    if not run:
        return jsonify({'error': 'Run not found'}), 404
    return jsonify(run)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
