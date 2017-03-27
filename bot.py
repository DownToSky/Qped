import discord
import asyncio
from discord.ext import commands
import networkx as nx
import os

class Bot(commands.Bot):
    def __init__(self, **args):
        self.configs = args["configurations"]
        default_prefix = self.configs["prefix"]
        description = self.configs["description"]
        super().__init__(command_prefix = commands.when_mentioned_or(default_prefix), description = description)
        self.TOKEN = args["token"]
        self.EMAIL   = args["email"]
        self.PASSWORD = args["password"]
        self.relationship_graph = nx.Graph()
        self.instantiate_relationships()
        if self.TOKEN == None and (self.EMAIL == None or self.PASSWORD == None):
            raise ValueError("A username and password combination or a token combination" 
                                "is required to connect to Discord server")
        extensions = ["core","love"]
        for e in extensions:
            self.load_extension("command_groups.{}".format(e))


    async def on_ready(self):
        print('Logging in as')
        print(self.user.name.encode('ascii', errors="backslashreplace").decode())
        print(self.user.id.encode("ascii", errors="bachslashreplace").decode())
        print("------------")
        if self.configs["user_status"] != None:
            await self.change_presence(game = discord.Game(name = self.configs["user_status"]))


    def instantiate_relationships(self):
        cwd = [f for f in os.listdir("./") if os.path.isfile(os.path.join("./", f))]
        if "relationships.gml" in cwd:
            self.relationship_graph = nx.read_gml("./relationships.gml")
        else:
            nx.write_gml(self.relationship_graph, "./relationships.gml")



    async def on_message(self, message):
        try:
            await self.process_commands(message)
        except Exception as e:
            print("Command error unhandled")
            print(message.content)
            print(e)
    
    def run(self):
        if self.TOKEN != None:
            super(Bot,self).run(self.TOKEN)
        else:
            super(Bot,self).run(email=self.EMAIL, password=self.PASSWORD)
