# %%
import os
import openai
from pathlib import Path
from dotenv import load_dotenv
from .chat_handle import load_json
load_dotenv()
openai.organization = "org-kyZVuvjYUDhFwFWSa6dkVdBK"
openai.api_key = os.getenv("OPENAI_API_KEY")

WORK_DIRECTORY = os.getcwd()

CHAT_RESPONSE_ROLE = load_json(
    Path(f'{WORK_DIRECTORY}/data/bot-config/chat_response_role.json'))
MESSAGE_SUMMARY_ROLE = load_json(
    Path(f'{WORK_DIRECTORY}/data/bot-config/message_summary_role.json'))
# %%


def get_chat_response(input_chat: str, model_response: str = "gpt-3.5-turbo"):
    """Get a response from the OpenAI API
    Args:
        input_chat (str): The input chat
        model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
    Returns:
        str: The response
    """
    response = openai.ChatCompletion.create(
        model=model_response,
        messages=CHAT_RESPONSE_ROLE +
        [
            {"role": "user", "content": input_chat}
        ]
    )
    return response.choices[0].message.content.strip()


def message_summary(input_chat: list[str], model_response: str = "gpt-3.5-turbo"):
    """Get a summary from the OpenAI API
    Args:
        input_chat (list[str]): The input chat
        model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
    Returns:
        str: The response
    """
    response = openai.ChatCompletion.create(
        model=model_response,
        messages=MESSAGE_SUMMARY_ROLE + input_chat
    )
    return response.choices[0].message.content.strip()


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
