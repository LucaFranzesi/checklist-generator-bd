#region ------- IMPORTS -------------------------------------------------------------------------------------

from sqlalchemy.orm import Session
from . import models, schemas

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------
#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- ROUTES --------------------------------------------------------------------------------------

def get_checklist(db: Session, checklist_id: int):
    # TODO: Prettify documentation
    '''Query the db for a specific checklist passed as parameter "checklist_id"'''
    return db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()

def get_checklists(db: Session, skip: int = 0, limit: int = 10):
    # TODO: Prettify documentation
    '''Query the db for all checklists with a given pagination (skip and limit parameters)'''
    return db.query(models.Checklist).offset(skip).limit(limit).all()

def create_checklist(db: Session, checklist: schemas.Checklist):
    # TODO: Prettify documentation
    '''Insert a new Checklist with its Sections and Checks inside the db'''
    db_checklist = models.Checklist(title=checklist.title)
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)

    # Add sections to checklist
    for section_data in checklist.sections:
        db_section = models.Section(checklist_id=db_checklist.id, title=section_data.title)
        db.add(db_section)
        db.commit()
        db.refresh(db_section)

        parent_check_id = []

        # Add checks to section
        for check_data in section_data.checks:
            db_check = models.Check(
                text=check_data.text,
                section_id=db_section.id,
                # Set correct check parent
                # NOTE: Actual max indentation = 1, possibly upgrade in future versions
                parent_id=None if check_data.parent_id is None else parent_check_id[-1]
            )

            db.add(db_check)
            db.commit()
            db.refresh(db_check)

            if(db_check.parent_id is None):
                parent_check_id.append(db_check.id)

    return db_checklist

#endregion ---- ROUTES --------------------------------------------------------------------------------------