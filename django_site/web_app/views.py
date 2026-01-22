from django.shortcuts import render
from pathlib import Path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import requests
import time


def home(request):
    return render(request, 'index.html')


# Page HTML
def chatbot(request):
    return render(request, "chatbot.html")


# API
@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        api_key = settings.GEMINI_API_KEY
        
        if not api_key:
             return JsonResponse({"response": "Erreur: Clé API manquante."}, status=500)

        # Prepare System Prompt
        try:
            # Locate preprompt.json relative to basedir or specific path
            # BASE_DIR is usually 2 levels up from views.py if structure is standard, 
            # but here views.py is in web_app, so we need to find migrations/services
            base_path = Path(__file__).resolve().parent
            json_path = base_path / "migrations" / "services" / "preprompt.json"
            
            with open(json_path, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
                system_instruction = prompts.get("roles", {}).get("chatbot_iabuddy", "")
                
        except Exception as e:
            print(f"Error loading system prompt: {e}")
            system_instruction = "Tu es un assistant administratif serviable."

        # Prepend system instruction to user message (best compatibility for text generation models)
        full_message = f"System Instruction: {system_instruction}\n\nUser Message: {message}"

        # Call Gemini API via REST
        # Switching to gemini-2.0-flash as confirmed by list_models.py
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": full_message}]
            }]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        # Increased backoff: 2s, 4s, 8s...
                        wait_time = 2 ** (attempt + 1)
                        print(f"Rate limited (429). Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print("Max retries reached for 429 error.")
                        return JsonResponse({"response": "Trop de requêtes. L'IA s'est endormie, réessaie dans une minute."}, status=429)

                response.raise_for_status()
                result = response.json()
                # Extract text from response
                try:
                    bot_response = result['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    bot_response = "Je n'ai pas compris la réponse de l'IA."
                    
                return JsonResponse({"response": bot_response})
                
            except requests.RequestException as e:
                print(f"Gemini API Exception: {e}")
                if response is not None:
                     print(f"Response content: {response.text}")
                return JsonResponse({"response": "Une erreur est survenue."}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)