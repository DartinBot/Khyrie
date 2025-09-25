#!/usr/bin/env python3
"""
Simple Demo Server for Trainer Registration Flow
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.parse
from trainer_marketplace import TrainerMarketplace
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize trainer marketplace
trainer_marketplace = TrainerMarketplace()

class TrainerDemoHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for trainer registration"""
        if self.path == '/api/trainers/register':
            try:
                # Get the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                trainer_data = json.loads(post_data.decode('utf-8'))
                
                logger.info(f"Received trainer registration: {trainer_data.get('name', 'Unknown')}")
                
                # Process the registration
                result = trainer_marketplace.register_trainer(trainer_data)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    'success': True,
                    'trainer_id': result.get('trainer_id'),
                    'message': 'Trainer registered successfully!',
                    'status': 'pending_verification',
                    'next_steps': [
                        'Complete your profile with additional certifications',
                        'Upload verification documents',
                        'Set your availability schedule',
                        'Create your first service offering'
                    ]
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
                
                # Log registration details
                logger.info(f"✅ Successfully registered trainer: {trainer_data.get('name')}")
                logger.info(f"   📧 Email: {trainer_data.get('email')}")
                logger.info(f"   📍 Location: {trainer_data.get('location')}")
                logger.info(f"   🏋️  Specializations: {', '.join(trainer_data.get('specializations', []))}")
                logger.info(f"   📜 Experience: {trainer_data.get('experience_years')} years")
                
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {
                    'success': False,
                    'error': str(e),
                    'message': 'Registration failed. Please try again.'
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        
        elif self.path == '/api/trainers/search':
            try:
                # Handle trainer search
                trainers = trainer_marketplace.search_trainers({})
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    'success': True,
                    'trainers': trainers.get('trainers', []),
                    'total_count': len(trainers.get('trainers', []))
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
                
            except Exception as e:
                logger.error(f"Search error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {'success': False, 'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        
        else:
            # Default POST handling
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Override to provide cleaner logging"""
        if not any(x in args[0] for x in ['.css', '.js', '.ico', '.png'] if args):
            super().log_message(format, *args)

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('localhost', PORT), TrainerDemoHandler)
    
    print(f"\n🚀 Khyrie Trainer Marketplace Demo Server")
    print(f"📍 Running at: http://localhost:{PORT}")
    print(f"🏋️  Trainer Registration: http://localhost:{PORT}/trainer_marketplace.html")
    print(f"📊 Server logs will show registration details...")
    print(f"\n⚡ Ready to demonstrate trainer registration flow!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped.")
        server.server_close()