from http.server import BaseHTTPRequestHandler
from .SwornOfficerChatbot import ContentChatbot
import json

chatbot = ContentChatbot()

def handle_chat(request_body):
    try:
        print(f"Request body received: {request_body}")  # Debug log
        user_input = request_body.get('message')
        if not user_input:
            return {'error': 'No message provided'}, 400
        
        response = chatbot.chat(user_input)
        print(f"Response to send: {response}")  # Debug log
        return {'response': response}, 200
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")  # Debug log
        return {'error': error_msg}, 500


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/api/chat':
            self.send_response(404)
            self.end_headers()
            return

        try:
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            request_json = json.loads(request_body)

            # Process the chat request
            response_data, status_code = handle_chat(request_json)

            # Send response
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Write valid JSON response
            self.wfile.write(json.dumps(response_data).encode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON input"}')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())


# Add to your index.py, at the bottom
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/chat', methods=['POST', 'OPTIONS'])
    def chat_endpoint():
        if request.method == 'OPTIONS':
            return '', 200
            
        # Use your existing handle_chat function
        response_data, status_code = handle_chat(request.json)
        return jsonify(response_data), status_code

    print("Starting development server on port 8000...")
    app.run(port=8000, debug=True)