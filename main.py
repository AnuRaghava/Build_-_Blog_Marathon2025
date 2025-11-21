import os
import json
import base64
import traceback
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google.cloud import firestore
import google.generativeai as genai # <--- NEW LIBRARY
from google.generativeai.types import FunctionDeclaration, Tool

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# 1. PASTE YOUR API KEY HERE
API_KEY = "AIzaSyApkeloSwZTBJigcjuXO5byNpGPdErrYOQ" 

# 2. Firestore Project (Keep your project ID here for the database)
PROJECT_ID = "build-and-blog-marathon-2025"
COLLECTION_LOGS = "audit_logs"

# Configure the AI with the Key
genai.configure(api_key=API_KEY)

# Global vars
db = None
model = None

# --- TOOL DEFINITION (Python Logic) ---
def check_expiry_logic(expiry_date_str: str):
    """Calculates if food is expired."""
    try:
        today = datetime.now().date()
        # Try to handle generic user input formats
        exp_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        delta = (exp_date - today).days
        
        if delta < 0:
            return {"status": "EXPIRED", "days_overdue": abs(delta), "safe": False}
        elif delta <= 2:
            return {"status": "EXPIRING_SOON", "days_left": delta, "safe": True}
        else:
            return {"status": "FRESH", "days_left": delta, "safe": True}
    except:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

# Define the tool for Gemini
expiry_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="check_expiry_logic",
            description="Checks if food is expired based on date.",
            parameters={
                "type": "object",
                "properties": {
                    "expiry_date_str": {
                        "type": "string", 
                        "description": "Expiry date in YYYY-MM-DD"
                    }
                },
                "required": ["expiry_date_str"]
            }
        )
    ]
)

# --- INITIALIZATION ---
def get_services():
    global db, model
    if db is None:
        # Firestore still needs the Project ID
        db = firestore.Client(project=PROJECT_ID)
    
    if model is None:
        # Initialize Gemini using the API Key (Simpler!)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            tools=[expiry_tool]
        )
    return db, model

@app.route("/", methods=["GET"])
def home():
    # Ensure you have the templates/index.html file!
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_compliance():
    try:
        db, agent_model = get_services()
        data = request.get_json()
        
        # Extract Inputs
        loc = data.get("location", "Unknown")
        desc = data.get("description", "")
        expiry = data.get("expiry_date", None)
        img_b64 = data.get("image_base64", None)

        # Start Chat
        chat = agent_model.start_chat(enable_automatic_function_calling=True)

        # Build Request
        prompt_parts = [
            f"You are a Food Safety Agent. Location: {loc}. Context: {desc}. Expiry Input: {expiry}. Analyze compliance.",
        ]

        # Add Image if present
        if img_b64:
            image_data = base64.b64decode(img_b64)
            prompt_parts.append({
                "mime_type": "image/jpeg",
                "data": image_data
            })

        # Send to AI
        response = chat.send_message(prompt_parts)
        
        # The library handles the tool calling automatically now with 'enable_automatic_function_calling=True'
        # We just need to parse the final text response.
        final_text = response.text
        
        # Try to find JSON in the response or create a wrapper
        result_obj = {
            "compliance_status": "INFO",
            "reasoning": final_text,
            "action_plan": "Check reasoning above."
        }
        
        # Clean Log
        try:
            clean = final_text.replace("```json", "").replace("```", "").strip()
            if "{" in clean:
                result_obj = json.loads(clean)
        except:
            pass

        # Save to Database
        db.collection(COLLECTION_LOGS).add({
            "timestamp": firestore.SERVER_TIMESTAMP,
            "input": desc,
            "ai_result": result_obj
        })

        return jsonify({"result": result_obj})

    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
