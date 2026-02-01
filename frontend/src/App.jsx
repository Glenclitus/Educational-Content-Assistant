import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [modules, setModules] = useState([]);
  const [selectedModule, setSelectedModule] = useState(null);
  const [question, setQuestion] = useState('');
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const API_BASE = 'http://localhost:5000/api';

  // Fetch modules on mount
  useEffect(() => {
    fetchModules();
  }, []);

  // Fetch conversations when module selected
  useEffect(() => {
    if (selectedModule) {
      fetchConversations(selectedModule.id);
    }
  }, [selectedModule]);

  const fetchModules = async () => {
    try {
      const res = await fetch(`${API_BASE}/modules`);
      const data = await res.json();
      setModules(data.modules || []);
    } catch (error) {
      console.error('Error fetching modules:', error);
    }
  };

  const fetchConversations = async (pdfId) => {
    try {
      const res = await fetch(`${API_BASE}/conversations/${pdfId}`);
      const data = await res.json();
      setConversations(data.conversations || []);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('module_name', file.name.replace('.pdf', ''));

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data.success) {
        alert('PDF uploaded successfully!');
        fetchModules();
        setUploadProgress(0);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading PDF');
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim() || !selectedModule) {
      alert('Please select a module and enter a question');
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pdf_id: selectedModule.id,
          question: question
        })
      });
      const data = await res.json();
      if (data.success) {
        setQuestion('');
        fetchConversations(selectedModule.id);
      }
    } catch (error) {
      console.error('Error asking question:', error);
      alert('Error submitting question');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteModule = async (id) => {
    if (window.confirm('Delete this module? This cannot be undone.')) {
      try {
        await fetch(`${API_BASE}/modules/${id}`, { method: 'DELETE' });
        fetchModules();
        if (selectedModule?.id === id) setSelectedModule(null);
      } catch (error) {
        console.error('Error deleting module:', error);
      }
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>📚 Educational Content Assistant</h1>
        <p>Upload PDFs, ask questions, and learn interactively</p>
      </header>

      <div className="container">
        {/* Left Sidebar - Modules */}
        <aside className="sidebar">
          <div className="upload-section">
            <h3>Upload Module</h3>
            <label htmlFor="pdf-upload" className="upload-btn">
              {loading ? 'Uploading...' : '+ Upload PDF'}
            </label>
            <input
              id="pdf-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              disabled={loading}
              style={{ display: 'none' }}
            />
            {uploadProgress > 0 && <p className="progress">{uploadProgress}%</p>}
          </div>

          <div className="modules-section">
            <h3>Your Modules ({modules.length})</h3>
            {modules.length === 0 ? (
              <p className="empty">No modules yet. Upload a PDF to start.</p>
            ) : (
              <ul className="modules-list">
                {modules.map((mod) => (
                  <li
                    key={mod.id}
                    className={`module-item ${selectedModule?.id === mod.id ? 'active' : ''}`}
                    onClick={() => setSelectedModule(mod)}
                  >
                    <span className="module-name">{mod.module_name}</span>
                    <button
                      className="delete-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteModule(mod.id);
                      }}
                    >
                      ✕
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {!selectedModule ? (
            <div className="welcome">
              <h2>Welcome! 👋</h2>
              <p>Select a module from the left or upload a new PDF to get started.</p>
            </div>
          ) : (
            <>
              <div className="module-header">
                <h2>{selectedModule.module_name}</h2>
                <p className="upload-date">Uploaded: {new Date(selectedModule.upload_date).toLocaleDateString()}</p>
              </div>

              {/* Conversation History */}
              <div className="conversation-section">
                <h3>Study & Doubts</h3>
                <div className="conversation-history">
                  {conversations.length === 0 ? (
                    <p className="empty">No questions yet. Ask something to get started!</p>
                  ) : (
                    conversations.map((conv, idx) => (
                      <div key={idx} className="conversation-item">
                        <div className="question">
                          <strong>Q:</strong> {conv.question}
                        </div>
                        <div className="answer">
                          <strong>A:</strong> {conv.answer}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Ask Question Section */}
              <div className="ask-section">
                <h3>Ask a Question</h3>
                <div className="input-group">
                  <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a doubt or question about this module..."
                    rows="3"
                    disabled={loading}
                  />
                  <button
                    onClick={handleAskQuestion}
                    disabled={loading || !question.trim()}
                    className="ask-btn"
                  >
                    {loading ? '⏳ Processing...' : '💡 Ask Question'}
                  </button>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
