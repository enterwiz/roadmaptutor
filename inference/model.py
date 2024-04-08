from langchain_core.pydantic_v1 import BaseModel, Field


class TechniquePoint(BaseModel):
    techs: list[str] = Field(description="技能名称")
