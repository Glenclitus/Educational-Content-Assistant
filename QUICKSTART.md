# 🚀 Educational Content Assistant - Complete User Guide

## ✅ What You Have

A **fully working web application** for interactive learning with AI-powered Q&A.

---

## 🎯 How to Use

### Step 1: Start the Backend
Open PowerShell in your project folder and run:

```powershell
cd "c:\Users\glenc\Documents\Educational content Assistant"
.\.venv\Scripts\Activate.ps1
python app.py
```

**You should see:**
```
* Running on http://127.0.0.1:5000
```

### Step 2: Open the Website
Open your browser and go to:
```
http://localhost:5000
```

### Step 3: Upload a PDF
1. Click the **"+ Upload PDF"** button
2. Select any PDF file with study material
3. The system will automatically extract text from the PDF

### Step 4: Ask Questions
1. Click on your uploaded module in the sidebar
2. Type a question about the content (e.g., "What are the main concepts?")
3. Click **"💡 Ask Question"**
4. Get an AI-powered answer based on your PDF content

### Step 5: Study & Learn
- All questions and answers are saved
- Scroll through conversation history
- Ask as many questions as you want
- Delete modules with the ✕ button

---

## 🎨 Features

✅ **PDF Upload** - Upload any study material  
✅ **Automatic Text Extraction** - Content automatically parsed from PDFs  
✅ **AI Q&A** - Ask questions and get intelligent answers  
✅ **Conversation History** - All Q&A saved and searchable  
✅ **Multiple Modules** - Manage multiple study materials  
✅ **Beautiful UI** - Modern gradient design with smooth interactions  
✅ **Auto-refresh** - Modules list updates automatically  
✅ **Mobile Friendly** - Works on tablets and phones  

---

## 📱 Website Interface

### Sidebar (Left)
- **Upload Module** - Button to upload PDF files
- **Your Modules** - List of uploaded study materials
- Click any module to select it

### Main Area (Right)
- **Module Info** - Name and upload date
- **Study & Ask Doubts** - Conversation history with all Q&A
- **Ask a Question** - Text box to enter your doubts

---

## 🔧 Troubleshooting

### Issue: "Cannot connect to backend"
**Solution:** Make sure Flask is running:
```powershell
python app.py
```

### Issue: "Upload fails"
**Solution:** 
- Check file is a valid PDF
- Maximum file size: 50MB
- Try a different PDF

### Issue: "No answer to my question"
**Solution:**
- Rephrase your question
- Make sure the answer exists in your PDF
- Try asking simpler questions first

### Issue: Module not appearing
**Solution:**
- Wait 5 seconds (auto-refresh interval)
- Manually refresh the page (F5)
- Check browser console for errors (F12)

---

## 📊 API Endpoints (Advanced)

If you want to integrate this with other apps:

```bash
# Get health status
GET /api/health

# Upload a PDF
POST /api/upload
Body: FormData with 'file' and 'module_name'

# List all modules
GET /api/modules

# Get specific module
GET /api/modules/{id}

# Ask a question
POST /api/ask
Body: {"pdf_id": 1, "question": "Your question"}

# Get conversation history
GET /api/conversations/{id}

# Delete a module
DELETE /api/modules/{id}
```

---

## 📁 Project Files

```
.
├── app.py                    # Flask backend server
├── static/index.html         # Website UI
├── pdf_processor.py          # PDF text extraction
├── llm_handler.py           # AI Q&A engine
├── requirements.txt         # Python dependencies
├── test_system.py           # System test script
├── run_backend.bat          # Quick start script
├── assistant.db             # SQLite database
├── uploads/                 # Uploaded PDF folder
└── README.md                # This file
```

---

## 🚀 Quick Start Commands

**Start everything:**
```powershell
# Terminal 1 - Start Backend
cd "c:\Users\glenc\Documents\Educational content Assistant"
.\.venv\Scripts\Activate.ps1
python app.py

# Terminal 2 (optional) - Test System
.\.venv\Scripts\python.exe test_system.py
```

**Then open:** http://localhost:5000

---

## 💡 Pro Tips

1. **Better Questions** - Ask specific questions related to the PDF content
2. **Bookmark** - Save http://localhost:5000 in your bookmarks
3. **Multiple PDFs** - Upload different subjects/modules separately
4. **Save Answers** - Screenshot important answers for your notes
5. **Share PDFs** - Both students can use the same modules

---

## 🔐 Storage

- All PDFs stored in `uploads/` folder
- All conversations stored in `assistant.db` (SQLite)
- Nothing is uploaded to cloud - everything is local

---

## 📈 Next Steps

1. **For Production**: Use a proper web server (Gunicorn, uWSGI)
2. **Add Authentication**: Implement user login/signup
3. **Multi-format Support**: Add Word, PowerPoint, ePub support
4. **Mobile App**: Create mobile versions for Android/iOS
5. **Advanced Analytics**: Track learning progress and patterns

---

## ❓ FAQ

**Q: Can I use this offline?**  
A: Yes! Everything runs locally on your machine.

**Q: Is there a file size limit?**  
A: 50MB max per PDF. You can upload multiple files.

**Q: Where is my data stored?**  
A: Locally in the `uploads/` folder and `assistant.db` file.

**Q: Can multiple people use it?**  
A: Yes, from different computers on the same network using your computer's IP.

**Q: Will my questions be saved forever?**  
A: Yes, until you delete the module or clear the database.

---

## 🎓 Educational Use Cases

- **Students** - Study help and doubt clearing
- **Teachers** - Student support tool
- **Online Learning** - Supplement course materials
- **Self-Study** - Interactive learning companion
- **Research** - Quick document analysis

---

## 📞 Support

For issues:
1. Check the **Troubleshooting** section above
2. Open browser console: Press F12
3. Check backend logs in terminal
4. Review error messages carefully

---

**Happy Learning! 🎉**

Version: 1.0  
Last Updated: February 2, 2026
