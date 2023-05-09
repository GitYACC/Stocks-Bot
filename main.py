import lightbulb
import hikari
import asyncio, json

with open("secret.json") as f:
    token = json.load(f)['token']

bot = lightbulb.BotApp(
    token=token,
    default_enabled_guilds=1103421333523660902
)

@bot.command
@lightbulb.option("text", "text option")
@lightbulb.command("echo", "base command")
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context):
    await ctx.respond(ctx.options.text)


@bot.command
@lightbulb.command("id", "returns current channel id")
@lightbulb.implements(lightbulb.SlashCommand)
async def id(ctx: lightbulb.Context):
    await ctx.respond(ctx.channel_id)
    await asyncio.sleep(3)
    await ctx.delete_last_response()

bot.run()