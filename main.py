from core.models import AIModel
from const import *
from core.database import DatabaseManager

if __name__ == "__main__":
    # Initialize the model

    ai_model = AIModel(model_path)

    db = DatabaseManager(db_path)
    
    ai_model.update_known_info(db.get_bot("bot4")["prompts"])
    
    user_message = input("prompt:")
    # Get the chat response
    while not "end" == user_message:
        print("Response:", end=" ", flush=True)
        for content in ai_model.chat(user_message):
            print(content, end="", flush=True)
        print("\n")
        user_message = input("prompt:")
    # Terminate the model
    ai_model.terminate()
