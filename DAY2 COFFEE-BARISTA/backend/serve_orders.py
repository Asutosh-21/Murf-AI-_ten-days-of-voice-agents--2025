#!/usr/bin/env python3

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def serve_orders():
    """Start a simple HTTP server to view order HTML files"""
    
    # Change to orders directory
    orders_dir = os.path.join(os.getcwd(), "orders")
    
    if not os.path.exists(orders_dir):
        print("No orders directory found!")
        return
    
    os.chdir(orders_dir)
    
    # Find available port
    PORT = 8000
    
    # List HTML files
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    if not html_files:
        print("No HTML order files found!")
        return
    
    print(f"Found {len(html_files)} order visualizations:")
    for i, file in enumerate(html_files, 1):
        print(f"  {i}. {file}")
    
    print(f"\nStarting HTTP server on port {PORT}...")
    print(f"View orders at: http://localhost:{PORT}/")
    print("Press Ctrl+C to stop the server")
    
    # Start server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server running at http://localhost:{PORT}/")
            
            # Open browser to first HTML file
            if html_files:
                webbrowser.open(f"http://localhost:{PORT}/{html_files[0]}")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {PORT} is already in use. Try a different port.")
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    serve_orders()