from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        message = query.get('message', [''])[0]
        
        if not message:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error: No message provided')
            return
        
        # Get environment variables
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        channel_name = os.environ.get('TELEGRAM_CHANNEL')
        
        if not bot_token or not channel_name:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error: Telegram credentials not configured')
            return
        
        # Send message to Telegram
        api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': channel_name,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(api_url, data=payload)
            response.raise_for_status()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Message sent successfully')
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error sending message: {str(e)}'.encode())
