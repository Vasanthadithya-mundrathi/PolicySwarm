import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:12b"

def get_llm_response(prompt: str, model_name=MODEL_NAME):
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Ollama Error: {e}")
        return "Error generating response. Is Ollama running?"

def get_json_response(prompt: str, model_name=MODEL_NAME):
    """
    Forces the LLM to return valid JSON by cleaning the output.
    """
    full_prompt = prompt + "\n\nIMPORTANT: Return ONLY valid JSON. No markdown formatting, no backticks."
    text = get_llm_response(full_prompt, model_name)
    
    # Clean up markdown code blocks if present
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```", "", text)
    text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"JSON Parse Error. Raw text: {text}")
        return {"message": text, "score": 50} # Fallback
