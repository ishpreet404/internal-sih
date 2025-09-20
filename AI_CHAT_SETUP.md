# AI Chat Configuration Guide

## 🤖 Setting up AI-Powered Chat

The Railway Document Intelligence System uses AI to provide intelligent responses about your processed documents. Here's how to set it up:

### 1. Get GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token (classic) with these permissions:
   - `read:packages` (for accessing GitHub Models)
3. Copy the generated token

### 2. Configure Environment
Create a `.env` file in the backend directory with:

```env
GITHUB_TOKEN=your_github_token_here
GITHUB_MODELS_ENDPOINT=https://models.github.ai
GITHUB_MODEL_NAME=gpt-4o
MAX_CHUNK_TOKENS=5000
```

### 3. Available AI Features

Once configured, the AI can:

#### 📋 **Document Analysis**
- Identify document types and structure
- Extract key information and metadata
- Analyze railway-specific content

#### 🔍 **Information Extraction**
- Find specific dates, schedules, and deadlines
- Extract technical specifications
- Identify compliance requirements

#### 🛡️ **Safety & Compliance**
- Analyze safety protocols and procedures
- Identify regulatory requirements
- Explain compliance guidelines

#### 📚 **Knowledge Assistant**
- Explain railway terminology
- Provide context about standards
- Answer questions about document content

### 4. Example Questions to Try

```
"What are the main safety requirements in this document?"
"Extract all mentioned dates and their significance"
"What railway standards are referenced?"
"Explain the compliance requirements"
"Summarize the technical specifications"
```

### 5. Fallback Mode

If the AI service isn't configured, the system will:
- Use basic rule-based responses
- Provide document summaries from processing
- Show classification results
- Give helpful error messages

### 6. Troubleshooting

**No AI responses?**
- Check if `.env` file exists with correct token
- Verify GitHub token has required permissions
- Check backend logs for API errors

**Generic responses only?**
- Token might be invalid or expired
- GitHub Models service might be unavailable
- Check network connectivity

**Need help?**
The chat system will automatically fall back to basic responses if AI isn't available, so the application remains functional even without the AI service configured.