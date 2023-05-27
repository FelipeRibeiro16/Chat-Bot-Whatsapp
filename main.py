# %%
import time
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
start_time = time.time()
chat.reply_message(main_chat, msg_bot('Bot', 'Olá! Estou pronto!'))

print('Running...')
while True:
    start_time = time.time()
    chat_atual = chat.listen_chats(corresponded)
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    message = chat.last_message(chat_atual)
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    if not message:
        continue
    if f'{corresponded} figurinha' in chat_atual['last_message']:
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
        if not chat_atual['is_group']:
            chat.reply_message(
                chat_atual, msg_bot('Bot', 'Grupos arquivados com sucesso!'))
            chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} arquivar contatos' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
        chat.archive('chats')
        if chat_atual['is_group']:
            chat.reply_message(
                chat_atual, msg_bot('Bot', 'Contatos arquivados com sucesso!'))
            chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} arquivar' in chat_atual['last_message'] and chat.is_main_chat(chat_atual):
        chat.archive()
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
    print("--- %s seconds ---" % (time.time() - start_time))
# %%
wp.close()
# %%
chat.update()
# %%
chat.__set_main_chat(chat._chats[0])
# %%
chat_atual
# %%
chat._chats
# %%
chat.main_chat
# %%
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
try:
    WebDriverWait(driver, 1).until(
        EC.staleness_of(main_chat['id']))
except TimeoutException:
    print('TimeoutException')
# %%
main_chat
# %%
while True:
    for chats_listening in chat._chats:
        if corresponded in chats_listening['id'].text:
            print(chats_listening['id'].text)
# %%
