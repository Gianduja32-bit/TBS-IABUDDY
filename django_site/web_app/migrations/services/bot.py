import json
import os
import google.generativeai as genai
from django.conf import settings


class BotBuddy:
    def __init__(
        self,
        role="chatbot_iabuddy",
        model_name="models/gemini-2.5-flash",
        temperature=0.7,
    ):
        # Configuration Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Chargement du JSON (roles + countries)
        base_dir = os.path.dirname(__file__)
        data_path = os.path.join(base_dir, "preprompt.json")

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Prompt système selon le rôle
        self.system_prompt = data.get("roles", {}).get(
            role,
            "Tu es un assistant administratif utile."
        )

        # Données pays (JSON brut, non normalisé)
        self.countries_data = data.get("countries", [])

        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature

    def _get_country_context(self, country: str | None) -> str:
        """
        Recherche du pays en utilisant la clé 'Country'
        telle qu'elle existe dans le JSON actuel.
        """
        if not country:
            return "Aucun pays fourni."

        country = country.strip().lower()

        for c in self.countries_data:
            country_name = c.get("Country")
            if country_name and country_name.lower() == country:
                return json.dumps(c, ensure_ascii=False, indent=2)

        return f"Aucune correspondance trouvée pour : {country}"

    def talk(
        self,
        message: str,
        city: str | None = None,
        country: str | None = None
    ) -> str:
        try:
            country_context = self._get_country_context(country)

            # Construction du message utilisateur
            user_prompt = message
            if city:
                user_prompt = f"Ville : {city}\n{user_prompt}"
            if country:
                user_prompt = f"Pays : {country}\n{user_prompt}"

            if not country_context:
                country_context = (
                    "Aucune règle spécifique trouvée pour ce pays. "
                    "Demande des précisions à l'utilisateur si nécessaire."
                )

            # Prompt final envoyé au modèle
            full_prompt = (
                f"{self.system_prompt}\n\n"
                f"Contexte administratif pour ce pays :\n"
                f"{country_context}\n\n"
                f"Question utilisateur :\n{user_prompt}"
            )

            response = self.model.generate_content(
                full_prompt,
                generation_config={"temperature": self.temperature},
            )

            return response.text.strip()

        except Exception as e:
            return f"ERREUR GEMINI : {e}"


