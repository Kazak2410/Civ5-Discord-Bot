import asyncio
import random
import discord
from discord.ext import commands


PREFIX = "/"

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
bot.remove_command('help')

nations = ["персия", "вавилон", "сиам", "россия", "австрия", "ацтеки", "германия", "египет", "ирокезы", "корея",
           "полинезия", "америка", "бразилия", "голландия", "зулусы", "испания", "майя", "польша", "сонгай", "шошоны",
           "англия", "греция", "индия", "карфаген", "марокко", "португалия", "турция", "эфиопия", "аравия", "венеция",
           "гунны", "индонезия", "кельты", "монголия", "рим", "франция", "япония", "ассирия", "византия", "дания",
           "инки", "китай", "швеция"]


@bot.event
async def on_ready():
    print("bot is ready")


@bot.command()
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам', colour=discord.Colour.red())
    emb.add_field(name=f'{PREFIX}start', value='Генерирует нации, и распределяет их по игрокам')
    await ctx.send(embed=emb)


@bot.command()
async def start(ctx):
    await ctx.channel.send("Какие нации вы хоетите запретить?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        message = await bot.wait_for("message", check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.channel.send("Слишком долго, все заново!")
    else:
        chosen_nations = set(set(nations) - set([i.lower() for i in message.content.split()]))
        await ctx.channel.send("Количество игроков?")

        try:
            message_cnt_players = await bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send("Слишком долго, все заново!")
        else:
            await ctx.channel.send("Количество наций на выбор?")

            try:
                message_cnt_nat = await bot.wait_for("message", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.channel.send("Слишком долго, все заново!")
            else:
                nat = []
                for n in range(int(message_cnt_players.content)):
                    a = random.sample(chosen_nations, int(message_cnt_nat.content))
                    nat.append(a)
                    chosen_nations -= set(a)

                res = ' \n'.join(f"> ``Игрок {i}:``  ```{' / '.join(n.title() for n in nat[i - 1])}```\n" for i in range(1, int(message_cnt_players.content) + 1))

                await ctx.channel.send(res)
                chosen_nations = set()


def run_bot():
    bot.run("")