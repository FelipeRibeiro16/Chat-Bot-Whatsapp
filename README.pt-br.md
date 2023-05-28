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
Em seguida, você deve escanear o código QR que aparece no CMD. Após isso, o bot exibirá a mensagem "Define main chat..." (Definir chat principal...), o que significa que você precisa definir o chat principal enviando uma mensagem para o chat que deseja que seja o chat principal, usando o comando de configuração no método listen_set_main_chat(command). Tenha cuidado, pois depois de definir o chat principal, não será possível alterá-lo até que o bot seja reiniciado, e pode ser perigoso definir um chat principal no qual outras pessoas possam enviar mensagens, então escolha com sabedoria. Depois disso, o bot exibirá a mensagem "'Main chat defined!" (Chat principal definido!). Em seguida, o bot estará pronto para uso.

## Comandos
Os comandos do bot precisam ser escritos com o prefixo "/bot" (isso pode ser alterado no arquivo main.py), por exemplo:
```bash
/bot oi
```
Os comandos são:
- oi: O bot responderá com "Olá, tudo bem?".
- adicionar: O bot listará os chats que não estão arquivados e você deverá escolher um deles para adicionar à lista de chats que o bot ouvirá. Para escolher um chat, você deve enviar o número correspondente no chat, conforme listado pelo bot. Em seguida, o bot responderá com "Adicionado com sucesso!" e, em caso de erro, o bot responderá com "Não foi possível adicionar!" (disponível apenas no chat principal).
- sair: O bot responderá com "Saindo!" e deixará de funcionar (disponível apenas no chat principal).
- figurinha: O bot criará uma figurinha com a última imagem enviada no chat.
- arquivar: O bot arquivará todos os chats (disponível apenas no chat principal).
- arquivar grupo: O bot arquivará todos os chats de grupos (disponível apenas no chat principal).
- arquivar chats: O bot arquivará todos os chats que não são grupos (disponível apenas no chat principal).

E se você enviar uma mensagem com o prefixo "/bot" e o bot não reconhecer o comando ou for digitado em um chat sem permissões, ele responderá com "Não entendi".

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
- [X] Criar figurinha com a última imagem enviada no chat.
- [X] Arquivar todas as conversas.
- [X] Arquivar todas as conversas em grupo.
- [X] Arquivar todas as conversas que não são em grupo.
- [ ] Resumir mensagens.
- [ ] Integração com o ChatGPT.
- [ ] Criar figurinha com o último vídeo enviado no chat.
- [ ] Criar figurinha com o último gif enviado no chat.

## Contribuição
Pull requests são bem-vindos. Para alterações importantes, abra uma issue primeiro para discutir o que você gostaria de mudar.

## Aviso Legal
Este projeto é apenas para fins educacionais. O desenvolvedor não se responsabiliza pelo uso indevido do projeto.