from fastapi import APIRouter
from app.models.request_model import NewGame, Action
from app.services import game_service as gameService


router: APIRouter = APIRouter(prefix="/game")

@router.post("/start")
def start_game(new_game: NewGame):
    state = gameService.new_game(new_game)
    return state

@router.post("/{game_id}/action")
def execute_action(game_id: str, action: Action):
    print("testsete 234523erewqf")
    state = gameService.process_action(game_id, action)
    return state