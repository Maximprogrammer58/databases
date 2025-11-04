from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.orm_repositories import CustomerRepository
from dtos.api_dtos import CustomerCreate

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    return repo.get_all()

@router.get("/{customer_id}")
def get_by_id(customer_id: int, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    obj = repo.get_by_id(customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("/")
def create(customer: CustomerCreate, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    obj = repo.add(repo.model(**customer.dict()))
    return obj

@router.put("/{customer_id}")
def update(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    obj = repo.get_by_id(customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.passport = customer.passport
    obj.first_name = customer.first_name
    obj.last_name = customer.last_name
    obj.phone = customer.phone
    repo.update()
    return obj

@router.delete("/{customer_id}")
def delete(customer_id: int, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    obj = repo.get_by_id(customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    repo.delete(obj)
    return {"detail": "Deleted"}
