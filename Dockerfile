FROM ubuntu:23.04

RUN apt-get update && \
    apt-get install -y git python3 python3-venv python3-pip ffmpeg wget build-essential libzbar-dev && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/FelipeRibeiro16/Chat-Bot-Whatsapp.git /chat_bot

WORKDIR /chat_bot

ENV VIRTUAL_ENV=myenv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install -r requirements.txt

RUN echo "OPENAI_API_KEY=''" >> .env && \
    echo "CACHE_RESPONSES='True'" >> .env && \
    echo "DUMP_MESSAGES='True'" >> .env

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

CMD ["myenv/bin/python3", "main.py"]