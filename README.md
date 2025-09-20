# Railway Document Intelligence System

A comprehensive document processing system for railway operations with OCR, AI analysis, and document classification capabilities. Built for Smart India Hackathon 2025.

## Features

- 🚂 **Railway-Specific Document Classification** - Automatically categorizes documents based on railway operations
- 🔍 **Advanced OCR** - Extracts text from PDFs and images with support for Malayalam + English
- 🤖 **AI-Powered Analysis** - Generates intelligent summaries using GitHub Models
- 3. **AI service not responding**: Check GitHub token configuration and network connectivity
4. **Chat responses are generic**: Verify that the GitHub token is valid and has appropriate permissions

### AI Chat Features

The AI chat functionality provides:

- **Context-Aware Responses**: The AI understands your document content and provides relevant answers
- **Information Extraction**: Ask for specific dates, numbers, references, or technical details
- **Railway Expertise**: Specialized knowledge about railway terminology, standards, and regulations
- **Safety & Compliance**: Analysis of safety protocols and compliance requirements
- **Document Analysis**: Insights about document structure, content, and key information

**Example Questions:**
- "What are the main safety requirements mentioned?"
- "Extract all important dates and deadlines"
- "What railway standards are referenced in this document?"
- "Explain the compliance requirements"
- "Summarize the technical specifications"

**Note**: AI chat requires a GitHub token to be configured. See the [AI Chat Setup Guide](./AI_CHAT_SETUP.md) for detailed instructions.
- 🎯 **KMRL Integration** - Specialized support for Kochi Metro Rail Limited documents
- 🌐 **Modern React Frontend** - Responsive and intuitive user interface

## Tech Stack

### Backend
- **Python 3.9+** with Flask
- **OCR**: Tesseract, PyMuPDF, OpenCV
- **AI**: OpenAI API via GitHub Models
- **Classification**: Custom railway document classifier

### Frontend
- **React 18** with Vite
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Lucide React** for icons

## Installation & Setup

### Prerequisites

1. **Python 3.9+** installed
2. **Node.js 16+** and npm installed
3. **Tesseract OCR** installed:
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr tesseract-ocr-mal`
   - macOS: `brew install tesseract tesseract-lang`

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   GITHUB_TOKEN=your_github_token_here
   GITHUB_MODELS_ENDPOINT=https://models.github.ai/inference
   GITHUB_MODELS_MODEL=openai/gpt-4o
   MAX_CHUNK_TOKENS=5000
   CHUNK_DELAY_SECONDS=3
   RATE_LIMIT_RETRY_DELAY=30
   ```

3. **Get GitHub Token**:
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Generate a new token with appropriate permissions
   - Add it to your `.env` file

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

2. **Create environment file** (optional):
   Create a `.env.local` file in the root directory:
   ```env
   VITE_API_URL=http://localhost:5000/api
   ```

## Running the Application

### Start Backend Server

```bash
python app.py
```
The Flask server will start on `http://localhost:5000`

### Start Frontend Development Server

```bash
npm run dev
```
The React app will start on `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Usage

### Document Upload & Processing

1. **Upload Files**: Drag and drop or browse for PDF/image files
2. **Configure Options**:
   - OCR Language: Choose language detection mode
   - Classification Mode: Select railway-specific or general classification
3. **Process**: Click "Process Documents" to start analysis

### AI Chat Interface

1. Navigate to the "AI Chat" tab after processing documents
2. Ask questions about the processed content
3. Use quick question buttons for common queries
4. Get intelligent responses about railway operations, safety, schedules, etc.

### Results Analysis

1. **Document Overview**: View metadata and processing statistics
2. **Railway Classification**: See categorized document types with confidence scores
3. **OCR Results**: Review extracted text with download options
4. **AI Summary**: Get comprehensive document summaries
5. **Key Information**: Extract important details automatically

## Document Categories

The system classifies documents into various railway-specific categories:

- **Safety Manual** - Safety procedures, hazard identification, emergency protocols
- **Technical Documentation** - Specifications, maintenance procedures, engineering docs
- **Operational Procedures** - Standard operating procedures, work instructions
- **Schedule Timetable** - Service schedules, departure/arrival times, routes
- **Compliance Regulatory** - Regulatory requirements, audits, standards
- **Training Manual** - Educational content, certification materials
- **Infrastructure** - Track, signaling, station, platform documentation
- **Rolling Stock** - Locomotive, coach, wagon specifications
- **Passenger Services** - Customer service, ticketing, amenities
- **Freight Operations** - Cargo handling, loading procedures
- **Signaling Communication** - Control systems, communication protocols
- **Electrical Systems** - Power supply, traction systems

## KMRL-Specific Features

The system includes specialized support for Kochi Metro Rail Limited:

- Recognition of KMRL-specific terminology and locations
- Kochi Metro station names and route information
- Kerala-specific railway operations
- Malayalam language support for local documents

## API Endpoints

### Backend API

- `GET /api/health` - Health check
- `POST /api/upload` - Upload files for processing
- `POST /api/process` - Process uploaded documents
- `POST /api/chat` - Chat with AI about documents
- `POST /api/download/<type>` - Download processed data

### Example API Usage

```javascript
// Upload files
const formData = new FormData()
formData.append('files', file)
formData.append('ocrLanguage', 'mal+eng')
formData.append('classificationMode', 'railway')

const response = await fetch('/api/upload', {
  method: 'POST',
  body: formData
})
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token for AI models | Required |
| `GITHUB_MODELS_ENDPOINT` | GitHub Models API endpoint | `https://models.github.ai/inference` |
| `GITHUB_MODELS_MODEL` | AI model to use | `openai/gpt-4o` |
| `MAX_CHUNK_TOKENS` | Max tokens per chunk for large documents | `5000` |
| `CHUNK_DELAY_SECONDS` | Delay between API calls | `3` |
| `RATE_LIMIT_RETRY_DELAY` | Retry delay for rate limits | `30` |

### Supported File Types

- **PDF**: `.pdf`
- **Images**: `.png`, `.jpg`, `.jpeg`

### File Size Limits

- Maximum individual file size: 16MB
- Multiple files supported per upload

## Troubleshooting

### Common Issues

1. **Tesseract not found**: Ensure Tesseract is installed and in PATH
2. **GitHub API errors**: Check your GITHUB_TOKEN and API limits
3. **OCR quality issues**: Try preprocessing images or adjusting OCR language settings
4. **Large file processing**: Files are automatically chunked for processing

### Performance Tips

1. **Optimize images** before upload for better OCR results
2. **Use appropriate OCR language** settings for your documents
3. **Process smaller batches** for faster response times
4. **Check network connectivity** for AI API calls

## Development

### Project Structure

```
backend/
├── src/                     # React frontend source
│   ├── components/         # React components
│   ├── services/          # API services
│   └── App.jsx           # Main app component
├── app.py                # Flask backend server
├── ocr.py               # OCR processing module
├── llm_summarizer.py    # AI summarization
├── kmrl_classifier.py   # Railway classification
├── requirements.txt     # Python dependencies
├── package.json        # Node.js dependencies
└── vite.config.js     # Vite configuration
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for Smart India Hackathon 2025.

## Support

For technical support or questions about the Railway Document Intelligence System, please refer to the documentation or contact the development team.