"""Category DTOs."""


from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    name_english: str | None = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    name_english: str | None = None

    model_config = ConfigDict(from_attributes=True)
