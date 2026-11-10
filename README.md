# AI Text Assistant

Assistant web multilingue qui utilise un LLM pour résumer, corriger et reformuler des textes en français, anglais et arabe. L'application propose une interface Flask simple, s'appuie sur l'API Groq et permet d'exporter le résultat au format PDF.

## Fonctionnalités

- résumés courts, moyens ou détaillés ;
- correction orthographique et grammaticale ;
- reformulation simple ou professionnelle ;
- transformation d'un texte en liste à puces ;
- réponse en français, anglais, arabe ou dans la langue détectée ;
- conservation optionnelle de la structure des paragraphes ;
- copie, comparaison avant/après et export PDF ;
- interface responsive avec prise en charge du sens d'écriture RTL.

## Technologies

- **Backend :** Python, Flask
- **IA générative :** Groq API avec `llama-3.3-70b-versatile`
- **PDF :** ReportLab
- **Frontend :** HTML, CSS et JavaScript natif

## Prérequis

- Python 3.10 ou une version plus récente ;
- `pip` ;
- une clé API Groq, disponible depuis la [console Groq](https://console.groq.com/keys).

## Installation

Clonez le dépôt, puis placez-vous dans son dossier :

```bash
git clone https://github.com/SafiaTirar/AI-text-Assistant.git
cd ai-text-assistant
```

Créez et activez un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows (PowerShell), utilisez plutôt :

```powershell
.venv\Scripts\Activate.ps1
```

Installez ensuite les dépendances :

```bash
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

## Configuration

Copiez le fichier d'exemple puis renseignez votre clé Groq :

```bash
cp .env.example .env
```

Contenu attendu dans `.env` :

```dotenv
GROQ_API_KEY=votre_cle_groq_ici
```

Le fichier `.env` contient un secret local et est volontairement exclu de Git.

## Lancement

Depuis la racine du projet :

```bash
python backend/app.py
```

Ouvrez ensuite [http://localhost:5001](http://localhost:5001) dans votre navigateur.

Pour utiliser l'application, saisissez un texte, sélectionnez une opération et une langue, puis cliquez sur **Générer**. Le raccourci `Ctrl + Entrée` lance également le traitement.

## API

### Traiter un texte

`POST /api/process`

Exemple de requête :

```bash
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Votre texte à résumer.",
    "operation": "resume_court",
    "language": "fr",
    "options": {
      "preserveFormatting": false,
      "strictSpelling": false
    }
  }'
```

Exemple de réponse :

```json
{
  "result": "Le texte résumé...",
  "detected_language": "fr"
}
```

Opérations acceptées :

- `resume_court`, `resume_moyen`, `resume_long`
- `correction`
- `reformulation_simple`, `reformulation_professionnelle`
- `bullets`

Langues acceptées : `auto`, `fr`, `en` et `ar`.

### Exporter un PDF

`POST /api/download-pdf`

```json
{
  "content": "Contenu à exporter"
}
```

La réponse est un fichier PDF nommé `resultat.pdf`.

## Structure du projet

```text
ai-text-assistant/
├── .env.example               # Exemple de configuration locale
├── .gitignore                 # Fichiers exclus du dépôt
├── README.md
├── backend/
│   ├── app.py                 # Application Flask et routes HTTP
│   ├── llm_client.py          # Client de l'API Groq
│   ├── processors.py          # Construction des prompts
│   ├── pdf_generator.py       # Génération des PDF
│   ├── requirements.txt       # Dépendances Python
│   └── templates/index.html   # Interface servie par Flask
└── frontend/index.html        # Copie statique de l'interface
```

Le parcours principal est le suivant :

```text
Navigateur → API Flask → construction du prompt → API Groq → résultat JSON
                                                   ↓
                                            export ReportLab
```

Pour plus de détails, consultez [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) et [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md).

## Sécurité

- ne publiez jamais votre fichier `.env` ni votre clé API ;
- renouvelez immédiatement une clé qui aurait été exposée ;
- l'application est configurée pour un usage local et le serveur Flask intégré ne doit pas être utilisé tel quel en production.

## Équipe

Projet réalisé par Safia Tirar, Boussoufi Kenza et Souhaib Madhour dans le cadre du PFA.
