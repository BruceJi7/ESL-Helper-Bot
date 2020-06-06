import discord
from discord.ext import commands
from naver_dict_tools import *
from dict_com_tools import *
from docx_tools import writeMessageListToDoc
from datetime import datetime


class ESLCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Get Dict.com definition
    @commands.command(aliases=['dict'], brief='Get definition from Dictionary.com')
    async def define(cself, ctx, *, search_word):
        print(f'Command: define - Performing English word meaning search for {search_word} on Dictionary.com...')

        definition = formatDictcomResponse(getDefinitionFromDictSite(search_word))

        response = f'Command .define\nDictionary.com results for English word {search_word}:\n{definition}'
        
        await ctx.send(response)

    # Get a link to a word on dict.com
    @commands.command(brief="Get link to Dictionary.com page for a word.")
    async def dictlink(self, ctx, *, search_word):
        print(f'Command: dictlink, terms: {search_word}')
        
        response = getDictLink(search_word)

        await ctx.send(response)
    
    # Get a link to a word on Naver
    @commands.command(brief="Get link to Naver Dict page for a word.")
    async def naverlink(self, ctx, *, search_word):
        print(f'Command: naverlink, terms: {search_word}')
        
        response = f'Command .naverlink\n{getNaverDictLink(search_word)}'

        await ctx.send(response)

    # Get the English meanings for a Korean word
    @commands.command(aliases=['K2E', 'k2e'], brief='(.K2E word) Get English meanings for a Korean word')
    async def korean_to_english(self, ctx, *, search_word):

        print(f'Command: K2E - Performing Korean into English search for {search_word} on Naver...')

        result = getNaverDef_KORintoENG(search_word)

        if result:
            EngMeaning = formatNaverResponse(result)
            response = f'Command .K2E\nNaver results for Korean word {search_word}:\n{EngMeaning}'
           
        else:
            response = f'fCommand .K2E\nNaver results for Korean word {search_word}:\n\nSearch failed - no results returned.'

        await ctx.send(response)
    # Get the Korean meanings for an English word
    @commands.command(aliases=['E2K', 'e2k'], brief='(.E2K word) Get Korean meanings for an English word')
    async def english_to_korean(self, ctx, *, search_word):

        print(f'Command: E2K - Performing English into Korean search for {search_word} on Naver...')
        result = getNaverDef_ENGintoKOR(search_word)

        if result:

            KorMeaning = formatNaverResponse(result)
            response = f'Command .E2K\nNaver results for English word {search_word}:\n{KorMeaning}'
    
        else:
            response = f'Command .E2K\nNaver results for English word {search_word}:\n\nSearch failed - no results returned.'
        await ctx.send(response)

    # Save the Discord message history into a .docx file
    @commands.command(brief='Save last 20 messages to .docx. Option: Add number of messages to go back',)
    async def makenotes(self, ctx, number=20):

        # Get the messages from the channel
        messages = await ctx.history(limit=abs(int(number))).flatten()

        # Create title for document - .docx extension is added later
        users = list(set([m.author.name for m in messages if m.author.bot == False]))
        datestamp = datetime.strftime(datetime.today(), '%Y-%m-%d')
        document_title = f"{datestamp} {' '.join(users)}"

        # Get the text content of the messages only
        note_content = [m.content for m in messages]
        note_content.reverse()

        # Write the messages into a docx file
        writeMessageListToDoc(note_content, document_title)


def setup(client):
    client.add_cog(ESLCog(client))