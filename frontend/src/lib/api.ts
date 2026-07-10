import type { TestCaseCollection } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export class ApiError extends Error {}

export async function generateTestCases(userStory: string): Promise<TestCaseCollection> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}/api/generate-test-cases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_story: userStory }),
    })
  } catch {
    throw new ApiError('Could not reach the backend. Is it running?')
  }

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`
    try {
      const body = await response.json()
      if (typeof body.detail === 'string') detail = body.detail
    } catch {
      // response body wasn't JSON; fall back to the default detail message
    }
    throw new ApiError(detail)
  }

  return response.json() as Promise<TestCaseCollection>
}
