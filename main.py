import nextcord
import json
import os
from nextcord.ext import commands

command_info = {
    'help': 'you literally just used it',
    'prefix': 'change the command prefix',
}

client = commands.Bot(command_prefix = 'dont ', help_command = None)

# Events
@client.event
async def on_ready():
    data = await get_data()
    client.command_prefix = data['prefix']

    print(f'Logged in as\n{client.user.name}\n{client.user.id}\n\nPrefix: {client.command_prefix}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = 'hyper sleep'))

# Commands
@client.command()
async def help(ctx):
    embed = nextcord.Embed(title = 'Help', description = 'very cool help command\n(see below for a list of commands)', color = nextcord.Colour.blurple())

    for name, command in command_info.items():
        embed.add_field(name = name, value = command, inline = False)

    await ctx.reply(embed = embed)

@client.command()
async def prefix(ctx, arg = None):
    if arg == None:
        await ctx.reply(f'The current prefix is `{client.command_prefix}`')

    else:
        if arg.endswith(' ') == False:
            arg += ' '

        current_prefix = await get_data()
        current_prefix['prefix'] = arg
        
        with open('stuff.json', 'w') as f:
            json.dump(current_prefix, f)

        client.command_prefix = arg
        await ctx.reply(f'The prefix has been set to `{client.command_prefix}`')

async def get_data():
    with open('stuff.json', 'r') as f:
        return json.load(f)

client.run(os.environ['CLIENT_TOKEN'])