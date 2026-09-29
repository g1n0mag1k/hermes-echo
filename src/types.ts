// Echo Probe — an executable question
export interface EchoProbe {
  args: string[]
  confidence: number
  source: 'baseline' | 'fixture' | 'readme' | 'test'
}

// Echo Observation — the immutable answer
export interface EchoObservation {
  probe: EchoProbe
  exitCode: number | null
  stdout: string
  stderr: string
  stdoutNormalized: string
  stderrNormalized: string
  timedOut: boolean
  skipped: boolean
  skipReason?: string
  durationMs: number
  environment: {
    python?: string
    platform: string
    commit: string
    timestamp: string
  }
}

// Echo Contract — an accepted behavioral statement
export interface EchoContract {
  version: 1
  probe: {
    command: string
    args: string[]
  }
  environment: {
    python?: string
    platform: string
  }
  accepted: {
    exit_code: number
    stdout: string
    stderr_contains: string[]
  }
  normalization: {
    version: number
  }
  accepted_at: string
  accepted_by: string
  commit: string
  note: string
  signing: {
    signed: false
    signature: null
    public_key: null
  }
}

// Echo Receipt — a verifiable record
export interface EchoReceipt {
  id: string
  probe: EchoProbe
  observation: EchoObservation
  contract?: EchoContract
  classification:
    | 'unchanged'
    | 'possible_change'
    | 'contract_violation'
    | 'skipped'
    | 'timed_out'
  generatedAt: string
}

// The two emotional outcomes
export type EchoOutcome = 'ECHO VERIFIED' | 'ECHO DETECTED A CHANGE'
