import { Download } from 'lucide-react'

import type { TestCase } from '../lib/types'

interface Props {
  testCases: TestCase[]
}

function downloadFile(filename: string, contents: string, mimeType: string) {
  const blob = new Blob([contents], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

function toCsv(testCases: TestCase[]): string {
  const header = ['id', 'scenario', 'preconditions', 'steps', 'expected_result', 'type']
  const escape = (value: string) => `"${value.replace(/"/g, '""')}"`
  const rows = testCases.map((tc) =>
    [tc.id, tc.scenario, tc.preconditions, tc.steps.join(' | '), tc.expected_result, tc.type]
      .map(escape)
      .join(','),
  )
  return [header.join(','), ...rows].join('\n')
}

export function ExportButton({ testCases }: Props) {
  return (
    <div className="flex gap-2">
      <button
        onClick={() => downloadFile('test-cases.csv', toCsv(testCases), 'text/csv')}
        className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
      >
        <Download className="h-3.5 w-3.5" /> CSV
      </button>
      <button
        onClick={() =>
          downloadFile('test-cases.json', JSON.stringify({ test_cases: testCases }, null, 2), 'application/json')
        }
        className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
      >
        <Download className="h-3.5 w-3.5" /> JSON
      </button>
    </div>
  )
}
