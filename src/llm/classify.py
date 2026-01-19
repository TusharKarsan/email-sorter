import json
import requests

OLLAMA_URL = "http://design:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:latest"

def classify_email(email_body):
    prompt = f"""
    Classify the email into: [Job, News, Financial, Personal, Social, Spam].
    Respond with a JSON object only.
    
    Email Body: {email_body[:2000]}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json", # Forces Ollama's JSON mode
        "options": { "temperature": 0 }
    }

    try:
        # Increase timeout to 90s; complex emails can take time on local hardware
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        response.raise_for_status()
        
        reply = response.json().get("response", "").strip()
        if not reply:
            raise ValueError("Empty response")
            
        return json.loads(reply)
    except Exception as e:
        return {"category": "Error", "reason": str(e)}
