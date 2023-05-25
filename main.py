# %%
from bot_modules import whatsapp
from bot_modules import chat as chat_module
wp = whatsapp()
wp.start()
driver = wp.driver
chat = chat_module(driver)
# %%
print('Running...')
corresponded = '/bot'
while True:
    chat_atual = chat.listen_chats(corresponded)
    message = chat.listen_messages(chat_atual, chat_atual['last_message'])
    if f'{corresponded} sticker' in chat_atual['last_message']:
        if chat.create_sticker(message):
            chat.reply_message(
                chat_atual, '_*Bot*_: ```Sticker criado com sucesso```')
            chat.mark_as_replied(chat_atual, message)
        else:
            chat.reply_message(
                chat_atual, '_*Bot*_: ```Falha na criação do sticker```')
            chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} sair' in chat_atual['last_message']:
        chat.reply_message(chat_atual, '*Bot*: Saindo!')
        chat.mark_as_replied(chat_atual, message)
        break
    elif f'{corresponded} oi' in chat_atual['last_message']:
        chat.reply_message(chat_atual, '_*Bot*_: ```Olá, tudo bem?```')
        chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} tchau' in chat_atual['last_message']:
        chat.reply_message(chat_atual, '_*Bot*_: ```Tchau!```')
        chat.mark_as_replied(chat_atual, message)
    elif f'{corresponded} display' in chat_atual['last_message']:
        chat.display()
        chat.reply_message(chat_atual, '_*Bot*_: ```Na tela!```')
        chat.mark_as_replied(chat_atual, message)
    else:
        chat.reply_message(chat_atual, '_*Bot*_: ```Não entendi```')
        chat.mark_as_replied(chat_atual, message)
# %%
wp.close()
# %%
