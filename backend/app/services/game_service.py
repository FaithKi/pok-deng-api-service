from app.models.game_model import Game, GameState
import uuid

games: dict[int: Game] = {}

def new_game(data):
    game_id = uuid.uuid4()
    game = Game(game_id, int(data.balance))
    games[game_id] = game
    print("Running Games",[ids for ids in games.keys()])
    return game.get_state()

def process_action(game_id, action):
    game = games[uuid.UUID(game_id)]
    state = game.player_action(action.action, action.amount)
    print("game state is",state["state"])
    if state["state"] == GameState.ROUND_END:
        print("Deleting Game")
        del games[uuid.UUID(game_id)]
        del game
    return state