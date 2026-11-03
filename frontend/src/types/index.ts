export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export type TwinNodeType = "desk" | "meeting_room" | "breakout_zone" | "employee_avatar";
export type TwinNodeStatus = "idle" | "active" | "collaborating" | "alert" | "focused";

export interface DigitalTwinNode {
  id: string;
  node_type: TwinNodeType;
  label: string;
  position: Vector3D;
  status: TwinNodeStatus;
  state_metadata: Record<string, unknown>;
  updated_at?: string;
}

export interface ZoneClusterData {
  id: string;
  name: string;
  color: string;
  bounds: {
    min_x: number;
    max_x: number;
    min_z: number;
    max_z: number;
  };
}

export interface DigitalTwinSnapshot {
  office_name: string;
  grid_size: Vector3D;
  nodes: DigitalTwinNode[];
  zones: ZoneClusterData[];
  timestamp: string;
}

export interface AgentMetadata {
  agent_id: string;
  name: string;
  description: string;
  capabilities: string[];
  is_active: boolean;
}

export interface AgentEvaluationResult {
  agent_id: string;
  target_id: string;
  score: number;
  rationale: string;
  findings: string[];
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface DepartmentScore {
  department: string;
  headcount: number;
  activity_score: number;
  fairness_score: number;
  culture_health: number;
}

export interface WorkplaceSummary {
  workplace_score: number;
  total_employees: number;
  total_events_processed: number;
  average_fairness_index: number;
  culture_vibe: string;
  department_scores: DepartmentScore[];
  recent_insights: string[];
  generated_at: string;
}

export interface WorkplaceEvent {
  id: string;
  source: string;
  event_type: string;
  employee_id?: string;
  payload: Record<string, unknown>;
  processed: boolean;
  created_at: string;
}
