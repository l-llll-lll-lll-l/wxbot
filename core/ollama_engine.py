import requests

class OllamaEngine:
    def __init__(self, base_url="http://localhost:11434", model_name="model_name"):
        """
        Initialize the Ollama engine.

        Parameters:
            base_url (str): The base URL of the Ollama server.
            model_name (str): The name of the model to use.
        """
        self.base_url = base_url
        self.model_name = model_name

    def create_completion(self, messages, stream=True):
        """
        Send a completion request to the Ollama server.

        Parameters:
            messages (list): A list of messages in the format [{"role": "user/system", "content": "..."}].
            stream (bool): Whether to stream the response.

        Yields:
            str: Each segment of the response as it is generated.
        """
        url = f"{self.base_url}/api/chat"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": stream,
        }

        response = requests.post(url, json=payload, headers=headers, stream=True)
        
        if response.status_code != 200:
            raise RuntimeError(f"Ollama server error: {response.text}")
        
        if stream:
            for line in response.iter_lines():
                if line:
                    yield line.decode("utf-8")
        else:
            yield response.json().get("text", "")
