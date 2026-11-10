import os
from groq import Groq

# Choix du modèle (très bon pour texte) :
MODEL = "llama-3.3-70b-versatile"   # ou un autre modèle Groq si tu veux

def call_llm(prompt: str) -> str:
    """
    Appelle le modèle Groq (LLama 3.3) avec un prompt
    et renvoie le texte généré.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "[Erreur LLM Groq] GROQ_API_KEY n'est pas défini. Ajoute ta clé API (export GROQ_API_KEY=...)."

    try:
        # Client Groq (utilise l'API gratuite avec ta clé)
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"[Erreur LLM Groq] {e}"
