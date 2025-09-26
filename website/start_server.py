#!/usr/bin/env python3
"""
Simple HTTP server for FitFriendsClub website preview
Run this to view your website locally at http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time

# Change to website directory
os.chdir('/Users/darnellamcguire/Khyrie3.0/src/fitness_mcp/fitness app/fitness app2.0/fitness app 3.0/website')

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()

def open_browser():
    """Open browser after server starts"""
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    print("🚀 Starting FitFriendsClub Website Server...")
    print(f"📁 Serving from: {os.getcwd()}")
    print(f"🌐 URL: http://localhost:{PORT}")
    print("📱 Perfect for testing on mobile (use your computer's IP)")
    print("🔥 Press Ctrl+C to stop the server\n")
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}/")
            print("🎉 Your FitFriendsClub website is now live!\n")
            print("Features to test:")
            print("  • 📱 Mobile responsive design")
            print("  • 🎯 Smooth scroll navigation") 
            print("  • 💫 Interactive animations")
            print("  • 📝 Contact form")
            print("  • 🏃‍♀️ Membership signup modal")
            print("  • 📊 Counter animations")
            print("  • 🎨 Premium design elements")
            print("\n" + "="*50)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped. Thanks for testing FitFriendsClub!")
        print("🌟 Your website is ready for deployment!")

if __name__ == "__main__":
    main()