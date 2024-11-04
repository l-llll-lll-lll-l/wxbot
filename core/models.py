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
        self.known_info = []

    def chat(self, message, stream=True):
        """
        Generate chat completion from the model.

        Parameters:
            message (str): The user's input message.
            stream (bool): Whether to stream the response.

        Yields:
            str: Each segment of the response as it is generated.
        """
        messages = [{"role": "system", "content": '\n'.join(self.known_info)}] + [{"role": "user", "content": message}]
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
