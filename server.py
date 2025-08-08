#!/usr/bin/env python3
"""
Simple HTTP server for serving the LunatiSynergy landing page
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve index.html for root requests"""
    
    def end_headers(self):
        # Add security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def start_server():
    """Start the HTTP server"""
    PORT = 5000
    HOST = "0.0.0.0"
    
    # Change to the directory containing this script
    os.chdir(Path(__file__).parent)
    
    try:
        with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 LunatiSynergy landing page server starting...")
            print(f"🌙 Server running at http://{HOST}:{PORT}")
            print(f"💫 Access the site at http://localhost:{PORT}")
            print(f"🛑 Press Ctrl+C to stop the server")
            
            # Check if index.html exists
            if not Path("index.html").exists():
                print("⚠️  Warning: index.html not found in current directory")
                print("📁 Current directory:", os.getcwd())
                print("📄 Files in directory:", list(Path(".").glob("*")))
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🌙 Server shutting down gracefully...")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Please try a different port or stop the existing server.")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_server()
