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
        discordChannel = self.get_channel(discordChannelID)  # Replace YOUR_CHANNEL_ID with the actual channel ID
        if discordChannel:
            await channel.send('Bot has been started!')
            await channel.send("Checking twitch channels")
                        
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
                for channel in channels:
                    is_live = check_if_live(client_id,oauth_token,channel)
                    if is_live:
                        if channel in liveChannels:
                            print("channel found live in live channels, continue through")
                        elif channel in channels:
                            #offline channel just wnet live send message to discord and move to live channels
                            print(channel + " is live\n")
                            await client.send_message(channel)
                            channels.remove(channel)
                            liveChannels.append(channel)
                    else:
                        #not live
                        if channel in liveChannels:
                            #channel is not live but in live channel -> move back to channels
                            liveChannels.remove(channel)
                            channels.append(channel)
                        print(channel + " is offline\n")      
                await asyncio.sleep(90)
        else:
            print("Channel not found")

    async def send_message(self,name):
        print("sending message:")
        channel = self.get_channel(discordChannelID)
        if channel:
           await channel.send("Noob " + name + " has gone live! Watch them here: https://twitch.tv/" + name)

intents = discord.Intents.default()
intents.messages = True
client = MyBot(intents=intents)
client.run(discordBotToken)    
