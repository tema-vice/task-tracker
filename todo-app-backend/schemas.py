from pydantic import BaseModel, ConfigDict, Field


class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    completed: bool | None = None


class TaskReadSchema(BaseModel):
    id: str
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class CategoryCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class CategoryReadSchema(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)