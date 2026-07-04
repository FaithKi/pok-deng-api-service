from pydantic import BaseModel
from typing import Optional

class NewGame(BaseModel):
    balance: int

class Action(BaseModel):
    action: str
    amount: Optional[int] = None