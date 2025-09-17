from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import json
from werkzeug.utils import secure_filename
from ocr import extract_document_text
from llm_summarizer import create_document_summary
from kmrl_classifier import classify_railway_document
import load_env  # Load environment variables
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        ocr_language = request.form.get('ocrLanguage', 'mal+eng')
        classification_mode = request.form.get('classificationMode', 'railway')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        total_size = 0
        
        for file in files:
            if file and allowed_file(file.filename):
                # Check file size
                file.seek(0, 2)  # Seek to end
                file_size = file.tell()
                file.seek(0)  # Reset to beginning
                
                total_size += file_size
                if total_size > MAX_FILE_SIZE:
                    return jsonify({'error': 'Total file size exceeds limit'}), 400
                
                filename = secure_filename(file.filename)
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                uploaded_files.append({
                    'filename': filename,
                    'original_name': file.filename,
                    'path': filepath,
                    'size': file_size
                })
        
        if not uploaded_files:
            return jsonify({'error': 'No valid files uploaded'}), 400
        
        return jsonify({
            'message': f'{len(uploaded_files)} files uploaded successfully',
            'files': uploaded_files,
            'ocr_language': ocr_language,
            'classification_mode': classification_mode
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_documents():
    try:
        data = request.get_json()
        
        if not data or 'files' not in data:
            return jsonify({'error': 'No files provided for processing'}), 400
        
        files = data['files']
        ocr_language = data.get('ocr_language', 'mal+eng')
        classification_mode = data.get('classification_mode', 'railway')
        
        # Create temporary output directory
        output_dir = tempfile.mkdtemp()
        
        all_page_texts = {}
        combined_text = ""
        page_counter = 1
        
        # Process each file
        for file_info in files:
            filepath = file_info['path']
            
            if not os.path.exists(filepath):
                continue
            
            try:
                # Extract text from document
                page_texts, file_combined_text = extract_document_text(
                    file_path=filepath,
                    output_dir=output_dir,
                    tesseract_langs=ocr_language
                )
                
                # Renumber pages to be sequential across all files
                for original_page_num, page_info in page_texts.items():
                    page_info['global_page_num'] = page_counter
                    page_info['source_file'] = file_info['original_name']
                    all_page_texts[page_counter] = page_info
                    page_counter += 1
                
                combined_text += f"\n\n--- Document: {file_info['original_name']} ---\n\n"
                combined_text += file_combined_text
                
            except Exception as e:
                print(f"Error processing file {filepath}: {str(e)}")
                continue
        
        if not all_page_texts:
            return jsonify({'error': 'Failed to extract text from any documents'}), 500
        
        # Generate AI summary
        summary_data = create_document_summary(all_page_texts, combined_text, output_dir)
        
        # Perform railway classification
        classifications = []
        if classification_mode in ['railway', 'both']:
            classifications = classify_railway_document(
                combined_text, 
                summary_data.get('overall_summary', '')
            )
        
        # Prepare response
        result = {
            'document_type': summary_data.get('document_type', 'Unknown'),
            'ocr_text': combined_text,
            'summary': summary_data.get('overall_summary', ''),
            'classification': classifications,
            'metadata': {
                'total_pages': len(all_page_texts),
                'total_characters': len(combined_text),
                'languages_detected': list(set(
                    page_info.get('language', 'unknown') 
                    for page_info in all_page_texts.values()
                )),
                'processing_time': f"{len(files)} file(s) processed",
                'files_processed': len(files),
                'ocr_language': ocr_language,
                'classification_mode': classification_mode
            },
            'key_information': summary_data.get('key_information', {}),
            'error': summary_data.get('error')
        }
        
        # Clean up uploaded files
        for file_info in files:
            try:
                if os.path.exists(file_info['path']):
                    os.remove(file_info['path'])
            except:
                pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_documents():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        processed_data = data.get('processed_data', {})
        
        # Simple rule-based responses for demo
        # In production, this would integrate with the LLM
        message_lower = message.lower()
        
        if 'type' in message_lower or 'document' in message_lower:
            response = f"Based on my analysis, this appears to be a **{processed_data.get('document_type', 'Railway Document')}**. The document contains railway-specific terminology and follows standard railway documentation formatting."
        
        elif 'date' in message_lower or 'schedule' in message_lower:
            response = "I've identified several key dates and schedules in the document:\n\n• Implementation timeline: Q2 2025\n• Review cycles: Monthly\n• Compliance deadlines: Various throughout the document\n\nWould you like me to extract specific date ranges or schedules?"
        
        elif 'safety' in message_lower or 'compliance' in message_lower:
            response = "The document contains several safety and compliance sections:\n\n• **Safety Protocols**: Standard operating procedures for railway operations\n• **Compliance Requirements**: Regulatory adherence guidelines\n• **Risk Assessment**: Hazard identification and mitigation strategies\n\nThese sections emphasize the importance of following established safety protocols and maintaining compliance with railway regulations."
        
        elif 'summarize' in message_lower or 'summary' in message_lower:
            response = processed_data.get('summary', 'This railway document outlines important operational guidelines, safety protocols, and compliance requirements. Key areas covered include operational procedures, safety guidelines, regulatory compliance, and technical specifications.')
        
        else:
            response = "I've analyzed your question about the railway documents. Based on the processed content, I can provide insights about operational procedures, safety protocols, compliance requirements, and technical specifications. Could you be more specific about what aspect you'd like me to focus on?"
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<data_type>', methods=['POST'])
def download_data(data_type):
    try:
        data = request.get_json()
        
        if data_type == 'ocr':
            content = data.get('ocr_text', '')
            filename = 'ocr_results.txt'
        elif data_type == 'summary':
            content = data.get('summary', '')
            filename = 'ai_summary.txt'
        else:
            return jsonify({'error': 'Invalid data type'}), 400
        
        return jsonify({
            'content': content,
            'filename': filename,
            'content_type': 'text/plain'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)