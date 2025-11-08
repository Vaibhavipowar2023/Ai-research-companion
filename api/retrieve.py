from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
CORS(app)

# Import your existing modules
from api.utils.api_utils import fetch_arxiv, fetch_pubmed
from api.utils.nlp_utils import rank_papers_by_query

@app.route('/api/retrieve', methods=['POST'])
def retrieve_papers():
    try:
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', 6)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Fetch from sources
        try:
            arx = fetch_arxiv(query, max_results=10)
        except Exception as e:
            print(f"ArXiv fetch error: {e}")
            arx = []
        
        try:
            pub = fetch_pubmed(query, retmax=10)
        except Exception as e:
            print(f"PubMed fetch error: {e}")
            pub = []
        
        combined = arx + pub
        
        if not combined:
            return jsonify({'papers': []})
        
        # Rank papers
        ranked = rank_papers_by_query(query, combined, top_k=top_k)
        
        return jsonify({'papers': ranked})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
