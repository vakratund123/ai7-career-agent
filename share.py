"""
AI7 Career Agent — Instant Live Web Share
Starts FastAPI backend server on port 8001 and establishes an encrypted public HTTPS tunnel via SSH (localhost.run).
"""
import os
import sys
import time
import re
import subprocess
import threading
import urllib.request
from pathlib import Path

# Force UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
LIVE_URL_FILE = BASE_DIR / "data" / "live_url.txt"

def is_server_ready(port=8001):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/candidate", timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False

def start_backend():
    print("[*] Starting AI7 Career Agent backend on port 8001...")
    env = os.environ.copy()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd=str(BASE_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env
    )
    return proc

def main():
    print("=" * 65)
    print(" AI7 CAREER AGENT - SECURE LIVE SHARING ENGINE")
    print(" Candidate: V. Jagannath (Dubai, UAE)")
    print(" Target: Senior Asset Management & Real Estate Roles")
    print("=" * 65)

    if LIVE_URL_FILE.exists():
        try:
            LIVE_URL_FILE.unlink()
        except Exception:
            pass

    backend_proc = None
    if not is_server_ready(8001):
        backend_proc = start_backend()
        for i in range(25):
            time.sleep(0.5)
            if is_server_ready(8001):
                break
        print("[+] Backend server is up and responsive at http://localhost:8001")
    else:
        print("[+] Existing backend detected and responsive at http://localhost:8001")

    print("[*] Initiating secure HTTPS live tunnel...")
    ssh_cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=5",
        "-R", "80:127.0.0.1:8001",
        "nokey@localhost.run"
    ]

    tunnel_proc = subprocess.Popen(
        ssh_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    public_url = None
    url_pattern = re.compile(r"tunneled with tls termination,\s*(https://[^\s,]+)")
    fallback_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.lhr\.life")

    def monitor_stream(stream):
        nonlocal public_url
        for line in iter(stream.readline, ""):
            match = url_pattern.search(line) or fallback_pattern.search(line)
            if match and not public_url:
                public_url = match.group(1) if match.lastindex else match.group(0)
                try:
                    LIVE_URL_FILE.write_text(public_url, encoding="utf-8")
                except Exception:
                    pass
                print("\n" + "=" * 65)
                print(" [SUCCESS] AI7 CAREER AGENT IS NOW LIVE ONLINE!")
                print(" Share this secure link with Jagannath:\n")
                print(f" >>> {public_url} <<<")
                print("\n (He can open this directly on mobile, tablet, or desktop)")
                print(" Keep this window open to maintain the live link.")
                print("=" * 65 + "\n", flush=True)

    thread = threading.Thread(target=monitor_stream, args=(tunnel_proc.stdout,), daemon=True)
    thread.start()

    try:
        while True:
            time.sleep(1)
            if tunnel_proc.poll() is not None:
                print("[!] Tunnel disconnected.")
                break
    except KeyboardInterrupt:
        print("\n[*] Shutting down live share tunnel...")
    finally:
        tunnel_proc.terminate()
        if backend_proc:
            backend_proc.terminate()
        print("[+] Session closed.")

if __name__ == "__main__":
    main()
