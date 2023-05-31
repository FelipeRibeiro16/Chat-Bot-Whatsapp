# %%
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.organization = "org-kyZVuvjYUDhFwFWSa6dkVdBK"
openai.api_key = os.getenv("OPENAI_API_KEY")

# %%


def get_chat_response(input_chat: str, history=str, engine: str = "text-davinci-003", temperature: float = 0.9, max_tokens: int = 150, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0.6, stop: list = ["\n", " Human:", " AI:"]):
    """Get a response from the OpenAI API
    Args:
        input_chat (str): The input chat
        history (str): The history to use
        engine (str, optional): The engine to use. Defaults to "davinci".
        temperature (float, optional): The temperature to use. Defaults to 0.9.
        max_tokens (int, optional): The maximum number of tokens to use. Defaults to 150.
        top_p (float, optional): The top p to use. Defaults to 1.
        frequency_penalty (float, optional): The frequency penalty to use. Defaults to 0.
        presence_penalty (float, optional): The presence penalty to use. Defaults to 0.6.
        stop (list, optional): The stop tokens to use. Defaults to ["\n", " Human:", " AI:"].

    Returns:
        str: The response
    """
    response = openai.Completion.create(
        engine=engine,
        prompt=f"""{history}
        Human: {input_chat}
        AI:""",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    return response.choices[0].text.strip()


def message_summary(input_chat: str, engine: str = "text-davinci-003", temperature: float = 0.9, max_tokens: int = 150, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0.6, stop: list = ["Faça um resumo das seguintes mensagens:", "AI:"]):
    """Get a response from the OpenAI API
    Args:
        input_chat (str): The input chat
        engine (str, optional): The engine to use. Defaults to "davinci".
        temperature (float, optional): The temperature to use. Defaults to 0.9.
        max_tokens (int, optional): The maximum number of tokens to use. Defaults to 150.
        top_p (float, optional): The top p to use. Defaults to 1.
        frequency_penalty (float, optional): The frequency penalty to use. Defaults to 0.
        presence_penalty (float, optional): The presence penalty to use. Defaults to 0.6.
        stop (list, optional): The stop tokens to use. Defaults to ["\n", " Human:", " AI:"].

    Returns:
        str: The response
    """
    response = openai.Completion.create(
        engine=engine,
        prompt=f"""Faça um resumo sobre as seguintes mensagens:
        {input_chat}
        AI:""",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    return response.choices[0].text.strip()


def audio_transcriber(audio_path: str) -> str:
    """Transcribe an audio file using the OpenAI API
    Args:
        audio_path (str): The path to the audio file

    Returns:
        str: The transcript
    """
    audio_file = open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']
