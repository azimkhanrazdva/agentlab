export type Trace = {
  id: string;
  session_id: string | null;
  name: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  metadata: Record<string, unknown>;
};

export type Span = {
  id: string;
  type: string;
  name: string;
  status: string;
  duration_ms: number | null;
  input: Record<string, unknown>;
  output: Record<string, unknown>;
  token_usage: Record<string, number>;
  model: string | null;
  provider: string | null;
  risk_score: number | null;
};

export type TraceDetail = {
  trace: Trace;
  spans: Span[];
  events: Array<{ id: string; type: string; payload: Record<string, unknown>; created_at: string }>;
};

export const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function getTraces(): Promise<Trace[]> {
  const res = await fetch(`${apiBase}/api/v1/traces`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function getTrace(id: string): Promise<TraceDetail | null> {
  const res = await fetch(`${apiBase}/api/v1/traces/${id}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

