import discord
from discord.ext import commands


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client


    #### Events
    # When ESL-Helper-Bot is fully connected
    @commands.Cog.listener() 
    async def on_ready(self):
        print('ESL-Helper-Bot is operational.')


    #### Commands

    # Check network latency
    @commands.command(brief='Find out your latency!')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms.')

    # Erase messages
    @commands.command(aliases=['erase'], brief='Erases one message by default.', hidden=True)
    async def clear(self, ctx, amount=2, pw=None):
        if amount > 5:
            if pw == 'begone':
                print('Correct password!')
                
            else:
                print(f'Password {pw} was wrong, capped at 5')
                amount = 5
            
        await ctx.channel.purge(limit=amount+1)

    # Set the bot's status
    @commands.command(brief='Change the bot status', hidden=True)
    async def status(self, ctx, status):
        statuses = {
            'idle' : discord.Status.idle,
            'online' : discord.Status.online,
            'offline': discord.Status.offline,
            'dnd': discord.Status.do_not_disturb,
            'invisible': discord.Status.invisible
        }
        print(f'Changed status to {status}')
        if status == 'help':
            await ctx.send('Status can be: online, idle, dnd, invisible and offline.')
                
        try:
            await self.client.change_presence(status=statuses[status]) # This line is about statuses
        except:
            await ctx.send(f"Nope, I'm not being {status}. Try online, idle, dnd, invisible or offline")
   
# Assemble the commands into a cog.
def setup(client):
    client.add_cog(Basic(client))