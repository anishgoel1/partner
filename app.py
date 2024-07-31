from flask import Flask, request, jsonify, render_template
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory storage for simplicity
conversations = {
    'anish-greg': [],
    'anish-greg-ai': []
}

AI_MODEL = "gpt-3.5-turbo"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user = data['user']
    message = data['message']
    panel = data['panel']
    
    conversations[panel].append({'user': user, 'message': message})
    
    if panel == 'anish-greg-ai':
        # Determine which AI should respond
        ai_user = 'Greg' if user == 'Anish' else 'Anish'
        ai_response = generate_ai_response(ai_user, message)
        conversations[panel].append({'user': f'{ai_user}-AI', 'message': ai_response})
    
    return jsonify(conversations)

def generate_ai_response(ai_user, message):
    # Get the original conversation
    original_convo = conversations['anish-greg']
    
    # Prepare the context from the original conversation
    context = []
    for entry in original_convo:
        role = "assistant" if entry['user'] == ai_user else "user"
        context.append({"role": role, "content": entry['message']})
    
    # Add the current message to the context
    context.append({"role": "user", "content": message})
    
    # Prepare the full message list for the API call
    messages = [
        {"role": "system", "content": f"You are {ai_user}. Respond as {ai_user} would, based on the previous conversation and {ai_user}'s personality."},
    ] + context

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=messages
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True, port=5000)