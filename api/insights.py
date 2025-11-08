from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
CORS(app)

from api.models.get_summarizer import try_llm_completion
from api.utils.prompt_templates import insight_prompt_for_summaries

REQUIRED_KEYS = {"themes": list, "pros": list, "cons": list, "gaps": list}

def _validate(obj: dict) -> dict:
    valid = {k: [] for k in REQUIRED_KEYS}
    if not isinstance(obj, dict):
        return valid
    for k, t in REQUIRED_KEYS.items():
        v = obj.get(k, [])
        valid[k] = v if isinstance(v, t) else []
    return valid

def _format_raw(obj: dict) -> str:
    lines = []
    if obj.get("themes"): 
        lines += ["Themes:"] + [f"• {x}" for x in obj["themes"]] + [""]
    if obj.get("pros"):   
        lines += ["Pros:"]   + [f"+ {x}" for x in obj["pros"]]     + [""]
    if obj.get("cons"):   
        lines += ["Cons:"]   + [f"- {x}" for x in obj["cons"]]     + [""]
    if obj.get("gaps"):   
        lines += ["Gaps:"]   + [f"? {x}" for x in obj["gaps"]]
    return "\n".join(lines).strip()

@app.route('/api/insights', methods=['POST'])
def synthesize_insights():
    try:
        data = request.get_json()
        summaries = data.get('summaries', [])
        
        if not summaries:
            return jsonify({'error': 'Summaries array is required'}), 400
        
        prompt = insight_prompt_for_summaries(summaries)
        resp = try_llm_completion(prompt, expect_json=True)
        
        if isinstance(resp, dict) and resp.get("error"):
            return jsonify(resp), 500
        
        try:
            obj = json.loads(resp) if isinstance(resp, str) else resp
            obj = _validate(obj)
            obj["raw"] = _format_raw(obj)
            return jsonify(obj)
        except Exception as e:
            return jsonify({"error": f"Failed to parse insights JSON: {e}"}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
