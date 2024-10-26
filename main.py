import asyncio
import discord
from discord.ext import commands
import yt_dlp
import os

Token = os.getenv('DISCORD_TOKEN')

audios = [
    {
        'name': 'hijo de puta',
        'audio': './audios/hijo_de_puta.mp3'
    },
    {
        'name': 'que linda cancion',
        'audio': './audios/que_linda_cancion.mp3'
    },
    {
        'name': 'sapucai male',
        'audio': './audios/sapucai.ogg'
    }
]

queue = []
queueSeconday = []
ALLOWED_CHANNEL_NAME = "malebot"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def send_to_malebot_channel(message, ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name=ALLOWED_CHANNEL_NAME)
    if channel:
        await channel.send(message)

@bot.command()
async def boraaa(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await send_to_malebot_channel(f"Llego el malebot, aguardaaaaaaaaaaa!!!!", ctx)

@bot.command()
async def diseloMale(ctx, *arg):

   
    if ctx.voice_client is None:
        channel = ctx.author.voice.channel
        await channel.connect()

    respuesta = ' '.join(arg).lower()

    print(respuesta)
    if ctx.voice_client is None:
        await send_to_malebot_channel("Mete al malebot wachoooo", ctx)
        return
    
    audio = None
    for a in audios:
        if a['name'] in respuesta:
            audio = a
            break
    
   
    if audio is None:
        await send_to_malebot_channel("Todavía el sinverguenza no aprendió a decir eso",ctx)
        return
    
    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(audio['audio']))
    await send_to_malebot_channel(f"El malebot va a decir '{audio['name']}'",ctx)


@bot.command()
async def cantaloMale(ctx, url: str):
    if ctx.voice_client is None:
        channel = ctx.author.voice.channel
        await channel.connect()
    
    if not url:
        await send_to_malebot_channel("Pone una url de youtube gato, para que el malebot cante",ctx)


    queue.append(url)
    queueSeconday.append(url)

    print(queue)

    if len(queueSeconday) > 1:
        await send_to_malebot_channel("El malebot ya guardo el tema en la lista, awanta un toque",ctx)
   
    if not ctx.voice_client.is_playing():
        print('Cuando entro aca?')
        await laQueSigueMale(ctx, primero=True)

@bot.command()
async def laQueSigueMale(ctx, primero=False):

    if len(queue) > 0:
            if not primero:
                await send_to_malebot_channel('Ahi te pongo el tema que sigue gato', ctx)

            # Extraemos y eliminamos la primera URL de la cola
            url = queue.pop(0)

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'audio_only': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url_audio = info['url']
                    name_audio = info['title']
                    await send_to_malebot_channel(f"El malebot te va cantar esta: {name_audio}", ctx)

            except Exception as e:
                await send_to_malebot_channel(f"Al malebot no le dío el bocho para cantar eso", ctx)
                return

            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -bufsize 64k'
            }

            if not primero:
                ctx.voice_client.stop()
                print(f'Pare la siguiente cancion {name_audio}')

            # Reproducimos la nueva canción
            ctx.voice_client.play(
                discord.FFmpegOpusAudio(url_audio, **ffmpeg_options),
                after=lambda e: asyncio.run_coroutine_threadsafe(chequearYReproducir(ctx), bot.loop)
                )
    else:
            await send_to_malebot_channel("El malebot se quedo sin temas para cantar, prendele alguna", ctx)

async def chequearYReproducir(ctx):
    if ctx.voice_client.is_playing():
        return  

    if len(queue) > 0:
        await laQueSigueMale(ctx) 
    else:
        await send_to_malebot_channel("Ya no hay más canciones en la cola, ¡prendele alguna!", ctx)


@bot.command()
async def frenaMale(ctx):
    await ctx.voice_client.disconnect()
    await send_to_malebot_channel("El malebot se fue a la mierda",ctx)

@bot.command()
async def comandzera(ctx):
    await send_to_malebot_channel("Comandos disponibles: \n - !boraaa: Aparece el malebot en el canal de los pibes \n - !diseloMale [frase]: El bot reproduce una frase del malebot \n - !cantaloMale [url]: El malebot empieza a cantar un tema \n - !laQueSigueMale: El malebot saltea la cancion de mierda que esta sonando \n - !frenaMale: El malebot deja de hacer lo que este haciendo  \n - !frasesDelMale: Muestra las frases íconicas del Male",ctx)

@bot.command()
async def frasesDelMale(ctx):
    await send_to_malebot_channel("Frases disponibles: \n - hijo de puta \n - que linda cancion \n - sapucai male",ctx)

@bot.command()
async def borraTodoMale(ctx):
    await ctx.channel.purge()

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="!comandzera")
    await bot.change_presence(activity=activity)
    # ensordecer al bot
    for vc in bot.voice_clients:
        await vc.disconnect()

bot.run(Token)