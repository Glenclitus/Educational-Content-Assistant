# Educational Content Assistant - Web Application Setup

A full-stack web application for educators to upload PDF modules, study content, and ask AI-powered questions about the material.

## Features

✅ **PDF Upload & Storage** - Upload educational modules (PDFs) to the platform  
✅ **Interactive Study** - Browse and read PDF content through web interface  
✅ **AI-Powered Q&A** - Ask questions about module content and get AI-generated answers  
✅ **Conversation History** - Track all questions and answers for each module  
✅ **Module Management** - Organize and manage multiple study modules  

## Project Structure

```
.
├── app.py                          # Flask backend (main API server)
├── pdf_processor.py                # PDF extraction and processing
├── llm_handler.py                  # OpenAI integration for Q&A
├── requirements.txt                # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # React main component
│   │   ├── App.css                # Styling
│   │   ├── main.jsx               # React entry point
│   │   └── index.css              # Global styles
│   ├── index.html                 # HTML template
│   ├── package.json               # Frontend dependencies
│   └── vite.config.js             # Vite build config
├── uploads/                        # Uploaded PDFs (auto-created)
├── assistant.db                   # SQLite database (auto-created)
└── README.md                      # This file
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- OpenAI API Key (for Q&A feature)

### Step 1: Backend Setup

1. Create virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:
```powershell
pip install -r requirements.txt
```

3. Set up environment variables:
```powershell
# Create .env file in project root
$env:OPENAI_API_KEY = "your-openai-api-key-here"
```

### Step 2: Frontend Setup

1. Navigate to frontend folder:
```powershell
cd frontend
npm install
```

2. Start frontend dev server:
```powershell
npm run dev
```

Frontend runs on `http://localhost:3000`

### Step 3: Start Backend

In a new PowerShell terminal:
```powershell
python app.py
```

Backend runs on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health` - Check API status

### PDF Management
- **POST** `/api/upload` - Upload PDF module
- **GET** `/api/modules` - Get all uploaded modules
- **GET** `/api/modules/<id>` - Get specific module content
- **DELETE** `/api/modules/<id>` - Delete a module

### Q&A System
- **POST** `/api/ask` - Submit question about module
- **GET** `/api/conversations/<id>` - Get conversation history for module

## How to Use

1. **Open the App**: Navigate to `http://localhost:3000`

2. **Upload a Module**: 
   - Click "+ Upload PDF" button
   - Select a PDF file from your computer
   - Module is automatically processed and stored

3. **Select a Module**:
   - Click any module from the left sidebar
   - Module content is displayed and ready for study

4. **Ask Questions**:
   - Type your doubt/question in the "Ask a Question" section
   - Click "💡 Ask Question"
   - AI-generated answer appears in conversation history

5. **View Conversation History**:
   - All Q&A for each module is saved
   - Scroll through past questions and answers

## Database Schema

### `pdfs` table
```sql
- id (INTEGER PRIMARY KEY)
- filename (TEXT)
- filepath (TEXT)
- upload_date (TIMESTAMP)
- content_text (TEXT) - Extracted PDF text
- module_name (TEXT)
```

### `conversations` table
```sql
- id (INTEGER PRIMARY KEY)
- pdf_id (INTEGER, FK)
- question (TEXT)
- answer (TEXT)
- timestamp (TIMESTAMP)
```

## Configuration

### Environment Variables
```
OPENAI_API_KEY=your-api-key          # Required for Q&A
FLASK_ENV=development                # Set to production for deployment
MAX_FILE_SIZE=52428800               # Max PDF size (50MB)
```

### File Limits
- Max PDF size: 50MB
- Supported format: PDF only
- Max context length for Q&A: 3000 tokens

## Deployment Options

### Option 1: Local Development
- Run `python app.py` and `npm run dev` as described above

### Option 2: Docker (Recommended for production)
Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```powershell
docker build -t edu-assistant .
docker run -p 5000:5000 -e OPENAI_API_KEY=$env:OPENAI_API_KEY edu-assistant
```

### Option 3: Cloud Deployment (Heroku/Railway)
1. Push code to GitHub
2. Connect repository to deployment platform
3. Set environment variable `OPENAI_API_KEY`
4. Deploy

## Troubleshooting

**Issue**: "No module named 'flask'"
- Solution: Ensure virtual environment is activated: `.\.venv\Scripts\Activate.ps1`

**Issue**: "OPENAI_API_KEY not found"
- Solution: Set environment variable or create `.env` file in project root

**Issue**: Frontend shows "Connection refused" 
- Solution: Ensure backend is running on port 5000

**Issue**: PDF not extracting text properly
- Solution: Ensure PDF is text-based (not image/scanned). OCR not supported yet.

## Future Enhancements

- 🔐 User authentication and profiles
- 📊 Advanced analytics and progress tracking
- 🎯 Adaptive learning recommendations
- 📱 Mobile app (React Native)
- 🌍 Multi-language support
- 🔍 Full-text search across modules
- 📧 Email notifications for study reminders

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open Pull Request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation in `/docs` folder
- Review API response error messages
