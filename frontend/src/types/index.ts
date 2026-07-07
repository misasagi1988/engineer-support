export interface User { id: string; username: string; email: string; role: string }
export interface Ticket {
  id: string; title: string; description: string; status: string; priority: string;
  module_id: string | null; version_id: string | null; deploy_mode: string | null;
  customer_id: string | null; deployment_id: string | null; source: string;
  assignee_id: string | null; created_at: string; resolved_at: string | null;
  updated_at: string; identified_root_cause: string; solution: string;
  troubleshooting_checklist: any[]; auto_identified: boolean;
}
export interface Case {
  id: string; title: string; module_id: string; deploy_mode: string | null;
  root_cause: string; solution: string; tags: string[]; confidence_score: number;
  review_status: string; ticket_id: string; customer_id: string | null;
  created_by: string; created_at: string; updated_at: string; troubleshooting_path: any[];
}
export interface Customer { id: string; name: string; contract_level: string; contact_info: string }
export interface Deployment {
  id: string; name: string; deploy_mode: string; environment: string;
  customer_id: string; version_id: string | null; config_summary: Record<string, any>;
}
export interface Module { id: string; name: string; description: string }
export interface Version { id: string; name: string; is_active: boolean; release_date: string | null }
export interface AILocateResult {
  module_candidates: Array<{module: string; confidence: number}>;
  version_candidates: Array<{version: string; confidence: number}>;
  deploy_mode_hints: string | null;
  root_cause_candidates: Array<{description: string; keywords: string[]; confidence: number}>;
  similar_cases: Array<{id: string; title: string; module_id: string; deploy_mode: string | null; root_cause: string; solution: string; confidence_score: number}>;
  troubleshooting_path: Array<{id: string; title: string; description: string; order: number}>;
}
