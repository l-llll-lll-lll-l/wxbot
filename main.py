from core.models import AIModel

if __name__ == "__main__":
    # Initialize the model
    model_path = "./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC"
    ai_model = AIModel(model_path)

    # Get the chat response
    user_message = "What is the meaning of life?"
    print("Response:", end=" ", flush=True)
    for content in ai_model.chat(user_message):
        print(content, end="", flush=True)
    print("\n")

    # Terminate the model
    ai_model.terminate()
