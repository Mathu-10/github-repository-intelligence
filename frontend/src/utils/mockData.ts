import type { AnalysisResult, AnalysisHistoryItem, UserProfile } from '../types';

export const MOCK_USER: UserProfile = {
  name: "Sarah Jenkins",
  email: "s.jenkins@developer.io",
  analysesCompleted: 42,
  repositoriesAnalyzedCount: 18,
  favoriteLanguages: ["Python", "TypeScript", "Go"],
  joinedDate: "October 12, 2025"
};

export const MOCK_HISTORY: AnalysisHistoryItem[] = [
  {
    id: "hist-1",
    repositoryUrl: "https://github.com/Mathu-10/github-repository-intelligence",
    name: "github-repository-intelligence",
    owner: "Mathu-10",
    date: "2026-07-12",
    language: "Python",
    architecture: "Web API Backend (Layered Modular)",
    score: 94,
    status: "completed"
  },
  {
    id: "hist-2",
    repositoryUrl: "https://github.com/openai/openai-python",
    name: "openai-python",
    owner: "openai",
    date: "2026-07-11",
    language: "Python",
    architecture: "Client Library / SDK",
    score: 89,
    status: "completed"
  },
  {
    id: "hist-3",
    repositoryUrl: "https://github.com/pallets/flask",
    name: "flask",
    owner: "pallets",
    date: "2026-07-08",
    language: "Python",
    architecture: "Web Framework (Modular)",
    score: 92,
    status: "completed"
  },
  {
    id: "hist-4",
    repositoryUrl: "https://github.com/facebook/react",
    name: "react",
    owner: "facebook",
    date: "2026-07-05",
    language: "JavaScript",
    architecture: "UI Library (Component-based)",
    score: 96,
    status: "completed"
  }
];

export const MOCK_REPORTS: Record<string, AnalysisResult> = {
  "github-repository-intelligence": {
    status: "valid",
    repository: "github-repository-intelligence",
    repository_summary: {
      repository_identity: {
        name: "github-repository-intelligence",
        description: "An AI-powered system for analyzing, understanding, and explaining GitHub repositories using static code analysis and a fine-tuned code model.",
        primary_language: "Python",
        stars: 342,
        forks: 58,
        created_at: "2026-02-15T08:30:00Z",
        updated_at: "2026-07-12T12:00:00Z",
        owner: "Mathu-10",
        license: "MIT"
      },
      architecture: {
        primary: "Web API Backend",
        types: ["web_api_backend", "layered_modular"],
        layers: ["analysis", "api", "model", "repository"]
      },
      entry_points: ["backend/main.py"],
      important_files: [
        { path: "backend/app/api/repository_routes.py", structural_score: 300 },
        { path: "backend/app/repository/github_client.py", structural_score: 60 },
        { path: "backend/app/repository/content_fetcher.py", structural_score: 45 },
        { path: "backend/app/analysis/external_dependency_analyzer.py", structural_score: 30 },
        { path: "backend/app/analysis/structural_ranker.py", structural_score: 30 }
      ],
      languages_by_file_count: {
        "Python": 20,
        "JSON": 4,
        "Markdown": 2,
        "Config": 3
      },
      file_categories: {
        "source_code": 20,
        "dependency": 2,
        "configuration": 3,
        "other": 4
      },
      code_structure: {
        total_functions: 33,
        total_classes: 1
      },
      dependencies: {
        directly_used: ["python-dotenv", "fastapi", "pydantic", "requests", "uvicorn"],
        imported_but_undeclared: [],
        external_library_count: 5
      }
    },
    important_file_details: [
      {
        path: "backend/app/api/repository_routes.py",
        structural_score: 300,
        category: "source_code",
        functions: ["analyze_repository", "get_dataset_stats"],
        classes: ["RepositoryRequest"],
        imports: [
          "app.analysis.dependency_summary",
          "fastapi.APIRouter",
          "fastapi.HTTPException",
          "pydantic.BaseModel",
          "pydantic.HttpUrl",
          "app.repository.github_client.get_repository_metadata",
          "app.repository.github_client.get_repository_tree",
          "app.services.repository_analysis_service.analyze_repository_pipeline"
        ]
      },
      {
        path: "backend/app/repository/github_client.py",
        structural_score: 60,
        category: "source_code",
        functions: ["get_repository_metadata", "get_repository_tree", "get_file_content"],
        classes: [],
        imports: ["base64", "os", "requests", "dotenv.load_dotenv"]
      },
      {
        path: "backend/app/repository/content_fetcher.py",
        structural_score: 45,
        category: "source_code",
        functions: ["fetch_repository_contents"],
        classes: [],
        imports: ["app.repository.github_client.get_file_content"]
      },
      {
        path: "backend/app/analysis/external_dependency_analyzer.py",
        structural_score: 30,
        category: "source_code",
        functions: ["extract_root_module", "find_external_dependencies"],
        classes: [],
        imports: ["sys"]
      },
      {
        path: "backend/app/analysis/structural_ranker.py",
        structural_score: 30,
        category: "source_code",
        functions: ["calculate_structural_score", "rank_structurally_important_files"],
        classes: [],
        imports: []
      }
    ],
    internal_dependencies: [
      { source: "backend/main.py", target: "backend/app/api/repository_routes.py", import: "app.api.repository_routes.router" },
      { source: "backend/app/api/repository_routes.py", target: "backend/app/services/repository_analysis_service.py", import: "app.services.repository_analysis_service.analyze_repository_pipeline" },
      { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/repository/github_client.py", import: "app.repository.github_client" },
      { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/repository/content_fetcher.py", import: "app.repository.content_fetcher" },
      { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/analysis/structural_ranker.py", import: "app.analysis.structural_ranker" },
      { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/analysis/external_dependency_analyzer.py", import: "app.analysis.external_dependency_analyzer" }
    ],
    training_quality: {
      passed: true,
      score: 95,
      metrics: {
        "completeness": 98,
        "structural_fidelity": 94,
        "factual_accuracy": 96,
        "formatting": 92
      }
    },
    target_output: {
      overview: "github-repository-intelligence is a **FastAPI-based Python backend** that performs static and structural analysis on public GitHub repositories to build dataset training samples.",
      purpose: "The main goal of this repository is to analyze public repos, rank critical files by dependency importance, detect architectural types, and generate fine-tuning training records for AI code models.",
      architecture_explanation: "The codebase implements a clean **Layered Modular architecture**. It isolates repository connectors (`app/repository`) from processing algorithms (`app/analysis`), routes requests through an orchestration controller (`app/services`), and exposes them via FastAPI controller routing rules (`app/api`).",
      execution_flow: [
        { source: "Client Request", target: "backend/main.py (FastAPI App)", relationship: "HTTPS POST /analyze", starts_from_entry_point: true },
        { source: "backend/main.py (FastAPI App)", target: "backend/app/api/repository_routes.py", relationship: "Delegates endpoint routing", starts_from_entry_point: false },
        { source: "backend/app/api/repository_routes.py", target: "backend/app/services/repository_analysis_service.py", relationship: "Executes pipeline service", starts_from_entry_point: false },
        { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/repository/github_client.py", relationship: "Fetches GitHub file tree & content", starts_from_entry_point: false },
        { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/analysis/structural_ranker.py", relationship: "Computes file dependency scores", starts_from_entry_point: false },
        { source: "backend/app/services/repository_analysis_service.py", target: "backend/app/model/training_example_builder.py", relationship: "Wraps analysis in LLM prompt templates", starts_from_entry_point: false }
      ],
      important_files: [
        { path: "backend/app/api/repository_routes.py", reason: "Houses the FastAPI controllers. Handles incoming validation using Pydantic HttpUrl models and calls the orchestration pipeline." },
        { path: "backend/app/services/repository_analysis_service.py", reason: "The orchestrator of the repo analysis. Links tree filters, requirements parsing, file rankers, and target outputs." },
        { path: "backend/app/repository/github_client.py", reason: "Manages network requests to the GitHub REST API and parses Base64 payloads." },
        { path: "backend/app/analysis/structural_ranker.py", reason: "Implements page-rank style importance algorithms based on incoming and outgoing internal imports." }
      ],
      dependency_explanation: "The project directly imports **FastAPI** for web hosting, **Pydantic** for typed data verification, and **Requests** for querying GitHub's API. A `.env` file is loaded using **python-dotenv** to access GITHUB_TOKEN API headers.",
      strengths: [
        "Strong structural modularity with clear separation of analysis algorithms and networking layers.",
        "Automatic pipeline validation using a quality gate evaluation before saving examples.",
        "Strict input validation using pydantic models."
      ],
      potential_improvements: [
        "Support multi-threading or asynchronous fetches when downloading multiple source files.",
        "Add unit test coverage for file parsing utilities (`app/analysis/python_parser.py`).",
        "Implement code-complexity metrics beyond file ranks (e.g. cyclomatic complexity parsing)."
      ]
    }
  },
  "openai-python": {
    status: "valid",
    repository: "openai-python",
    repository_summary: {
      repository_identity: {
        name: "openai-python",
        description: "The official Python library for the OpenAI API, providing convenient access to assistants, chat completions, embeddings, and more.",
        primary_language: "Python",
        stars: 18500,
        forks: 3100,
        created_at: "2020-06-11T16:00:00Z",
        updated_at: "2026-07-12T14:45:00Z",
        owner: "openai",
        license: "Apache-2.0"
      },
      architecture: {
        primary: "Client SDK / Library",
        types: ["client_sdk", "object_oriented"],
        layers: ["resources", "client", "types", "http_transport"]
      },
      entry_points: ["src/openai/__init__.py"],
      important_files: [
        { path: "src/openai/_client.py", structural_score: 250 },
        { path: "src/openai/_base_client.py", structural_score: 190 },
        { path: "src/openai/resources/chat/completions.py", structural_score: 110 },
        { path: "src/openai/_models.py", structural_score: 95 }
      ],
      languages_by_file_count: {
        "Python": 142,
        "JSON": 2,
        "YAML": 5,
        "Markdown": 4
      },
      file_categories: {
        "source_code": 110,
        "dependency": 2,
        "test": 30,
        "configuration": 5,
        "other": 5
      },
      code_structure: {
        total_functions: 840,
        total_classes: 240
      },
      dependencies: {
        directly_used: ["httpx", "pydantic", "anyio", "distro", "typing-extensions"],
        imported_but_undeclared: [],
        external_library_count: 5
      }
    },
    important_file_details: [
      {
        path: "src/openai/_client.py",
        structural_score: 250,
        category: "source_code",
        functions: ["close", "request"],
        classes: ["OpenAI", "AsyncOpenAI"],
        imports: ["httpx", ".resources", "._base_client"]
      },
      {
        path: "src/openai/_base_client.py",
        structural_score: 190,
        category: "source_code",
        functions: ["_request", "_build_request", "auth_headers"],
        classes: ["SyncAPIClient", "AsyncAPIClient"],
        imports: ["httpx", "typing", "anyio"]
      },
      {
        path: "src/openai/resources/chat/completions.py",
        structural_score: 110,
        category: "source_code",
        functions: ["create"],
        classes: ["Completions", "AsyncCompletions"],
        imports: ["pydantic", "._models"]
      }
    ],
    internal_dependencies: [
      { source: "src/openai/__init__.py", target: "src/openai/_client.py", import: "OpenAI" },
      { source: "src/openai/_client.py", target: "src/openai/_base_client.py", import: "SyncAPIClient" },
      { source: "src/openai/_client.py", target: "src/openai/resources/chat/completions.py", import: "Completions" },
      { source: "src/openai/resources/chat/completions.py", target: "src/openai/_models.py", import: "BaseModel" }
    ],
    training_quality: {
      passed: true,
      score: 91,
      metrics: {
        "completeness": 94,
        "structural_fidelity: ": 88,
        "factual_accuracy": 92,
        "formatting": 90
      }
    },
    target_output: {
      overview: "openai-python is the official **Python SDK** developed by OpenAI, offering unified interfaces for HTTP REST API completions, streaming, and error handler routing.",
      purpose: "Designed to allow Python developers to quickly query OpenAI's LLMs via strongly-typed interfaces, automatic exponential retry strategies, sync/async threads, and clean payload schemas.",
      architecture_explanation: "The package utilizes a core **Object-Oriented Client SDK design**. Global entry points instantiate client objects (`OpenAI` or `AsyncOpenAI`), which inherit from a common transport driver client (`SyncAPIClient` or `AsyncAPIClient`). All model request categories are represented as child modular resources (e.g., `.chat.completions` or `.embeddings`).",
      execution_flow: [
        { source: "User Application", target: "src/openai/__init__.py (Client Instance)", relationship: "Instantiates client config", starts_from_entry_point: true },
        { source: "src/openai/__init__.py (Client Instance)", target: "src/openai/_client.py (OpenAI)", relationship: "Constructs resource nodes", starts_from_entry_point: false },
        { source: "src/openai/_client.py (OpenAI)", target: "src/openai/resources/chat/completions.py", relationship: "Executes .chat.completions.create()", starts_from_entry_point: false },
        { source: "src/openai/resources/chat/completions.py", target: "src/openai/_base_client.py", relationship: "Constructs HTTP request parameters", starts_from_entry_point: false },
        { source: "src/openai/_base_client.py", target: "HTTPX Client Transport", relationship: "Sends Request to api.openai.com", starts_from_entry_point: false }
      ],
      important_files: [
        { path: "src/openai/_client.py", reason: "Defines the main public client instance interfaces, grouping all API endpoints as sub-objects." },
        { path: "src/openai/_base_client.py", reason: "Houses generic HTTP request dispatching, authentication token parsing, backoff retries, and network configurations." },
        { path: "src/openai/resources/chat/completions.py", reason: "Contains the creation logic and types for chat conversations, which is the most widely used component of the SDK." }
      ],
      dependency_explanation: "The client abstracts raw transport by wrapping **HTTPX** for synchronous and asynchronous HTTP/2 request channels. It also leverages **Pydantic** v2 to enforce runtime request body layouts and JSON parse compliance.",
      strengths: [
        "Clean OOP structures mirroring API structures.",
        "Automatic retry middleware with exponential backoff.",
        "Comprehensive typing support for static IDE validations."
      ],
      potential_improvements: [
        "Reduce code bloat in auto-generated model validation bindings.",
        "Enable connection pooling controls in the base client instantiation options."
      ]
    }
  }
};

// Generates directory contents based on repository name for the TreeView component
export const getMockTreeStructure = (repoName: string) => {
  if (repoName.includes("github-repository-intelligence") || repoName === "default" || repoName === "") {
    return [
      { path: "backend", isDir: true, children: [
        { path: "backend/main.py", isDir: false },
        { path: "backend/requirements.txt", isDir: false },
        { path: "backend/.env", isDir: false },
        { path: "backend/app", isDir: true, children: [
          { path: "backend/app/__init__.py", isDir: false },
          { path: "backend/app/api", isDir: true, children: [
            { path: "backend/app/api/__init__.py", isDir: false },
            { path: "backend/app/api/repository_routes.py", isDir: false }
          ]},
          { path: "backend/app/repository", isDir: true, children: [
            { path: "backend/app/repository/__init__.py", isDir: false },
            { path: "backend/app/repository/github_client.py", isDir: false },
            { path: "backend/app/repository/content_fetcher.py", isDir: false }
          ]},
          { path: "backend/app/analysis", isDir: true, children: [
            { path: "backend/app/analysis/__init__.py", isDir: false },
            { path: "backend/app/analysis/file_filter.py", isDir: false },
            { path: "backend/app/analysis/file_ranker.py", isDir: false },
            { path: "backend/app/analysis/python_parser.py", isDir: false },
            { path: "backend/app/analysis/dependency_analyzer.py", isDir: false },
            { path: "backend/app/analysis/dependency_summary.py", isDir: false },
            { path: "backend/app/analysis/structural_ranker.py", isDir: false },
            { path: "backend/app/analysis/external_dependency_analyzer.py", isDir: false },
            { path: "backend/app/analysis/entry_point_detector.py", isDir: false },
            { path: "backend/app/analysis/architecture_analyzer.py", isDir: false },
            { path: "backend/app/analysis/dependency_comparator.py", isDir: false },
            { path: "backend/app/analysis/requirements_parser.py", isDir: false },
            { path: "backend/app/analysis/pyproject_parser.py", isDir: false },
            { path: "backend/app/analysis/repository_summarizer.py", isDir: false }
          ]},
          { path: "backend/app/services", isDir: true, children: [
            { path: "backend/app/services/__init__.py", isDir: false },
            { path: "backend/app/services/repository_analysis_service.py", isDir: false }
          ]},
          { path: "backend/app/model", isDir: true, children: [
            { path: "backend/app/model/__init__.py", isDir: false },
            { path: "backend/app/model/llm.py", isDir: false },
            { path: "backend/app/model/model_schema.py", isDir: false },
            { path: "backend/app/model/training_example_builder.py", isDir: false },
            { path: "backend/app/model/training_quality.py", isDir: false },
            { path: "backend/app/model/dataset_writer.py", isDir: false },
            { path: "backend/app/model/dataset_inspector.py", isDir: false }
          ]}
        ]}
      ]},
      { path: "frontend", isDir: true, children: [
        { path: "frontend/package.json", isDir: false },
        { path: "frontend/vite.config.ts", isDir: false },
        { path: "frontend/index.html", isDir: false },
        { path: "frontend/src", isDir: true, children: [
          { path: "frontend/src/main.tsx", isDir: false },
          { path: "frontend/src/App.tsx", isDir: false },
          { path: "frontend/src/index.css", isDir: false }
        ]}
      ]},
      { path: "README.md", isDir: false }
    ];
  } else {
    // Return a standard project layout
    return [
      { path: "src", isDir: true, children: [
        { path: "src/openai", isDir: true, children: [
          { path: "src/openai/__init__.py", isDir: false },
          { path: "src/openai/_client.py", isDir: false },
          { path: "src/openai/_base_client.py", isDir: false },
          { path: "src/openai/_models.py", isDir: false },
          { path: "src/openai/_utils.py", isDir: false },
          { path: "src/openai/_exceptions.py", isDir: false },
          { path: "src/openai/resources", isDir: true, children: [
            { path: "src/openai/resources/__init__.py", isDir: false },
            { path: "src/openai/resources/audio.py", isDir: false },
            { path: "src/openai/resources/embeddings.py", isDir: false },
            { path: "src/openai/resources/chat", isDir: true, children: [
              { path: "src/openai/resources/chat/__init__.py", isDir: false },
              { path: "src/openai/resources/chat/completions.py", isDir: false }
            ]}
          ]}
        ]}
      ]},
      { path: "tests", isDir: true, children: [
        { path: "tests/test_client.py", isDir: false },
        { path: "tests/test_completions.py", isDir: false }
      ]},
      { path: "pyproject.toml", isDir: false },
      { path: "requirements.txt", isDir: false },
      { path: "README.md", isDir: false }
    ];
  }
};
