import copy, math, random
from itertools import combinations

m =[[50,	57.1,	50.52,	48.52,	41.33,	44.79,	35.03,	68.16,	56.01],
[42.9,	50,	64.9,	61.17,	50.25,	63.64,	69.03,	18.9,	53.79],
[49.48,	35.1,	50,	61.14,	62.07,	59.69,	58.24,	46.78,	59.33],
[51.48,	38.83,	38.86,	50,	58.78,	55.19,	49.64,	62.43,	52.44],
[58.67,	49.75,	37.93,	41.22,	50,	50.88,	47.9,	60.41,	70.43],
[55.21,	36.36,	40.31,	44.81,	49.12,	50,	53.45,	56.19,	40.99],
[64.97,	30.97,	41.76,	50.36,	52.1,	46.55,	50,	67.2,	36.58],
[31.84,	81.1,	53.22,	37.57,	39.59,	43.81,	32.8,	50, 31.72],
[43.99,	46.21,	40.67,	47.56,	29.57,	59.01,	63.42,	68.28,	50]
]

names = ['No Minion Mage', 'Control Priest', 'Rush Warrior',
'Miracle Rogue', 'Secret Paladin', 'Token Druid', 'Face Hunter', 'Control Warlock', 'Lifesteal Demon Hunter']
p1 = [0,1,2,3]

def findBestLineup(matchups, odeck, deckNames):
    bestBanWR = 0
    bestBanLineup = []
    bestBan = 0
    for i in range(4):
        newDecks = copy.copy(odeck)
        ban = newDecks.pop(i)
        (lineup, wr) = findBestLineupHelper(matchups, newDecks, deckNames)
        if wr > bestBanWR:
            bestBanWR = wr
            bestBanLineup = lineup
            bestBan = ban
    return (odeck, deckNames[bestBan], bestBanLineup, bestBanWR)




def findBestLineupHelper(matchups, opdecks, deckNames):
    deckcount = len(matchups)
    decks = range(deckcount)
    bestLineup = []
    bestLineupWR = 0
    bestLineupBan = 0
    for combo in combinations(decks, 4):
        worstLineup = []
        worstLineupWR = 1
        worstLineupBan = 0
        for i in range(4):
            c = list(combo)
            p = c.pop(i)
            x = runSimulation(matchups, c, opdecks, 0, 0)
            if x < worstLineupWR:
                worstLineup = c
                worstLineupWR = x
                worstLineupBan = p
        if worstLineupWR > bestLineupWR:
            bestLineup = worstLineup
            bestLineupWR = worstLineupWR
            bestLineupBan = worstLineupBan
    bestLineup = [deckNames[bestLineup[0]], deckNames[bestLineup[1]], deckNames[bestLineup[2]], deckNames[bestLineupBan]]
    return (bestLineup, bestLineupWR)

def tournament(matchups, deckNames):
    lineups = []
    for combo in combinations(range(len(matchups)), 4):
        lineups.append(list(combo))
    wrs = []
    for i in range(len(lineups)):
        totalwr = 0
        for j in range(len(lineups)):
            totalwr += play(matchups, lineups[i], lineups[j])
        totalwr /= len(lineups)
        wrs.append([totalwr, lineups[i]])
    return wrs[0]

def play(matchups, p1decks, p2decks):
    p1new = copy.copy(p1decks)
    p2new = copy.copy(p2decks)
    ban1 = calculateBan(matchups, p1decks, p2decks)
    ban2 = calculateBan(matchups, p2decks, p1decks)
    p1new.remove(ban1)
    p2new.remove(ban2)
    return runSimulation(matchups, p1decks, p2decks, 0, 0)
    


def calculateBan(matchups, p1decks, p2decks):
    bestaverageWR = 0
    bestBan = 0
    for i in range(4):
        averageWR = 0
        newDecks1 = copy.copy(p1decks)
        ban = newDecks1.pop(i)
        for j in range(4):
            newDecks2 = copy.copy(p1decks)
            newDecks2.pop(j)
            averageWR += runSimulation(matchups, newDecks1, newDecks2, 0, 0)
        averageWR /= 4
        if averageWR > bestaverageWR:
            bestaverageWR = averageWR
            bestBan = ban
    return bestBan


def runSimulation(matchups, p1decks, p2decks, p1wins, p2wins):
    if p1wins == 3: return 1
    if p2wins == 3: return 0
    n = len(p1decks)*len(p2decks)
    total = 0
    for i in range(len(p1decks)):
        for j in range(len(p2decks)):
            deck1 = p1decks[i]
            deck2 = p2decks[j]
            wr = matchups[deck1][deck2]/100
            p1deckscopy = copy.copy(p1decks)
            p2deckscopy = copy.copy(p2decks)
            p1deckscopy.remove(deck1)
            p2deckscopy.remove(deck2)
            total += wr*runSimulation(matchups, p1deckscopy, p2decks, p1wins+1, p2wins)
            total += (1-wr)*runSimulation(matchups, p1decks, p2deckscopy, p1wins, p2wins+1)
    return total/n

#print(findBestLineup(m, p1, names))
#print(play(m, [0,1,2,3], [5,6,7,8]))
tournament(m, names)


