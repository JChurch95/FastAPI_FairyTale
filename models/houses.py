from sqlmodel import Field
from .base import Base

class House(Base, table=True):
    __tablename__ = "houses"

    house_type: str
    house_sturdiness: int
    pig_id: int= Field(default=None, foreign_key="pigs.id")