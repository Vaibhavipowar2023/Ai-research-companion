def abstractive_prompt_for_paper(title, extractive, full_abstract):
    return (
        f"You are an expert research summarizer.\n\n"
        f"Paper Title: {title}\n\n"
        f"Key Sentences (Extractive):\n{extractive}\n\n"
        f"Full Abstract:\n{full_abstract}\n\n"
        "Task: Write a clear, human-friendly summary in 2–3 sentences.\n"
        "- Use plain language.\n"
        "- Focus on the method and main results.\n"
        "- Highlight any important terms in **bold**.\n"
        "- Keep it factual and concise."
    )

def insight_prompt_for_summaries(summaries):
    joined = "\n\n".join(f"{i+1}. {s}" for i, s in enumerate(summaries))
    return (
        "You are a research synthesizer.\n\n"
        "Below are summaries of several research papers:\n\n"
        f"{joined}\n\n"
        "Return a JSON object with keys exactly: "
        "themes (list), pros (list), cons (list), gaps (list). "
        "Make items specific and concise."
    )

def planner_prompt_from_insights(insights_json, topic):
    return (
        f"You are a senior researcher guiding a new project.\n"
        f"Research Topic: {topic}\n"
        f"Synthesized Insights (JSON): {insights_json}\n\n"
        "Provide a 3-step research roadmap:\n"
        "1. Immediate Small Reproduction (2 weeks)\n"
        "2. Small Extension (1 month)\n"
        "3. Full Experiment (2 months)\n"
        "For each, recommend papers, datasets, tools, and give short bullet justifications. Highlight key recommendations."
    )
