import { Loader2, Sparkles } from 'lucide-react'

interface Props {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  loading: boolean
}

const PLACEHOLDER = `As a Returning Customer,
I want to log in using my email/phone number and password,
So that I can access my account, order history, and personalized recommendations.

Acceptance Criteria
AC 1: The login page must have distinct input fields for "Email or mobile phone number" and "Password".
AC 2: The "Continue" button should remain disabled or trigger an inline validation error if the identifier field is empty.
AC 3: ...`

export function UserStoryInput({ value, onChange, onSubmit, loading }: Props) {
  return (
    <div className="flex flex-col gap-3">
      <label htmlFor="user-story" className="text-sm font-medium text-slate-700 dark:text-slate-200">
        Paste a user story with acceptance criteria
      </label>
      <textarea
        id="user-story"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={PLACEHOLDER}
        rows={14}
        className="w-full rounded-lg border border-slate-300 bg-white p-3 font-mono text-sm text-slate-900 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
      />
      <button
        onClick={onSubmit}
        disabled={loading || value.trim().length < 20}
        className="inline-flex w-fit items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
        {loading ? 'Generating…' : 'Generate Test Cases'}
      </button>
    </div>
  )
}
