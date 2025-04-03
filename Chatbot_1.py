from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Get the absolute path of the current script's directory (app.py or main.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Correct the path to the templates folder (inside 'chatbots' folder)
template_folder = os.path.join(BASE_DIR, 'chatbots', 'templates')  # Corrected this line

# Debugging: Verify the paths
print("Template Folder Path:", template_folder)
print("Templates Folder Exists:", os.path.exists(template_folder))
print("Index.html Exists:", os.path.exists(os.path.join(template_folder, "index.html")))

# Create Flask app with the correct template folder
app = Flask(__name__, template_folder=template_folder)  # Use the correct variable name

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded
if not openai.api_key:
    raise ValueError("API Key not found. Make sure it's set as an environment variable.")

# Store conversation state
conversation_state = {
    'step': 'start',
    'user_input': '',
    'user_email': ''
}

@app.route("/")
def index():
    # Render the index.html template from the 'chatbots/templates' directory
    return render_template("index.html")




def generate_response(user_input):
    """Handles chatbot responses using OpenAI's latest API format."""
    try:
        client = openai.OpenAI()  # NEW: Create an OpenAI client

        response = client.chat.completions.create(  # NEW: Updated API format
            model="gpt-4",  # Use "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()  # NEW: Updated response format

    except Exception as e:
        print("🔥 ERROR:", str(e))  # Debugging: Print the exact error in the terminal
        return f"Sorry, I ran into an issue: {str(e)}"  # Show actual error message in response


@app.route("/chat", methods=["POST"])
def chat():
    """Handles incoming chatbot messages using OpenAI."""
    user_input = request.json.get('message')  
    bot_response = generate_response(user_input)  
    return jsonify({"response": bot_response}), 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(debug=True)
