import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        return 0 if player == 1 else 1

    def switch_player(self):
        self.player = Nim.other_player(self.player)

    def move(self, action):
        pile, count = action
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")
        self.piles[pile] -= count
        self.switch_player()
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        state = tuple(state)
        return self.q.get((state, action), 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        state = tuple(state)
        new_q = old_q + self.alpha * (reward + future_rewards - old_q)
        self.q[(state, action)] = new_q

    def best_future_reward(self, state):
        state = tuple(state)
        best = 0
        for action in Nim.available_actions(state):
            best = max(best, self.get_q_value(state, action))
        return best

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        state = tuple(state)
        actions = list(Nim.available_actions(state))
        if not actions:
            return None
        if epsilon and random.random() < self.epsilon:
            return random.choice(actions)
        else:
            best = None
            best_q = -math.inf
            for action in actions:
                q = self.get_q_value(state, action)
                if q > best_q:
                    best = action
                    best_q = q
            return best


def train(n):
    player = NimAI()
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }
        while True:
            if game.winner is not None:
                break
            state = game.piles.copy()
            action = player.choose_action(game.piles)
            if action is None:
                break  # No valid actions left, game is over
            last[game.player]["state"] = state
            last[game.player]["action"] = action
            game.move(action)
            new_state = game.piles.copy()
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )
    print("Done training")
    return player


def play(ai, human_player=None):
    if human_player is None:
        human_player = random.randint(0, 1)
    game = Nim()
    while True:
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")
        else:
            print("AI's Turn")
            action = ai.choose_action(game.piles, epsilon=False)
            if action is None:
                print("No available actions for AI. Ending game.")
                return
            pile, count = action
            print(f"AI chose to take {count} from pile {pile}.")
        game.move((pile, count))
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return