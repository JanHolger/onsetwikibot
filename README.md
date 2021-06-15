# onsetwikibot
A discord bot written in python 3 allowing to search the Onset Developer Wiki

## Usage
At the moment i'm not hosting a public instance of it but you can run it on your own machine!

### Running it yourself
1. [Create a Discord Bot Account](https://discordpy.readthedocs.io/en/stable/discord.html#creating-a-bot-account)
2. Set your bot token using the env variable DISCORD_BOT_TOKEN or using the .env file
3. Install the dependencies using `pip3 install -r requirements.txt`
4. Run the Bot using `python3 onsetwikibot.py`
5. Invite it to your server and check if it works using the configured command (`$wiki` by default)

### Available commands
Command        | Description
-------------- | --------------
$wiki          | Shows the info and usage
$wiki [search] | Search for pages, use * as a wildcard
$wiki [page]   | Shows the docs of a specific command or event

## Credits
This bot depends on some awesome libraries!
- [discord.py](https://github.com/Rapptz/discord.py)
- [mwclient](https://github.com/mwclient/mwclient)
- [html2markdown](https://github.com/dlon/html2markdown)
- [python-dotenv](https://github.com/theskumar/python-dotenv)