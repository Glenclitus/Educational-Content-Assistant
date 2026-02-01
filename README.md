# Educational Content Assistant

An interactive web platform for students and educators to upload educational PDFs, study content, ask AI-powered questions, and get personalized learning assistance.

**What It Does:**
- 📚 Upload study modules (PDFs)
- 💬 Ask questions about content and get AI-generated answers
- 📊 Track conversation history
- 🎯 Create adaptive learning experiences
- 🔍 Search and reference module content

**Why Use It?**
- **For Students:** Study smarter by asking questions about module content and getting instant answers
- **For Teachers:** Offload repetitive Q&A and focus on deeper engagement
- **For Educators:** Build interactive learning experiences without coding

---

## Quick Demo

**1. Start Backend (Python Flask API):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**2. Start Frontend (React + Vite):**
```powershell
cd frontend
npm install
npm run dev
```

**3. Open http://localhost:3000 and:**
- Upload a PDF module
- Ask a question about the content
- Get AI-powered answers instantly

---

## Features

### ✅ Core Features
1. **PDF Upload & Management** — Upload, organize, and manage multiple study modules
2. **Real-Time Q&A** — Ask questions about module content and get instant answers
3. **Conversation History** — All Q&A saved and searchable per module
4. **Database Backend** — SQLite for reliable data persistence
5. **API-First Design** — Extensible REST API for integration

### 🎯 5 Creative Features (Planned)
1. **Adaptive Learning Path Generator** — Auto-structure topics with spaced repetition
2. **Real-Time Interactive Quiz Engine** — Dynamic quizzes with adaptive difficulty
3. **Multi-Modal Content Generation** — Convert PDFs to lessons, infographics, video scripts
4. **Peer Collaboration & Review** — Real-time collaborative editing and peer feedback
5. **Intelligent Progress Dashboard** — Analytics, mastery tracking, predictive insights

---

## Project Structure

```
├── app.py                          # Flask backend server
├── pdf_processor.py                # PDF extraction & processing
├── llm_handler.py                  # OpenAI/Claude API integration
├── requirements.txt                # Python dependencies
│
├── frontend/                       # React web application
│   ├── src/
│   │   ├── App.jsx                # Main UI component
│   │   └── App.css                # Styling
│   ├── package.json               # npm dependencies
│   └── vite.config.js             # Vite bundler config
│
├── docs/                          # Project documentation
│   ├── index.md                   # Docs overview
│   ├── getting_started.md         # Setup guide
│   └── architecture.md            # System design
│
├── CREATIVE_FEATURE.md            # Feature specifications
├── SETUP.md                       # Detailed setup instructions
└── README.md                      # This file
```

---

## Technology Stack

**Backend:**
- Python 3.8+
- Flask 2.3 (REST API)
- SQLite (Database)
- PyPDF2 (PDF processing)
- OpenAI API (AI Q&A)

**Frontend:**
- React 18
- Vite (Build tool)
- CSS3 (Styling)

**Infrastructure:**
- Local development or Docker/Cloud deployment ready

---

## Installation & Setup

See **[SETUP.md](./SETUP.md)** for detailed instructions.

**Quick start (Windows PowerShell):**

```powershell
# 1. Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY = "your-key-here"
python app.py

# 2. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

**Then:** Open http://localhost:3000

---

## API Documentation

### Upload PDF
```bash
POST /api/upload
Content-Type: multipart/form-data
- file: <PDF file>
- module_name: "Module Name"
```

### Get All Modules
```bash
GET /api/modules
```

### Ask Question
```bash
POST /api/ask
Body: {
  "pdf_id": 1,
  "question": "What is X?"
}
```

### Get Conversations
```bash
GET /api/conversations/{pdf_id}
```

---

## How It Works

1. **Upload** — Teacher uploads a PDF module to the platform
2. **Extract** — System extracts and indexes text content
3. **Store** — PDF stored in database with metadata
4. **Ask** — Student asks a question about the module
5. **Process** — Question + module content sent to LLM
6. **Answer** — AI generates contextual answer
7. **Save** — Q&A saved to conversation history

---

## Environment Variables

```bash
OPENAI_API_KEY=your-openai-api-key         # Required for Q&A
FLASK_ENV=development                      # development or production
MAX_FILE_SIZE=52428800                     # Max 50MB
```

---

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push branch (`git push origin feature/your-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Roadmap

- [x] PDF upload & storage
- [x] Basic Q&A system
- [x] Conversation history
- [ ] User authentication
- [ ] Advanced PDF processing (OCR, scans)
- [ ] Spaced repetition scheduler
- [ ] Quiz generator
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Team collaboration features

---

## License

MIT License — See [LICENSE](./LICENSE) for details.

---

## Support & Contact

- **GitHub Issues**: Report bugs or suggest features
- **Documentation**: See `/docs` folder
- **LinkedIn**: Share your feedback @Glenclitus

**Version:** 0.1.0 (Alpha)  
**Last Updated:** February 2, 2026

---

**Ready to get started?** 
- 📖 [Setup Guide](./SETUP.md)
- 🎯 [Creative Features](./CREATIVE_FEATURE.md)
- 🏗️ [Architecture](./docs/architecture.md)
