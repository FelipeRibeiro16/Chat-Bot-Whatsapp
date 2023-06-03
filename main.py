# %%
from bot_modules import whatsapp
from bot_modules import chat as chat_module
from bot_modules import chat_processor, message_processor
import os
import time
from bot_modules import message_summary
from bot_modules import gpt_response
from bot_modules import load_json, save_json, get_closest_match, get_inputs, get_answer, new_input
# %%
wp = whatsapp()
wp.start()
driver = wp.driver
chat = chat_module(driver)
# %%


def msg_bot(bot_name: str, message: str) -> str:
    """Returns a message with the bot name and the message in a code block
    Args:
        bot_name (str): Bot name
        message (str): Message to be sent

    Returns:
        str: Message with the bot name and the message in a code block
    """
    return f'_*{bot_name}*_: ```{message}```'


# %%
chat.reset()
# %%
corresponded = '/bot'
print('Define main chat...')
if chat.listen_set_main_chat(f'{corresponded} principal'):
    print('Main chat defined!')
main_chat = chat.main_chat
chat.reply_message(main_chat, msg_bot('Bot', 'Olá! Estou pronto!'))
print('Running...')
while True:
    chat.rest()
    chat_atual = chat.listen_chats(corresponded)
    message = chat.last_message(chat_atual)
    if not message:
        continue

    answers = load_json(r'data\messages\answers.json')

    input = message_processor(chat_atual['last_message'], corresponded)

    inputs = get_inputs(answers['answers'])

    match = get_closest_match(input, inputs)

    if match:
        if match == 'resumir' and chat.is_main_chat(chat_atual):
            chat.list_chats()
            chat.reply_message(chat_atual, msg_bot(
                'Bot', 'Qual chat você deseja resumir?'))
            chat.mark_as_replied(chat_atual, message)
            chat_escolhido = chat.listen_messages(
                main_chat, 'Qual chat você deseja resumir?')
            if chat_escolhido['message'] in chat.title_of_chats.keys():
                chat.reply_message(chat_atual, msg_bot(
                    'Bot', 'Extraindo mensagens...'))
                chat.mark_as_replied(chat_atual, chat_escolhido)
                chat.extract_messages(
                    chat.title_of_chats[chat_escolhido['message']])
                chat.reply_message(
                    chat_atual, msg_bot('Bot', 'Processando...'))
                chat_processor(f'{os.getcwd()}\\data\\messages\\messages_extracted.csv',
                               f'{os.getcwd()}\\data\\messages\\messages_process.csv')
                with open(f'{os.getcwd()}\\data\\messages\\messages_process.csv', 'r', encoding='utf-8') as file:
                    messages = file.read()
                chat.reply_message(chat_atual, msg_bot(
                    'Bot', message_summary(messages)))
            else:
                chat.reply_message(chat_atual, msg_bot(
                    'Bot', 'Chat não encontrado!'))
                chat.mark_as_replied(chat_atual, chat_escolhido)
        elif match == 'transcrever':
            transcribe = chat.audio_reader()
            if transcribe:
                chat.reply_message(chat_atual, msg_bot('Bot', transcribe))
                chat.mark_as_replied(chat_atual, message)
            else:
                chat.reply_message(chat_atual, msg_bot(
                    'Bot', 'Não foi possível transcrever!'))
                chat.mark_as_replied(chat_atual, message)
        elif match == 'adicionar':
            chat.list_chats()
            chat.reply_message(main_chat, msg_bot(
                'Bot', 'Selecione o contato ou grupo?'))
            chat.mark_as_replied(chat_atual, message)
            chat_escolhido = chat.listen_messages(
                main_chat, 'Selecione o contato ou grupo')
            if chat_escolhido['message'].strip() in chat.title_of_chats.keys():
                if chat.new_chat(chat.title_of_chats[chat_escolhido['message']]):
                    chat.reply_message(main_chat, msg_bot(
                        'Bot', 'Adicionado com sucesso!'))
                    chat.mark_as_replied(main_chat, chat_escolhido)
                else:
                    chat.reply_message(main_chat, msg_bot(
                        'Bot', 'Não foi possível adicionar!'))
                    chat.mark_as_replied(main_chat, chat_escolhido)
            else:
                chat.reply_message(main_chat, msg_bot(
                    'Bot', 'Contato ou grupo não encontrado!'))
                chat.mark_as_replied(chat_atual, message)
        elif match == 'figurinha':
            if chat.create_sticker():
                chat.reply_message(
                    chat_atual, msg_bot('Bot', 'Sticker criado com sucesso!'))
                chat.mark_as_replied(chat_atual, message)
            else:
                chat.reply_message(
                    chat_atual, msg_bot('Bot', 'Não foi possível criar o sticker!'))
                chat.mark_as_replied(chat_atual, message)
        elif match == 'arquivar grupos' and chat.is_main_chat(chat_atual):
            chat.archive('groups')
            chat.reply_message(
                chat_atual, msg_bot('Bot', 'Grupos arquivados com sucesso!'))
            chat.mark_as_replied(chat_atual, message)
        elif match == 'arquivar contatos' and chat.is_main_chat(chat_atual):
            chat.archive('chats')
            chat.reply_message(
                chat_atual, msg_bot('Bot', 'Contatos arquivados com sucesso!'))
            chat.mark_as_replied(chat_atual, message)
        elif match == 'arquivar' and chat.is_main_chat(chat_atual):
            chat.archive()
            chat.reply_message(chat_atual, msg_bot(
                'Bot', 'Conversas arquivadas com sucesso!'))
        elif match == 'sair' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
            chat.reply_message(chat_atual, msg_bot('Bot', 'Saindo...'))
            chat.mark_as_replied(chat_atual, message)
            time.sleep(1)
            break
        elif match == 'display' and chat.is_main_chat(chat_atual):
            display = chat.display()
            if display:
                chat.reply_message(chat_atual, msg_bot(
                    'Bot', display))
                chat.mark_as_replied(chat_atual, message)
            else:
                chat.reply_message(chat_atual, msg_bot(
                    'Bot', 'Não foi possível exibir!'))
                chat.mark_as_replied(chat_atual, message)
        else:
            response = get_answer(match, answers['answers'])
            chat.reply_message(chat_atual, msg_bot(
                'Bot', response))
            chat.mark_as_replied(chat_atual, message)
    else:
        response = gpt_response(input)
        if response:
            chat.reply_message(chat_atual, msg_bot(
                'Bot', response))
            new_answer = new_input(input, inputs, response)
            if new_answer is None:
                continue
            answers['answers'].append(new_answer)
            save_json(r'data\messages\answers.json', answers)
        else:
            chat.reply_message(chat_atual, msg_bot(
                'Bot', 'Não entendi!'))
        chat.mark_as_replied(chat_atual, message)
# %%
wp.close()
# %%
