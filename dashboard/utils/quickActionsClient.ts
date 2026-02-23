/**
 * Quick Actions API Client
 * Frontend TypeScript client for FastAPI endpoints under /api/quick-actions
 */
export type ActionResult = {
  success: boolean;
  message: string;
  data?: any;
  execution_time: number;
  timestamp: string;
};

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

async function get<T>(path: string): Promise<T> {
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (API_KEY) headers['X-API-Key'] = API_KEY;

  const res = await fetch(`${BASE_URL}${path}`, { method: 'GET', headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (API_KEY) headers['X-API-Key'] = API_KEY;

  // Best-effort Idempotency-Key
  let idKey = '';
  try {
    const anyCrypto = (globalThis as any).crypto;
    idKey = anyCrypto && typeof anyCrypto.randomUUID === 'function'
      ? anyCrypto.randomUUID()
      : `${Date.now()}-${Math.random()}`;
  } catch {
    idKey = `${Date.now()}-${Math.random()}`;
  }
  headers['Idempotency-Key'] = idKey;

  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

export const QuickActionsAPI = {
  createSprint: (params: {
    business_id: string;
    sprint_duration?: number;
    ai_generate_tasks?: boolean;
    focus_areas?: string[];
  }) => post<ActionResult>('/api/quick-actions/create-sprint', params),

  investorUpdate: (params: {
    business_id: string;
    period?: string;
    include_financials?: boolean;
    include_metrics?: boolean;
    auto_send?: boolean;
    recipient_list?: string[];
  }) => post<ActionResult>('/api/quick-actions/investor-update', params),

  deployFeature: (params: {
    business_id: string;
    environment?: string;
    run_tests?: boolean;
    auto_promote?: boolean;
    features?: string[];
  }) => post<ActionResult>('/api/quick-actions/deploy-feature', params),

  teamCheckin: (params: {
    business_id: string;
    include_mood?: boolean;
    include_blockers?: boolean;
    generate_summary?: boolean;
  }) => post<ActionResult>('/api/quick-actions/team-checkin', params),

  // Synchronous report (default)
  generateReport: (params: {
    business_id: string;
    report_type?: string;
    include_predictions?: boolean;
    include_recommendations?: boolean;
    time_period?: string;
  }) => post<ActionResult>('/api/quick-actions/generate-report', params),

  // Asynchronous report: returns { task_id, status } with HTTP 202
  generateReportAsync: (params: {
    business_id: string;
    report_type?: string;
    include_predictions?: boolean;
    include_recommendations?: boolean;
    time_period?: string;
  }) => post<{ task_id: string; status: string }>('/api/quick-actions/generate-report', { ...params, async_mode: true }),

  // Poll background task status
  getTaskStatus: (taskId: string) => get<any>(`/api/quick-actions/tasks/${taskId}`),
};