export interface RepositoryIdentity {
  name: string;
  description: string;
  primary_language: string;
  stars?: number;
  forks?: number;
  created_at?: string;
  updated_at?: string;
  owner?: string;
  license?: string;
}

export interface Architecture {
  primary: string;
  types: string[];
  layers: string[];
}

export interface CodeStructure {
  total_functions: number;
  total_classes: number;
}

export interface DependenciesSummary {
  directly_used: string[];
  imported_but_undeclared: string[];
  external_library_count: number;
}

export interface ImportantFileDetail {
  path: string;
  structural_score: number;
  category: string;
  functions: string[];
  classes: string[];
  imports: string[];
}

export interface InternalDependency {
  source: string;
  target: string;
  import: string;
}

export interface RepositorySummary {
  repository_identity: RepositoryIdentity;
  architecture: Architecture;
  code_structure: CodeStructure;
  dependencies: DependenciesSummary;
  entry_points: string[];
  important_files: {
    path: string;
    structural_score: number;
  }[];
  languages_by_file_count: Record<string, number>;
  file_categories: Record<string, number>;
}

export interface ExecutionFlowStep {
  source: string;
  target: string;
  relationship: string;
  starts_from_entry_point: boolean;
}

export interface AISummaryImportantFile {
  path: string;
  reason: string;
}

export interface AISummary {
  overview: string;
  purpose: string;
  architecture_explanation: string;
  execution_flow: string[] | ExecutionFlowStep[];
  important_files: AISummaryImportantFile[];
  dependency_explanation: string;
  strengths: string[];
  potential_improvements: string[];
}

export interface TrainingQuality {
  passed: boolean;
  score?: number;
  metrics?: Record<string, number>;
}

export interface AnalysisResult {
  status: string;
  repository: string;
  repository_summary: RepositorySummary;
  target_output: AISummary;  // Keeps target_output required to prevent type check warnings
  ai_summary?: string;       // Represents the raw markdown AI Summary output (optional)
  analysis_id?: string;      // Represents the unique analysis UUID
  important_file_details?: ImportantFileDetail[];
  internal_dependencies?: InternalDependency[];
  training_quality?: TrainingQuality;
  dataset_save_result?: any;
}

export interface AnalysisHistoryItem {
  id: string;
  repositoryUrl: string;
  name: string;
  owner: string;
  date: string;
  language: string;
  architecture: string;
  score: number;
  status: 'completed' | 'failed' | 'processing';
  result?: AnalysisResult;
}

export interface UserProfile {
  name: string;
  email: string;
  avatarUrl?: string;
  analysesCompleted: number;
  repositoriesAnalyzedCount: number;
  favoriteLanguages: string[];
  joinedDate: string;
}
