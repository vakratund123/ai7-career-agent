"""
AI7 Career Agent — Autonomous Career Operating System
Launcher script.
Starts the backend FastAPI server on port 8000.
"""
import sys
import os
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print(" AI7 CAREER AGENT — AUTONOMOUS CAREER OPERATING SYSTEM")
    print(" Candidate: V. Jagannath (Dubai, UAE)")
    print(" Target: Senior Asset Management & Real Estate Roles")
    print(" Web Interface: http://localhost:8001")
    print("=" * 60)

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8001, reload=False)
