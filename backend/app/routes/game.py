from fastapi import APIRouter

router: APIRouter = APIRouter(prefix="/game")

@router.post("/start")
def start_game():
    pass

@router.post("/{game_id}/action")
def execute_action():
    pass