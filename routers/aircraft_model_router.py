from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.orm_repositories import AircraftModelRepository
from dtos.api_dtos import AircraftModelCreate

router = APIRouter(prefix="/aircraft_models", tags=["Aircraft Models"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    repo = AircraftModelRepository(db)
    return repo.get_all()

@router.get("/{model_id}")
def get_by_id(model_id: int, db: Session = Depends(get_db)):
    repo = AircraftModelRepository(db)
    obj = repo.get_by_id(model_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("/")
def create(model: AircraftModelCreate, db: Session = Depends(get_db)):
    repo = AircraftModelRepository(db)
    obj = repo.add(repo.model(**model.dict()))
    return obj

@router.put("/{model_id}")
def update(model_id: int, model: AircraftModelCreate, db: Session = Depends(get_db)):
    repo = AircraftModelRepository(db)
    obj = repo.get_by_id(model_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.model_title = model.model_title
    repo.update()
    return obj

@router.delete("/{model_id}")
def delete(model_id: int, db: Session = Depends(get_db)):
    repo = AircraftModelRepository(db)
    obj = repo.get_by_id(model_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    repo.delete(obj)
    return {"detail": "Deleted"}
