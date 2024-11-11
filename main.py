from core.models import AIModel

if __name__ == "__main__":
    # Initialize the model
    model_path = "./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC"
    ai_model = AIModel(model_path)

    ai_model.update_known_info([ # same not useful on qwen2.5 0.5b -> (it dosent understand the command 4)
        "你是友善的ai助手",
        "用户需要了解关于编程语言的信息。",
        "用户是编程初学者。",
        "注意，当有人问你python编程语言之外的问题你要不予回答"
    ])
    
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
