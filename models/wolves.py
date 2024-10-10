from .base import Base

class Wolf(Base, table=True):
    __tablename__ = "wolves"

    wolf_name: str
    wolf_power: int