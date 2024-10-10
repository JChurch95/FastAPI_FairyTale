import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session, init_db
from models.pigs import Pig
from models.wolves import Wolf
from models.houses import House
from datetime import date
from typing import List

app = FastAPI()


# Initialize the database
init_db()



# Operations
@app.get("/")
async def root():
    return {"message": "Let's fry some bacon!"}


# ROUTES FOR HOUSE
# Create House
# Create House
@app.post("/create_house", response_model=House)
async def create_house(
    house_type: str, 
    house_sturdiness: int, 
    pig_id: int = None,
    session: Session = Depends(get_session)
):
    try:
        house = House(
            house_type=house_type,
            house_sturdiness=house_sturdiness,
            pig_id=pig_id
        )
        session.add(house)
        session.commit()
        session.refresh(house)
        return house
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the house: {str(e)}")


# Read House
@app.get("/houses/{house_id}", response_model=House)
async def read_house(house_id: int, session: Session = Depends(get_session)):
    house = session.get(House, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
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
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the house: {str(e)}")



# Delete House
@app.delete("/houses/{house_id}")
async def delete_house(
    house_id: int,
    session: Session = Depends(get_session)
):
    house = session.get(House, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    
    try:
        session.delete(house)
        session.commit()
        return {"message": f"House with id {house_id} has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the house: {str(e)}")




# ROUTES FOR PIG
# Create Pig
@app.post("/create_pig", response_model=Pig)
async def create_pig(
    pig_house: str, 
    pig_name: str, 
    session: Session = Depends(get_session)
):
    try:
        pig = Pig(
            pig_name=pig_name,
            pig_house=pig_house
        )
        session.add(pig)
        session.commit()
        session.refresh(pig)
        return pig
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the pig: {str(e)}")


# Read Pigs
@app.get("/pigs", response_model=List[Pig])
async def read_pigs(session: Session = Depends(get_session)):
    try:
        pigs = session.exec(select(Pig)).all()
        return pigs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching pigs: {str(e)}")

# Read Pig
@app.get("/pigs/{pig_id}", response_model=Pig)
async def read_pig(pig_id: int, session: Session = Depends(get_session)):
    pig = session.get(Pig, pig_id)
    if not pig:
        raise HTTPException(status_code=404, detail="Pig not found")
    return pig


# Update Pig
@app.put("/pigs/{pig_id}", response_model=Pig)
async def update_pig(
    pig_id: int,
    pig_name: str = None,
    pig_house: str = None,
    session: Session = Depends(get_session)
):
    pig = session.get(Pig, pig_id)
    if not pig:
        raise HTTPException(status_code=404, detail="Pig not found")
    
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the pig: {str(e)}")



# Delete Pig
@app.delete("/pigs/{pig_id}")
async def delete_pig(
    pig_id: int,
    session: Session = Depends(get_session)
):
    pig = session.get(Pig, pig_id)
    if not pig:
        raise HTTPException(status_code=404, detail="Pig not found")
    
    try:
        session.delete(pig)
        session.commit()
        return {"message": f"Pig with id {pig_id} has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the pig: {str(e)}")





# ROUTES FOR WOLF
# Create Wolf
@app.post("/create_wolf", response_model=Wolf)
async def create_wolf(
    wolf_name: str, 
    wolf_power: int, 
    session: Session = Depends(get_session)
):
    try:
        wolf = Wolf(
            wolf_name=wolf_name,
            wolf_power=wolf_power
        )
        session.add(wolf)
        session.commit()
        session.refresh(wolf)
        return wolf
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the wolf: {str(e)}")



# Read Wolves
@app.get("/wolves", response_model=List[Wolf])
async def read_wolves(session: Session = Depends(get_session)):
    try:
        wolves = session.exec(select(Wolf)).all()
        return wolves
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching wolves: {str(e)}")

# Read Wolf
@app.get("/wolves/{wolf_id}", response_model=Wolf)
async def read_wolf(wolf_id: int, session: Session = Depends(get_session)):
    wolf = session.get(Wolf, wolf_id)
    if not wolf:
        raise HTTPException(status_code=404, detail="Wolf not found")
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
    if not wolf:
        raise HTTPException(status_code=404, detail="Wolf not found")
    
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the wolf: {str(e)}")



# Delete Wolf
@app.delete("/wolves/{wolf_id}")
async def delete_wolf(
    wolf_id: int,
    session: Session = Depends(get_session)
):
    wolf = session.get(Wolf, wolf_id)
    if not wolf:
        raise HTTPException(status_code=404, detail="Wolf not found")
    
    try:
        session.delete(wolf)
        session.commit()
        return {"message": f"Wolf with id {wolf_id} has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the wolf: {str(e)}")
