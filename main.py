# %%
from bot_modules import whatsapp
from bot_modules import chat as chat_module
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
corresponded = '/bot'
if chat.listen_set_main_chat(f'{corresponded} principal'):
    print('Chat principal definido com sucesso!')
main_chat = chat.main_chat
chat.reply_message(main_chat, msg_bot('Bot', 'Olá! Estou pronto!'))
print('Running...')
while True:
    chat_atual = chat.listen_chats(corresponded)
    message = chat.last_message(chat_atual)
    if not message:
        continue
    if f'{corresponded} adicionar' in chat_atual['last_message']:
        chat.list_chats()
        chat.reply_message(main_chat, msg_bot(
            'Bot', 'Selecione o contato ou grupo?'))
        chat.mark_as_replied(chat_atual, message)
        chat_escolhido = chat.listen_messages(
            main_chat, 'Selecione o contato ou grupo')['message']
        if chat_escolhido in chat.title_of_chats.keys():
            if chat.new_chat(chat.title_of_chats[chat_escolhido]):
                chat.reply_message(main_chat, msg_bot(
                    'Bot', 'Adicionado com sucesso!'))
                chat.mark_as_replied(main_chat, message)
            else:
                chat.reply_message(main_chat, msg_bot(
                    'Bot', 'Não foi possível adicionar!'))
                chat.mark_as_replied(main_chat, message)
        else:
            chat.reply_message(main_chat, msg_bot(
                'Bot', 'Contato ou grupo não encontrado!'))
            chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} figurinha' in chat_atual['last_message']:
        if chat.create_sticker():
            chat.reply_message(
                chat_atual, msg_bot('Bot', 'Sticker criado com sucesso!'))
            chat.mark_as_replied(chat_atual, message)
        else:
            chat.reply_message(
                chat_atual, msg_bot('Bot', 'Não foi possível criar o sticker!'))
            chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} arquivar grupos' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
        chat.archive('groups')
        chat.reply_message(
            chat_atual, msg_bot('Bot', 'Grupos arquivados com sucesso!'))
        chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} arquivar contatos' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
        chat.archive('chats')
        chat.reply_message(
            chat_atual, msg_bot('Bot', 'Contatos arquivados com sucesso!'))
        chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} arquivar' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
        chat.archive()
        chat.reply_message(chat_atual, msg_bot(
            'Bot', 'Conversas arquivadas com sucesso!'))
    elif f'{corresponded} sair' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
        chat.reply_message(chat_atual, msg_bot('Bot', 'Saindo...'))
        chat.mark_as_replied(chat_atual, message)
        break
    elif f'{corresponded} oi' in chat_atual['last_message']:
        chat.reply_message(chat_atual, msg_bot('Bot', 'Olá! Tudo bem?'))
        chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} display' in chat_atual['last_message']:
        chat.display()
        chat.reply_message(chat_atual, msg_bot('Bot', 'Na tela!'))
        chat.mark_as_replied(chat_atual, message)
    else:
        chat.reply_message(chat_atual, msg_bot('Bot', 'Não entendi!'))
        chat.mark_as_replied(chat_atual, message)

# %%
wp.close()
# %%
