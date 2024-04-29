import json


strat_file = open('games/3aee5fc8-58a4-49b6-b7a2-0558c23bba69.json')
strats = json.load(strat_file)
NUM_GAMES = 5
NUM_TURNS = 100
you = 1 #opponent is player 0, keep this in mind
for game in range(NUM_GAMES):
    current_game = strats['history'][game]
    print(current_game)
