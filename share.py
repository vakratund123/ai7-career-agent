"""
AI7 Career Agent — Robust Self-Healing Live Web Share
Starts FastAPI backend server on port 8001 and maintains a continuous, auto-reconnecting encrypted public HTTPS tunnel via SSH.
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

def ensure_backend(port=8001):
    if is_server_ready(port):
        print(f"[+] AI7 Career Agent backend is already active at http://localhost:{port}")
        return None

    print(f"[*] Starting AI7 Career Agent backend on port {port}...")
    env = os.environ.copy()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", str(port)],
        cwd=str(BASE_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env
    )
    for _ in range(30):
        time.sleep(0.5)
        if is_server_ready(port):
            print(f"[+] Backend server initialized successfully at http://localhost:{port}")
            return proc
    print("[!] Warning: Backend took longer than expected to initialize. Proceeding with tunnel...")
    return proc

def main():
    print("=" * 65)
    print(" AI7 CAREER AGENT - SELF-HEALING LIVE SHARING ENGINE")
    print(" Candidate: V. Jagannath (Dubai, UAE)")
    print(" Target: Senior Asset Management & Real Estate Roles")
    print("=" * 65)

    backend_proc = ensure_backend(8001)

    cloudflared_bin = BASE_DIR / "cloudflared.exe"
    if not cloudflared_bin.exists():
        cloudflared_bin = BASE_DIR / "data" / "cloudflared.exe"

    use_cloudflared = cloudflared_bin.exists()

    url_pattern = re.compile(r"(https://[a-zA-Z0-9-]+\.(?:trycloudflare\.com|serveousercontent\.com|serveo\.net|lhr\.life))")
    reconnect_count = 0

    try:
        while True:
            # Verify backend is healthy before launching tunnel
            if not is_server_ready(8001):
                print("[*] Restarting backend server...")
                backend_proc = ensure_backend(8001)

            if use_cloudflared:
                print(f"[*] Connecting high-speed Cloudflare HTTPS tunnel (attempt #{reconnect_count + 1})...")
                tunnel_cmd = [str(cloudflared_bin), "tunnel", "--url", "http://127.0.0.1:8001"]
            else:
                server = "serveo.net"
                print(f"[*] Connecting secure public HTTPS tunnel via {server} (attempt #{reconnect_count + 1})...")
                tunnel_cmd = [
                    "ssh",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ServerAliveInterval=15",
                    "-o", "ServerAliveCountMax=4",
                    "-R", "80:127.0.0.1:8001",
                    server
                ]


            tunnel_proc = subprocess.Popen(
                tunnel_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            current_url = None

            def read_tunnel_output(proc):
                nonlocal current_url
                for line in iter(proc.stdout.readline, ""):
                    match = url_pattern.search(line)
                    if match and not current_url:
                        current_url = match.group(1)
                        try:
                            LIVE_URL_FILE.write_text(current_url, encoding="utf-8")
                        except Exception:
                            pass
                        print("\n" + "=" * 65)
                        print(" [SUCCESS] AI7 CAREER AGENT IS LIVE ONLINE!")
                        print(" Share this secure link with Jagannath:\n")
                        print(f" >>> {current_url} <<<")
                        print("\n (Directly accessible on Mobile, Tablet, and Desktop)")
                        print(" Automatic keepalive and re-connection are active.")
                        print("=" * 65 + "\n", flush=True)

            t = threading.Thread(target=read_tunnel_output, args=(tunnel_proc,), daemon=True)
            t.start()

            # Monitor tunnel process
            while tunnel_proc.poll() is None:
                time.sleep(2)

            reconnect_count += 1
            print(f"[!] Tunnel disconnected (exit code {tunnel_proc.returncode}). Re-establishing link in 3s...")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[*] Stopping live share engine...")
    finally:
        if backend_proc:
            try:
                backend_proc.terminate()
            except Exception:
                pass
        print("[+] Engine stopped safely.")

if __name__ == "__main__":
    main()
