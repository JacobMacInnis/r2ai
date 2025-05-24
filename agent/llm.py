from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI


def get_llm(model_choice: str):
    if model_choice == "ollama":
        return OllamaLLM(model="mistral")
    elif model_choice == "gpt":
        return ChatOpenAI(model="gpt-3.5-turbo")
    else:
        raise ValueError(f"Unsupported model: {model_choice}")
