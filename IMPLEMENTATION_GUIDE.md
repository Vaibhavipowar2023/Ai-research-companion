# 🚀 AI Research Companion - Complete Implementation Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [What Changed](#what-changed)
3. [Architecture Overview](#architecture-overview)
4. [Deployment Options](#deployment-options)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Going to Production](#going-to-production)

---

## Quick Start

### Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed
- OpenAI API key
- Git installed
- Vercel account (free)

### 5-Minute Local Setup

```bash
# 1. Navigate to project
cd vercel-research-app

# 2. Install dependencies
npm install
pip3 install -r requirements.txt

# 3. Set up environment
cp .env.example .env.local
# Edit .env.local and add your OPENAI_API_KEY

# 4. Run development server
npm run dev

# 5. Open browser
# Visit http://localhost:3000
```

### 10-Minute Vercel Deployment

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Add environment variables
vercel env add OPENAI_API_KEY production
# Paste your key when prompted

vercel env add OPENAI_MODEL production
# Enter: gpt-4o-mini

vercel env add EMBEDDING_MODEL production
# Enter: all-MiniLM-L6-v2

# 5. Deploy to production
vercel --prod

# Done! Your app is live 🎉
```

---

## What Changed

### From Streamlit to Vercel

Your original Streamlit app has been **completely refactored** to work with Vercel's serverless architecture:

#### Frontend
- **Was**: Streamlit (Python-based UI)
- **Now**: Next.js 14 + React + TypeScript + Tailwind CSS

#### Backend
- **Was**: Integrated with Streamlit app
- **Now**: Separate Flask API endpoints (serverless functions)

#### Database
- **Was**: SQLite for session storage
- **Now**: Stateless (no built-in persistence)*

*Can easily add database if needed - see MIGRATION_GUIDE.md

#### Key Benefits
✅ Much faster page loads  
✅ Better mobile experience  
✅ Scales to thousands of users automatically  
✅ Global CDN distribution  
✅ Modern, customizable UI  
✅ API endpoints available for integrations  

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (Next.js)                  │
│  ┌────────────────────────────────────────────────┐ │
│  │  pages/index.tsx - Main React Component        │ │
│  │  - Search form                                  │ │
│  │  - Progress tracking                            │ │
│  │  - Results display                              │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────┐
│            API Layer (Python/Flask)                  │
│  ┌─────────────┬─────────────┬─────────────┐        │
│  │ /api/retrieve│ /api/summarize│ /api/insights│    │
│  │             │             │             │        │
│  │  Fetch      │  Generate   │  Synthesize │        │
│  │  papers     │  summaries  │  insights   │        │
│  └─────────────┴─────────────┴─────────────┘        │
│                      │                               │
│                      │ /api/plan                     │
│                      │ Generate research roadmap     │
└──────────────────────┼───────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌────────────────┐          ┌────────────────┐
│ External APIs  │          │ AI Models      │
│ - arXiv        │          │ - OpenAI       │
│ - PubMed       │          │ - Transformers │
└────────────────┘          └────────────────┘
```

### File Structure Explained

```
vercel-research-app/
│
├── api/                          # Python serverless functions
│   ├── retrieve.py               # GET papers from arXiv/PubMed
│   ├── summarize.py              # Generate summaries
│   ├── insights.py               # Synthesize insights
│   ├── plan.py                   # Generate research plan
│   │
│   ├── models/
│   │   └── get_summarizer.py    # OpenAI integration
│   │
│   └── utils/
│       ├── api_utils.py          # arXiv/PubMed fetchers
│       ├── nlp_utils.py          # Embeddings & ranking
│       └── prompt_templates.py   # LLM prompts
│
├── pages/
│   ├── _app.tsx                  # Next.js app wrapper
│   └── index.tsx                 # Main UI (React)
│
├── styles/
│   └── globals.css               # Tailwind CSS styles
│
├── public/                       # Static assets
│
├── vercel.json                   # Vercel configuration
├── next.config.js                # Next.js config
├── package.json                  # Node dependencies
├── requirements.txt              # Python dependencies
│
└── Documentation/
    ├── README.md                 # Main docs
    ├── DEPLOYMENT_GUIDE.md       # Detailed deployment
    └── MIGRATION_GUIDE.md        # Streamlit → Vercel
```

---

## Deployment Options

You have **multiple ways** to deploy this application:

### Option 1: Vercel (Recommended)
**Best for**: Production, public apps, scaling

**Pros**:
- ✅ Automatic scaling
- ✅ Global CDN
- ✅ Free tier generous
- ✅ Zero configuration
- ✅ Auto HTTPS

**Deployment**:
```bash
vercel --prod
```

### Option 2: Keep Original Streamlit
**Best for**: Internal tools, quick demos

**Pros**:
- ✅ Faster to iterate
- ✅ Python-only
- ✅ Built-in session management

**Deployment**:
```bash
streamlit run main.py
```

### Option 3: Hybrid Approach
Run **both versions** in parallel:
- Streamlit for internal research team
- Vercel for public access/API

---

## Configuration

### Environment Variables

#### Required
```env
OPENAI_API_KEY=sk-...           # Your OpenAI key
```

#### Optional (with defaults)
```env
OPENAI_MODEL=gpt-4o-mini        # Model to use
EMBEDDING_MODEL=all-MiniLM-L6-v2 # Embedding model
```

### Adding to Vercel

**Via Dashboard**:
1. Project Settings → Environment Variables
2. Add each variable
3. Select Production, Preview, Development

**Via CLI**:
```bash
vercel env add OPENAI_API_KEY production
vercel env add OPENAI_MODEL production
```

### Customization Options

#### 1. Adjust Paper Sources
Edit `api/utils/api_utils.py`:
```python
ARXIV_BASE = "http://export.arxiv.org/api/query"
# Add more sources here
```

#### 2. Change UI Theme
Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ }
    }
  }
}
```

#### 3. Modify Prompts
Edit `api/utils/prompt_templates.py`:
```python
def abstractive_prompt_for_paper(title, extractive, full_abstract):
    return f"Your custom prompt here..."
```

#### 4. Adjust API Limits
Edit `api/retrieve.py`:
```python
max_results = 20  # Increase/decrease
```

---

## Testing

### Local Testing

```bash
# Start dev server
npm run dev

# In another terminal, test API endpoints
curl http://localhost:3000/api/health

# Test retrieval
curl -X POST http://localhost:3000/api/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning","top_k":3}'
```

### Testing on Vercel

```bash
# Deploy to preview
vercel

# Test the preview URL
curl https://your-app-preview.vercel.app/api/health
```

### Manual Testing Checklist

- [ ] Enter query and click "Run Analysis"
- [ ] Verify papers are retrieved
- [ ] Check summaries are generated
- [ ] Verify insights display correctly
- [ ] Check research plan is generated
- [ ] Test download buttons
- [ ] Test on mobile device
- [ ] Verify error handling (try invalid query)

---

## Going to Production

### Pre-Launch Checklist

#### 1. Security
- [ ] Rotate API keys
- [ ] Set up usage alerts on OpenAI dashboard
- [ ] Review environment variables (no secrets in code)
- [ ] Enable HTTPS (automatic on Vercel)

#### 2. Performance
- [ ] Test with realistic data volume
- [ ] Monitor function execution times
- [ ] Check cold start latency
- [ ] Optimize heavy dependencies if needed

#### 3. Monitoring
- [ ] Enable Vercel Analytics
- [ ] Set up error tracking (optional: Sentry)
- [ ] Monitor OpenAI API costs
- [ ] Set up uptime monitoring

#### 4. Documentation
- [ ] Update README with your deployment URL
- [ ] Document any custom modifications
- [ ] Create user guide if needed

### Launch Steps

```bash
# 1. Final testing on preview
vercel

# 2. Deploy to production
vercel --prod

# 3. Verify deployment
curl https://your-app.vercel.app/api/health

# 4. Test full workflow
# Visit https://your-app.vercel.app
# Run complete analysis

# 5. Monitor for issues
# Check Vercel dashboard → Logs
```

### Post-Launch

1. **Monitor Usage**
   - Vercel dashboard for traffic
   - OpenAI dashboard for API costs
   - User feedback

2. **Scale as Needed**
   - Free tier: ~1000 requests/day
   - Upgrade to Pro if you exceed limits

3. **Regular Maintenance**
   - Update dependencies monthly
   - Monitor security advisories
   - Rotate API keys quarterly

---

## Common Workflows

### Adding a New Paper Source

1. Add fetch function to `api/utils/api_utils.py`:
```python
def fetch_newsource(query, max_results=10):
    # Your implementation
    return papers
```

2. Update `api/retrieve.py`:
```python
newsource = fetch_newsource(query)
combined = arx + pub + newsource
```

### Customizing the UI

1. Edit `pages/index.tsx` for layout changes
2. Edit `styles/globals.css` for styling
3. Edit `tailwind.config.js` for theme colors

### Adding Database Support

1. Choose a database (Vercel Postgres, Supabase, MongoDB Atlas)
2. Install client library
3. Create schema/tables
4. Add CRUD operations to API endpoints
5. Update UI to load/save sessions

---

## Troubleshooting

### "Missing OPENAI_API_KEY"
→ Add to Vercel environment variables and redeploy

### Function Timeout
→ Reduce paper count or upgrade to Pro plan

### Import Errors
→ Ensure all dependencies in `requirements.txt`

### CORS Issues
→ Already handled by `flask-cors`, check network tab

### Slow First Request
→ Normal cold start (~1-2s), subsequent requests faster

---

## Cost Estimates

### Vercel Hosting
- **Hobby (Free)**: 100 GB bandwidth, 100h execution
  - ~1000-5000 analyses/month (depending on paper count)
  - $0/month

- **Pro ($20/month)**: 1 TB bandwidth, 1000h execution
  - ~50,000-100,000 analyses/month
  - Better for production apps

### OpenAI API
- **GPT-4o-mini**: ~$0.15 per 1M input tokens
- **Per Analysis**: ~$0.01-0.05 (varies by paper count)
- **1000 analyses**: ~$10-50/month

### Total Cost Example
- **Light usage** (100 analyses/month): $1-5/month
- **Medium usage** (1000 analyses/month): $10-50/month
- **Heavy usage** (10,000 analyses/month): $100-500/month + Vercel Pro

---

## Support & Resources

### Documentation
- [README.md](README.md) - Overview
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed deployment
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Streamlit migration

### External Resources
- **Vercel**: https://vercel.com/docs
- **Next.js**: https://nextjs.org/docs
- **OpenAI**: https://platform.openai.com/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

### Getting Help
- GitHub Issues: Create issue in your repo
- Vercel Support: https://vercel.com/support
- OpenAI Forum: https://community.openai.com

---

## Next Steps

1. ✅ **Deploy locally** and test
2. ✅ **Deploy to Vercel** preview
3. ✅ **Verify all features** work
4. ✅ **Deploy to production**
5. 📊 **Monitor usage** and costs
6. 🎨 **Customize** as needed
7. 🚀 **Share** with users!

---

**Congratulations!** You now have a production-ready AI Research Companion deployed on Vercel! 🎉

Your app features:
- ✅ Modern, responsive UI
- ✅ Intelligent paper retrieval
- ✅ AI-powered summarization
- ✅ Research insights synthesis
- ✅ Automated research planning
- ✅ Global CDN distribution
- ✅ Automatic scaling
- ✅ Production-grade infrastructure

Happy researching! 🔬✨
