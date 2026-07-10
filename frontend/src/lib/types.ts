export type TestCaseType = 'Positive' | 'Negative' | 'Boundary'

export interface TestCase {
  id: string
  scenario: string
  preconditions: string
  steps: string[]
  expected_result: string
  type: TestCaseType
}

export interface TestCaseCollection {
  test_cases: TestCase[]
}
