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

def generate_chat_response(message: str, processed_data: dict) -> str:
    """
    Generate AI chat response using the LLM service
    """
    try:
        from openai import OpenAI
        
        # Get GitHub token
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return "I need a GitHub token to be configured to provide intelligent responses. Please check the environment configuration."
        
        # Initialize OpenAI client with GitHub endpoint
        client = OpenAI(
            base_url=os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.github.ai"),
            api_key=token
        )
        
        # Prepare context from processed document data
        context = ""
        if processed_data:
            if processed_data.get('document_type'):
                context += f"Document Type: {processed_data['document_type']}\n\n"
            
            if processed_data.get('summary'):
                context += f"Document Summary: {processed_data['summary']}\n\n"
            
            if processed_data.get('classification'):
                classifications = processed_data['classification']
                if classifications:
                    context += "Railway Classifications:\n"
                    for cls in classifications:
                        context += f"- {cls.get('category', 'Unknown')}: {cls.get('confidence', 0):.2f} confidence\n"
                        if cls.get('keywords'):
                            context += f"  Keywords: {', '.join(cls['keywords'])}\n"
                    context += "\n"
            
            if processed_data.get('key_information'):
                key_info = processed_data['key_information']
                context += "Key Information:\n"
                for key, value in key_info.items():
                    context += f"- {key}: {value}\n"
                context += "\n"
            
            # Add a portion of the OCR text for context (limit to avoid token limits)
            ocr_text = processed_data.get('ocr_text', '')
            if ocr_text:
                # Limit OCR text to first 2000 characters for context
                ocr_preview = ocr_text[:2000]
                if len(ocr_text) > 2000:
                    ocr_preview += "...\n[Document continues]"
                context += f"Document Content (Preview):\n{ocr_preview}\n\n"
        
        # Create the system prompt
        system_prompt = """You are an AI assistant specialized in analyzing railway documents. You have access to processed document data including OCR text, summaries, and classifications. 

Your role is to:
1. Answer questions about the railway documents based on the provided context
2. Provide specific information extraction when asked
3. Explain railway terminology and concepts
4. Help with compliance and safety-related queries
5. Provide insights about document structure and content

Be accurate, helpful, and specific in your responses. If you don't have enough information to answer a question, say so clearly. Format your responses in a clear, readable manner with bullet points or sections when appropriate."""

        # Create the user prompt with context
        user_prompt = f"""Context from processed railway documents:
{context}

User Question: {message}

Please provide a helpful and accurate response based on the document context above."""

        # Make the API call
        response = client.chat.completions.create(
            model=os.getenv("GITHUB_MODEL_NAME", "gpt-4o"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating chat response: {str(e)}")
        # Fallback to rule-based responses if AI fails
        return generate_fallback_response(message, processed_data)

def generate_fallback_response(message: str, processed_data: dict) -> str:
    """
    Generate fallback responses when AI is unavailable
    """
    message_lower = message.lower()
    
    if 'type' in message_lower or 'document' in message_lower:
        doc_type = processed_data.get('document_type', 'Railway Document')
        return f"Based on my analysis, this appears to be a **{doc_type}**. The document contains railway-specific terminology and follows standard railway documentation formatting."
    
    elif 'date' in message_lower or 'schedule' in message_lower:
        return "I've analyzed the document for dates and schedules. To provide specific information, I would need access to the AI service. Please ensure your GitHub token is configured correctly."
    
    elif 'safety' in message_lower or 'compliance' in message_lower:
        return "The document contains safety and compliance information. For detailed analysis, please ensure the AI service is properly configured with your GitHub token."
    
    elif 'summarize' in message_lower or 'summary' in message_lower:
        summary = processed_data.get('summary', '')
        if summary:
            return summary
        return "This railway document contains operational guidelines, safety protocols, and compliance requirements. For a detailed summary, please ensure the AI service is configured."
    
    else:
        return "I can help analyze your railway documents. For detailed AI-powered responses, please ensure your GitHub token is configured in the environment. Otherwise, I can provide basic information about document types, summaries, and classifications."

@app.route('/api/chat', methods=['POST'])
def chat_with_documents():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        processed_data = data.get('processed_data', {})
        
        # Use the actual LLM service for chat
        response = generate_chat_response(message, processed_data)
        
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