from mwclient import Site
import html2markdown
import re
import discord
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

command = os.getenv('DISCORD_BOT_COMMAND')
if command == None or len(command) == 0:
    command = '$wiki'

def tomd(html):
    text = re.sub(r'<!--[\s\S]*-->', '', html)
    text = re.sub(r'<div.*>', '', text, 1)[:-6]
    text = re.sub(r'(<span( [a-z]*="[A-Za-z0-9\-_ ]*")*>)|(</span>)', '', text)
    text = re.sub(r'(<div( [a-z]*="[A-Za-z0-9\-_ ]*")*>)|(</div>)', '', text)
    text = re.sub(r'<pre>', '```lua\n', text)
    text = re.sub(r'</pre>', '```', text)
    text = re.sub(r'<table.*>[\s\S]*</table>', '', text)
    text = html2markdown.convert(text)
    text = re.sub(r'(<a( [a-z]*="[A-Za-z0-9\-_ ]*")*>)|(</a>)', '', text)
    text = re.sub(r'\n[ \t]*\* ', '\n', text)
    return text

def todiscord(text):
    def replaceLinks(source):
        link = source.group(2).split(' ')[0]
        if not link.startswith('http'):
            link = 'https://dev.playonset.com' + link
        return source.group(1) + ' (' + link + ')'
    text = re.sub(r'\[([A-Za-z0-9\-_ ]*)\]\(([A-Za-z0-9\-_ /:"]*)\)', replaceLinks, text)
    def replaceHeaders(source):
        return '**' + source.group(2) + '**'
    text = re.sub(r'([#]+ )(.*)\n', replaceHeaders, text)
    return text

onsetwiki = Site('dev.playonset.com', path='/')

print('Fetching wiki pages...')
wikipages = []
for p in onsetwiki.allpages():
    wikipages.append(p)
print(str(len(wikipages)) + ' pages fetched!')

def searchwiki(search):
    pages = []
    search = search.replace('*', '.*')
    for p in wikipages:
        if re.search(search, p.page_title):
            pages.append(p)
    return pages

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == command:
        await message.channel.send(embed = discord.Embed(title = 'Onset Wiki Bot', url = 'https://github.com/JanHolger/onsetwikibot', description = 'by Jan Bebendorf aka. JanHolger').add_field(name = 'Usage', value = 'Use `' + command + ' <search>` to search the wiki!'))
    elif message.content.startswith(command + ' '):
        query = message.content[6:]
        results = searchwiki(query)
        if len(results) == 0:
            await message.channel.send(embed = discord.Embed(colour = discord.Colour.red(), title = 'No results found!'))
        elif len(results) == 1:
            await message.channel.send(embed = discord.Embed(title = results[0].page_title, url = 'https://dev.playonset.com/wiki/' + results[0].name, colour = discord.Colour.green())
                .add_field(
                    name = 'Docs',
                    value = '\n' + todiscord(tomd(onsetwiki.get('parse', pageid=results[0].pageid, disableeditsection=True, disabletoc=True)['parse']['text']['*'])),
                    inline = False
                )
            )
        else:
            embed = discord.Embed(title = 'Results for "' + query + '"', url = 'https://dev.playonset.com/index.php?search=' + query, colour = discord.Colour.blue())
            for r in results:
                if(len(embed.fields) == 16):
                    await message.channel.send(embed = embed)
                    embed = discord.Embed(colour = discord.Colour.blue())
                embed.add_field(name = r.page_title, value = 'https://dev.playonset.com/wiki/' + r.name)
            await message.channel.send(embed = embed)

if os.getenv('DISCORD_BOT_TOKEN') == None or len(os.getenv('DISCORD_BOT_TOKEN')) == 0:
    print('Environment variable "DISCORD_BOT_TOKEN" not set! Either set it or create a .env file.')
    exit(1)

print("Starting Bot")
client.run(os.getenv('DISCORD_BOT_TOKEN'))