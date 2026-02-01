"""
Flask backend for Educational Content Assistant
Handles PDF uploads, storage, retrieval, and LLM-powered Q&A
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sqlite3
import json
from datetime import datetime
import traceback
from pdf_processor import extract_text_from_pdf
from llm_handler import answer_question

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DB_NAME = 'assistant.db'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pdfs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            content_text TEXT,
            module_name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdf_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pdf_id) REFERENCES pdfs(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Educational Content Assistant API running'})

@app.route('/')
def index():
    """Serve the main index page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """Upload a PDF module"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        module_name = request.form.get('module_name', 'Untitled Module')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files allowed'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        content_text = extract_text_from_pdf(filepath)
        
        # Store in database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO pdfs (filename, filepath, content_text, module_name)
            VALUES (?, ?, ?, ?)
        ''', (filename, filepath, content_text, module_name))
        pdf_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'pdf_id': pdf_id,
            'filename': filename,
            'module_name': module_name,
            'message': 'PDF uploaded successfully'
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Get all uploaded modules"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, filename, module_name, upload_date FROM pdfs ORDER BY upload_date DESC')
        modules = c.fetchall()
        conn.close()
        
        return jsonify({
            'modules': [
                {
                    'id': m[0],
                    'filename': m[1],
                    'module_name': m[2],
                    'upload_date': m[3]
                }
                for m in modules
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modules/<int:pdf_id>', methods=['GET'])
def get_module(pdf_id):
    """Get specific module content"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, filename, module_name, content_text FROM pdfs WHERE id = ?', (pdf_id,))
        module = c.fetchone()
        conn.close()
        
        if not module:
            return jsonify({'error': 'Module not found'}), 404
        
        return jsonify({
            'id': module[0],
            'filename': module[1],
            'module_name': module[2],
            'content': module[3]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_doubt():
    """Submit a doubt/question about a module"""
    try:
        data = request.get_json()
        pdf_id = data.get('pdf_id')
        question = data.get('question')
        
        if not pdf_id or not question:
            return jsonify({'error': 'Missing pdf_id or question'}), 400
        
        # Get PDF content from database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT content_text FROM pdfs WHERE id = ?', (pdf_id,))
        result = c.fetchone()
        
        if not result:
            return jsonify({'error': 'Module not found'}), 404
        
        content_text = result[0]
        
        # Get answer from LLM
        answer = answer_question(question, content_text)
        
        # Store conversation
        c.execute('''
            INSERT INTO conversations (pdf_id, question, answer)
            VALUES (?, ?, ?)
        ''', (pdf_id, question, answer))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations/<int:pdf_id>', methods=['GET'])
def get_conversations(pdf_id):
    """Get conversation history for a module"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            SELECT question, answer, timestamp
            FROM conversations
            WHERE pdf_id = ?
            ORDER BY timestamp DESC
        ''', (pdf_id,))
        conversations = c.fetchall()
        conn.close()
        
        return jsonify({
            'conversations': [
                {
                    'question': conv[0],
                    'answer': conv[1],
                    'timestamp': conv[2]
                }
                for conv in conversations
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modules/<int:pdf_id>', methods=['DELETE'])
def delete_module(pdf_id):
    """Delete a module"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT filepath FROM pdfs WHERE id = ?', (pdf_id,))
        result = c.fetchone()
        
        if not result:
            return jsonify({'error': 'Module not found'}), 404
        
        filepath = result[0]
        
        # Delete from database
        c.execute('DELETE FROM pdfs WHERE id = ?', (pdf_id,))
        c.execute('DELETE FROM conversations WHERE pdf_id = ?', (pdf_id,))
        conn.commit()
        conn.close()
        
        # Delete file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({'success': True, 'message': 'Module deleted'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
