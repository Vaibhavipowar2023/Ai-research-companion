from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
CORS(app)

from api.utils.nlp_utils import extractive_summary_by_embedding
from api.models.get_summarizer import generate_abstractive
from api.utils.prompt_templates import abstractive_prompt_for_paper

@app.route('/api/summarize', methods=['POST'])
def summarize_papers():
    try:
        data = request.get_json()
        papers = data.get('papers', [])
        
        if not papers:
            return jsonify({'error': 'Papers array is required'}), 400
        
        summaries = []
        
        for paper in papers:
            abstract_field = paper.get("abstract", "")
            if isinstance(abstract_field, dict):
                abstract = " ".join(str(v) for v in abstract_field.values())
            elif isinstance(abstract_field, list):
                abstract = " ".join(str(v) for v in abstract_field)
            else:
                abstract = str(abstract_field or "")
            abstract = abstract.strip()

            title = str(paper.get("title", "No title") or "").strip()
            extractive = extractive_summary_by_embedding(abstract, top_n=2) if abstract else ""
            abstractive = extractive

            if abstract:
                try:
                    prompt = abstractive_prompt_for_paper(
                        title=title, 
                        extractive=extractive, 
                        full_abstract=abstract
                    )
                    abstractive = generate_abstractive(prompt, max_tokens=220)
                except Exception as e:
                    print(f"Abstractive generation failed: {e}")

            summaries.append({
                "title": title,
                "authors": paper.get("authors", []),
                "link": paper.get("link", ""),
                "source": paper.get("source", ""),
                "extractive": extractive,
                "abstractive": abstractive
            })
        
        return jsonify({'summaries': summaries})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
