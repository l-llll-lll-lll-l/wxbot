from mlc_llm import MLCEngine

class AIModel:
    def __init__(self, model_path, memory_size=5):
        """
        Initialize the AI model engine.
        
        Parameters:
            model_path (str): Path to the model file.
        """
        self.model_path = model_path
        self.engine = MLCEngine(self.model_path)
        self.known_info = []
        self.memory_size = memory_size
        self.chat_history = []

    def chat(self, message, stream=True):
        """
        Generate chat completion from the model.

        Parameters:
            message (str): The user's input message.
            stream (bool): Whether to stream the response.

        Yields:
            str: Each segment of the response as it is generated.
        """
        self.chat_history.append({"role": "user", "content": message})
        if len(self.chat_history) > self.memory_size:
            self.chat_history = self.chat_history[-self.memory_size:]

        messages = [{"role": "system", "content": '\n'.join(self.known_info)}] + self.chat_history # history same not useful on qwen2.5 0.5b ->（has effect but not so well）
        for response in self.engine.chat.completions.create(messages=messages, model=self.model_path, stream=stream):
            for choice in response.choices:
                yield choice.delta.content

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
        Terminate the engine and free resources.
        """
        self.engine.terminate()
