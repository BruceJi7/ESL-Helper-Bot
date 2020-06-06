import discord, random, os
import setENV
from discord.ext import commands

### ESL-Helper-Bot by Tobias 'Bruce Ji ###
### Other projects at https://github.com/BruceJi7 ###


client = commands.Bot(command_prefix = '.')


# These commands handle loading and unloading things from the cogs file.
@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command(hidden=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# Load the cogs - the bot's modular capabilities
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded cogs from {filename}')



client.run(os.environ.get('BOT_KEY'))