import os
import discord
import logging
import datetime
import re

# regex from https://stackoverflow.com/a/3809435/5013267
RE_URL = r"(?:http(s)?:\/\/.)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)"

logging.basicConfig(level=logging.INFO)

if "AUTH_TOKEN" in os.environ:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
else:
    with open("auth.txt", "r") as f:
        AUTH_TOKEN = f.read().strip()

def correct(msg):
    """
    WARNING: does not sanitise at this stage for comparison purposes
    """
    ret = ""
    for word in re.split(r"(" + RE_URL + r"|.+?\b)", msg):
        if word is None:
            continue

        if len(word.strip()) > 2:
            if all((
                not word.isupper(),
                not re.fullmatch(RE_URL, word),
                not (word[-1] in ['s', 'z'] and word[:-1].isupper()),
            )):
                word = word[0] + word[1:].lower()
        ret += word
    return ret

def sanitise(msg):
    # surround @ characters with ZWSP for safety
    return msg.replace("@", "\u200b@\u200b")

def quote_text(msg):
    txt = ""
    for line in msg.splitlines(keepends=True):
        txt += "> " + sanitise(line)
    return txt

class BotClient(discord.Client):
    async def login(self, *args, **kwargs):
        await super().login(AUTH_TOKEN, bot=True)

    async def on_ready(self):
        logging.info("Logged in as {}".format(self.user.name))

        await self.change_presence(activity=discord.Game("git.io/JtZ5T"))
        logging.info("Changed presence")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.author.bot:
            return

        # if message.author.id != "REDACTED": return

        logging.info("{}: Message: {}".format(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), message.content))

        corrected_msg = correct(message.content)
        if message.content != corrected_msg:
            txt = ""
            txt += message.author.mention + "\n"
            txt += quote_text(message.content)

            txt += "\n\nCorrected:\n"
            txt += quote_text(corrected_msg)

            await message.channel.send(txt)
            logging.info("corrected")
        else:
            logging.info("no correcting needed")

if __name__ == '__main__':
    client = BotClient()
    client.run()
