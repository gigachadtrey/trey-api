from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import google.generativeai as genai
from groq import Groq
from flask_cors import CORS
import traceback
import sys
import os

app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# Fetch API keys from environment variables (set in Vercel's dashboard)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Ensure the API keys are set
if not GEMINI_API_KEY or not GROQ_API_KEY:
    raise ValueError("API keys not set in environment variables.")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Configure the Groq API client
groq_client = Groq(api_key=GROQ_API_KEY)

@app.route('/ping')
def index():
    # Return a simple HTML response for testing
    return "<h1>Hello from Flask on Vercel!</h1>"

@app.route('/generate', methods=['POST'])
def generate_content():
    access_key = request.json.get('accessKey')
    user_input = request.json.get('input')
    model_name = request.json.get('model', 'gemini-1.5-flash')

    if access_key != 'geminiaccesskey6383':
        return jsonify({"error": "Unauthorized"}), 403

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    image_file = request.files.get('image')
    try:
        model = genai.GenerativeModel(model_name)
        if image_file:
            image_data = image_file.read()
            response = model.generate_content(user_input, image=image_data)
        else:
            response = model.generate_content(user_input)
        return jsonify({"generated_content": response.text})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 500

@app.route('/websim', methods=['POST'])
def generate_websim_content():
    access_key = request.json.get('accessKey')
    user_input = request.json.get('input')
    model_name = request.json.get('model', 'tunedModels/websimmodel12-2rec21oedmrx')

    if access_key != 'geminiaccesskey6383':
        return jsonify({"error": "Unauthorized"}), 403
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_input)
        return jsonify({"generated_content": response.text})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 500

@app.route('/groq', methods=['POST'])
def generate_groq_content():
    access_key = request.json.get('accessKey')
    user_input = request.json.get('input')
    model_name = request.json.get('model', 'llama-3.3-70b-versatile')  # Default Groq model

    if access_key != 'geminiaccesskey6383':
        return jsonify({"error": "Unauthorized"}), 403
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Enable streaming for the Groq API call
        stream = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model=model_name,
            stream=True
        )
        
        # Generator to stream tokens as they arrive
        def generate():
            for chunk in stream:
                token = chunk.choices[0].delta.get("content", "")
                if token:
                    yield token + " "  # Add a space after each token for readability
                    sys.stdout.flush()  # Force flush the output buffer

        return Response(stream_with_context(generate()), mimetype='text/plain')

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 500

@app.route('/getKey', methods=['POST'])
def get_gemini_key():
    access_key = request.json.get('accessKey')
    if access_key != 'geminiaccesskey6383':
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify({"GEMINI_API_KEY": GEMINI_API_KEY}), 200

# Expose the WSGI callable for Vercel
handler = app.wsgi_app
