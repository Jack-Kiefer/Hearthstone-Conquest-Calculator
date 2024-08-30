import copy
import random
from itertools import combinations
import numpy as np
import argparse

# Matchup matrix and deck names
m = [[50, 57.1, 50.52, 48.52, 41.33, 44.79, 35.03, 68.16, 56.01],
     [42.9, 50, 64.9, 61.17, 50.25, 63.64, 69.03, 18.9, 53.79],
     [49.48, 35.1, 50, 61.14, 62.07, 59.69, 58.24, 46.78, 59.33],
     [51.48, 38.83, 38.86, 50, 58.78, 55.19, 49.64, 62.43, 52.44],
     [58.67, 49.75, 37.93, 41.22, 50, 50.88, 47.9, 60.41, 70.43],
     [55.21, 36.36, 40.31, 44.81, 49.12, 50, 53.45, 56.19, 40.99],
     [64.97, 30.97, 41.76, 50.36, 52.1, 46.55, 50, 67.2, 36.58],
     [31.84, 81.1, 53.22, 37.57, 39.59, 43.81, 32.8, 50, 31.72],
     [43.99, 46.21, 40.67, 47.56, 29.57, 59.01, 63.42, 68.28, 50]]

names = ['No Minion Mage', 'Control Priest', 'Rush Warrior',
         'Miracle Rogue', 'Secret Paladin', 'Token Druid', 'Face Hunter', 'Control Warlock', 'Lifesteal Demon Hunter']

memo = {}

def calculateGameValue(matchups, lineup1, lineup2):
    lineup1 = tuple(sorted(lineup1))
    lineup2 = tuple(sorted(lineup2))
    
    if (lineup1, lineup2) in memo:
        return memo[(lineup1, lineup2)]
    
    if (lineup2, lineup1) in memo:
        return 1 - memo[(lineup2, lineup1)]

    win_rate = np.mean([matchups[i][j] for i in lineup1 for j in lineup2]) / 100

    memo[(lineup1, lineup2)] = win_rate
    memo[(lineup2, lineup1)] = 1 - win_rate

    return win_rate

def findTopLineups(matchups, deckNames, top_n=20, verbose=False):
    """
    Finds best n lineups against the entire field.
    """
    lineup_scores = []
    total_combinations = len(list(combinations(range(len(deckNames)), 4)))
    current_combination = 0
    
    for combo in combinations(range(len(deckNames)), 4):
        current_combination += 1
        wr = evaluateLineup(matchups, combo)
        lineup_scores.append((combo, wr))

        if verbose and (current_combination % 10 == 0):
            print(f"Evaluating combination {current_combination}/{total_combinations}")
    
    lineup_scores.sort(key=lambda x: x[1], reverse=True)
    top_lineups = lineup_scores[:top_n]
    
    return top_lineups

def findBestAgainstField(top_lineups, matchups, verbose=False):
    """
    Finds best n lineups against the top n lineups.
    """
    bestLineup = None
    bestLineupWR = 0
    
    for index, (lineup, lineup_wr) in enumerate(top_lineups):
        totalWR = 0
        for opponent_lineup, _ in top_lineups:
            if set(lineup) != set(opponent_lineup):
                totalWR += calculateGameValue(matchups, list(lineup), list(opponent_lineup))
        
        averageWR = totalWR / (len(top_lineups) - 1)
        
        if averageWR > bestLineupWR:
            bestLineupWR = averageWR
            bestLineup = lineup
        
        if verbose:
            print(f"Evaluating lineup {index + 1}/{len(top_lineups)} against the field.")
    
    return bestLineup, bestLineupWR

def evaluateLineup(matchups, lineup):
    totalWR = 0
    numComparisons = 0
    
    for opponentLineup in combinations(range(len(matchups)), 4):
        if set(lineup) == set(opponentLineup):
            totalWR += 0.5
        else:
            totalWR += calculateGameValue(matchups, list(lineup), list(opponentLineup))
        numComparisons += 1
    
    return totalWR / numComparisons if numComparisons > 0 else 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate Hearthstone lineups.')
    parser.add_argument('--verbose', action='store_true', help='Print progress information')
    parser.add_argument('--top_n_runoff', type=int, default=10, help='Number of top lineups to consider for runoff')
    args = parser.parse_args()
    
    # Find the top lineups
    top_lineups = findTopLineups(m, names, top_n=args.top_n_runoff, verbose=args.verbose)

    print(f"Top {args.top_n_runoff} Lineups:")
    for lineup, wr in top_lineups:
        lineup_names = [names[i] for i in lineup]
        print(f"{lineup_names}: Win Rate = {wr:.2f}")

    # Determine the best lineup against the field using the specified number of top lineups
    best_lineup, best_wr = findBestAgainstField(top_lineups, m, verbose=args.verbose)
    best_lineup_names = [names[i] for i in best_lineup]

    print(f"\nBest Lineup Against the Field: {best_lineup_names} with win rate: {best_wr:.2f}")
