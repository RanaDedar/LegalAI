from pydantic import BaseModel
class Querry_Schema(BaseModel):
    prompt: str
    uid: int