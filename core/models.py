from .ollama_engine import OllamaEngine  
import json

class AIModel:
    def __init__(self, model_name, base_url="http://localhost:11434", memory_size=5):
        """
        Initialize the AI model engine.

        Parameters:
            model_name (str): Name of the model on the Ollama server.
            base_url (str): Base URL of the Ollama server.
        """
        self.model_name = model_name
        self.engine = OllamaEngine(base_url, model_name)
        self.known_info = []
        self.memory_size = memory_size

    def chat_stream(self, message):
        """
        Generate chat completion from the model.

        Parameters:
            message (str): The user's input message.
            stream (bool): Whether to stream the response.

        Yields:
            str: Each segment of the response as it is generated.
        """
        messages = [{"role": "system", "content": '\n'.join(self.known_info)}] + [{"role": "user", "content": message}]
        
        for response in self.engine.create_completion(messages=messages, stream=True):
            yield response

    def chat(self, message):
        """
        Generate chat completion from the model without streaming.

        Parameters:
            message (str): The user's input message.

        Returns:
            str: The response from the model.
        """
        response = [json.loads(i)["message"]["content"] for i in self.chat_stream(message)]
        response = ''.join(response)
        return response

    def update_known_info(self, new_info):
        """
        Update the known information.

        Parameters:
            new_info (list): A list of strings representing the new known information.
        """
        self.known_info = new_info

    def add_to_known_info(self, additional_info):
        """
        Add new information to the existing known information.

        Parameters:
            additional_info (str or list): A string or list of strings to add to the known information.
        """
        if isinstance(additional_info, str):
            self.known_info.append(additional_info)
        elif isinstance(additional_info, list):
            self.known_info.extend(additional_info)

    def terminate(self):
        """
        Terminate the engine (not required for Ollama).
        """
        pass  # Ollama doesn't require explicit termination

if __name__ == "__main__":
    model = AIModel(model_name="qwen2.5:0.5b")

    # 更新已知信息
    model.add_to_known_info("This is a known fact.")

    # 生成对话
    user_input = "What is your knowledge on AI?"
    print(model.chat(user_input))
    # 释放资源（如果需要）
    
    model.terminate()
