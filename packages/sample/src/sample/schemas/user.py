from pydantic import BaseModel, Field, ConfigDict


class CreateUser(BaseModel):
    name: str = Field(max_length=30)


class UserResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
