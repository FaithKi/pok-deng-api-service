from enum import Enum
import random
from uuid import UUID

class GameState(Enum):
    WAITING_FOR_CUT = "WAITING_FOR_CUT"
    WAITING_FOR_BET = "WAITING_FOR_BET"
    WAITING_FOR_DECISION = "WAITING_FOR_DECISION"
    DEALER_TURN = "DEALER_TURN"
    ROUND_END = "ROUND_END"

class Game:
    def __init__(self, game_id, balance):
        self.game_id: UUID = game_id
        self.balance: int = balance
        self.state: GameState = GameState.WAITING_FOR_CUT
        self.deck: Deck = Deck()
        self.bet: int = 0
        self.player_hand = []
        self.dealer_hand = []
    
    def player_action(self, action: str, amount: int = None):
        match action:
            case "cut":
                self.deck.cut(amount)
                self.state = GameState.WAITING_FOR_BET
            case "bet":
                self.balance -= amount
                self.bet += amount
                self.state = GameState.WAITING_FOR_DECISION
                for _ in range(2):
                    self.player_hand.append(self.deck.draw())
                    self.dealer_hand.append(self.deck.draw())
                if self.calc_score(self.player_hand) >= 8:
                    if self.calc_score(self.dealer_hand) >= 8:
                        print("Game Draw")
                    else:
                        print("Player Wins")
                    self.state = GameState.ROUND_END
                elif self.calc_score(self.dealer_hand) >= 8:
                    print("Player Loses")
                    self.state = GameState.ROUND_END
            case "draw":
                self.player_hand.append(self.deck.draw())
                self.state = GameState.ROUND_END
                self.dealer_turn()
            case "stay":
                self.state = GameState.ROUND_END
                self.dealer_turn()
        sum_state = self.get_state()
        return sum_state

    def calc_score(self, hand):
        return sum([c["value"] for c in hand]) % 10

    
    def dealer_turn(self):
        if self.calc_score(self.dealer_hand) < 4:
            self.dealer_hand.append(self.deck.draw())

        dealer_score = self.calc_score(self.dealer_hand)
        player_score = self.calc_score(self.player_hand)

        if player_score > dealer_score:
            print("Player Wins")
        elif player_score < dealer_score:
            print("Player Loses")
        else:
            print("Game Draw")
    
    def get_state(self):
        round_end = self.state == GameState.ROUND_END
        winner = None
        if round_end:
            dealer_score = self.calc_score(self.dealer_hand)
            player_score = self.calc_score(self.player_hand)

            if player_score > dealer_score:
                winner = "Player"
            elif player_score < dealer_score:
                winner = "Dealer"
            else:
                winner = "Tie"


        return {
            "game_id": self.game_id,
            "state": self.state,
            "balance": self.balance,
            "player_hand": self.player_hand,
            "dealer_hand_visible": self.dealer_hand if round_end else [],
            "player_score": self.calc_score(self.player_hand),
            "dealer_score": self.calc_score(self.dealer_hand) if round_end else None,
            "winner": winner
        }

    



# card is AH (ace of heart), 7C (7 of clubs)
# las elem of deck cards is top of deck
class Deck:
    def __init__(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]
        ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        suits = ["Hearts","Spades","Clubs","Diamonds"] # hearts, spades, clubs, diamonds
        self.cards: list[str] = [{"rank":ranks[i], "suit": s, "value": values[i]} for i in range(len(ranks)) for s in suits]
        random.shuffle(self.cards)

    def cut(self, n: int):
        m = len(self.cards) - n
        self.cards = self.cards[m:] + self.cards[:m]
    
    def draw(self):
        return self.cards.pop()

# d = Deck()
# print(d.cards)
# d.cut(5)
# print(d.cards)
    