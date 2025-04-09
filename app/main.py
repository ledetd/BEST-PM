from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models import Crew, Project


# Create the FastAPI app
app = FastAPI()

# Create the SQLite database engine - Refactor to Postgresql
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Dependency: Get the session
def get_session():
    with Session(engine) as session:
        yield session

#Home Page
@app.get("/")
def root():
    return {"Data": "BEST-PM"}

# Crew CRUD
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

# Project CRUD
# Create a Project
@app.post("/projects", response_model=Project)
def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

# Read all projects
@app.get("/projects", response_model=list[Project])
def read_projects(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    projects = session.exec(select(Project).offset(skip).limit(limit)).all()
    return projects

# Read a project by ID
@app.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Update a Project
@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, project_data: Project, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update the project's attributes
    for field, value in project_data.model_dump().items():
        setattr(project, field, value)
    session.commit()
    session.refresh(project)
    return project

# Delete a Project
@app.delete("/projects/{project_id}", response_model=Project)
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()
    return project



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Run App With: uv run app/main.py