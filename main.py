import lightbulb
import hikari
import json
import asyncio
import typing
import random

import database.access as db
from dataclasses import dataclass


@dataclass
class BetMap:
    uid: str
    owner: str
    target: str
    description: str
    amount: int

    def __repr__(self):
        return f"Bet[{self.owner}::{self.uid}] -> {self.target} ({self.amount})"

global_bets: typing.List[BetMap] = []

with open("secret.json") as f:
    token = json.load(f)['token']

bot = lightbulb.BotApp(
    token=token,
    default_enabled_guilds=1103421333523660902
)

@bot.command
@lightbulb.option("text", "text option")
@lightbulb.command("echo", "base command")
#@lightbulb.checks.has_roles(1103421583982338111)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context):
    await ctx.respond(ctx.options.text)


@bot.command
@lightbulb.command("id", "returns current channel id")
#@lightbulb.checks.has_roles(1103421583982338111)
@lightbulb.implements(lightbulb.SlashCommand)
async def id(ctx: lightbulb.Context):
    await ctx.respond(ctx.channel_id)
    await asyncio.sleep(3)
    await ctx.delete_last_response()

@bot.command
@lightbulb.option("name", "name of profile", type=hikari.User)
@lightbulb.command("profile", "returns profile json")
#@lightbulb.checks.has_roles(1103421583982338111)
@lightbulb.implements(lightbulb.SlashCommand)
async def profile(ctx: lightbulb.Context):
    user = str(ctx.options.name).split("#")[0]
    json_link = await db.get_player_data(user)
    assets = await db.get_assets(json_link)
    await ctx.respond(assets)

@bot.command
@lightbulb.command("bet", "place bet")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def bet(ctx: lightbulb.Context):
    print("invoked")
    

@bet.child
@lightbulb.option("amount", "cash amount")
@lightbulb.option("target", "who you are betting on", type=hikari.User)
@lightbulb.option("description", "what you are betting on")
@lightbulb.command("add", "add a new bet")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bet_add(ctx: lightbulb.Context):
    global global_bets
    global_bets.append(
        BetMap(
            uid := hex(random.randint(1, 1000000)),
            str(ctx.author),
            str(ctx.options.target),
            ctx.options.description,
            int(ctx.options.amount)
        )
    )
    await ctx.respond(f"Bet UID is {uid}")



@bet.child
@lightbulb.command("lineup", "[admin only] list all ongoing bets")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def lineup(ctx: lightbulb.Context):
    await ctx.respond(global_bets)


@bet.child
@lightbulb.option("uid", "bet uid")
@lightbulb.command("resolve", "resolve bets")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def resolve(ctx: lightbulb.Context):
    global global_bets

    res = 0
    for bet in global_bets:
        if bet.uid == ctx.options.uid:
            break
        res += 1

    bet_removed = global_bets.pop(res)
    await ctx.respond(f"Removed bet {bet_removed}")


bot.run()