# app.py
from flask import Flask, render_template, request, jsonify
import threading
import time
from jarvis import JarvisEngine

app = Flask(__name__)
jarvis = JarvisEngine()

# Global state
app_state = {
    'last_user_input': '',
    'last_response': '',
    'is_listening': False,
    'auto_speak': True,
    'conversation_history': []
}

@app.route('/')
def index():
    return render_template('index.html', 
                         user_input=app_state['last_user_input'], 
                         response=app_state['last_response'])

@app.route('/status')
def status():
    """API endpoint for status updates"""
    return jsonify({
        'user_input': app_state['last_user_input'],
        'response': app_state['last_response'],
        'is_listening': app_state['is_listening'],
        'history': app_state['conversation_history'][-5:]  # Last 5 conversations
    })

@app.route('/', methods=['POST'])
def handle_text_command():
    command = request.form.get('command', '').strip()
    if command:
        app_state['last_user_input'] = command
        print(f"📥 Received text command: {command}")
        
        response = jarvis.handle_command(command)
        app_state['last_response'] = response
        
        # Add to history
        app_state['conversation_history'].append({
            'user': command,
            'response': response,
            'timestamp': time.time()
        })
        
        # Keep only last 20 conversations
        if len(app_state['conversation_history']) > 20:
            app_state['conversation_history'] = app_state['conversation_history'][-20:]
        
        if app_state['auto_speak']:
            threading.Thread(target=jarvis.speak, args=(response,)).start()
    
    return render_template('index.html',
                         user_input=app_state['last_user_input'],
                         response=app_state['last_response'])

@app.route('/voice', methods=['POST'])
def handle_voice_command():
    """Enhanced voice command handling"""
    def process_voice():
        app_state['is_listening'] = True
        try:
            command = jarvis.listen_with_timeout(timeout=8)
            if command and command not in ['timeout', 'unclear']:
                app_state['last_user_input'] = command
                response = jarvis.handle_command(command)
                app_state['last_response'] = response
                
                # Add to history
                app_state['conversation_history'].append({
                    'user': command,
                    'response': response,
                    'timestamp': time.time()
                })
                
                jarvis.speak(response)
            else:
                app_state['last_response'] = "I didn't catch that. Please try again."
                jarvis.speak(app_state['last_response'])
                
        except Exception as e:
            app_state['last_response'] = "Sorry, there was an error processing your voice command."
            print(f"Voice processing error: {e}")
        finally:
            app_state['is_listening'] = False
    
    threading.Thread(target=process_voice).start()
    return '', 204

@app.route('/settings', methods=['POST'])
def update_settings():
    """Update application settings"""
    data = request.get_json()
    if 'auto_speak' in data:
        app_state['auto_speak'] = data['auto_speak']
    return jsonify({'status': 'updated'})

if __name__ == '__main__':
    print("🚀 Starting Enhanced Jarvis Lite...")
    print("Features: Voice commands, fuzzy matching, Wikipedia search, calculator, and more!")
    app.run(debug=True, host='0.0.0.0', port=5000)