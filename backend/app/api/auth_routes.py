import json
import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from app.model.dataset_writer import DATASET_FILE

router = APIRouter()

class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class RegisterRequest(BaseModel):
  name: str
  email: EmailStr
  password: str

@router.post("/auth/register")
def register_user(request: RegisterRequest):
  # Simulate JWT registration token issuance
  return {
    "access_token": f"mock-jwt-token-register-{request.email}",
    "token_type": "bearer",
    "user": {
      "name": request.name,
      "email": request.email,
      "analysesCompleted": 0,
      "repositoriesAnalyzedCount": 0,
      "favoriteLanguages": [],
      "joinedDate": "July 12, 2026"
    }
  }

@router.post("/auth/login")
def login_user(request: LoginRequest):
  # Standard default mock login profile parameters matching mockData configurations
  name_part = request.email.split("@")[0].capitalize()
  return {
    "access_token": f"mock-jwt-token-login-{request.email}",
    "token_type": "bearer",
    "user": {
      "name": name_part if name_part else "Developer",
      "email": request.email,
      "analysesCompleted": 34,
      "repositoriesAnalyzedCount": 12,
      "favoriteLanguages": ["Python", "TypeScript", "Go"],
      "joinedDate": "October 12, 2025"
    }
  }

@router.get("/users/profile")
def get_user_profile(authorization: str = Header(None)):
  if not authorization:
    raise HTTPException(status_code=401, detail="Missing authorization header")
  
  # Decode mock username from JWT payload string
  email = "s.jenkins@developer.io"
  name = "Sarah Jenkins"
  if "login-" in authorization:
    email = authorization.split("login-")[-1]
    name = email.split("@")[0].capitalize()
  elif "register-" in authorization:
    email = authorization.split("register-")[-1]
    name = email.split("@")[0].capitalize()

  return {
    "name": name,
    "email": email,
    "analysesCompleted": 34,
    "repositoriesAnalyzedCount": 12,
    "favoriteLanguages": ["Python", "TypeScript", "Go"],
    "joinedDate": "October 12, 2025"
  }

@router.get("/repositories/history")
def get_repository_history(authorization: str = Header(None)):
  if not authorization:
    raise HTTPException(status_code=401, detail="Missing authorization header")
  
  history_logs = []
  
  # Attempt to read compiled scan items from the local JSONL training dataset file
  if os.path.exists(DATASET_FILE):
    try:
      with open(DATASET_FILE, "r", encoding="utf-8") as f:
        for line in f:
          line = line.strip()
          if not line:
            continue
          record = json.loads(line)
          
          # Map JSONL record fields to history logs structures
          record_id = record.get("record_id", "hist-1")
          repo_summary = record.get("input", {}).get("repository_summary", {})
          identity = repo_summary.get("repository_identity", {})
          arch = repo_summary.get("architecture", {})
          
          name = identity.get("name", "unknown")
          owner = identity.get("owner", "github")
          lang = identity.get("primary_language", "Python")
          
          history_logs.append({
            "id": record_id,
            "repositoryUrl": f"https://github.com/{owner}/{name}",
            "name": name,
            "owner": owner,
            "date": "2026-07-12",
            "language": lang,
            "architecture": arch.get("primary", "General Software Repository"),
            "score": record.get("training_quality", {}).get("score", 90),
            "status": "completed",
            "result": {
              "status": "valid",
              "repository": name,
              "repository_summary": repo_summary,
              "target_output": record.get("output", {}),
              "important_file_details": record.get("input", {}).get("important_file_details", []),
              "internal_dependencies": record.get("input", {}).get("internal_dependencies", []),
              "training_quality": record.get("training_quality", {})
            }
          })
    except Exception as e:
      print(f"Error parsing dataset history: {e}")

  # If history is empty, supply prebuilt fallbacks
  if not history_logs:
    history_logs = [
      {
        "id": "hist-1",
        "repositoryUrl": "https://github.com/Mathu-10/github-repository-intelligence",
        "name": "github-repository-intelligence",
        "owner": "Mathu-10",
        "date": "2026-07-12",
        "language": "Python",
        "architecture": "Web API Backend (Layered Modular)",
        "score": 94,
        "status": "completed"
      },
      {
        "id": "hist-2",
        "repositoryUrl": "https://github.com/openai/openai-python",
        "name": "openai-python",
        "owner": "openai",
        "date": "2026-07-11",
        "language": "Python",
        "architecture": "Client Library / SDK",
        "score: ": 89,
        "status": "completed"
      }
    ]

  return history_logs

@router.delete("/repositories/history/{id}")
def delete_history_item(id: str, authorization: str = Header(None)):
  if not authorization:
    raise HTTPException(status_code=401, detail="Missing authorization header")
  
  # Return success code. History logs lists are kept updated inside local state parameters.
  return {"status": "deleted", "id": id}
