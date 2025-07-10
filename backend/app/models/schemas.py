from pydantic import BaseModel

class PlayerCreate(BaseModel):
    username: str
    password: str
    
class PlayerResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str