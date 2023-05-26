# Chat Bot WhatsApp
## Descrição
Este projeto é um chat bot para o WhatsApp. É um bot que pode ser usado para enviar mensagens, criar figurinhas e arquivar conversas. Este projeto é feito com a ajuda da biblioteca [selenium](https://www.selenium.dev/), que é uma biblioteca que nos permite automatizar o navegador. Neste caso, usamos para automatizar o WhatsApp.

## Instalação
Para instalar o projeto, você deve ter o Python 3.8 ou superior instalado e, em seguida, instalar as dependências com o seguinte comando:
```bash
pip install -r requirements.txt
```

## Uso
Para usar o projeto, você deve executar o arquivo main.py com o seguinte comando:
```bash
python main.py
```
Em seguida, você deve escanear o código QR que aparece no CMD e pronto, você pode usar o bot em qualquer chat no WhatsApp.

## Comandos
Os comandos do bot devem ser escritos com o prefixo "/bot", por exemplo:
```bash
/bot oi
```
Os comandos são:
- oi: O bot responderá com "Olá, tudo bem?".
- sair: O bot responderá com "Saindo!" e irá parar de ser executado.
- sticker: O bot criará uma figurinha com a última imagem enviada no chat.
- arquivar: O bot arquivará todas as conversas.
- arquivar grupo: O bot arquivará todas as conversas em grupo.
- arquivar chats: O bot arquivará todas as conversas que não são em grupo.

E se você enviar uma mensagem com o prefixo "/bot" e o bot não reconhecer o comando, ele responderá com "Não entendi".

## Arquivos e pastas
- O arquivo main.py usa os módulos do projeto para executar o bot.
- A pasta bot_modules contém os módulos do projeto.
- O arquivo whatsapp.py presente na pasta bot_modules contém os módulos responsáveis por automatizar o WhatsApp.
- A pasta data contém os arquivos que são usados para armazenar dados, como cookies do Chrome e a pasta de download do bot.
- E a pasta .wdm contém o chromedriver que é usado para automatizar o navegador.

## Módulos
Os módulos do projeto são:
- whatsapp: Este módulo é responsável por iniciar o navegador e fechá-lo.
- chat: Este módulo é responsável por automatizar o chat, como enviar mensagens, criar adesivos e arquivar conversas.

## TODO
- [X] Criar um adesivo com a última imagem enviada no chat.
- [X] Arquivar todas as conversas.
- [X] Arquivar todas as conversas em grupo.
- [X] Arquivar todas as conversas que não são em grupo.
- [ ] Criar um adesivo com o último vídeo enviado no chat.
- [ ] Criar um adesivo com o último gif enviado no chat.

## Contribuição
Pull requests são bem-vindos. Para alterações importantes, abra uma issue primeiro para discutir o que você gostaria de mudar.

## Aviso Legal
Este projeto é apenas para fins educacionais. O desenvolvedor não se responsabiliza pelo uso indevido do projeto.