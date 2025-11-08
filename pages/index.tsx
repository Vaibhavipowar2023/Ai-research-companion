import { useState } from 'react'
import Head from 'next/head'
import axios from 'axios'

interface Paper {
  title: string
  authors: string[]
  abstract: string
  link: string
  source: string
  score?: number
}

interface Summary {
  title: string
  authors: string[]
  link: string
  source: string
  extractive: string
  abstractive: string
}

interface Insights {
  themes: string[]
  pros: string[]
  cons: string[]
  gaps: string[]
  raw: string
}

export default function Home() {
  const [query, setQuery] = useState('')
  const [numPapers, setNumPapers] = useState(4)
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [progressText, setProgressText] = useState('')
  const [papers, setPapers] = useState<Paper[]>([])
  const [summaries, setSummaries] = useState<Summary[]>([])
  const [insights, setInsights] = useState<Insights | null>(null)
  const [plan, setPlan] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('')
    setPapers([])
    setSummaries([])
    setInsights(null)
    setPlan('')
    setProgress(0)

    try {
      // Step 1: Retrieve papers
      setProgressText('Retrieving papers...')
      setProgress(10)
      
      const retrieveResponse = await axios.post('/api/retrieve', {
        query,
        top_k: numPapers
      })

      const retrievedPapers = retrieveResponse.data.papers || []
      setPapers(retrievedPapers)

      if (retrievedPapers.length === 0) {
        setError('No papers found. Try a different query.')
        setLoading(false)
        return
      }

      // Step 2: Summarize papers
      setProgressText('Generating summaries...')
      setProgress(30)
      
      const summarizeResponse = await axios.post('/api/summarize', {
        papers: retrievedPapers
      })

      const generatedSummaries = summarizeResponse.data.summaries || []
      setSummaries(generatedSummaries)
      setProgress(60)

      // Step 3: Synthesize insights
      setProgressText('Synthesizing insights...')
      
      const summaryTexts = generatedSummaries.map(
        (s: Summary) => s.abstractive || s.extractive || ''
      )

      const insightsResponse = await axios.post('/api/insights', {
        summaries: summaryTexts
      })

      const generatedInsights = insightsResponse.data
      setInsights(generatedInsights)
      setProgress(80)

      // Step 4: Generate research plan
      setProgressText('Drafting research plan...')
      
      const planResponse = await axios.post('/api/plan', {
        insights: generatedInsights.raw || JSON.stringify(generatedInsights),
        topic: query
      })

      const generatedPlan = planResponse.data.plan || ''
      setPlan(generatedPlan)
      setProgress(100)
      setProgressText('Done!')

    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'An error occurred')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const downloadText = (content: string, filename: string) => {
    try {
      // Validate content
      if (!content || content.trim() === '') {
        alert('No content to download. Please run an analysis first.')
        return
      }

      // Create blob with UTF-8 encoding
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      
      // Create temporary link
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      a.style.display = 'none'
      
      // Append, click, and cleanup
      document.body.appendChild(a)
      a.click()
      
      // Cleanup after a short delay to ensure download starts
      setTimeout(() => {
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      }, 100)
    } catch (error) {
      console.error('Download error:', error)
      alert('Failed to download file. Please try copying the text manually.')
    }
  }

  const copyToClipboard = async (content: string) => {
    try {
      if (!content || content.trim() === '') {
        alert('No content to copy.')
        return
      }

      if (navigator.clipboard && window.isSecureContext) {
        // Modern async clipboard API
        await navigator.clipboard.writeText(content)
        alert('Copied to clipboard!')
      } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea')
        textArea.value = content
        textArea.style.position = 'fixed'
        textArea.style.left = '-999999px'
        textArea.style.top = '-999999px'
        document.body.appendChild(textArea)
        textArea.focus()
        textArea.select()
        
        try {
          document.execCommand('copy')
          alert('Copied to clipboard!')
        } catch (err) {
          console.error('Fallback copy failed:', err)
          alert('Could not copy to clipboard. Please select and copy manually.')
        }
        
        document.body.removeChild(textArea)
      }
    } catch (error) {
      console.error('Copy error:', error)
      alert('Failed to copy. Please select and copy manually.')
    }
  }

  return (
    <>
      <Head>
        <title>AI Research Companion</title>
        <meta name="description" content="Find, summarize, and synthesize research papers" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🔬 AI Research Companion
            </h1>
            <p className="text-gray-600">
              Find, summarize, synthesize — then turn it into a concrete plan.
            </p>
          </div>

          {/* Search Form */}
          <div className="max-w-2xl mx-auto mb-12">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                  Research Question or Topic
                </label>
                <input
                  type="text"
                  id="query"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., transformer models for protein folding"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={loading}
                />
              </div>

              <div>
                <label htmlFor="numPapers" className="block text-sm font-medium text-gray-700 mb-2">
                  Number of papers to analyze: {numPapers}
                </label>
                <input
                  type="range"
                  id="numPapers"
                  min="2"
                  max="8"
                  value={numPapers}
                  onChange={(e) => setNumPapers(parseInt(e.target.value))}
                  className="w-full"
                  disabled={loading}
                />
              </div>

              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Processing...' : 'Run Analysis'}
              </button>
            </form>

            {/* Progress Bar */}
            {loading && (
              <div className="mt-6">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>{progressText}</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}
          </div>

          {/* Results Section */}
          {summaries.length > 0 && (
            <div className="space-y-12">
              {/* Papers and Summaries */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">📚 Top Papers</h2>
                <div className="grid gap-4">
                  {summaries.map((summary, idx) => (
                    <div key={idx} className="card bg-white">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="text-lg font-semibold text-gray-900 flex-1">
                          {idx + 1}. {summary.title}
                        </h3>
                        <div className="flex gap-2 ml-4">
                          <span className="badge bg-blue-50 text-blue-700 border-blue-200">
                            {summary.source}
                          </span>
                          {papers[idx]?.score && (
                            <span className="badge bg-gray-50 text-gray-700 border-gray-200">
                              {papers[idx].score.toFixed(3)}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      {summary.link && (
                        <a
                          href={summary.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline text-sm mb-3 inline-block"
                        >
                          Open paper →
                        </a>
                      )}
                      
                      <p className="text-gray-700 leading-relaxed">
                        {summary.abstractive || summary.extractive}
                      </p>
                    </div>
                  ))}
                </div>
              </section>

              {/* Insights */}
              {insights && (
                <section>
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">💡 Synthesized Insights</h2>
                  
                  <div className="grid md:grid-cols-4 gap-4 mb-6">
                    <div className="card bg-purple-50">
                      <h3 className="font-semibold text-purple-900 mb-3">Themes</h3>
                      <ul className="space-y-2">
                        {insights.themes.map((theme, idx) => (
                          <li key={idx} className="text-sm text-purple-800">• {theme}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="card bg-green-50">
                      <h3 className="font-semibold text-green-900 mb-3">Pros</h3>
                      <ul className="space-y-2">
                        {insights.pros.map((pro, idx) => (
                          <li key={idx} className="text-sm text-green-800">+ {pro}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="card bg-red-50">
                      <h3 className="font-semibold text-red-900 mb-3">Cons</h3>
                      <ul className="space-y-2">
                        {insights.cons.map((con, idx) => (
                          <li key={idx} className="text-sm text-red-800">− {con}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="card bg-yellow-50">
                      <h3 className="font-semibold text-yellow-900 mb-3">Gaps</h3>
                      <ul className="space-y-2">
                        {insights.gaps.map((gap, idx) => (
                          <li key={idx} className="text-sm text-yellow-800">? {gap}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="card bg-white">
                    <div className="flex justify-between items-center mb-3">
                      <h3 className="font-semibold text-gray-900">Raw (copyable)</h3>
                      <div className="flex gap-2">
                        <button
                          onClick={() => copyToClipboard(insights.raw)}
                          className="text-sm px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded transition-colors"
                          title="Copy to clipboard"
                        >
                          📋 Copy
                        </button>
                        <button
                          onClick={() => downloadText(insights.raw, 'insights.txt')}
                          className="text-sm px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                          title="Download as text file"
                        >
                          ⬇️ Download
                        </button>
                      </div>
                    </div>
                    <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono bg-gray-50 p-4 rounded-lg overflow-x-auto">
                      {insights.raw}
                    </pre>
                  </div>
                </section>
              )}

              {/* Research Plan */}
              {plan && (
                <section>
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">🗺️ Research Plan</h2>
                  <div className="card bg-white">
                    <div className="flex justify-end gap-2 mb-4">
                      <button
                        onClick={() => copyToClipboard(plan)}
                        className="text-sm px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded transition-colors"
                        title="Copy to clipboard"
                      >
                        📋 Copy
                      </button>
                      <button
                        onClick={() => downloadText(plan, 'research_plan.txt')}
                        className="text-sm px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                        title="Download as text file"
                      >
                        ⬇️ Download
                      </button>
                    </div>
                    <div 
                      className="prose prose-sm max-w-none text-gray-700"
                      dangerouslySetInnerHTML={{ __html: plan.replace(/\n/g, '<br />') }}
                    />
                  </div>
                </section>
              )}
            </div>
          )}
        </div>
      </main>
    </>
  )
}
