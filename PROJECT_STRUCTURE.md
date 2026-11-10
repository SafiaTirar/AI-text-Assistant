# AI Text Assistant — Structure et fonctionnement

This document explains the repository structure, the runtime flow (UI → API → LLM → response), and how to run the project locally.

## Repository structure

High-level tree (important files only):

```text
ai-text-assistant/
├─ .env.example                     # exemple de configuration
├─ .gitignore                       # exclusions Git
├─ README.md                         # installation et utilisation
├─ PROJECT_STRUCTURE.md              # this document
├─ backend/
│  ├─ app.py                         # Flask entrypoint (routes + API)
│  ├─ llm_client.py                  # Groq client wrapper (calls the LLM)
│  ├─ processors.py                  # Prompt builder (operation/language/options)
│  ├─ pdf_generator.py               # PDF generation (ReportLab)
│  ├─ requirements.txt               # Python dependencies
│  ├─ templates/
│  │  └─ index.html                  # Main UI served by Flask
└─ frontend/
   └─ index.html                     # interface statique alternative
```

## What runs where

- **Backend (`backend/`)**: Python + Flask web server.
  - Serves the HTML UI at `/`.
  - Exposes HTTP endpoints used by the UI:
    - `POST /api/process` → builds a prompt + calls the Groq LLM → returns JSON
    - `POST /api/download-pdf` → generates a PDF from content → returns a downloadable file
- **Frontend (`frontend/`)**: A static HTML page that looks similar to the Flask template.
  - If you open `frontend/index.html` directly in the browser, it will try to call `fetch('/api/process')`.
  - That works only if the frontend is served from the **same origin** as the Flask backend (or you add CORS + configure the URL).

In practice, the simplest path is to run the Flask app and use the UI served from `backend/templates/index.html` at `http://localhost:5001/`.

## End-to-end flow (how it works)

### 1) UI collects user input

The UI (HTML + embedded JS) lets the user:

- Paste input text
- Choose an **operation** (short/medium/long summary, correction, reformulation, bullets)
- Choose a **language** (`auto`, `fr`, `en`, `ar`)
- Toggle **options**:
  - preserve formatting (paragraphs)
  - strict spelling/correction mode

### 2) UI calls the backend API

The UI sends a JSON payload to the Flask backend:

- **Endpoint**: `POST /api/process`
- **Payload**:
  - `text`: string
  - `operation`: one of `resume_court`, `resume_moyen`, `resume_long`, `correction`, `reformulation_simple`, `reformulation_professionnelle`, `bullets`
  - `language`: `auto | fr | en | ar`
  - `options`: `{ preserveFormatting: boolean, strictSpelling: boolean }`

### 3) Backend builds the LLM prompt

`backend/processors.py` contains `build_prompt(text, operation, language, options)`:

- Maps `operation` → instruction (e.g., “Fais un résumé très court (3–4 lignes).”)
- Maps `language` → wording (français/anglais/arabe/auto)
- Adds “extra” instructions if:
  - `strictSpelling` is enabled
  - `preserveFormatting` is enabled

This produces a final prompt string sent to the LLM.

### 4) Backend calls the Groq LLM

`backend/llm_client.py` wraps Groq:

- Reads the API key from the environment variable **`GROQ_API_KEY`**
- Uses model: `llama-3.3-70b-versatile`
- Returns the generated text (or an error string if the call fails)

### 5) Backend returns JSON to the UI

`backend/app.py` returns:

- `result`: the generated text from the LLM
- `detected_language`: a simple heuristic:
  - returns `"ar"` if the response contains some Arabic characters
  - otherwise `"fr"`

The UI displays `result`, and optionally switches the page direction to RTL for Arabic.

## PDF download flow

### Endpoint

- `POST /api/download-pdf`

### What it does

`backend/app.py`:

- Creates a temporary file (e.g., `.../tmpXXXXX.pdf`)
- Calls `backend/pdf_generator.py::generate_pdf(content, path)`
- Returns the file via Flask `send_file(..., as_attachment=True, download_name="resultat.pdf")`

`backend/pdf_generator.py` utilise ReportLab pour créer un PDF simple. Il gère les paragraphes, les listes à puces et une syntaxe minimale de texte en gras (`**texte**`).

## How to run locally

### 1) Create/activate a virtual environment (recommended)

Depuis la racine du dépôt :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 3) Set the Groq API key

```bash
export GROQ_API_KEY="YOUR_KEY_HERE"
```

### 4) Start the server

```bash
python backend/app.py
```

Then open:

- `http://localhost:5001/`

## Key files (quick reference)

- **`backend/app.py`**: Flask routes (`/`, `/api/process`, `/api/download-pdf`)
- **`backend/processors.py`**: prompt construction for each operation/language/options combo
- **`backend/llm_client.py`**: Groq LLM invocation (reads `GROQ_API_KEY`)
- **`backend/pdf_generator.py`**: PDF creation via ReportLab
- **`backend/templates/index.html`**: main UI (calls the backend using `fetch('/api/process')`)

## Notes / gotchas

- Les dossiers d'environnements virtuels (`.venv/`, `venv/`) et les secrets `.env` sont exclus par `.gitignore`.
- **Language detection** in `backend/app.py` is heuristic and only checks the LLM output; if you need robust detection, consider adding a real language detector and/or detecting from the input text.
- If you want to use `frontend/index.html` independently, you’ll likely need to:
  - serve it from the same Flask app, or
  - configure it to call `http://localhost:5001/api/process`, and enable CORS in Flask.
