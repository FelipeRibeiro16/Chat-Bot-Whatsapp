# Chat Bot WhatsApp
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/FelipeRibeiro16/Chat-Bot-Whatsapp/blob/d8987a06d7b5a4796090d6b2fd5dc8e2e01ce6af/README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/FelipeRibeiro16/Chat-Bot-Whatsapp/blob/d8987a06d7b5a4796090d6b2fd5dc8e2e01ce6af/README.pt-br.md)
## Description
This project is a chat bot for WhatsApp, it is a bot that can be used to send messages, create stickers and archive chats. This project is made with the help of the [selenium](https://www.selenium.dev/) library, which is a library that allows us to automate the browser, in this case we use it to automate WhatsApp.

## Installation
To install the project you must have python 3.8 or higher installed, then you must install the dependencies with the following command:
```bash
pip install -r requirements.txt
```

## Usage
To use the project you must run the main.py file with the command:
```bash
python main.py
```
Then you must scan the QR code that appears in the CMD and that's it, you can use the bot on any chat in WhatsApp.

## Commands
The commands of the bot need to be written with the prefix "/bot", for example:
```bash
/bot oi
```
The commands are:
- oi: The bot will respond with "Olá, tudo bem?".
- sair: The bot will respond with "Saindo!" and will stop running.
- sticker: The bot will create a sticker with the last image sent in the chat.
- arquivar: The bot will archive all chats.
- arquivar grupo: The bot will archive all groups chats.
- arquivar chats: The bot will archive all chats there are not groups.

and if you send a message with the prefix "/bot" and the bot does not recognize the command, it will respond with "Não entendi".

## Files and folders
- The main.py file uses the modules of the project to run the bot.
- The folder bot_modules contains the modules of the project.
- The whatsapp.py present in the folder bot_modules file contains the modules that is responsible for automating WhatsApp.
- The folder data contains the files that are used to store data, such as chrome cookies and the bot's download folder.
- And the .wdm folder contains the chromedriver that is used to automate the browser.

## Modules
The modules of the project are:
- whatsapp: This module is responsible for starting the browser and closing it.
- chat: This module is responsible for automating the chat, such as sending messages, creating stickers and archiving chats.

## TODO
- [X] Create a sticker with the last image sent in the chat.
- [X] Archive all chats.
- [X] Archive all groups chats.
- [X] Archive all chats there are not groups.
- [ ] Create a sticker with the last video sent in the chat.
- [ ] Create a sticker with the last gif sent in the chat.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer
This project is for educational purposes only, the developer is not responsible for the misuse of the project.