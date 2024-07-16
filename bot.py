import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene el TOKEN desde las variables de entorno
TOKEN = os.getenv('TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Permiso para leer el contenido de los mensajes

# Inicializa el bot con el prefijo de comando que prefieras (en este caso, '$') y los intents.
bot = commands.Bot(command_prefix='$', intents=intents)

# Reemplaza 'YOUR_BOT_TOKEN' con el token de tu bot
# TOKEN = 'YOUR_BOT_TOKEN'

@bot.event
async def on_ready():
    print(f'{bot.user} se ha conectado')

@bot.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.voice} no esta en un canal de voz')
        return
    else:
        channel = ctx.message.author.voice.channel

        await channel.connect()

@bot.command(name='play')
async def play(ctx, *, filename: str):
    server = ctx.message.guild
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice_client:
        await ctx.send("El bot no esta conectado a un canal de voz")
        return

    if not ctx.author.voice:
        await ctx.send("Debes estar en un canal de voz")
        return
    
    channel = ctx.author.voice.channel

    try:
        await channel.connect()
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    except discord.ClientException:
        pass

    # Asegurate de que el archivo existe en la carpeta del bot
    audio_path = f'./music/{filename}.mp3'

    try:
        voice_client.play(discord.FFmpegPCMAudio(audio_path), after=lambda e: print(f'Error: {e}') if e else None)
        await ctx.send(f'Reproduciendo: {filename}')
    except Exception as e:
        await ctx.send(f'Error al reproducir el archivo: {str(e)}')

@bot.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("El bot no esta conectado a un canal de voz")

# Ejecuta el Bot
bot.run(TOKEN)