from urllib.request import Request, urlopen
import json
import re
import os
import pathlib
import requests

def getJson(url):
	global data

	requestData = Request(url, headers={'User-agent': 'your bot 0.1'})
	openData = urlopen(requestData).read()

	data = json.loads(openData)

	return data

def replacer(s, newstring, index, nofail=False):
	# raise an error if index is outside of the string
	if not nofail and index not in range(len(s)):
		raise ValueError("index outside given string")

	# if not erroring, but the index is still not in the correct range..
	if index < 0:  # add it to the beginning
		return newstring + s
	if index > len(s):  # add it to the end
		return s + newstring

	# insert the new string between "slices" of the original
	return s[:index] + newstring + s[index + 1:]

collectionList = getJson('http://runemanager.habski.me/api/collection/all') # Fetch list of available bosses

for collection in collectionList:
	if collection["name"] != "goblin":
		imageDir = "/mnt/c/laragon/www/RuneManager-OSRS/public/images/boss" # Path to RuneManager image directory

		pathToImageDir = os.path.join(imageDir, collection["name"].replace(" ", "_"))

		if not os.path.isdir(pathToImageDir):
			os.mkdir(pathToImageDir)

			bossData = getJson('http://runemanager.habski.me/api/hiscore/boss/' + collection["name"].replace(" ", "%20")) # Fetch boss data

			logItems = bossData["data"][0] # We only need the first element

			for item in logItems["log"]:
				item = item.replace("_", " ")

				oldName = item

				splitWords = item.split()

				# Some item names has an ending with 's. The API only returns without apostrophe. To be able to retrieve item icon, we have to append back the apostrophe
				if splitWords[0].endswith('s'):
					if splitWords[0] != "dexterous" and splitWords[0] != "archers" and splitWords[0] != "seers" and splitWords[0] != "bandos" and splitWords[0] != "bottomless" and splitWords[0] != "kronos" and splitWords[0] != "attas" and splitWords[0] != "sarachnis" and splitWords[0] != "skotos" and splitWords[0] != "venenatis" and splitWords[0] != "treasonous":
						if len(splitWords) == 1:
							item = (replacer(splitWords[0], "'s", len(splitWords[0]) - 1))
						elif len(splitWords) == 2:
							item = (replacer(splitWords[0], "'s", len(splitWords[0]) - 1) + ' ' + splitWords[1])
						elif len(splitWords) == 3:
							item = (replacer(splitWords[0], "'s", len(splitWords[0]) - 1) + ' ' + splitWords[1] + ' ' + splitWords[2])

				if (item == "pet kreearra"):
					item = "pet kree%27arra"
				elif (item == "pet kril tsutsaroth"):
					item = "pet k%27ril tsutsaroth"
				elif (item == "lil zik"):
					item = "lil%27 zik"
				elif (item == "vetion jr"):
					item = "vet%27ion jr."

				newItemName = item.replace(" ", "%20").replace("(", "%28").replace(")", "%29").capitalize() # Parse to URL friendly string

				print(newItemName)

				itemData = getJson('http://localhost/items?where=%7B"name":"' + newItemName + '","duplicate":false%7D') # Fetch item data

				itemId = itemData["_items"][0]["id"] # Item ID

				# Download item icon and place it in imageDir
				with open(imageDir + '/' + collection["name"].replace(" ", "_") + '/' + oldName.replace(" ", "_") + '.png', 'wb') as f:
					f.write(requests.get('https://www.osrsbox.com/osrsbox-db/items-icons/' + itemId + '.png').content)