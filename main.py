#!/usr/local/bin/python3.6
import os
import discord
import asyncio
import re
import requests
import json

client_id = os.environ['DISCORD_CLIENT_ID']
secret_id = os.environ['DISCORD_SECRET_ID']

client = discord.Client()

channels = ['buying-selling', 'siring', 'price-discussions', 'market-discussions', 'collectors', 'voice-text-nsfw', 'voice-text-sfw']
cooldown_map = {0:'Fast', 1:'Swift', 2:'Snappy', 3:'Brisk', 
				4:'Plodding', 5:'Slow', 6:'Sluggish', 7:'Catatonic'}

@client.event
async def on_ready():
	print ("Bot Online")
	print ("Name: {}".format(client.user.name))
	print ("ID: {}".format(client.user.id))


@client.event
async def on_message(message):
	regex = re.search('https://www.cryptokitties.co/kitty/([0-9]+)', message.content)
	if bool(regex) and message.channel.name in channels and message.author:
		kitty_id = regex.group(1)

		r = requests.get("https://api.cryptokitties.co/kitties/{}".format(kitty_id))
		if r.status_code != requests.codes.ok:
			return 1	
		
		kitty_info = r.json()
		cooldown = ""
		_range = [x for x in range(0, 8)]
		if kitty_info['status']['cooldown_index'] not in _range:
			cooldown = "N/A"
		else:
			cooldown = cooldown_map[kitty_info['status']['cooldown_index']]
	
		# CHange this when updated
		cooldown = "ToBeUpdated"

		msg = "```Kitty#: {}    FancyType: {}    Gen: {}    Cooldown: {}\n".format(
                        kitty_info['id'], kitty_info['fancy_type'], kitty_info['generation'],
                        cooldown)

		if not kitty_info['is_fancy']:
			
			cattributes = [cattribute['description'] for cattribute in kitty_info['cattributes']]
			msg = "{}Cattributes: {}```".format(msg, cattributes)

		else:
			msg = "{}```".format(msg)
		
		await client.send_message(message.channel, msg)


client.run(secret_id)

