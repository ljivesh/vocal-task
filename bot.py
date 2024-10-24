import discord
from discord.ext import commands

# Define the bot with command prefix
intents = discord.Intents.default()
intents.message_content = True  
intents.voice_states = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# Confirmation that the bot is running
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Command to make the bot join the voice channel
@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()
        await ctx.send(f"Joined {channel}!")
    else:
        await ctx.send("You are not connected to a voice channel!")

# Command to make the bot leave the voice channel
@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel!")
    else:
        await ctx.send("I'm not in a voice channel!")

# Command to make the bot respond with a greeting
@bot.command(name='hello')
async def hello(ctx):
    user_mention = ctx.author.mention  
    await ctx.send(f"Hello {user_mention}! I am VocalTask, How may I assist you?")

#Command to shut down the bot
@bot.command(name='shutdown', help='Shuts down the bot')
@commands.is_owner() 
async def shutdown(ctx):
    await ctx.send("Shutting down... Goodbye!")
    await bot.close()

# Start the bot 
bot.run('discord_key')