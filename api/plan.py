from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
CORS(app)

from api.models.get_summarizer import generate_abstractive
from api.utils.prompt_templates import planner_prompt_from_insights

@app.route('/api/plan', methods=['POST'])
def plan_research():
    try:
        data = request.get_json()
        insights = data.get('insights', {})
        topic = data.get('topic', '')
        
        if not insights or not topic:
            return jsonify({'error': 'Insights and topic are required'}), 400
        
        insight_str = insights if isinstance(insights, str) else json.dumps(insights)
        prompt = planner_prompt_from_insights(insight_str, topic)
        
        try:
            plan = generate_abstractive(prompt, max_tokens=600)
            return jsonify({'plan': plan})
        except Exception as e:
            return jsonify({'error': f"Planner failed: {e}"}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
