# 🚀 Complete Vercel Deployment Guide

## Overview

This guide will walk you through deploying your AI Research Companion to Vercel step-by-step.

## Prerequisites Checklist

- ✅ GitHub account
- ✅ Vercel account (sign up at vercel.com using GitHub)
- ✅ OpenAI API key (get from platform.openai.com)
- ✅ Git installed locally

## Step 1: Prepare Your Repository

### 1.1 Create a new repository on GitHub

```bash
# Go to github.com and create a new repository named "ai-research-companion"
```

### 1.2 Initialize and push your code

```bash
# Navigate to your project directory
cd vercel-research-app

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Vercel-ready AI Research Companion"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/ai-research-companion.git

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard (Easiest)

1. **Go to Vercel**
   - Visit https://vercel.com
   - Click "Login" and sign in with GitHub

2. **Create New Project**
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Find your `ai-research-companion` repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

4. **Add Environment Variables**
   
   Click "Environment Variables" and add:
   
   | Name | Value |
   |------|-------|
   | `OPENAI_API_KEY` | Your OpenAI API key (from platform.openai.com) |
   | `OPENAI_MODEL` | `gpt-4o-mini` |
   | `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` |

   **Important**: Select "Production", "Preview", and "Development" for all variables

5. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes for build to complete
   - Your app will be live at `https://your-project-name.vercel.app`

### Option B: Via Vercel CLI (For Advanced Users)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Link Project**
```bash
cd vercel-research-app
vercel link
```

4. **Add Environment Variables**
```bash
# Add production environment variables
vercel env add OPENAI_API_KEY production
# Paste your OpenAI API key when prompted

vercel env add OPENAI_MODEL production
# Enter: gpt-4o-mini

vercel env add EMBEDDING_MODEL production
# Enter: all-MiniLM-L6-v2

# Repeat for preview and development environments
vercel env add OPENAI_API_KEY preview
vercel env add OPENAI_MODEL preview
vercel env add EMBEDDING_MODEL preview
```

5. **Deploy**
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Step 3: Verify Deployment

### 3.1 Test the Application

1. Visit your deployment URL
2. Enter a test query: "transformer models for NLP"
3. Click "Run Analysis"
4. Verify all steps complete successfully

### 3.2 Check API Endpoints

Test each endpoint individually:

```bash
# Health check
curl https://your-project-name.vercel.app/api/health

# Retrieve papers (example)
curl -X POST https://your-project-name.vercel.app/api/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 3}'
```

## Step 4: Monitor and Debug

### 4.1 View Logs

In Vercel Dashboard:
- Go to your project
- Click "Deployments"
- Click on a deployment
- Click "Runtime Logs" to see API logs

### 4.2 Check Build Logs

If deployment fails:
- Check "Build Logs" in the deployment details
- Look for Python or Node.js errors
- Common issues:
  - Missing environment variables
  - Package installation failures
  - Import errors

### 4.3 Function Errors

For runtime errors:
- Check "Functions" tab in project settings
- View invocation logs
- Look for timeout or memory issues

## Step 5: Custom Domain (Optional)

### 5.1 Add Custom Domain

1. Go to Project Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., `research.yourdomain.com`)
4. Follow DNS configuration instructions
5. Wait for SSL certificate provisioning (automatic)

### 5.2 Verify Domain

```bash
curl https://research.yourdomain.com/api/health
```

## Common Issues and Solutions

### Issue 1: "Missing OPENAI_API_KEY"

**Solution:**
1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Add `OPENAI_API_KEY` with your key
3. Redeploy (or trigger automatic redeploy by pushing to GitHub)

### Issue 2: Function Timeout

**Error:** `Function execution timed out`

**Solution:**
- Vercel free tier has 10-second timeout
- Reduce number of papers (use 3-4 instead of 6-8)
- Upgrade to Pro plan for 60-second timeout

### Issue 3: Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
1. Ensure `requirements.txt` includes all dependencies
2. Check Python version compatibility
3. Try redeploying with cache cleared:
   ```bash
   vercel --force
   ```

### Issue 4: NLTK Data Not Found

**Error:** `Resource punkt not found`

**Solution:**
- The code automatically downloads NLTK data
- If it persists, check function logs
- May need to increase memory limit (Pro plan)

### Issue 5: Sentence Transformers Memory Error

**Error:** `Out of memory` or `Killed`

**Solution:**
- Use lighter model: `all-MiniLM-L6-v2` (already configured)
- Reduce batch sizes in code
- Consider upgrading to Pro plan (more memory)

### Issue 6: CORS Errors

**Error:** `No 'Access-Control-Allow-Origin' header`

**Solution:**
- Already handled by `flask-cors` in API files
- If issues persist, check `vercel.json` routing
- Ensure requests go to correct API paths

## Performance Optimization

### 1. Enable Edge Caching

Add to `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=60, stale-while-revalidate"
        }
      ]
    }
  ]
}
```

### 2. Use Edge Functions (Pro Plan)

For faster global performance:
- Upgrade to Vercel Pro
- Enable Edge Functions for API routes
- Deploy to multiple regions

### 3. Optimize Dependencies

Reduce cold start times:
```bash
# Remove unused dependencies
# Use lighter alternatives where possible
# Consider lambda layers for large packages
```

## Security Best Practices

### 1. Secure API Keys

- ✅ Never commit `.env` files to Git
- ✅ Use Vercel environment variables
- ✅ Rotate API keys regularly
- ✅ Set up key usage alerts in OpenAI dashboard

### 2. Rate Limiting

Add rate limiting to prevent abuse:
```typescript
// Consider using Vercel's Edge Middleware
// Or Upstash Redis for rate limiting
```

### 3. Input Validation

Already implemented in API endpoints:
- Query length limits
- Parameter validation
- Error handling

## Monitoring and Analytics

### 1. Vercel Analytics

Enable in Project Settings:
- Real-time visitor data
- Performance metrics
- Page views and unique visitors

### 2. OpenAI Usage Monitoring

Track API costs:
- Visit platform.openai.com/usage
- Set up billing alerts
- Monitor token consumption

### 3. Error Tracking

Consider integrating:
- Sentry for error tracking
- LogRocket for session replay
- Custom logging solution

## Scaling Considerations

### Free Tier Limits
- 100 GB bandwidth/month
- 100 hours serverless execution
- 10s function timeout
- 1024 MB function memory

### Pro Tier ($20/month)
- 1 TB bandwidth/month
- 1000 hours serverless execution
- 60s function timeout
- 3008 MB function memory
- Team collaboration
- Custom domains

### When to Upgrade
- High traffic (>1000 requests/day)
- Long-running functions (>10s)
- Large model requirements
- Need for team features

## Maintenance

### Regular Updates

```bash
# Update dependencies monthly
npm update
pip list --outdated

# Update Next.js
npm install next@latest react@latest react-dom@latest

# Update Python packages
pip install --upgrade openai sentence-transformers
```

### Monitor Costs

- Check Vercel usage dashboard
- Monitor OpenAI API costs
- Set up budget alerts

### Backup Strategy

- GitHub is your backup
- Export environment variables
- Document custom configurations

## Next Steps

1. ✅ Deploy successfully
2. ✅ Test all features
3. 📊 Set up analytics
4. 🔒 Review security
5. 📈 Monitor performance
6. 🎨 Customize UI (optional)
7. 🚀 Share with users!

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Vercel Community**: https://github.com/vercel/vercel/discussions

## Troubleshooting Checklist

If something doesn't work:

- [ ] Environment variables set correctly?
- [ ] All dependencies in `requirements.txt` and `package.json`?
- [ ] API endpoints returning 200 status?
- [ ] OpenAI API key valid and has credits?
- [ ] Build completed successfully?
- [ ] Function logs show no errors?
- [ ] Browser console shows no errors?

## Conclusion

You now have a fully deployed AI Research Companion on Vercel! 🎉

Your app is:
- ✅ Globally distributed via CDN
- ✅ Automatically scaled
- ✅ HTTPS secured
- ✅ Continuously deployed from Git
- ✅ Production-ready

Enjoy your research companion and happy coding! 🔬✨
