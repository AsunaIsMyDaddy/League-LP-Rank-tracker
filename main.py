import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError, TftWatcher
import asyncio

bot = discord.Client() #initalizes the bot
bot = commands.Bot(command_prefix='!') #! is the prefix of the bot this can be changed to any char

def getTier(num): #converts ranks to numarical values to be compared
    if (num == "IRON"): 
        num = 1
    if (num == "BRONZE"):
        num = 2
    if (num == "SILVER"):
        num = 3
    if (num == "GOLD"):
        num = 4
    if (num == "PLATINUM"):
        num = 5
    if (num == "DIAMOND"):
        num = 6
    if (num == "MASTER"):
        num = 7
    if (num == "GRANDMASTER"):
        num = 8
    if (num == "CHALLENGER"):
        num = 9
    return num
def getRank(num): #converts from roman numerals to ints
    if (num == 'IV'): 
        num = 4
    if (num == 'III'):
        num = 3
    if (num == 'II'):
        num = 2
    if (num == 'I'):
        num = 1
    return num 
def command(RAPI, region, Gname, Name): #this returns the string of ranked stats based on input of thier irl name and in game name
    lol_watcher = LolWatcher(RAPI) #use the API key to acess API
    a_region = region #sets the region they are in 
    a = lol_watcher.summoner.by_name(a_region, Gname) #creates 
    a_ranked_stats = lol_watcher.league.by_summoner(a_region, a['id']) 
    num = len(a_ranked_stats) - 1
    if (a_ranked_stats[num]['leaguePoints'] == 100): #check if they are in promos 
        tempS = ''
        for i in a_ranked_stats[num]['miniSeries']['progress']:
            if i == 'L':
                tempS += ':x: ' #put discord emojis in sttring to represent promos
            elif i == 'W':
                tempS += ':white_check_mark: '
            elif i == 'N':
                tempS += ':grey_question: '
        return Name + ' is ' + a_ranked_stats[num]['tier'] + ' ' + a_ranked_stats[num]['rank'] + ' ' + str(a_ranked_stats[num]['leaguePoints']) + ' LP ' + tempS
    else:
        return Name + ' is ' + a_ranked_stats[num]['tier'] + ' ' + a_ranked_stats[num]['rank'] + ' ' + str(a_ranked_stats[num]['leaguePoints']) + ' LP'
    
global RAPI 
RAPI = 'RiotAPI 000000-AA-00000-AAAa' #put your riot api here aply for developer so it doesnt expire
@bot.event #constant while loop looking for a change in LP
async def on_ready():
    channel = bot.get_channel(channelID000000) #channel id to send messages
    lol_watcher = LolWatcher(RAPI) #riot API key 
    a_region = 'na1'
    a = lol_watcher.summoner.by_name(a_region, '43HardstuckNoJob') #players name
    a_ranked_stats = lol_watcher.league.by_summoner(a_region, a['id']) 
    tempTier = getTier(a_ranked_stats[0]['tier']) #gets inital rank and lp to cpmare too
    tempRank = getRank(a_ranked_stats[0]['rank'])
    tempPoints = a_ranked_stats[0]['leaguePoints']  
    sentOnce = False #check variable
    while True:
        await asyncio.sleep(8) #waits to acess riot api again 
        lol_watcher = LolWatcher(RAPI)
        a_region = 'na1'
        a = lol_watcher.summoner.by_name(a_region, 'RiotIngame username')
        a_ranked_stats = lol_watcher.league.by_summoner(a_region, a['id'])
        Tier = getTier(a_ranked_stats[0]['tier']) #new variables retrived from riot to compare to temp
        Rank = getRank(a_ranked_stats[0]['rank'])
        Points = a_ranked_stats[0]['leaguePoints']
        hasMessage = False 
        if (Tier < tempTier): #runs checks on rank, division and lp in order so write message apears first
            message = 'IRLname has massively deranked and is now ' + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True
        elif (Tier > tempTier):
            message = '@everyone this man finally did it!!! IRLname has massively ranked up and is now ' + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True
        elif (tempRank > Rank):
            message = 'IRLname has deranked and is now ' + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True
        elif (tempRank < Rank):
            message = 'IRLname has ranked up and is now ' + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True
        elif (tempRank < Rank):
            message = 'IRLname has ranked up and is now ' + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True
        elif(tempPoints > a_ranked_stats[0]['leaguePoints']):
            message = 'IRLname has Lost ' + str(tempPoints - a_ranked_stats[0]['leaguePoints']) + " LP and is now " + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True
        elif(tempPoints < a_ranked_stats[0]['leaguePoints'] and tempRank == a_ranked_stats[0]['rank'] and tempTier == a_ranked_stats[0]['tier']):
            message = 'IRLname has gained ' + str(a_ranked_stats[0]['leaguePoints'] - tempPoints) + " LP and is now " + a_ranked_stats[0]['tier'] + ' ' + a_ranked_stats[0]['rank'] + ' ' + str(a_ranked_stats[0]['leaguePoints']) + ' LP'
            hasMessage = True 
        if(hasMessage == True):
            await asyncio.sleep(8)
            await channel.send(message) #sends message
            tempPoints = Points #resets variables
            tempTier = Tier
            tempRank = Rank
            sentOnce = True

@bot.command() #this initalizes the comand to check a players stats 
async def name(ctx): #name is what follows the start char in this case !name would couse this function to activate (name can be changed)
    await ctx.reply(command(RAPI, 'na1', 'leaugeInGameUsername', 'IRLname')) #na1 is the region code you will have to look up the others if you want to change it


bot.run("This Is where the discord api key goes") #runs the bot with bot API key
