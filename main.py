 
import os
import discord
import logging
import datetime
import json

logging.basicConfig(level=logging.INFO)


if "AUTH_TOKEN" in os.environ:
	AUTH_TOKEN = os.environ["AUTH_TOKEN"]
else:
	with open("auth.txt", "r") as f:
		AUTH_TOKEN = f.read().strip()


def needs_correcting(msg):
	for word in msg.split(" "):
		word = word.strip()
		if len(word) < 2:
			continue

		if any([c.isupper() for c in word[1:]]):
			if not all([c.isupper() for c in word]):
				return True
	return False


class BotClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	async def login(self, *args, **kwargs):
		await super().login(AUTH_TOKEN, bot=True)

	async def on_ready(self):
		logging.info("Logged in as {}".format(self.user.name))

	async def on_message(self, message):
		if message.author == client.user:
			return

		if message.author.bot:
			return

		# if message.author.id != "REDACTED": return

		logging.info("{}: Message: {}".format(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), message.content))
		if needs_correcting(message.content):
			txt = ""
			txt += message.author.mention + "\n"

			for line in message.content.splitlines(keepends=True):
				txt += "> " + line.replace("@", "​@​")

			txt += "\n\nCorrected:\n"

			for line in message.content.splitlines(keepends=True):
				txt += "> " + line.lower().replace("@", "​@​")
			await message.channel.send(txt)
			logging.info("corrected")
		else:
			logging.info("no correcting needed")

if __name__ == '__main__':
	client = BotClient()
	client.run()