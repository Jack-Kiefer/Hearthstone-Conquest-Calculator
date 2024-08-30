---

## README.md

### Project: Conquest Simulation

The goal of this project is to simulate the best lineup of 4 decks in Hearthstone for the conquest format. This is done using matchup winrate data. It first finds the top n lineups out of every combination of 4 decks my simulating a conquest match against every deck. The conquest matches are simulating by having each player can the deck that maximzes their minimum winrate and then having each player choose random decks from their available decks each game. Finally the top n decks all face against eachother to decide the winner.

### Files

- **`conquest.py`**: This script defines the matchup matrix and includes necessary imports and initial setup. It likely contains functions to handle different aspects of the simulation, including setting up match scenarios and managing player interactions.
  
- **`play_conquest.py`**: Contains the main function `playConquest`, which is used to simulate individual conquest matches. This function takes as input:
  - `matchups`: A matrix defining win rates between various decks.
  - `p1decks`, `p2decks`: Lists of decks available to Player 1 and Player 2.
  - `p1ban`, `p2ban`: Decks banned by Player 1 and Player 2.

### Requirements

- Python 3.x
- `numpy` library

### Installation

1. Clone the repository or download the files.
2. Ensure you have Python 3.x installed on your system.
3. Install the required Python libraries using:
   ```bash
   pip install numpy
   ```

### Usage

1. Change the deck names and matchup matrix to the current metagame using data from hsreplay. 
2. Run the simulation using the command line with the desired parameters. Example:

```bash
python conquest.py --verbose --top_n_runoff 10
```
---

