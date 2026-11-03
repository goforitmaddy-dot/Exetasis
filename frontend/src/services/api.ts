import {
  AgentEvaluationResult,
  AgentMetadata,
  DigitalTwinSnapshot,
  WorkplaceEvent,
  WorkplaceSummary,
} from "../types";

const BASE_URL = "/api";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API Error [${res.status}]: ${errorText || res.statusText}`);
  }

  return res.json() as Promise<T>;
}

export const api = {
  getHealth: () => request<{ status: string; app_name: string; database: string }>("/health"),

  getSummary: () => request<WorkplaceSummary>("/analytics/summary"),

  getDigitalTwinState: () => request<DigitalTwinSnapshot>("/digital-twin/state"),

  getAgents: () => request<AgentMetadata[]>("/agents"),

  evaluateAgent: (agentId: string, targetId: string, context: Record<string, unknown> = {}) =>
    request<AgentEvaluationResult>(`/agents/${agentId}/evaluate`, {
      method: "POST",
      body: JSON.stringify({ target_id: targetId, context }),
    }),

  runOrchestration: (targetId: string, eventIds: string[] = [], parameters: Record<string, unknown> = {}) =>
    request<{
      run_id: string;
      target_id: string;
      status: string;
      agent_results: Record<string, AgentEvaluationResult>;
      overall_score: number;
      summary: string;
    }>("/orchestration/run", {
      method: "POST",
      body: JSON.stringify({ target_id: targetId, event_ids: eventIds, parameters }),
    }),

  getEvents: (limit: number = 20, offset: number = 0) =>
    request<WorkplaceEvent[]>(`/events?limit=${limit}&offset=${offset}`),

  ingestEvent: (event: { source: string; event_type: string; employee_id?: string; payload: Record<string, unknown> }) =>
    request<WorkplaceEvent>("/events/ingest", {
      method: "POST",
      body: JSON.stringify(event),
    }),
};
