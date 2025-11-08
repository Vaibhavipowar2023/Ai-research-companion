# Migration Guide: Streamlit → Vercel

This guide helps you migrate from the original Streamlit app to the Vercel-compatible Next.js version.

## Key Differences

### Architecture Changes

| Aspect | Streamlit Version | Vercel Version |
|--------|------------------|----------------|
| Frontend | Streamlit (Python) | Next.js + React (TypeScript) |
| Backend | Integrated in Streamlit | Separate Flask API endpoints |
| Deployment | Streamlit Cloud, Railway, Render | Vercel (serverless) |
| Session Storage | SQLite database | No persistence (stateless) |
| WebSocket | Yes (Streamlit requires it) | No (REST API) |
| State Management | Streamlit session state | React useState |

### What Changed

#### 1. **File Structure**
```
OLD (Streamlit):                    NEW (Vercel):
├── main.py                         ├── pages/index.tsx
├── agents/                         ├── api/
│   ├── retriever_agent.py          │   ├── retrieve.py
│   ├── summarizer_agent.py         │   ├── summarize.py
│   ├── insight_agent.py            │   ├── insights.py
│   └── planner_agent.py            │   └── plan.py
├── models/                         ├── api/models/
└── utils/                          └── api/utils/
```

#### 2. **Session Management**

**Streamlit** (saved to SQLite):
```python
save_session(query, papers, summaries, insights, plan)
```

**Vercel** (no persistence - client-side only):
```typescript
// Data only exists during page session
// Users can download results as text files
```

#### 3. **UI Components**

**Streamlit**:
```python
st.title("🔬 AI Research Companion")
st.form("query_form")
st.progress(0, text="Retrieving papers...")
```

**Next.js**:
```tsx
<h1>🔬 AI Research Companion</h1>
<form onSubmit={handleSubmit}>
<progress value={progress} max={100} />
```

#### 4. **API Calls**

**Streamlit** (direct function calls):
```python
papers = retrieve_papers(query, top_k=num_papers)
summaries = [summarize_paper(p) for p in papers]
```

**Next.js** (HTTP API calls):
```typescript
const response = await axios.post('/api/retrieve', { query, top_k })
const papers = response.data.papers
```

## Migration Steps

### Option 1: Keep Both Versions

You can maintain both versions for different use cases:

- **Streamlit**: For internal use, rapid prototyping, local experiments
- **Vercel**: For public deployment, production, scalable access

### Option 2: Full Migration to Vercel

1. **Copy Your Customizations**
   - Custom prompts → Update `api/utils/prompt_templates.py`
   - Custom logic → Update relevant API endpoints
   - UI preferences → Modify `pages/index.tsx` and `styles/globals.css`

2. **Handle Data Migration**
   - Export existing SQLite sessions: `sqlite3 research_memory.db .dump > backup.sql`
   - Sessions won't auto-migrate (Vercel version is stateless)
   - Consider adding a database for persistence (see below)

3. **Update Configuration**
   - Copy `.env` values to Vercel environment variables
   - Adjust any custom settings in code

### Adding Database Support (Optional)

If you need session persistence on Vercel, integrate a database:

#### Recommended Options:

1. **Vercel Postgres** (easiest)
```bash
vercel postgres create
```

2. **Supabase** (free tier available)
```typescript
import { createClient } from '@supabase/supabase-js'
```

3. **MongoDB Atlas** (free tier available)
```python
from pymongo import MongoClient
```

4. **PlanetScale** (MySQL compatible)
```typescript
import { PrismaClient } from '@prisma/client'
```

## Features Comparison

### Maintained Features ✅
- ✅ Paper retrieval from arXiv and PubMed
- ✅ Extractive and abstractive summarization
- ✅ Insight synthesis (themes, pros, cons, gaps)
- ✅ Research plan generation
- ✅ Download results as text files
- ✅ Adjustable number of papers
- ✅ Real-time progress tracking

### Changed Features 🔄
- 🔄 Session history (removed in base version, can be added with DB)
- 🔄 UI styling (from Streamlit → modern Tailwind CSS)
- 🔄 API architecture (from integrated → serverless functions)

### New Features ✨
- ✨ Modern, responsive UI
- ✨ Global CDN distribution
- ✨ Automatic scaling
- ✨ Better mobile experience
- ✨ Faster page loads
- ✨ TypeScript type safety

## Performance Considerations

### Streamlit
- Single process, limited concurrency
- WebSocket overhead
- Good for <100 concurrent users
- Best for internal tools

### Vercel
- Serverless, auto-scaling
- REST API, stateless
- Handles thousands of concurrent users
- Best for public applications
- Cold start latency (0.5-2s first request)

## Cost Comparison

### Streamlit Cloud
- Free: 1 private app + community apps
- Team: $20/month per editor

### Vercel
- Hobby (Free): 100 GB bandwidth, 100h execution
- Pro: $20/month (1 TB bandwidth, 1000h execution)

### OpenAI API Costs
Same for both versions:
- GPT-4o-mini: ~$0.15 per 1M input tokens
- ~$0.01-0.05 per analysis (depending on paper count)

## When to Use Each Version

### Use Streamlit When:
- 🏠 Deploying internally within organization
- 🔬 Rapid prototyping and experimentation
- 👥 Small team (<50 users)
- 💾 Need built-in session management
- 🐍 Team prefers Python for everything

### Use Vercel When:
- 🌍 Public-facing application
- 📈 Need to scale to many users
- ⚡ Want fastest global performance
- 💰 Cost-effective at scale
- 🎨 Want modern, customizable UI
- 🔧 Need API endpoints for integrations

## Deployment Comparison

### Streamlit Cloud
```bash
streamlit run main.py
# Deploy: Push to GitHub, connect to Streamlit Cloud
```

### Vercel
```bash
vercel
# Deploy: Push to GitHub, auto-deploys on commit
```

## Troubleshooting Migration Issues

### Issue: Missing SQLite Sessions

**Streamlit**: Sessions saved to `research_memory.db`  
**Vercel**: No built-in persistence

**Solutions**:
1. Export important sessions before migration
2. Add database integration (see above)
3. Use client-side downloads for now

### Issue: Different UI Behavior

**Streamlit**: Server-side rendering with automatic re-runs  
**Vercel**: Client-side React state management

**Solutions**:
1. Test all workflows in new UI
2. Adjust user expectations
3. Customize UI in `pages/index.tsx`

### Issue: API Timeouts

**Streamlit**: No hard timeout (depends on hosting)  
**Vercel Free**: 10-second timeout

**Solutions**:
1. Reduce paper count (use 3-4 instead of 6-8)
2. Upgrade to Vercel Pro (60s timeout)
3. Optimize code for faster execution

## Code Porting Examples

### Example 1: Retrieving Papers

**Before (Streamlit)**:
```python
from agents.retriever_agent import retrieve_papers
papers = retrieve_papers(query, top_k=num_papers)
```

**After (Vercel)**:
```typescript
const response = await axios.post('/api/retrieve', {
  query: query,
  top_k: numPapers
})
const papers = response.data.papers
```

### Example 2: Progress Updates

**Before (Streamlit)**:
```python
progress = st.progress(0, text="Retrieving papers…")
progress.progress(20, text="Summarizing…")
```

**After (Vercel)**:
```typescript
setProgress(0)
setProgressText('Retrieving papers...')
// ... later
setProgress(20)
setProgressText('Summarizing...')
```

### Example 3: Displaying Results

**Before (Streamlit)**:
```python
with st.expander(f"{idx}. {paper['title']}"):
    st.markdown(f"**{paper['source']}**")
    st.write(summary)
```

**After (Vercel)**:
```tsx
<div className="card">
  <h3>{idx}. {paper.title}</h3>
  <span className="badge">{paper.source}</span>
  <p>{summary}</p>
</div>
```

## Getting Help

### Streamlit Resources
- Docs: https://docs.streamlit.io
- Forum: https://discuss.streamlit.io
- GitHub: https://github.com/streamlit/streamlit

### Vercel Resources
- Docs: https://vercel.com/docs
- GitHub: https://github.com/vercel/vercel
- Discord: https://vercel.com/discord

## Conclusion

Both versions have their strengths:

- **Keep Streamlit** for internal tools and rapid development
- **Use Vercel** for public applications and scale

You can even run both in parallel:
- Streamlit for your research team
- Vercel for public access or API integrations

Choose based on your specific needs! 🚀
