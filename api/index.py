"""
Vercel Serverless Entry Point for SupportIQ FastAPI Backend.
Wraps the FastAPI app for deployment as a Vercel Python function.
"""
import sys
import os

# Add the project root to path so backend modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app  # noqa: E402 — import after path fix
