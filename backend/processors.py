def build_prompt(text, operation, language, options):
    preserve = options.get("preserveFormatting", False)
    strict = options.get("strictSpelling", False)

    # Keep prompts consistent with the requested output language.
    # (Previously, instructions were mostly in French even for English, which made "English" feel broken.)

    tasks_fr = {
        "resume_court": "Fais un résumé très court (3–4 lignes).",
        "resume_moyen": "Fais un résumé moyen (un paragraphe).",
        "resume_long": "Fais un résumé détaillé et structuré.",
        "correction": "Corrige toutes les fautes de grammaire et orthographe.",
        "reformulation_simple": "Reformule de manière simple et accessible.",
        "reformulation_professionnelle": "Reformule avec un style professionnel et cohérent.",
        "bullets": "Transforme le texte en bullet points clairs et concis.",
    }

    tasks_en = {
        "resume_court": "Write a very short summary (3–4 lines).",
        "resume_moyen": "Write a medium-length summary (one paragraph).",
        "resume_long": "Write a detailed, well-structured summary.",
        "correction": "Correct all grammar and spelling mistakes.",
        "reformulation_simple": "Rewrite in a simple, easy-to-understand way.",
        "reformulation_professionnelle": "Rewrite in a professional, coherent style.",
        "bullets": "Convert the text into clear, concise bullet points.",
    }

    tasks_ar = {
        "resume_court": "اكتب ملخصًا قصيرًا جدًا (3–4 أسطر).",
        "resume_moyen": "اكتب ملخصًا متوسط الطول (فقرة واحدة).",
        "resume_long": "اكتب ملخصًا مفصلًا ومنظمًا.",
        "correction": "صحح جميع الأخطاء النحوية والإملائية.",
        "reformulation_simple": "أعد صياغة النص بطريقة بسيطة وواضحة.",
        "reformulation_professionnelle": "أعد صياغة النص بأسلوب مهني ومتناسق.",
        "bullets": "حوّل النص إلى نقاط واضحة ومختصرة.",
    }

    # Extra instructions per language
    if language == "en":
        base = "You are an expert text assistant. Respond ONLY in English."
        task = tasks_en.get(operation, tasks_en["resume_court"])
        extra_parts = []
        if strict:
            extra_parts.append("Use strict correction; briefly explain important changes if needed.")
        if preserve:
            extra_parts.append("Preserve the original paragraph structure.")
        extra = (" " + " ".join(extra_parts)) if extra_parts else ""
        return f"""{base}
Task: {task}{extra}

Text:
\"\"\"{text}\"\"\"
"""

    if language == "ar":
        base = "أنت مساعد خبير في معالجة النصوص. أجب باللغة العربية فقط."
        task = tasks_ar.get(operation, tasks_ar["resume_court"])
        extra_parts = []
        if strict:
            extra_parts.append("استخدم تصحيحًا صارمًا واذكر أهم التغييرات عند الحاجة.")
        if preserve:
            extra_parts.append("حافظ على بنية الفقرات الأصلية.")
        extra = (" " + " ".join(extra_parts)) if extra_parts else ""
        return f"""{base}
المهمة: {task}{extra}

النص:
\"\"\"{text}\"\"\"
"""

    # Default: French or auto
    if language == "auto":
        base = "Tu es un assistant expert en traitement de texte. Réponds dans la même langue que le texte fourni."
    else:
        base = "Tu es un assistant expert en traitement de texte. Réponds uniquement en français."

    task = tasks_fr.get(operation, tasks_fr["resume_court"])
    extra = ""
    if strict:
        extra += " Utilise une correction stricte et explique les modifications si nécessaire."
    if preserve:
        extra += " Préserve le formatage initial (paragraphes)."

    return f"""{base}
Tâche : {task}{extra}

Texte à traiter :
\"\"\"{text}\"\"\"
"""
