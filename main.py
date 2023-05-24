# %%
from bot_modules import whatsapp
wp = whatsapp()
wp.start()
chat = wp.Chat(wp.driver)
# %%
print('Running...')
corresponded = '/bot'
while True:
    chat_atual = chat.listen_chats()
    if corresponded not in chat_atual['last_message']:
        continue
    else:
        message = chat.listen_messages(chat_atual, corresponded)
        if message['message'] == f'{corresponded} sticker':
            if chat.create_sticker(message):
                chat.reply_message(
                    chat_atual, '_*Bot*_: ```Sticker criado com sucesso```')
                chat.mark_as_replied(chat_atual, message)
            else:
                chat.reply_message(
                    chat_atual, '_*Bot*_: ```Falha na criação do sticker```')
                chat.mark_as_replied(chat_atual, message)
        elif message['message'] == f'{corresponded} sair':
            break
        elif message['message'] == f'{corresponded} oi':
            chat.reply_message(chat_atual, '_*Bot*_: ```Olá, tudo bem?```')
            chat.mark_as_replied(chat_atual, message)
        elif message['message'] == f'{corresponded} tchau':
            chat.reply_message(chat_atual, '_*Bot*_: ```Tchau!```')
            chat.mark_as_replied(chat_atual, message)
        elif message['message'] == f'{corresponded} display':
            chat.display()
            chat.reply_message(chat_atual, '_*Bot*_: ```Na tela!```')
            chat.mark_as_replied(chat_atual, message)
        else:
            chat.reply_message(chat_atual, '_*Bot*_: ```Não entendi```')
            chat.mark_as_replied(chat_atual, message)
    if message['message'] == f'{corresponded} sair':
        chat.reply_message(chat_atual, '*Bot*: Saindo!')
        break
# %%
wp.close()
# %%