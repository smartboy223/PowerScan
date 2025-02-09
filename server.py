import os
import subprocess
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# Constants (using relative paths)
SCAN_SCRIPT = "FileScanner.ps1"
RESULTS_FILE = os.path.join("Refined_Results", "results.json")
PROGRESS_FILE = os.path.join("Refined_Results", "progress.txt")
SCAN_LOG_FILE = os.path.join("Refined_Results", "scan.log")
SESSION_LOG = "logs.txt"  # Session log for server errors

# Clear the session log on server start
with open(SESSION_LOG, "w", encoding="utf-8") as f:
    f.write("")

active_scan_process = None

def log_error(message):
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(message + "\n")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        try:
            if parsed_path.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            elif parsed_path.path == "/cwd":
                # Return current working directory (absolute path)
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                cwd = os.getcwd()
                self.wfile.write(cwd.encode("utf-8"))
            elif parsed_path.path == "/progress":
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                if os.path.exists(PROGRESS_FILE):
                    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                        self.wfile.write(f.read().encode("utf-8"))
                else:
                    self.wfile.write(b"0")
            elif parsed_path.path == "/results":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                if os.path.exists(RESULTS_FILE):
                    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                        contents = f.read()
                        if not contents.strip():
                            contents = "[]"
                        if contents.startswith("\ufeff"):
                            contents = contents.lstrip("\ufeff")
                        self.wfile.write(contents.encode("utf-8"))
                else:
                    self.wfile.write(json.dumps([]).encode("utf-8"))
            elif parsed_path.path == "/logs":
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                logs = "(No scan errors)"
                if os.path.exists(SCAN_LOG_FILE):
                    with open(SCAN_LOG_FILE, "r", encoding="utf-8") as f:
                        logs = f.read().strip()
                if os.path.exists(SESSION_LOG):
                    with open(SESSION_LOG, "r", encoding="utf-8") as f:
                        logs += "\n--- Session Log ---\n" + f.read().strip()
                self.wfile.write(logs.encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Endpoint not found.")
        except Exception as e:
            log_error("GET error: " + str(e))
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error processing request: {str(e)}".encode("utf-8"))

    def do_POST(self):
        global active_scan_process
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(post_data)
        except Exception as e:
            log_error("Invalid JSON in POST: " + str(e))
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Invalid JSON: {str(e)}".encode("utf-8"))
            return

        if parsed_path.path == "/scan":
            keywords = data.get("keywords", "")
            max_results = data.get("maxResults", "")
            include = data.get("include", "")
            exclude = data.get("exclude", "")
            root_folder = data.get("rootFolder", ".")

            if not keywords:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing 'keywords' parameter.")
                return

            # Convert root_folder to absolute path if not already absolute
            if not os.path.isabs(root_folder):
                root_folder = os.path.join(os.getcwd(), root_folder)

            command = [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", SCAN_SCRIPT,
                "-Keywords", keywords,
                "-OutputFile", RESULTS_FILE
            ]
            if max_results:
                command += ["-MaxResults", str(max_results)]
            if include:
                command += ["-Include", include]
            if exclude:
                command += ["-Exclude", exclude]
            if root_folder:
                command += ["-RootFolder", root_folder]

            if not os.path.exists("Refined_Results"):
                os.makedirs("Refined_Results")

            # Clear previous scan log, progress, and results
            for file in [PROGRESS_FILE, RESULTS_FILE, SCAN_LOG_FILE]:
                if os.path.exists(file):
                    try:
                        open(file, "w").close()
                    except Exception as e:
                        log_error(f"Error clearing {file}: {str(e)}")

            try:
                active_scan_process = subprocess.Popen(
                    command,
                    stdout=open(SCAN_LOG_FILE, "w", encoding="utf-8"),
                    stderr=subprocess.STDOUT,
                    cwd=os.getcwd()
                )
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Scan started successfully.")
            except Exception as e:
                log_error("Error starting scan: " + str(e))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error starting scan: {str(e)}".encode("utf-8"))
        elif parsed_path.path == "/stop":
            self.send_response(200)
            self.end_headers()
            if active_scan_process and active_scan_process.poll() is None:
                active_scan_process.terminate()
                self.wfile.write(b"Scan stopped.")
            else:
                self.wfile.write(b"No scan running.")
        elif parsed_path.path == "/clear":
            self.send_response(200)
            self.end_headers()
            for file in [PROGRESS_FILE, RESULTS_FILE, SCAN_LOG_FILE, SESSION_LOG]:
                if os.path.exists(file):
                    try:
                        open(file, "w").close()
                    except Exception as e:
                        log_error(f"Error clearing {file}: {str(e)}")
            self.wfile.write(b"Logs, progress, results, and session log cleared.")
        elif parsed_path.path == "/shutdown":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Server is shutting down.")
            if active_scan_process and active_scan_process.poll() is None:
                active_scan_process.terminate()
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found.")

def run_server():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port 8000...")
    try:
        httpd.serve_forever()
    except Exception as e:
        log_error("Server error: " + str(e))
    finally:
        httpd.server_close()
        print("Server stopped.")

if __name__ == "__main__":
    run_server()
