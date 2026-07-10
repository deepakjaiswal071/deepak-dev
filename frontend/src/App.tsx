import { useState } from 'react'

import { ErrorBanner } from './components/ErrorBanner'
import { TestCaseResults } from './components/TestCaseResults'
import { UserStoryInput } from './components/UserStoryInput'
import { ApiError, generateTestCases } from './lib/api'
import type { TestCase } from './lib/types'

export default function App() {
  const [story, setStory] = useState('')
  const [testCases, setTestCases] = useState<TestCase[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await generateTestCases(story)
      setTestCases(result.test_cases)
    } catch (err) {
      setTestCases([])
      setError(err instanceof ApiError ? err.message : 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto min-h-screen max-w-3xl px-4 py-10">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">AI Test Case Generator</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Paste a user story with acceptance criteria to get Positive, Negative, and Boundary test cases.
        </p>
      </header>

      <div className="flex flex-col gap-6">
        <UserStoryInput value={story} onChange={setStory} onSubmit={handleSubmit} loading={loading} />
        {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
        <TestCaseResults testCases={testCases} />
      </div>
    </div>
  )
}
