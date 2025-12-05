"""
PolicySwarm LLM Interface
Supports: Ollama (default), OpenAI, Gemini, Blaxel
"""
import json
import os
import requests

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default to Ollama if no config
        return {"llm_provider": "ollama", "ollama": {"base_url": "http://localhost:11434", "model": "gemma3:12b"}}

config = load_config()
PROVIDER = config.get("llm_provider", "ollama")

# ============ OLLAMA (Local - Default) ============
def get_ollama_response(prompt: str) -> str:
    """Local Ollama for maximum privacy"""
    ollama_config = config.get("ollama", {})
    url = f"{ollama_config.get('base_url', 'http://localhost:11434')}/api/generate"
    
    payload = {
        "model": ollama_config.get("model", "gemma3:12b"),
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 500}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Ollama error: {e}")
        return f"Error: {str(e)}"

# ============ OPENAI ============
def get_openai_response(prompt: str) -> str:
    """OpenAI GPT models"""
    openai_config = config.get("openai", {})
    api_key = openai_config.get("api_key") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return "Error: OpenAI API key not configured"
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=openai_config.get("model", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except ImportError:
        return "Error: openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"OpenAI error: {str(e)}"

# ============ GEMINI ============
def get_gemini_response(prompt: str) -> str:
    """Google Gemini models"""
    gemini_config = config.get("gemini", {})
    api_key = gemini_config.get("api_key") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        return "Error: Gemini API key not configured"
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(gemini_config.get("model", "gemini-1.5-flash"))
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return "Error: google-generativeai package not installed. Run: pip install google-generativeai"
    except Exception as e:
        return f"Gemini error: {str(e)}"

# ============ BLAXEL ============
def get_blaxel_response(prompt: str) -> str:
    """Blaxel AI platform"""
    blaxel_config = config.get("blaxel", {})
    api_key = blaxel_config.get("api_key") or os.getenv("BL_API_KEY")
    
    if not api_key:
        return "Error: Blaxel API key not configured"
    
    try:
        from blaxel.client import BlaxelClient
        client = BlaxelClient()
        # Blaxel uses workspace-based model access
        response = client.run(
            agent=blaxel_config.get("model", "blaxel-agent"),
            input=prompt
        )
        return str(response)
    except ImportError:
        return "Error: blaxel package not installed. Run: pip install blaxel"
    except Exception as e:
        return f"Blaxel error: {str(e)}"

# ============ UNIFIED INTERFACE ============
def get_llm_response(prompt: str) -> str:
    """Get response from configured LLM provider"""
    provider = config.get("llm_provider", "ollama")
    
    if provider == "ollama":
        return get_ollama_response(prompt)
    elif provider == "openai":
        return get_openai_response(prompt)
    elif provider == "gemini":
        return get_gemini_response(prompt)
    elif provider == "blaxel":
        return get_blaxel_response(prompt)
    else:
        return get_ollama_response(prompt)  # Fallback to Ollama

def get_json_response(prompt: str) -> dict:
    """Get JSON response from LLM"""
    response = get_llm_response(prompt)
    
    try:
        # Extract JSON from response
        import re
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            return json.loads(json_match.group())
        return {"message": response, "score": 50}
    except json.JSONDecodeError:
        return {"message": response, "score": 50}

def get_current_provider() -> str:
    """Get the current LLM provider name"""
    return config.get("llm_provider", "ollama")

def reload_config():
    """Reload configuration from file"""
    global config, PROVIDER
    config = load_config()
    PROVIDER = config.get("llm_provider", "ollama")
