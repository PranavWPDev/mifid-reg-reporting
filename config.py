# from __future__ import annotations

# import os
# from dataclasses import dataclass
# from functools import lru_cache
# from pathlib import Path


# def _get_env(key: str, default: str = "") -> str:
#     """
#     Safe env reader with fallback.
#     """
#     value = os.getenv(key)
#     if value is None or value.strip() == "":
#         return default
#     return value.strip()


# @dataclass(frozen=True)
# class Settings:
#     # ─────────────────────────────────────────────
#     # APP
#     # ─────────────────────────────────────────────
#     app_name: str = "mifid-agentic-reporting"
#     environment: str = _get_env("ENVIRONMENT", "local")

#     # ─────────────────────────────────────────────
#     # GCP CONFIG
#     # ─────────────────────────────────────────────
#     gcp_project_id: str = _get_env("GCP_PROJECT_ID", "deutschebank-aipocs")  # ✅ default added
#     gcp_region: str = _get_env("GCP_REGION", "asia-south1")
#     bq_dataset: str = _get_env("BQ_DATASET", "mifid_reporting")

#     # ─────────────────────────────────────────────
#     # PATHS
#     # ─────────────────────────────────────────────
#     backend_root: Path = Path(__file__).resolve().parent

#     reports_dir: Path = Path(
#         _get_env("REPORTS_DIR", str(Path(__file__).resolve().parent / "reports"))
#     )

#     inmemory_csv_path: Path = Path(
#         _get_env(
#             "INMEMORY_CSV_PATH",
#             str(Path(__file__).resolve().parent / "data" / "inmemory" / "trade_intake.csv"),
#         )
#     )

#     # ─────────────────────────────────────────────
#     # LLM CONFIG
#     # ─────────────────────────────────────────────
#     llm_model: str = _get_env("LLM_MODEL", "gpt-4.1-mini")
#     llm_timeout_seconds: int = int(_get_env("LLM_TIMEOUT_SECONDS", "30"))

#     # ─────────────────────────────────────────────
#     # POST INIT VALIDATION
#     # ─────────────────────────────────────────────
#     def __post_init__(self):
#         """
#         Validate critical config.
#         """
#         # Ensure directories exist
#         self.reports_dir.mkdir(parents=True, exist_ok=True)
#         self.inmemory_csv_path.parent.mkdir(parents=True, exist_ok=True)

#         # 🔥 CRITICAL FIX: Only enforce in prod
#         if self.environment != "local" and not self.gcp_project_id:
#             raise RuntimeError("GCP_PROJECT_ID is not configured.")



# # Singleton
# @lru_cache(maxsize=1)
# def get_settings() -> Settings:
#     return Settings()


from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

def _get_env(key: str, default: str = "") -> str:
    value = os.getenv(key)
    return value.strip() if value else default


@dataclass(frozen=True)
class Settings:
    app_name: str = _get_env("APP_NAME", "MiFID II Agentic POC")
    environment: str = _get_env("ENVIRONMENT", "local")

    # GCP / LLM
    gcp_project_id: str = _get_env("GCP_PROJECT_ID", "")
    gcp_region: str = _get_env("GCP_REGION", "asia-south1")
    bq_dataset: str = _get_env("BQ_DATASET", "mifid_reporting")

    # Gemini aliases for older code
    gemini_project_id: str = _get_env("GEMINI_PROJECT_ID", _get_env("GCP_PROJECT_ID", ""))
    gemini_location: str = _get_env("GEMINI_LOCATION", _get_env("GCP_REGION", "asia-south1"))
    gemini_model_name: str = _get_env("GEMINI_MODEL_NAME", _get_env("LLM_MODEL", "gemini-1.5-flash-002"))

    # Paths
    backend_root: Path = Path(__file__).resolve().parent
    reports_dir: Path = Path(_get_env("REPORTS_DIR", str(Path(__file__).resolve().parent / "reports")))
    inmemory_csv_path: Path = Path(
        _get_env(
            "INMEMORY_CSV_PATH",
            str(Path(__file__).resolve().parent / "data" / "inmemory" / "trade_intake.csv"),
        )
    )
    sqlite_path: Path = Path(_get_env("SQLITE_PATH", str(Path(__file__).resolve().parent / "mifid_poc.db")))
    chroma_path: Path = Path(_get_env("CHROMA_PATH", str(Path(__file__).resolve().parent / "chroma_db")))

    # Legacy aliases used by older files
    report_dir: Path = Path(_get_env("REPORT_DIR", str(Path(__file__).resolve().parent / "reports")))

    # CORS
    cors_allow_origins: str = _get_env("CORS_ALLOW_ORIGINS", "*")

    # LLM
    llm_model: str = _get_env("LLM_MODEL", "gemini-1.5-flash-002")
    llm_timeout_seconds: int = int(_get_env("LLM_TIMEOUT_SECONDS", "30"))

    def __post_init__(self):
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.inmemory_csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self.chroma_path.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()