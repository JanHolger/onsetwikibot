FROM gorialis/discord.py:alpine-master

RUN mkdir /bot
COPY * /bot/
WORKDIR /bot
RUN pip3 install -r requirements.txt

CMD python3 onsetwikibot.py