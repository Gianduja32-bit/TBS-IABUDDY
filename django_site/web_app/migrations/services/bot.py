import json
import os
import google.generativeai as genai
from django.conf import settings


class BotBuddy:
    def __init__(
        self,
        prompt_key="chatbot_iabuddy",
        model_name="models/gemini-2.5-flash",
        temperature=1,
    ):
        # Config API Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Charger le preprompt
        base_dir = os.path.dirname(__file__)
        preprompt_path = os.path.join(base_dir, "preprompt.json")

        with open(preprompt_path, "r", encoding="utf-8") as f:
            prompts = json.load(f)

        self.system_prompt = prompts.get(
            prompt_key, "Tu es un assistant coopératif."
        )

        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature

    def talk(self, message: str) -> str:
        try:
            full_prompt = f"{self.system_prompt}\n\nUtilisateur : {message}"
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Erreur : {e}"
