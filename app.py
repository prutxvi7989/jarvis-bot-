from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

headers = lambda: {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '')}",
    "Content-Type": "application/json"
}

def chat_with_groq(messages):
    if not os.getenv("GROQ_API_KEY"):
        raise Exception("GROQ_API_KEY not set in environment.")
    payload = {
        "model": MODEL,
        "messages": messages
    }
    response = requests.post(GROQ_API_URL, headers=headers(), json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            session['name'] = name
            return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'name' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', name=session['name'])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    messages = data.get('messages', [])
    try:
        reply = chat_with_groq(messages)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
