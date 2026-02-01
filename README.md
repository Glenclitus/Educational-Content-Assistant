# Educational Content Assistant

An LLM-powered assistant to help educators and content creators quickly produce structured, engaging educational materials: lesson plans, quizzes, summaries, and learning paths.

**Goal**
- Provide a reusable starter project for building an Educational Content Assistant that can integrate with LLM APIs (OpenAI, Anthropic, etc.) and generate adaptive learning experiences.

**What's included**
- `README.md` — this file
- `docs/` — project documentation (getting started, architecture)
- `src/assistant.py` — small CLI starter to generate content templates
- `CREATIVE_FEATURE.md` — description of a unique feature (Adaptive Learning Path Generator)
- `LINKEDIN_POST.md` — draft for Build-in-Public announcement

**Quick Start (local)**
1. Create a Python virtual environment and activate it (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the CLI starter:

```powershell
python src\assistant.py --topic "Photosynthesis" --level "beginner"
```

**Docs**
See `/docs/index.md` for full documentation and hosting instructions.

**How to push to GitHub**
1. Initialize git and commit:

```powershell
git init
git add .
git commit -m "chore: initial project scaffold"
```

2. Add remote and push to `main` (replace if remote already exists):

```powershell
git remote add origin https://github.com/Glenclitus/Educational-Content-Assistant.git
git branch -M main
git push -u origin main
```

**License**
This project uses the MIT License. See `LICENSE`.

**Next steps**
- Integrate an LLM provider (set API key via env var)
- Add interactive web UI or VS Code extension
- Add automated tests and CI (GitHub Actions)
