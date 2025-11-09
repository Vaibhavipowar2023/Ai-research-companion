# AI Research Companion 

A modern web application that helps researchers find, summarize, and synthesize academic papers from arXiv and PubMed, then generates actionable research plans.

## 🌟 Features

- **Smart Paper Retrieval**: Fetch papers from arXiv and PubMed APIs
- **AI-Powered Summarization**: Generate extractive and abstractive summaries using OpenAI
- **Insight Synthesis**: Automatically identify themes, pros, cons, and research gaps
- **Research Planning**: Get a structured 3-step research roadmap
- **Modern UI**: Built with Next.js and Tailwind CSS
- **Serverless Backend**: Python API endpoints optimized for Vercel

## 🏗️ Architecture

- **Frontend**: Next.js 14 + React + TypeScript + Tailwind CSS
- **Backend**: Python Flask APIs deployed as Vercel Serverless Functions
- **APIs**: OpenAI GPT-4o-mini, arXiv, PubMed, Sentence Transformers

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- OpenAI API key
- Vercel account (free tier works)
- Git

## 🚀 Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Ai-research-companion.git
cd Ai-research-companion
```

### 2. Install Node.js dependencies

```bash
npm install
# or
yarn install
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env.local` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 5. Run the development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🌐 Deploying to Vercel

### Method 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
vercel
```

4. **Set Environment Variables**:
```bash
vercel env add OPENAI_API_KEY
vercel env add OPENAI_MODEL
vercel env add EMBEDDING_MODEL
```

5. **Deploy to Production**:
```bash
vercel --prod
```

### Method 2: Deploy via GitHub Integration

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Import to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Configure Environment Variables**:
   - In Vercel dashboard → Project Settings → Environment Variables
   - Add:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `OPENAI_MODEL`: `gpt-4o-mini`
     - `EMBEDDING_MODEL`: `all-MiniLM-L6-v2`

4. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy automatically

## ⚙️ Configuration

### vercel.json

The `vercel.json` file configures:
- Python runtime for API endpoints
- Routing rules
- Environment variables

### API Endpoints

- `POST /api/retrieve` - Retrieve papers from arXiv and PubMed
- `POST /api/summarize` - Generate paper summaries
- `POST /api/insights` - Synthesize research insights
- `POST /api/plan` - Generate research roadmap
- `GET /api/health` - Health check

## 📦 Project Structure

```
vercel-research-app/
├── api/                      # Python serverless functions
│   ├── models/
│   │   └── get_summarizer.py
│   ├── utils/
│   │   ├── api_utils.py
│   │   ├── nlp_utils.py
│   │   └── prompt_templates.py
│   ├── retrieve.py           # Paper retrieval endpoint
│   ├── summarize.py          # Summarization endpoint
│   ├── insights.py           # Insights synthesis endpoint
│   └── plan.py               # Research planning endpoint
├── pages/
│   ├── _app.tsx              # Next.js app wrapper
│   └── index.tsx             # Main UI page
├── styles/
│   └── globals.css           # Global styles
├── public/                   # Static assets
├── vercel.json               # Vercel configuration
├── next.config.js            # Next.js configuration
├── tailwind.config.js        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Troubleshooting

### Common Issues

1. **"Missing OPENAI_API_KEY" error**
   - Ensure environment variable is set in Vercel dashboard
   - Redeploy after adding environment variables

2. **Timeout errors**
   - Vercel free tier has 10s timeout for serverless functions
   - Reduce `max_results` parameters or upgrade to Pro plan

3. **NLTK data not found**
   - The app automatically downloads NLTK punkt data
   - If issues persist, check Vercel build logs

4. **Sentence Transformers model loading fails**
   - Model is cached on first request
   - Subsequent requests will be faster
   - Consider upgrading Vercel plan for more memory

### Build Failures

If build fails:
```bash
# Clear Vercel cache
vercel --force

# Check build logs
vercel logs
```

## 🎯 Usage

1. Enter your research question or topic
2. Adjust the number of papers (2-8)
3. Click "Run Analysis"
4. View retrieved papers and summaries
5. Explore synthesized insights (themes, pros, cons, gaps)
6. Review the generated research plan
7. Download insights and plan as text files

## 📊 Performance Optimization

- API responses are streamed for faster perceived performance
- Sentence embeddings are cached using `@lru_cache`
- NLTK data is downloaded once and reused
- Lightweight embedding model (all-MiniLM-L6-v2) for fast inference

## 🔐 Security

- API keys stored as Vercel environment variables (encrypted)
- No sensitive data stored in code
- CORS enabled for API endpoints
- Rate limiting recommended for production use

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check Vercel documentation: https://vercel.com/docs
- OpenAI API docs: https://platform.openai.com/docs

## 🙏 Acknowledgments

- OpenAI for GPT models
- Sentence Transformers for embeddings
- arXiv and PubMed for paper APIs
- Vercel for hosting platform


