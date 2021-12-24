import discord
import random 
import os
import randomstuff
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot= commands.Bot(command_prefix=('h!'), intents=discord.Intents().all())
wee = randomstuff.AsyncClient(api_key='OiX0rPsfCvSJ')

@bot.event
async def chat(message):
    if bot.user == message.author:
        return
    if  message.channel.id == 922837080860684319:
            response = await weee.get_ai_response(message.content)  
            await message.reply(response.message)
    await bot.process_commands(message)

client = commands.Bot(command_prefix= "h!")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Himontor Koti")) 

    print('Himonto Bot is online')

#@client.event
#async def on_ready():
    #print("Himonto bot is online!")


"""@client.command(case_insensitive=True)
async def ping(ctx):
    await ctx.send("Pong!")"""

#cogs
"""@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename .endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')"""

#clear command
@client.command(aliases=['clear'])
async def purge(ctx, amount=11):
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Cannot run command! Requires: ``Manage Messages``')
        return
    amount = amount+1
    if amount > 101:
        await ctx.send('I can\'t delete more than 100 messages at a time!')
    else: 
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Sucessfully deleted {amount} messages!')

#slowmode command 
@client.command(case_insensitive=True)
async def slowmode(ctx, time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Cannot run command! Requires: ``Manage Messages``')
        return
    if time == 0:
        await ctx.send('Slowmode is currently set to `0`')
        await ctx.channel.edit(slowmode_delay = 0)
    elif time > 21600:
        await ctx.send('You cannot keep the slowmode higher than 6 hours!')
        return
    else:
        await ctx.channel.edit(slowmode_delay = time)
        await ctx.send(f"Slowmode has been set to `{time}` seconds!")

#8ball command 
@client.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    responses = ["hoi.",
                "himanta says yes.",
                "Without a doubt.",
                "ses ebur ki.",
                "hagi asu try again.",
                "hobo pare",
                "Dyan says no.",
                "najanu.",
                "Yes.",
                "gom napau.",
                "disturb nokor.",
                "moi no.",
                "bhaal question sun.",
                "ki je.",
                "ses.",
                "nohoi neki.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Maybe."]
    await ctx.send(f' Answer: {random.choice(responses)}')

#kick and ban command
@client.command(case_insensitive=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention}ok ulai dilu!')
 
@client.command(case_insensitive=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention}ok ulai dilu')

#mute and unmute
@client.command(case_insensitive=True)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        await ctx.send("No Mute Role found! Creating one now...")
        muteRole = await guild.create_role(name = "Muted")

        for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=True, read_message_history=True)
        await member.add_roles(muteRole, reason=reason)
        await ctx.send(f"{member.mention} etia chup | Reason: {reason}")
        await member.send(f"You have been muted in {ctx.guild} | Reason: {reason}")

@client.command(case_insensitive=True)
async def unmute(ctx, member: discord.Member, *, reason=None):

    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        await ctx.send("The Mute role can\'t be found! Please check if there is a mute role or if the user already has it!")
        return
    await member.remove_roles(muteRole, reason=reason)
    await ctx.send(f"{member.mention} etia kobo paro")
    await member.send(f"You have been unmuted in {ctx.guild}")

#say command
"""@client.command(case_insensitive=True)
async def say(ctx, *, text):
    message = ctx.message
    await message.delete()

    await ctx.send(f"{text}")"""

@client.command()
#@commands.has_guild_permissions(administrator=True)
async def say(ctx, *, message=None):
    message = message or "Please say something to use the say command!"
    message_components = message.split()
    if "@everyone" in message_components or "@here" in message_components:
        await ctx.send("Ma Chuda")
        return

    await ctx.message.delete()
    await ctx.send(message)

#avatar command
@client.command()
async def avatar(ctx, member: discord.Member=None):
	if member == None:
		member = ctx.author
	
	icon_url = member.avatar_url 

	avatarEmbed = discord.Embed(title = f"{member.name}\'s Avatar", color = 0xFFA500)

	avatarEmbed.set_image(url = f"{icon_url}")

	avatarEmbed.timestamp = ctx.message.created_at 

	await ctx.send(embed = avatarEmbed)

#poll command
@client.command()
async def poll(ctx, *, question=None):
    if question == None:
        await ctx.send("Please write a poll!")
 
    icon_url = ctx.author.avatar_url 
 
    pollEmbed = discord.Embed(title = "Poll eta", description = f"{question}")
 
    pollEmbed.set_footer(text = f"Poll given by {ctx.author}", icon_url = ctx.author.avatar_url)
 
    pollEmbed.timestamp = ctx.message.created_at 
 
    await ctx.message.delete()
 
    poll_msg = await ctx.send(embed = pollEmbed)
 
    await poll_msg.add_reaction("⬆️")
    await poll_msg.add_reaction("⬇️")

#snipe command
snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@client.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except: 
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")

#add and take role

#tokenkakunidibi
client.run("*********************************************************")
