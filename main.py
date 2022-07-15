import nextcord
import json
import os
from nextcord.ext import commands

command_info = {
    'help': 'you literally just used it',
    'prefix': 'change the command prefix',
    'status': 'change the bot\'s current status',
}

client = commands.Bot(command_prefix = 'dont ', help_command = None)

# Events
@client.event
async def on_ready():
    data = await get_data()
    client.command_prefix = data['prefix']

    print(f'Logged in as\n{client.user.name}\n{client.user.id}\n\nPrefix: {client.command_prefix}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = 'hyper sleep'))

@client.event
async def on_message(message):
    process_command = True

    if message.content.startswith('whats the prefix'):
        await message.reply(f'my current prefix is `{client.command_prefix}`')
        process_command = False

    elif message.author.id == 803404128600195133:
        await message.add_reaction('\N{SUNGLASSES}')

    if process_command == True:
        await client.process_commands(message)

# Commands
@client.command()
async def help(ctx):
    embed = nextcord.Embed(title = 'Help', description = 'very cool help command\n(see below for a list of commands)', color = nextcord.Colour.blurple())

    for name, command in command_info.items():
        embed.add_field(name = name, value = command, inline = False)

    await ctx.reply(embed = embed)

@client.command()
async def prefix(ctx, *, arg = None):
    if arg == None:
        await ctx.reply(f'The current prefix is `{client.command_prefix}`')

    else:
        if arg.endswith(' ') == False and len(arg) > 1:
            arg += ' '

        current_prefix = await get_data()
        current_prefix['prefix'] = arg
        
        with open('stuff.json', 'w') as f:
            json.dump(current_prefix, f)

        client.command_prefix = arg
        await ctx.reply(f'The prefix has been set to `{client.command_prefix}`')

@client.command()
async def status(ctx, *, arg = None):
    if arg == None:
        await ctx.reply('You need to include a status idiot :rolling_eyes:')

    else:
        await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = arg))
        await ctx.reply(f'Status set to `{arg}`')

async def get_data():
    with open('stuff.json', 'r') as f:
        return json.load(f)

client.run(os.environ['CLIENT_TOKEN'])