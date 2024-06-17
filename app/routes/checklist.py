#region ------- IMPORTS -------------------------------------------------------------------------------------

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..model import crud, schemas
from ..db.database import get_db

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------
#endregion ---- CONSTANTS -----------------------------------------------------------------------------------
#region ------- UTILS ---------------------------------------------------------------------------------------
#endregion ---- UTILS ---------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

router = APIRouter()

#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- MIDDLEWARE ----------------------------------------------------------------------------------
#endregion ---- MIDDLEWARE ----------------------------------------------------------------------------------

#region ------- ROUTES --------------------------------------------------------------------------------------

@router.post("/checklists/", response_model=schemas.Checklist)
def create_checklist(checklist: schemas.Checklist, db: Session = Depends(get_db)):
    # TODO: Document
    return crud.create_checklist(db=db, checklist=checklist)

@router.get("/checklists/", response_model=List[schemas.Checklist])
def read_checklists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # TODO: Document
    checklists = crud.get_checklists(db, skip=skip, limit=limit)
    return checklists

@router.get("/checklists/{checklist_id}", response_model=schemas.Checklist)
def read_checklist(checklist_id: int, db: Session = Depends(get_db)):
    # TODO: Document
    db_checklist = crud.get_checklist(db, checklist_id=checklist_id)
    if db_checklist is None:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return db_checklist

#endregion ---- ROUTES -------------------------------------------------------------------------------------