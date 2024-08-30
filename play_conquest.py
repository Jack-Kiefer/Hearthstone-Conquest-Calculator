import numpy as np

def playConquest(matchups, p1decks, p2decks, p1ban, p2ban):
    """
    Simulates a conquest match given the matchups, 
    the decks of each player, and the decks each player chooses to ban.
    """
    # Remove the banned decks from the lists
    p1decks = [d for d in p1decks if d != p2ban]
    p2decks = [d for d in p2decks if d != p1ban]

    p1wins, p2wins = 0, 0

    # Calculate winrate of the match
    def calculateWinRates(p1decks, p2decks, p1wins, p2wins):
        if p1wins == 3:
            return 1  
        if p2wins == 3:
            return 0  

        total_win_rate = 0
        total_cases = 0

        for p1deck in p1decks:
            for p2deck in p2decks:
                p1_win_rate = matchups[p1deck][p2deck] / 100

                new_p1decks = [d for d in p1decks if d != p1deck]
                new_p2decks = [d for d in p2decks if d != p2deck]
                total_win_rate += p1_win_rate * calculateWinRates(new_p1decks, p2decks, p1wins + 1, p2wins)

                total_win_rate += (1 - p1_win_rate) * calculateWinRates(p1decks, new_p2decks, p1wins, p2wins + 1)

                total_cases += 1

        return total_win_rate / total_cases if total_cases > 0 else 0

    overall_win_rate = calculateWinRates(p1decks, p2decks, p1wins, p2wins)

    return overall_win_rate

def generate4x4WinRateMatrix(matchups, lineup1, lineup2):
    """
    Generates a 4x4 win rate matrix for specific lineups, considering all possible bans.
    """
    win_rate_matrix = np.zeros((4, 4))

    # Calculate win rates for each possible ban combination
    total_combinations = len(lineup1) * len(lineup2)
    current_combination = 0

    for i, p1ban in enumerate(lineup1):
        for j, p2ban in enumerate(lineup2):
            current_combination += 1
            print(f"Calculating win rate for P1 ban: {p1ban}, P2 ban: {p2ban} ({current_combination}/{total_combinations})")
            
            win_rate = playConquest(matchups, lineup1, lineup2, p1ban, p2ban)
            win_rate_matrix[i][j] = win_rate

    return win_rate_matrix

def findBestDeterministicStrategy(win_rate_matrix):
    """
    Finds the best deterministic strategy for bans for both player based off of a winrate matrix.
    """
    num_decks = win_rate_matrix.shape[0]

    # Determine Player 1's best strategy: the one that maximizes their minimum guaranteed win rate
    p1_best_strategy = np.argmax(np.min(win_rate_matrix, axis=1))
    
    # Determine Player 2's best strategy: the one that minimizes Player 1's maximum win rate
    p2_best_strategy = np.argmin(np.max(win_rate_matrix, axis=0))
    
    # Return the win rate for Player 1 when both play their best deterministic strategies
    return win_rate_matrix[p1_best_strategy, p2_best_strategy]

def calculateGameValue(win_rate_matrix, lineup1, lineup2):
    """
    Calculates the value of the game, given the Nash equilibrium strategies and win rate matrix.
    """
    matrix = generate4x4WinRateMatrix(win_rate_matrix, lineup1, lineup2)
    return findBestDeterministicStrategy(matrix)