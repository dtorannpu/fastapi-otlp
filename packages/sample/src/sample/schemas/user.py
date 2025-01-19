from pydantic import BaseModel, Field, ConfigDict, RootModel


class UserBase(BaseModel):
    name: str = Field(max_length=30)


class CreateUser(UserBase):
    pass


class UpdateUser(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UsersResponse(RootModel[list[UserResponse]]):
    pass
