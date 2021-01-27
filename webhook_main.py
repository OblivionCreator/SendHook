import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

bot = commands.Bot(
command_prefix=['.'],
case_insensitive=True
)

try:
    with open('token.txt') as file:
        token = file.read()
        file.close()
except(FileNotFoundError, IOError):
    print("Unable to start! There is no token!")
    exit(99)

try:
    with open(".config") as file:
        file.close()
except (FileNotFoundError, IOError):
    print("No Config file found! A blank config file has been generated.")

    file = open('.config', 'x')
    file.close()

@bot.command()
async def send(ctx, name, *, message:str):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        img = attachment.url
    else:
        img = ctx.author.avatar_url

    channel = ctx.message.channel

    await sendWH(name=name, img=img, message=message, channel=channel, author=ctx.author)
    try:
        #await ctx.message.delete()
        pass
    except Exception as e:
        print(f"Unable to delete message due to exception:\n{e}")


async def sendWH(name, img, message, channel, author):

    webhook = await channel.create_webhook(name='NoWebhooks Generated Webhook', reason=f'{author} ({author.id}) used NoWebhooks to send a message in {channel}')

    async with aiohttp.ClientSession() as session:
        await webhook.send(message, username=name, avatar_url=img)
        await webhook.delete(reason="Auto-Delete Used Webhook")


bot.run(token)