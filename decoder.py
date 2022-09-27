from collections import namedtuple
import pandas as pd
from typing import NamedTuple
import csv

from sqlalchemy import true

class detail(NamedTuple):
    id: int
    index: int 
    rarity: int 
    level: int 
    color: int 
    skin: int
    stamina: int
    speed: int
    bombSkin: int
    bombCount: int
    bombPower: int
    bombRange: int
    abilities: list


def decode(details):
    id = decodeId(details)
    index = decodeIndex(details)
    rarity = decodeRarity(details)
    level = decodeLevel(details)
    color = (details >> 50) & 31
    skin = (details >> 55) & 31
    stamina = (details >> 60) & 31
    speed = (details >> 65) & 31
    bombSkin = (details >> 70) & 31
    bombCount = (details >> 75) & 31
    bombPower = (details >> 80) & 31
    bombRange = (details >> 85) & 31
    ability = (details >> 90) & 31
    abilities = ['-','-','-','-','-','-','-']
    for i in range(ability):
      abilities[((details >> (95 + i * 5)) & 31)-1] = 'X'
    dictresult = {'id':id,'index':index,'Rarity':rarity,'Level':level,'Color':color,'Skin':skin,'Stamina':stamina,'Speed':speed,'Bomb Skin':bombSkin,'Bomb Num':bombCount,'Power':bombPower,'Bomb Range':bombRange,'+2 Chest': list(str(abilities[0])),'+2 Jail': str(abilities[1]),'Super Bomb': str(abilities[2]),'Mana': str(abilities[3]),'Battery': str(abilities[4]),'Move Bomb': str(abilities[5]), 'Move Chest': str(abilities[6])}
    return dictresult

def decodeId(details):
    return details & ((1 << 30) - 1)

def decodeAbility(abilitynum):
    abilitylist = ['+2 Chest','+2 Jail','Super Bomb','Mana','Battery','Move Bomb', 'Move Chest']
    return abilitylist[abilitynum-1]

def decodeIndex(details):
    return (details >> 30) & ((1 << 10) - 1)

def decodeRarity(details):
    raritylist = ['Comum','Rare','Super Rare','Epic','Legend','Super Legend']
    return raritylist[(details >> 40) & 31]

def decodeLevel(details):
    return (details >> 45) & 31



df = pd.DataFrame()
with open('resultslist.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
    listresults = []
    for item in data[0]:
        itemnum = int(item)
        if itemnum != 0:
            df = pd.concat([df, pd.DataFrame(decode(itemnum))], ignore_index = True, axis = 0)
print(df.head())
#print(df.drop(columns='abilities')[df['rarity']==4])
#print(df.groupby('rarity').count())
