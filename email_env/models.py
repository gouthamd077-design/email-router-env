from pydantic import BaseModel


class Observation(BaseModel):
    email_type: str
    priority: str


class Action(BaseModel):
    action: str


class Reward(BaseModel):
    score: float