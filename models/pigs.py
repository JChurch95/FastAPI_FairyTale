from .base import Base

class Pig(Base, table=True):
    __tablename__ = "pigs"

    pig_house: str
    pig_name: str