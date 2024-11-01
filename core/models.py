from mlc_llm import MLCEngine

class AIModel:
    def __init__(self, model_path):
        """
        Initialize the AI model engine.
        
        Parameters:
            model_path (str): Path to the model file.
        """
        self.model_path = model_path
        self.engine = MLCEngine(self.model_path)

    def chat(self, message, stream=True):
        """
        Generate chat completion from the model.

        Parameters:
            message (str): The user's input message.
            stream (bool): Whether to stream the response.

        Yields:
            str: Each segment of the response as it is generated.
        """
        messages = [{"role": "user", "content": message}]
        for response in self.engine.chat.completions.create(messages=messages, model=self.model_path, stream=stream):
            for choice in response.choices:
                yield choice.delta.content

    def terminate(self):
        """
        Terminate the engine and free resources.
        """
        self.engine.terminate()
