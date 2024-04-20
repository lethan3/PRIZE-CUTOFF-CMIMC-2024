import argparse
from strategy import get_strategies
import random

class BlottoSwarmGame:
    NUM_CASTLES = 10
    GAP_SIZE = 2
    NUM_SOLDIERS = 60
    VISION_RANGE = 3

    def random_list(self, board_size, list_size):
        return [random.randint(0, board_size - 1) for _ in range(list_size)]

    def __init__(self) -> None:
        # num of each team at each position
        self.board = [[0] * (self.NUM_CASTLES * (self.GAP_SIZE + 1)) for _ in range(2)]
        self.board_sz = len(self.board[0])

        # positions of each soldier
        self.soldiers = [self.random_list(self.board_sz, self.NUM_SOLDIERS) for _ in range(2)]
        for team in range(2):
            for i in range(self.NUM_SOLDIERS):
                self.board[team][self.soldiers[team][i]] += 1

        self.pts = [0, 0]

    def state(self, team: int, id: int) -> tuple:
        """
        Returns the POV state of the soldier with the given id.
        """
        assert team in [0, 1]
        assert id in range(self.NUM_SOLDIERS)

        soldier_pos = self.soldiers[team][id]
        ally = [self.board[team][(i + self.board_sz) % self.board_sz] for i in range(soldier_pos-self.VISION_RANGE, soldier_pos+self.VISION_RANGE+1)]
        enemy = [self.board[1-team][(i + self.board_sz) % self.board_sz] for i in range(soldier_pos-self.VISION_RANGE, soldier_pos+self.VISION_RANGE+1)]

        offset = soldier_pos % (self.GAP_SIZE + 1)
        if offset == 2: # update this calculation if gap size changes
            offset = -1

        # negative to go from soldier to castle instead of castle to soldier
        return ally, enemy, -offset

    def move(self, team: int, id: int, offset: int):
        self.board[team][self.soldiers[team][id]] -= 1
        self.soldiers[team][id] = (self.soldiers[team][id] + offset + self.board_sz) % self.board_sz
        self.board[team][self.soldiers[team][id]] += 1

    def calc_score(self):
        """
        Calculates the score at the end of each day
        """
        castle_interval = self.GAP_SIZE + 1
        for i in range(self.NUM_CASTLES):
            soldiers0 = self.board[0][i * castle_interval]
            soldiers1 = self.board[1][i * castle_interval]

            if soldiers0 > soldiers1:
                self.pts[0] += 1
            elif soldiers1 > soldiers0:
                self.pts[1] += 1
        
        # print('P1:', self.board[0])
        # print('P2:', self.board[1], '\n')

    def scores(self) -> list:
        return self.pts

class BlottoSwarmGrader:
    """
    Blotto Swarm grading class used to locally test a Blotto Swarm submission.
    """
    NUM_DAYS = 100

    def __init__(self, num_games: int = 20, debug = False):
        self.num_games = num_games # number of games to play per pair of strategies
        self.debug = debug
        self.strategies = get_strategies()

    def grade(self, strategy1, strategy2):
        scores = [0, 0]
        for game_num in range(1, self.num_games+1):
            if self.debug and game_num % 100 == 0:
                print(f"Progress: {game_num} / {self.num_games} | {scores}")

            game = BlottoSwarmGame()
            for _ in range(self.NUM_DAYS):
                moves = [[], []]
                for team, strategy in enumerate([strategy1, strategy2]):
                    for i in range(BlottoSwarmGame.NUM_SOLDIERS):
                        ally, enemy, offset = game.state(team, i)
                        try:
                            move = strategy(ally, enemy, offset)
                            assert move in [-1, 0, 1]
                        except Exception as ex:
                            if self.debug:
                                raise ex
                            else:
                                move = random.randint(-1, 1)
                        moves[team].append(move)

                for team in range(2):
                    for i, move in enumerate(moves[team]):
                        game.move(team, i, move)
                game.calc_score()

            game_score = game.scores()
            if game_score[0] > game_score[1]:
                scores[0] += 1
            elif game_score[1] > game_score[0]:
                scores[1] += 1
            else:
                scores[0] += 0.5
                scores[1] += 0.5
        
        return scores
    
    def grade_all(self) -> None:
        """
        Grades all strategies against each other and prints the winrate of each strategy.
        """
        wins = [0] * len(self.strategies)
        for i in range(len(self.strategies)):
            for j in range(i+1, len(self.strategies)):
                if self.debug:
                    print(f"Grading strategies {i} and {j}:")

                scores = self.grade(self.strategies[i], self.strategies[j])
                wins[i] += scores[0]
                wins[j] += scores[1]
        
        total_games = self.num_games * len(self.strategies) * (len(self.strategies) - 1) // 2
        self.winrate = [win / total_games for win in wins]

    def print_result(self) -> None:
        for i in range(len(self.strategies)):
            print(f"Strategy {i+1}: {self.winrate[i]}")
        

if __name__ == "__main__":
    """
    Blotto Swarm local runner command line interface.

    Usage:
        usage: contestant_grader.py [-h] [--games GAMES] [--debug]
    """

    parser = argparse.ArgumentParser(description="Blotto Swarm local runner CLI")

    parser.add_argument("--games", "-g", type=int, default=20)
    parser.add_argument("--debug", "-d", action="store_true")

    args = parser.parse_args()

    grader = BlottoSwarmGrader(num_games=args.games, debug=args.debug)
    grader.grade_all()
    grader.print_result()