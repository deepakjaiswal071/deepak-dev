import type { TestCase, TestCaseType } from '../lib/types'
import { ExportButton } from './ExportButton'

interface Props {
  testCases: TestCase[]
}

const TYPE_STYLES: Record<TestCaseType, string> = {
  Positive: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  Negative: 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300',
  Boundary: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
}

export function TestCaseResults({ testCases }: Props) {
  if (testCases.length === 0) return null

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          {testCases.length} Test Case{testCases.length === 1 ? '' : 's'}
        </h2>
        <ExportButton testCases={testCases} />
      </div>
      <div className="flex flex-col gap-3">
        {testCases.map((tc) => (
          <article
            key={tc.id}
            className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <div className="mb-2 flex items-center gap-2">
              <span className="font-mono text-xs text-slate-500 dark:text-slate-400">{tc.id}</span>
              <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${TYPE_STYLES[tc.type]}`}>
                {tc.type}
              </span>
            </div>
            <p className="font-medium text-slate-900 dark:text-slate-100">{tc.scenario}</p>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              <span className="font-semibold">Preconditions:</span> {tc.preconditions}
            </p>
            <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm text-slate-700 dark:text-slate-300">
              {tc.steps.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ol>
            <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">
              <span className="font-semibold">Expected result:</span> {tc.expected_result}
            </p>
          </article>
        ))}
      </div>
    </div>
  )
}
