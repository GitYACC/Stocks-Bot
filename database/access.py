# implement class for parsing and structing the csv files for bets and stock market

import pandas as pd
import random
import numpy as np
import json
import typing
import asyncio

JSONLink = str

# ------------ DB FUNCTIONS ------------

async def get_table() -> pd.DataFrame:
    return pd.read_csv("database/database.csv")

async def set_table(table: pd.DataFrame):
    table.to_csv("database/database.csv", index=False)

async def get_player_data(name: str) -> JSONLink:
    table = await get_table()
    names = np.array(table["Client"])
    result = np.where(names == name)[0][0]
    return table["Assets"].get(result)

async def get_assets(profile: JSONLink) -> dict:
    fp = open(profile, "r")
    return json.load(fp)

# ------------ PROFILE FUNCTIONS ------------

uids: hex = []
cap_hit: float = 1

async def set_cap_hit():
    global cap_hit
    table = await get_table()
    amount = len(table["Cap Hit"])
    cap_hit = 1 / (amount + 1)

async def get_cap_hit():
    return cap_hit

async def create_profile(name: str) -> typing.Optional[str]:
    table = await get_table()

    if name in table["Client"].values:
        return "[client-found]"

    empty_assets = json.load(open("profiles/demo_empty.json"))
    while (uid := hex(random.randint(1, 1000000))) in uids:
        continue

    json.dump(empty_assets, open(f"profiles/{name}.json", "w"))

    uids.append(uid)
    table.loc[str(uid)] = [uid, name, f"profiles/{name}.json", "", "", "", "", ""]
    await set_cap_hit()
    table["Cap Hit"] = cap_hit
    await set_table(table)

    return str(uid)

async def edit_profile(uid: str, **columns) -> typing.Optional[str]:
    table = await get_table()

    if uid not in table["ID"].values:
        return "[unknown-uid]"

    keys = np.array(table["ID"])
    index = np.where(keys == uid)[0][0]

    table.loc[index, columns.keys()] = columns.values()

    await set_table(table)



#uid = asyncio.run(create_profile("YACC#5002"))
asyncio.run(edit_profile("0x6c4bd", **{"Market Mover": "False"}))

