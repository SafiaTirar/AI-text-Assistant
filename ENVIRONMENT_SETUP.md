# Configuration de l'environnement

Ce projet utilise la variable d'environnement **`GROQ_API_KEY`** pour appeler l'API Groq.

## Méthode recommandée : fichier `.env`

Depuis la racine du dépôt, copiez le fichier d'exemple :

```bash
cp .env.example .env
```

Remplacez ensuite la valeur d'exemple par votre clé :

```dotenv
GROQ_API_KEY=votre_cle_groq_ici
```

L'application charge automatiquement ce fichier au démarrage :

```bash
source .venv/bin/activate
python backend/app.py
```

## Alternative : variable du terminal

```bash
export GROQ_API_KEY="votre_cle_groq_ici"
```

Le fichier `.env` est ignoré par Git. Ne partagez jamais son contenu et révoquez toute clé accidentellement publiée.
