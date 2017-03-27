import discord
import asyncio
from discord.ext import commands
import utils


def setup(bot):
    bot.add_cog(Love(bot))
    print("{} module loaded".format(__file__))

class Love:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def marry(self, ctx, name):
        user = utils.find_user(ctx, name)
        if user == None:
            await self.bot.say("'{}' was not found in '{}'\n"
                                "Try mentioning (write '@<name of target>'"
                                " or use the user's id)"\
                                        .format(name, ctx.message.server)
                                        )
            return
        else:
            rg = self.bot.relationship_graph
            rg.add_node(ctx.message.author.id)
            rg.add_node(user.id)
            rg.add_edge(ctx.message.author.id, user.id)
            await self.bot.say("{} is now married to {}"\
                    .format(ctx.message.author.name, user.name))

    @commands.command(pass_context = True)
    async def divorce(self, ctx, name):
        user = utils.find_user(ctx, name)
        rg = self.bot.relationship_graph
        if user == None:
            await self.bot.say("'{}' was not found in '{}'\n"
                                "Try mentioning (write '@<name of target>'"
                                " or use the user's id)"\
                                        .format(name, ctx.message.server))
            return
        elif rg.has_edge(ctx.message.author.id, user.id):
            rg.remove_edge(user.id, ctx.message.author.id)
            if rg.degree(user.id) is 0:
                print("s")
                rg.remove_node(user.id)
            if rg.degree(ctx.message.author.id) is 0:
                print("s")
                rg.remove_node(user.id)
            await self.bot.say("You're not longer married to '{}'!".format(user.name))
        else:
            await self.bot.say("You were never married to '{}' O.o".format(user.name))

    @commands.command(name = "listmarried", pass_context = True)
    async def list_married(self, ctx):
        if self.bot.relationship_graph.has_node(ctx.message.author.id):
            await self.bot.say(self.bot.relationship_graph.neighbors(ctx.message.author.id))
        else:
            await self.bot.say("You're a dirty pringle always single :c")
        

