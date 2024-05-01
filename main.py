import requests
import discord
import asyncio
from creds import discordChannelID, discordBotToken, twitchClientID, twitchClientSecret

def get_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json()['access_token']

def check_if_live(client_id, oauth_token, channel_name):
    url = 'https://api.twitch.tv/helix/streams'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    params = {'user_login': channel_name}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return 'data' in data and len(data['data']) > 0


class MyBot(discord.Client):
    async def on_ready(self):

        print(f'Logged in as {self.user}!')
        discordChannel = self.get_channel(int(discordChannelID))  # Replace YOUR_CHANNEL_ID with the actual channel ID
        if discordChannel:
            await discordChannel.send('Bot has been started!')
            await discordChannel.send("Checking twitch channels")
                        
            # Replace 'your_client_id' and 'your_client_secret' with your actual Twitch app credentials
            
            oauth_token = get_oauth_token(twitchClientID, twitchClientSecret)

            # Replace 'channel_name' with the Twitch channel you want to check
            channels = [
                "capnkayso", "smofofthewild", "toxicremadi", "invalidssb", "DrewdyBoy",
                "britafilterina", "dags_ssb", "sugarbair", "brookiecookie", "vincentstylo",
                "sevan_ssbm", "that70sdrip", "yumizuro", "figleaff", "docshamrock",
                "hunt3r_robinson", "friendbndew", "themarmix", "scrobatapub", "cassup0p",
                "nicelaces", "meggieboo", "theatrociousgod", "landoslab", "tartylette",
                "soaral", "ellie_puppy", "nikumai", "jerry_the_crab", "hyo24"
            ]

            liveChannels = []

            while True:
                for twitchChannel in channels:
                    is_live = check_if_live(twitchClientID,oauth_token,twitchChannel)
                    if is_live:
                        if twitchChannel not in liveChannels:
                            await discordChannel.send("Noob " + twitchChannel + " has gone live! Watch them here: https://twitch.tv/" + twitchChannel)
                            print("Sent message: Noob " + twitchChannel + " has gone live! Watch them here: https://twitch.tv/" + twitchChannel + "\n")
                            liveChannels.append(twitchChannel)
                    else:
                        #not live
                        if twitchChannel in liveChannels:     
                            liveChannels.remove(twitchChannel)
                            print(twitchChannel + " is offline\n")
                    await asyncio.sleep(5)
                await asyncio.sleep(90)
        else:
            print("discord channel not found")

intents = discord.Intents.default()
intents.messages = True
client = MyBot(intents=intents)
client.run(discordBotToken)    
