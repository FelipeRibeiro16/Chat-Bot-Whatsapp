# Chat Bot WhatsApp
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/FelipeRibeiro16/Chat-Bot-Whatsapp/blob/master/README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/FelipeRibeiro16/Chat-Bot-Whatsapp/blob/cbb4e521e351c7d2d5a91978953c871917af3146/README.pt-br.md)
## Description
This project is a chat bot for WhatsApp, it is a bot that can be used to send messages, create stickers, archive chats, transcribe audios, summarize chats and use the ChatGPT in the chats. This project is made with the help of the [selenium](https://www.selenium.dev/) library, which is a library that allows us to automate the browser, in this case we use it to automate WhatsApp.

## Installation
To install the project you must have python 3.8 or higher installed, then you must clone the project with the following command:
```bash
git clone https://github.com/FelipeRibeiro16/Chat-Bot-Whatsapp.git
```

After that you must install the FFmpeg, you can download it [here](https://ffmpeg.org/download.html), then you must add the FFmpeg to the PATH of your system if you use windows, you can see how to do it [here](https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10).

Then you must install the dependencies with the following command:
```bash
pip install -r requirements.txt
```

And finnaly to use the ChatGPT you must provide a API key on a .env file in the root of the project, for caching responses and for dump the messages of summarization you must set 'True' or 'False' to not, the .env file must have the following content:
```bash
OPENAI_API_KEY=YOUR_API_KEY
CACHE_RESPONSES='True'
DUMP_MESSAGES='True'
```

You also can modify the personalization of the responses and summarizations of the ChatGPT in the files chat_response_role.json and message_summary_role.json in the folder /data/bot-config.
## Usage
To use the project you must run the main.py file with the command:
```bash
python main.py
```
Then you must scan the QR code that appears in the CMD, after that the bot will display the message "Define main chat...", which means that you have to define the main chat by sending a message to the chat you want to be the main chat with command setting in the method `listen_set_main_chat(command)`, beware that after set the main chat cannot be changed until the bot is restarted, and may be dangerous to set a main chat that others can send messages, so choose wisely. After that the bot will display the message "'Main chat defined!". Then the bot will be ready to use.
## Commands
The commands of the bot need to be written with the prefix "/bot"(this can be changed in the main.py file), for example:
```bash
/bot oi
```
The commands are:
- adicionar: The bot will list the chats there are unarchived and you must choose one of them to add to the list of chats that the bot will listen to. To choose a chat you must send the number of the chat, listed by the bot, after that the bot will respond with "Adicionado com sucesso!", in case of error the bot will respond with "Não foi possível adicionar!" (Only available in the main chat).
- sair: The bot will respond with "Saindo!" and will stop running (Only available in the main chat).
- figurinha: The bot will create a sticker with the last image sent in the chat.
- arquivar: The bot will archive all chats (Only available in the main chat).
- arquivar grupo: The bot will archive all groups chats (Only available in the main chat).
- arquivar chats: The bot will archive all chats there are not groups (Only available in the main chat).
- resumir: The bot will list the chats there are unarchived and you must choose one of them to
summarize the messages. To choose a chat you must send the number of the chat, listed by the bot, after that the bot will respond with "Extraindo mensagens..." and will start to extract the messages, after that the bot will respond with "Processando..." and will start to process the messages, after that the bot will respond with the summarize of the messages (Only available in the main chat).
- transcrever: The bot will transcribe the last audio sent in the chat.

And if you send a message with the prefix "/bot" without a command the bot will use the [ChatGPT] to respond to the message.
## Files and folders
- The main.py file uses the modules of the project to run the bot.
- The folder bot_modules contains the modules of the project.
- The whatsapp.py present in the folder bot_modules file contains the modules that is responsible for automating WhatsApp.
- The whatsapp_chat_processor.py in the folder bot_modules file contains the modules that is responsible for processing the messages of the chat.
- The chatgpt.py in the folder bot_modules file contains the modules that is responsible for using the ChatGPT to respond and summarize the messages.
- The chat_handle.py in the folder bot_modules file contains the modules that is responsible for handling the chat inputs, and find the best answer to the input.
- The folder data contains the files that are used to store data, such as chrome cookies, the bot's download folder, the bot's config files and the bot's messages dump.
- And the .wdm folder contains the chromedriver that is used to automate the browser.

## Modules
The modules of the project are:
- whatsapp: This module is responsible for starting the browser and closing it.
- chat: This module is responsible for automating the chat, such as sending messages, creating stickers and archiving chats.
- chat_processor: This module is responsible for processing the messages of the chat.
- message_summary: This module is responsible for summarizing the messages of the chat using ChatGPT.
- gpt_response: This module is responsible for using the ChatGPT to respond to the messages of the chat.
- transcriber: This module is responsible for transcribing the audios of the chat.
- chat_handle: This module is responsible for handling the chat inputs, and find the best answer to the input. 

## TODO
- [X] Create a sticker with the last image sent in the chat.
- [X] Archive all chats.
- [X] Archive all groups chats.
- [X] Archive all chats there are not groups.
- [X] Summarize messages.
- [X] Integration with ChatGPT.
- [X] Transcribe audios.
- [ ] Create a sticker with the last video sent in the chat.
- [ ] Create a sticker with the last gif sent in the chat.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer
This project is for educational purposes only, the developer is not responsible for the misuse of the project.
