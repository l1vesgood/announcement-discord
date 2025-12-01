import disnake
from disnake.ext import commands
from settings import TOKEN, init_db


bot = commands.Bot(command_prefix="?", intents=disnake.Intents.all())


@bot.event
async def on_ready():
    await init_db()
    bot.load_extensions("cogs/")

    print(f"Logged in as {bot.user}.")


bot.run(TOKEN)
