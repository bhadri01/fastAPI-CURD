from pydantic import BaseModel


class createData(BaseModel):
    name: str
    age: int
    email: str
