import os
os.environ['MLC_LLM_HOME'] = "./"

from mlc_llm import MLCEngine
if __name__ == "__main__":
    # Create engine
    model = "./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC"
    engine = MLCEngine(model)

    # Run chat completion in OpenAI API.
    for response in engine.chat.completions.create(
        messages=[{"role": "user", "content": "你是谁?"}],
        model=model,
        stream=True,
    ):
        for choice in response.choices:
            print(choice.delta.content, end="", flush=True)
    print("\n")

    engine.terminate()
