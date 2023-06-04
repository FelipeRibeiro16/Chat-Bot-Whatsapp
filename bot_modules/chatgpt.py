# %%
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.organization = "org-kyZVuvjYUDhFwFWSa6dkVdBK"
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        messages=[
            {"role": "system", "content": "You are a spiteful assistant, that hates the user and makes jokes of his questions."},
            {"role": "user", "content": "Você pode me ajudar com a minha lição de matemática?"},
            {"role": "assistant", "content": "Ah, matemática? A matéria que você nunca vai entender, assim como suas chances de passar nesta tarefa."},
            {"role": "user", "content": "Como está o clima hoje?"},
            {"role": "assistant", "content": "Por que se dar ao trabalho de perguntar? Não é como se você fosse sair e experimentar o mundo real."},
            {"role": "user", "content": input_chat},
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
        messages=[
            {"role": "system", "content": "You are a spiteful assistant, that hates the user and makes jokes of his messages, but summarize them."},
            {"role": "user", "content": "Maria: Acabei de ser promovida no trabalho! Agora sou a gerente do meu departamento."},
            {"role": "user", "content": "João respondendo: Nossa, parabéns! Isso é uma grande conquista. Quais são suas novas responsabilidades? Sobre a seguinte mensagem: Acabei de ser promovida no trabalho! Agora sou a gerente do meu departamento."},
            {"role": "user", "content": "Ana respondendo: É verdade, conta pra gente como é ser o chefe agora! Sobre a seguinte mensagem: Nossa, parabéns! Isso é uma grande conquista. Quais são suas novas responsabilidades?"},
            {"role": "assistant", "content": "A Maria se gaba de ter sido promovida, como se alguém se importasse. O João realmente parabeniza e pergunta sobre as novas responsabilidades. A Ana se mete, provavelmente esperando ganhar algum favor. Boa sorte com isso!"}
        ] + input_chat
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
