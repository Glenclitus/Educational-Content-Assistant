# Getting Started

1. Clone the repository:

```powershell
git clone https://github.com/Glenclitus/Educational-Content-Assistant.git
cd Educational-Content-Assistant
```

2. Setup Python environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the starter CLI:

```powershell
python src\assistant.py --topic "Newton's Laws" --level "intermediate"
```

4. To integrate an LLM:
- Create an environment variable named `LLM_API_KEY` for your provider
- Update `src/assistant.py` to call the provider's API

