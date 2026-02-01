# Architecture

This starter project uses a simple modular layout:

- `src/` — application code (CLI, service wrappers)
- `docs/` — documentation
- `tests/` — (optional) unit/integration tests

Components
- CLI: simple entrypoint to generate templates
- LLM Adapter: an interface module to plug different LLM providers
- Content Pipeline: templates -> structure -> quizzes -> export (PDF/HTML)

Scaling ideas
- Add a web UI (React + FastAPI)
- Persist content and user progress with a database (SQLite/Postgres)
- Add user accounts and personalization
