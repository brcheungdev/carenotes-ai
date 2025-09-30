# CareNotes AI
[中文](README.md)
**Version: v0.1.0 (MVP)**  
**CareNotes AI — An AI-powered assistant for nurses that turns spoken or handwritten notes into structured, auditable care records. Features timeline view and PDF export.**  
**CareNotes AI —— AI 助力的护理助手，能将口述或手写笔记快速转化为结构化护理记录，支持时间线视图和 PDF 导出功能。**

---

## Project Background & Vision

CareNotes AI was born from my reflections on the reality of nursing work — reducing the burden on nurses is both essential and urgent. The initial goal of this project was to help clinical nurses quickly convert scattered voice notes and handwritten memos into structured nursing records.

This project is guided by the following core principles:

- **Clinical First**: Leverage digital tools to reduce documentation load and give precious time back to the nurses.
- **Auditable Data**: Keep original notes throughout the process to support quality audits and shift handovers.
- **Structured + Narrative**: Provide standardized fields while preserving essential context and narrative.
- **Modular Evolution**: Decoupled core modules allow future expansion (e.g., real-time alerts, multilingual support, mobile clients, etc.).

---

## Feature Highlights

- 🔐 **Login & Roles**: Demo account login with JWT-based role distinction (nurse/admin).
- 👥 **Patient Management**: Create and query patient profiles as the entry point for care documentation.
- 📝 **Nursing Records**: Input via text or speech (transcribed using Whisper), processed with LLMs to generate structured SOAP notes, vitals, I/O, and more.
- 📄 **PDF Export**: Generate printable, archivable PDFs based on templates.
- 🕒 **Timeline View**: Reconstruct nursing activity timelines with filtering and alerts.
- 🔌 **Open API**: RESTful interface returns unified JSON for easy hospital system integration.

---

## Tech Stack

| Layer       | Technologies Used |
|------------|--------------------|
| Backend     | Python 3.10, Flask, Flask-CORS, SQLAlchemy, PyJWT, WeasyPrint, OpenAI API (Whisper + Chat models) |
| Database    | MySQL 8.0 |
| Frontend    | Vanilla HTML/CSS/JavaScript (modular scripts: api/auth/recorder/ui) |
| Tools       | PowerShell startup scripts, custom Python static server, virtual environment `.venv` |

---

## Project Structure

```
backend/
  app.py              # Flask app entry point
  config.py           # Environment variable loader
  db.py               # SQLAlchemy initializer
  models/             # ORM models
  routes/             # API routes: auth, patients, records, export
  services/           # Wrappers for STT, LLM, PDF services
  templates/pdf/      # PDF export templates
  migrations/schema.sql
frontend/
  index.html          # Login page
  patient.html        # Patient management UI
  record.html         # Nursing record editor
  timeline.html       # Timeline view
  assets/css/style.css
  assets/js/
README.md
StartCareNotes.bat    # One-click startup script (not implemented yet)
```

---

## Environment & Prerequisites

- Windows 10/11 + PowerShell (or compatible terminal)
- Python 3.10+
- pip / venv (bundled with Python)
- MySQL 8.0
- Modern browser (Edge / Chrome)
- Optional: OpenAI API Key (for transcription and structured parsing)

> If you're compiling WeasyPrint dependencies, make sure Microsoft Visual C++ Build Tools are installed.

---

## Installation & Setup

1. **Clone the repo and enter the directory**
   ```powershell
   git clone <your-repo>
   cd carenotes-ai
   ```

2. **Create virtual environment and install dependencies**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r backend\requirements.txt
   ```

3. **Initialize the database**
   ```powershell
   mysql -u <user> -p -e "CREATE DATABASE IF NOT EXISTS carenotes CHARACTER SET utf8mb4;"
   mysql -u <user> -p carenotes < backend\migrations\schema.sql
   ```

4. **Configure environment variables**
   ```powershell
   copy backend\.env.example backend\.env
   notepad backend\.env
   ```

   Fill in the following keys:
   - `OPENAI_API_KEY`
   - `OPENAI_TRANSCRIBE_MODEL` (e.g., whisper-1)
   - `OPENAI_PARSE_MODEL` (e.g., gpt-4o-mini)
   - `MYSQL_URL` (e.g., mysql+pymysql://user:pass@127.0.0.1:3306/carenotes)
   - `JWT_SECRET`

> The `.env` file in the repo uses placeholder values (like `yourapikey`, `mysql_username`, `mysql_password`). You’ll need to replace them with real values to enable database and OpenAI integration.

> If you run into a `'latin-1' codec can't encode characters` error while editing config files, it likely contains Chinese placeholders or other Unicode symbols. Just make sure your editor is using UTF-8 encoding to avoid this.

---

## Starting the Project

### Option 1: Manual Startup

1. **Start the backend**
   ```powershell
   cd backend
   ..\.venv\Scripts\activate
   flask --app app run --debug
   ```
   Default URL: `http://127.0.0.1:5000` (API base path: `/api`)

2. **Start the frontend static server**
   ```powershell
   cd ..\frontend
   ..\.venv\Scripts\python serve.py
   ```
   Default URL: `http://127.0.0.1:8001/index.html`

### Option 2: One-click startup (Coming Soon)

Just run this from the project root:
```powershell
StartCareNotes.bat
```
The script (once implemented) will launch both backend and frontend services and open the browser automatically.

---

## Demo Accounts

To help you explore the open-source version, here are two ready-to-use demo accounts:

- `admin / Passw0rd!`
- `nurse / Passw0rd!`

Once logged in, you can try out patient management, record editing, PDF exports, and timeline features.

---

## Version Roadmap

- Current version: v0.1.0 (MVP)
- Upcoming improvements may include:
  - Finer-grained permissions and audit logs
  - Smarter speech features (real-time noise suppression, speaker separation)
  - Integration with HIS/EMR systems
  - Richer visualizations and mobile-friendly UI
  - Automated testing and CI/CD pipelines

---

## Disclaimer

This project is intended for learning, research, and prototyping purposes only. It is **not suitable for production use or real clinical environments**. All sample data, accounts, and configs are for demo only.

We welcome feedback and will continue improving the project’s features and security.  
Interested in collaboration? Feel free to reach out via the contact info on our homepage.
