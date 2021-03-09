import discord
import config
import aiohttp
import os

from discord.ext import commands, tasks

class Summarize(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['s', 'sum', 'short', 'check', 'shorten'])
    async def summarize(self, ctx, *, args:str=None):
        if args is None:
            await ctx.reply("🔭 `You must supply something to summarise.`")
            return

        payload = {}

        # Check if it's a message
        if args.lower().startswith("https://discord.com/channels/") and len(args.split(" ")[0].split("/")) == 7:
            try:
                splitted = args.split(" ")[0].split("/")
                
                server = self.bot.get_guild(int(splitted[4]))
                channel = server.get_channel(int(splitted[5]))

                msg = await channel.fetch_message(int(splitted[6]))

                payload['txt'] = msg.content

                try:
                    payload['sentences'] = str(int(args.split(" ")[1]))
                except (IndexError, ValueError):
                    payload['sentences'] = "3"
            except (IndexError, discord.errors.NotFound):
                await ctx.reply("🔭 `That message link didn't seem to work.`")
                return


        # Check if it's a link
        elif args.lower().startswith("http://") or args.lower().startswith("https://"):
            payload['url'] = args.split(" ")[0]
            try:
                payload['sentences'] = str(int(args.split(" ")[1]))
            except (IndexError, ValueError):
                payload['sentences'] = "3"

        # Check if it's a channel
        # if args.startswith("")

        else:
            payload['txt'] = args
            payload['sentences'] = "3"

        if payload == {}:
            await ctx.reply("🔭 `Your input was not recognised.`")
            return

        headers = {
            'accept': "application/json",
            'x-rapidapi-key': os.environ.get("TELESCOPE_API"),
            'x-rapidapi-host': "meaningcloud-summarization-v1.p.rapidapi.com"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://meaningcloud-summarization-v1.p.rapidapi.com/summarization-1.0", headers=headers, params=payload) as r:
                js = await r.json()
                if js['status']['msg'] == "OK" and 'summary' in js.keys():
                    await ctx.reply(js['summary'][:2000])
                else:
                    await ctx.reply(f"🔭 `{js['status']['msg'][:2000]}`")



def setup(bot):
    bot.add_cog(Summarize(bot))