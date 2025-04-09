from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Crew(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    position: str
    location: str
   

# Create the FastAPI app
app = FastAPI()

# Create the SQLite database engine - Refactor to Postgresql
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Dependency: Get the session
def get_session():
    with Session(engine) as session:
        yield session

# Create a Crew Member
@app.post("/crews", response_model=Crew)
def create_crew(crew: Crew, session: Session = Depends(get_session)):
    session.add(crew)
    session.commit()
    session.refresh(crew)
    return crew
    
# Read all crews
@app.get("/crews", response_model=list[Crew])
def read_crews(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    crews = session.exec(select(Crew).offset(skip).limit(limit)).all()
    return crews

# Read a crew by ID
@app.get("/crews/{crew_id}", response_model=Crew)
def read_crew(crew_id: int, session: Session = Depends(get_session)):
    crew = session.get(Crew, crew_id)
    if not crew:
        raise HTTPException(status_code=404, detail="Crew member not found")
    return crew


# Update a Crew
@app.put("/crews/{crew_id}", response_model=Crew)
def update_crew(crew_id: int, crew_data: Crew, session: Session = Depends(get_session)):
    crew = session.get(Crew, crew_id)
    if not crew:
        raise HTTPException(status_code=404, detail="Crew member not found")

    # Update the crew's attributes
    for field, value in crew_data.model_dump().items():
        setattr(crew, field, value)
    session.commit()
    session.refresh(crew)
    return crew

# Delete a Crew
@app.delete("/crews/{crew_id}", response_model=Crew)
def delete_crew(crew_id: int, session: Session = Depends(get_session)):
    crew = session.get(Crew, crew_id)
    if not crew:
        raise HTTPException(status_code=404, detail="Crew member not found")

    session.delete(crew)
    session.commit()
    return crew


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)