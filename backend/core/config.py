import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "frontend"
EXPORTS_DIR = DATA_DIR / "exports"

DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "ai7_career.db"

CANDIDATE_CV_SOURCE = r"C:\Users\nirma\Downloads\3. V. JAGANNATH_SENIOR MANAGER – ASSET MANAGEMENT & PORTFOLIO DEVELOPMENT.pdf"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Autonomous levels: 1 = Copilot, 2 = AI-First (Default), 3 = High Autonomy
DEFAULT_AUTONOMY_LEVEL = 2

TARGET_COMPANIES = [
    "Goldman Sachs",
    "Morgan Stanley",
    "Etihad Airways",
    "Blackstone",
    "Amazon",
    "BlackRock",
    "J.P. Morgan Asset Management",
    "Invesco",
    "Microsoft",
    "Vanguard",
    "Fidelity",
    "McKinsey & Company",
    "PwC",
    "Deloitte",
    "KPMG",
    "EY",
    "Mastercard",
    "Visa"
]

TARGET_ROLES = [
    "Real Estate Manager",
    "Leasing Manager",
    "Retail Leasing Manager",
    "Commercial Leasing Manager",
    "Asset Manager",
    "Senior Asset Manager",
    "Portfolio Manager",
    "Real Estate Portfolio Manager",
    "Portfolio Development Manager",
    "Commercial Manager",
    "Commercial Asset Manager",
    "Real Estate Strategy Manager",
    "Asset Management Director",
    "Portfolio Strategy Manager"
]
