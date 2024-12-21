import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, NotFound

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=api_key)


class GeminiModel:

    def list_available_models(self):
        models = genai.list_models()
        for model in models:
            print(f"Model Name: {model.name}")
            print(f"Description: {model.description}")
            print("-" * 20)

    def generate_chess_move(self, board_state):
        prompt = f"Given the following board state, provide the best next move in JSON format. The output should be a JSON object with a 'move' key: {board_state}"
        generation_config = {
            "temperature": 1,
            "response_mime_type": "application/json",
        }
        model_name = "models/gemini-1.5-flash-8b-exp-0924"
        model = genai.GenerativeModel(model_name)
        try:
            response = model.generate_content(
                [prompt],
                generation_config=generation_config
            )
            return response
        except ResourceExhausted:
            print(f"Resource exhausted for {model_name}, retrying in 1 minute...")
            time.sleep(60)
            return self.generate_chess_move(board_state)
        except NotFound:
            print(f"Model {model_name} not found")
        raise RuntimeError("Failed to generate chess move.")


if __name__ == "__main__":
    gemini_model = GeminiModel()
    gemini_model.list_available_models()




