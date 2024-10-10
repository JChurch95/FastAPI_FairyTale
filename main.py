import uvicorn
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from db import get_session
from models.pigs import Pig
from models.wolves import Wolf
from models.houses import House
from datetime import date
from typing import List

app = FastAPI()



# Operations
@app.get("/")
async def root():
    return {"message": "Let's fry some bacon!"}


# ROUTES FOR HOUSE
# Create House
@app.post("/create_house", response_model=House)
async def create_house(
    house_type: str, 
    house_sturdiness: int, 
    pig_id: int = None,
    session: Session = Depends(get_session)
):
    
    house = House(
        house_type=house_type,
        house_sturdiness=house_sturdiness,
        pig_id=pig_id
    )
    session.add(house)
    session.commit()
    session.refresh(house)
    return house


# Read House
@app.get("/houses/{house_id}", response_model=House)
async def read_house(house_id: int, session: Session = Depends(get_session)):
    house = session.get(House, house_id)
    return house


# Update House
@app.put("/houses/{house_id}", response_model=House)
async def update_house(
    house_id: int,
    house_type: str = None,
    house_sturdiness: int = None,
    pig_id: int = None,
    session: Session = Depends(get_session)
):
    house = session.get(House, house_id)
    
    
    house_data = house.dict(exclude_unset=True)
    update_data = {
        "house_type": house_type,
        "house_sturdiness": house_sturdiness,
        "pig_id": pig_id
    }
    
    for field, value in update_data.items():
        if value is not None:
            house_data[field] = value
    
    for field, value in house_data.items():
        setattr(house, field, value)
    
    session.add(house)
    session.commit()
    session.refresh(house)
    return house
    


# Delete House
@app.delete("/houses/{house_id}")
async def delete_house(
    house_id: int,
    session: Session = Depends(get_session)
):
    house = session.get(House, house_id)
    
    session.delete(house)
    session.commit()
    return {"message": f"House with id {house_id} has been deleted successfully"}
    



# ROUTES FOR PIG
# Create Pig
@app.post("/create_pig", response_model=Pig)
async def create_pig(
    pig_house: str, 
    pig_name: str, 
    session: Session = Depends(get_session)
):
    
    pig = Pig(
        pig_name=pig_name,
        pig_house=pig_house
    )
    session.add(pig)
    session.commit()
    session.refresh(pig)
    return pig
    

# Read Pigs
@app.get("/pigs", response_model=List[Pig])
async def read_pigs(session: Session = Depends(get_session)):
        pigs = session.exec(select(Pig)).all()
        return pigs
    
# Read Pig
@app.get("/pigs/{pig_id}", response_model=Pig)
async def read_pig(pig_id: int, session: Session = Depends(get_session)):
    pig = session.get(Pig, pig_id)
    


# Update Pig
@app.put("/pigs/{pig_id}", response_model=Pig)
async def update_pig(
    pig_id: int,
    pig_name: str = None,
    pig_house: str = None,
    session: Session = Depends(get_session)
):
    pig = session.get(Pig, pig_id)
    
    pig_data = pig.dict(exclude_unset=True)
    update_data = {
        "pig_name": pig_name,
        "pig_house": pig_house
    }
    
    for field, value in update_data.items():
        if value is not None:
            pig_data[field] = value
    
    for field, value in pig_data.items():
        setattr(pig, field, value)
    
    session.add(pig)
    session.commit()
    session.refresh(pig)
    return pig


# Delete Pig
@app.delete("/pigs/{pig_id}")
async def delete_pig(
    pig_id: int,
    session: Session = Depends(get_session)
):
    pig = session.get(Pig, pig_id)
    
    
    session.delete(pig)
    session.commit()
    return {"message": f"Pig with id {pig_id} has been deleted successfully"}




# ROUTES FOR WOLF
# Create Wolf
@app.post("/create_wolf", response_model=Wolf)
async def create_wolf(
    wolf_name: str, 
    wolf_power: int, 
    session: Session = Depends(get_session)
):
    
    wolf = Wolf(
        wolf_name=wolf_name,
        wolf_power=wolf_power
    )
    session.add(wolf)
    session.commit()
    session.refresh(wolf)
    return wolf


# Read Wolves
@app.get("/wolves", response_model=List[Wolf])
async def read_wolves(session: Session = Depends(get_session)):
        wolves = session.exec(select(Wolf)).all()
        return wolves
    
# Read Wolf
@app.get("/wolves/{wolf_id}", response_model=Wolf)
async def read_wolf(wolf_id: int, session: Session = Depends(get_session)):
    wolf = session.get(Wolf, wolf_id)
    return wolf


# Update Wolf
@app.put("/wolves/{wolf_id}", response_model=Wolf)
async def update_wolf(
    wolf_id: int,
    wolf_name: str = None,
    wolf_power: int = None,
    session: Session = Depends(get_session)
):
    wolf = session.get(Wolf, wolf_id)
    wolf_data = wolf.dict(exclude_unset=True)
    update_data = {
        "wolf_name": wolf_name,
        "wolf_power": wolf_power
    }
    
    for field, value in update_data.items():
        if value is not None:
            wolf_data[field] = value
    
    for field, value in wolf_data.items():
        setattr(wolf, field, value)
    
    session.add(wolf)
    session.commit()
    session.refresh(wolf)
    return wolf


# Delete Wolf
@app.delete("/wolves/{wolf_id}")
async def delete_wolf(
    wolf_id: int,
    session: Session = Depends(get_session)
):
    wolf = session.get(Wolf, wolf_id)
    
    session.delete(wolf)
    session.commit()
    return {"message": f"Wolf with id {wolf_id} has been deleted successfully"}